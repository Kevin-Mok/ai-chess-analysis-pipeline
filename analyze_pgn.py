#!/usr/bin/env python3
import argparse
import math
import os
import queue
import re
import subprocess
import sys
import threading
import time

import chess
import chess.pgn

ENGINE = "/usr/games/stockfish"
CPU_THREADS = os.cpu_count() or 1
DEFAULT_THREADS = max(1, CPU_THREADS - 1)
DEFAULT_HASH_MB = 8192
DEFAULT_MAX_SECONDS = 60
DEFAULT_MIN_MS = 80
DEFAULT_MAX_MS = 2500
DEFAULT_POV_PLAYER = "SoloPistol"
PLY_COL_WIDTH = 5
TURN_COL_WIDTH = 3
MOVE_COL_WIDTH = 6
EVAL_COL_WIDTH = 7
PCT_COL_WIDTH = 5
DEFAULT_ANALYSIS_DIR = "analysis"

def pct(x, total):
    return round(100.0 * x / total, 1) if total else 0.0

def log(message):
    print(message, file=sys.stderr, flush=True)

def format_row(ply_label, turn, san, win, loss, draw, eval_str):
    def fmt_pct(value):
        if isinstance(value, (int, float)):
            return f"{value:>{PCT_COL_WIDTH}.1f}"
        return f"{value:>{PCT_COL_WIDTH}}"

    return (
        f"{ply_label:<{PLY_COL_WIDTH}} "
        f"{turn:<{TURN_COL_WIDTH}} "
        f"{san:<{MOVE_COL_WIDTH}} "
        f"{fmt_pct(win)} "
        f"{fmt_pct(loss)} "
        f"{fmt_pct(draw)} "
        f"{eval_str:>{EVAL_COL_WIDTH}}"
    )

def parse_info_line(line):
    tokens = line.split()
    cp = None
    mate = None
    wdl = None
    i = 1  # Skip "info"
    while i < len(tokens):
        tok = tokens[i]
        if tok == "score" and i + 2 < len(tokens):
            if tokens[i + 1] == "cp":
                try:
                    cp = int(tokens[i + 2])
                    mate = None
                except ValueError:
                    pass
            elif tokens[i + 1] == "mate":
                try:
                    mate = int(tokens[i + 2])
                    cp = None
                except ValueError:
                    pass
            i += 3
            continue
        if tok == "wdl" and i + 3 < len(tokens):
            try:
                wdl = (int(tokens[i + 1]), int(tokens[i + 2]), int(tokens[i + 3]))
            except ValueError:
                pass
            i += 4
            continue
        i += 1
    return cp, mate, wdl

def approx_wdl_from_cp(cp_white):
    # Lightweight fallback if Stockfish omits WDL in a short search.
    win = 100.0 / (1.0 + math.exp(-cp_white / 180.0))
    loss = 100.0 - win
    draw = max(0.0, min(25.0, 25.0 - abs(cp_white) / 40.0))
    scale = max(1e-9, win + loss)
    factor = (100.0 - draw) / scale
    return round(win * factor, 1), round(draw, 1), round(loss * factor, 1)

class UCIStockfish:
    def __init__(self, engine_path, threads, hash_mb):
        self.proc = subprocess.Popen(
            [engine_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._lines = queue.Queue()
        self._reader = threading.Thread(target=self._reader_loop, daemon=True)
        self._reader.start()
        self.threads = max(1, int(threads))
        self.hash_mb = max(16, int(hash_mb))
        self._init_uci()

    def _reader_loop(self):
        if self.proc.stdout is None:
            return
        for line in self.proc.stdout:
            self._lines.put(line.rstrip("\n"))
        self._lines.put(None)

    def _send(self, cmd):
        if self.proc.stdin is None:
            raise RuntimeError("Stockfish stdin is unavailable.")
        self.proc.stdin.write(cmd + "\n")
        self.proc.stdin.flush()

    def _readline(self, timeout_s):
        timeout_s = max(0.0, timeout_s)
        try:
            line = self._lines.get(timeout=timeout_s)
        except queue.Empty:
            return None
        if line is None:
            raise RuntimeError("Stockfish exited unexpectedly.")
        return line

    def _wait_for(self, expected, timeout_s):
        deadline = time.monotonic() + timeout_s
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Timed out waiting for '{expected}'.")
            line = self._readline(remaining)
            if line is None:
                continue
            if line == expected or line.startswith(expected + " "):
                return

    def _init_uci(self):
        self._send("uci")
        self._wait_for("uciok", 5.0)
        self._send(f"setoption name Threads value {self.threads}")
        self._send(f"setoption name Hash value {self.hash_mb}")
        self._send("setoption name UCI_ShowWDL value true")
        self._send("isready")
        self._wait_for("readyok", 5.0)

    def analyse_fen(self, fen, movetime_ms, hard_timeout_ms):
        self._send(f"position fen {fen}")
        self._send(f"go movetime {max(1, int(movetime_ms))}")

        cp = None
        mate = None
        wdl = None

        deadline = time.monotonic() + (hard_timeout_ms / 1000.0)
        stop_sent = False

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                if not stop_sent:
                    self._send("stop")
                    stop_sent = True
                    deadline = time.monotonic() + 1.5
                    continue
                raise TimeoutError("Timed out waiting for bestmove from Stockfish.")

            line = self._readline(remaining)
            if line is None:
                continue

            if line.startswith("info "):
                cp_new, mate_new, wdl_new = parse_info_line(line)
                if cp_new is not None:
                    cp = cp_new
                if mate_new is not None:
                    mate = mate_new
                if wdl_new is not None:
                    wdl = wdl_new
                continue

            if line.startswith("bestmove "):
                return cp, mate, wdl

    def quit(self):
        if self.proc.poll() is not None:
            return
        try:
            self._send("quit")
        except Exception:
            pass
        try:
            self.proc.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=2.0)

def normalize_player_name(name):
    return " ".join((name or "").split()).casefold()

def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", normalize_player_name(value))
    return slug.strip("-") or "unknown"

def resolve_pov(game, pov_player):
    white = game.headers.get("White", "?")
    black = game.headers.get("Black", "?")
    if pov_player:
        target = normalize_player_name(pov_player)
        if normalize_player_name(white) == target:
            return chess.WHITE, white, black, True
        if normalize_player_name(black) == target:
            return chess.BLACK, black, white, True
    return chess.WHITE, white, black, False

def default_output_md_path(white, black, pov_name, opponent_name, pov_found):
    if pov_found:
        left = pov_name
        right = opponent_name
    else:
        left = white
        right = black
    filename = f"{slugify(left)}-vs-{slugify(right)}.md"
    return os.path.join(DEFAULT_ANALYSIS_DIR, filename)

def to_pov(board, cp, mate, wdl, pov_color):
    if cp is not None and board.turn != pov_color:
        cp = -cp
    if mate is not None and board.turn != pov_color:
        mate = -mate
    if wdl is not None and board.turn != pov_color:
        wdl = (wdl[2], wdl[1], wdl[0])
    return cp, mate, wdl

def main(
    pgn_path,
    depth=18,
    threads=DEFAULT_THREADS,
    hash_mb=DEFAULT_HASH_MB,
    max_seconds=DEFAULT_MAX_SECONDS,
    min_ms=DEFAULT_MIN_MS,
    max_ms=DEFAULT_MAX_MS,
    pov_player=DEFAULT_POV_PLAYER,
    output_md=None,
):
    with open(pgn_path, "r", encoding="utf-8", errors="replace") as f:
        game = chess.pgn.read_game(f)
    if not game:
        raise SystemExit("No game found in PGN.")

    start = time.perf_counter()
    deadline = start + max(1, float(max_seconds))
    engine = UCIStockfish(ENGINE, threads=threads, hash_mb=hash_mb)

    try:
        threads = max(1, int(threads))
        hash_mb = max(16, int(hash_mb))
        min_ms = max(20, int(min_ms))
        max_ms = max(min_ms, int(max_ms))

        total_plies = sum(1 for _ in game.mainline_moves())
        white = game.headers.get("White", "?")
        black = game.headers.get("Black", "?")
        pov_color, pov_name, opponent_name, pov_found = resolve_pov(game, pov_player)
        pov_side = "White" if pov_color == chess.WHITE else "Black"
        if output_md is None:
            output_md = default_output_md_path(
                white,
                black,
                pov_name,
                opponent_name,
                pov_found,
            )

        if output_md != "-":
            output_dir = os.path.dirname(output_md)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            out = open(output_md, "w", encoding="utf-8")
        else:
            out = sys.stdout

        if pov_found:
            title = f"# {pov_name} vs {opponent_name} ({pov_name} POV)"
        else:
            title = f"# {white} vs {black}"
        log(
            f"Starting analysis: {white} vs {black}, plies={total_plies}, depth_hint={depth}, "
            f"threads={threads}, hash_mb={hash_mb}, max_seconds={max_seconds}"
        )
        if pov_found:
            log(f"POV mode: player='{pov_name}' ({pov_side})")
        else:
            log(
                f"POV mode: player='{pov_player}' not found in headers; "
                "falling back to White POV."
            )
        log("Engine mode: direct UCI subprocess (no python-chess engine wrapper).")

        # Stream markdown output immediately so redirected output grows during analysis.
        print(title, file=out, flush=True)
        print("", file=out, flush=True)
        print(f"- White: `{white}`", file=out, flush=True)
        print(f"- Black: `{black}`", file=out, flush=True)
        if pov_found:
            print(f"- POV: `{pov_name}` ({pov_side})", file=out, flush=True)
            print(
                f"- Turn labels: `me` = `{pov_name}`, `op.` = `{opponent_name}`",
                file=out,
                flush=True,
            )
        else:
            print("- POV: `White` (fallback)", file=out, flush=True)
            print(f"- Turn labels: `me` = `{white}`, `op.` = `{black}`", file=out, flush=True)
        print("", file=out, flush=True)
        header = format_row("Ply", "Turn", "Move", "Win%", "Loss%", "Draw%", "Eval")
        print("```text", file=out, flush=True)
        print(header, file=out, flush=True)
        print("-" * len(header), file=out, flush=True)

        board = game.board()
        ply = 0
        for move in game.mainline_moves():
            san = board.san(move)
            board.push(move)
            ply += 1

            remaining_plies = max(1, total_plies - ply + 1)
            remaining_ms = max(0, int((deadline - time.perf_counter()) * 1000))
            # Keep a small guard band so wall time stays under target more reliably.
            usable_remaining_ms = int(remaining_ms * 0.92)
            target_ms = usable_remaining_ms // remaining_plies if remaining_plies else min_ms
            movetime_ms = max(min_ms, min(max_ms, max(1, target_ms)))
            hard_timeout_ms = movetime_ms + 2500

            cp = None
            mate = None
            wdl = None
            try:
                cp, mate, wdl = engine.analyse_fen(board.fen(), movetime_ms, hard_timeout_ms)
            except Exception as exc:
                log(f"[{ply}/{total_plies}] engine timeout/error at move {san}: {exc}; restarting engine.")
                engine.quit()
                engine = UCIStockfish(ENGINE, threads=threads, hash_mb=hash_mb)

            cp, mate, wdl = to_pov(board, cp, mate, wdl, pov_color)

            if mate is not None:
                eval_str = f"M{mate:+d}"
            elif cp is not None:
                eval_str = f"{cp / 100:.2f}"
            else:
                eval_str = "?"

            if wdl is not None:
                total = wdl[0] + wdl[1] + wdl[2]
                w, d, l = pct(wdl[0], total), pct(wdl[1], total), pct(wdl[2], total)
            elif cp is not None:
                w, d, l = approx_wdl_from_cp(cp)
            else:
                w, d, l = 0.0, 100.0, 0.0

            move_no = (ply + 1) // 2
            prefix = f"{move_no}." if ply % 2 == 1 else f"{move_no}..."
            mover_color = chess.WHITE if ply % 2 == 1 else chess.BLACK
            turn_label = "me" if mover_color == pov_color else "op."
            print(format_row(prefix, turn_label, san, w, l, d, eval_str), file=out, flush=True)
            elapsed = time.perf_counter() - start
            log(
                f"[{ply}/{total_plies}] {prefix} {san}: eval={eval_str}, W/D/L={w}/{d}/{l}, "
                f"movetime_ms={movetime_ms}, elapsed={elapsed:.1f}s"
            )

        print("```", file=out, flush=True)
        if out is not sys.stdout:
            out.close()
            log(f"Wrote analysis markdown to {output_md}")

        elapsed = time.perf_counter() - start
        log(f"Completed analysis in {elapsed:.1f}s.")
    finally:
        try:
            if "out" in locals() and out is not sys.stdout and not out.closed:
                out.close()
        except Exception:
            pass
        engine.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PGN and stream WDL markdown output.")
    parser.add_argument("pgn_path", help="Path to PGN file")
    parser.add_argument(
        "depth",
        nargs="?",
        type=int,
        default=18,
        help="Legacy quality hint, kept for CLI compatibility (default: 18)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help=f"Stockfish Threads option (default: cpu_count-1={DEFAULT_THREADS})",
    )
    parser.add_argument(
        "--hash-mb",
        type=int,
        default=DEFAULT_HASH_MB,
        help=f"Stockfish Hash option in MB (default: {DEFAULT_HASH_MB})",
    )
    parser.add_argument(
        "--max-seconds",
        type=int,
        default=DEFAULT_MAX_SECONDS,
        help=f"Target wall-time budget in seconds (default: {DEFAULT_MAX_SECONDS})",
    )
    parser.add_argument(
        "--min-ms",
        type=int,
        default=DEFAULT_MIN_MS,
        help=f"Minimum movetime per ply in ms (default: {DEFAULT_MIN_MS})",
    )
    parser.add_argument(
        "--max-ms",
        type=int,
        default=DEFAULT_MAX_MS,
        help=f"Maximum movetime per ply in ms (default: {DEFAULT_MAX_MS})",
    )
    parser.add_argument(
        "--pov-player",
        type=str,
        default=DEFAULT_POV_PLAYER,
        help=(
            f"Player name for POV-oriented Eval/WDL (default: {DEFAULT_POV_PLAYER}); "
            "if not found in PGN headers, falls back to White POV"
        ),
    )
    parser.add_argument(
        "--output-md",
        type=str,
        default=None,
        help=(
            "Markdown output path (default: auto-generated under analysis/). "
            "Use '-' to write to stdout."
        ),
    )
    args = parser.parse_args()
    main(
        args.pgn_path,
        depth=args.depth,
        threads=args.threads,
        hash_mb=args.hash_mb,
        max_seconds=args.max_seconds,
        min_ms=args.min_ms,
        max_ms=args.max_ms,
        pov_player=args.pov_player,
        output_md=args.output_md,
    )
