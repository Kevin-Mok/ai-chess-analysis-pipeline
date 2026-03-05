from __future__ import annotations

import re
from pathlib import Path


class FakeEngine:
    def __init__(self, *args, **kwargs):
        self.calls = 0

    def analyse_fen(self, fen, movetime_ms, hard_timeout_ms):
        self.calls += 1
        cp = 3000
        return cp, None, None

    def analyse_fen_detailed(
        self,
        fen,
        movetime_ms,
        hard_timeout_ms,
        multipv=1,
        moves_uci=None,
    ):
        _ = (fen, movetime_ms, hard_timeout_ms, multipv, moves_uci)
        return {
            "cp": 0,
            "mate": None,
            "wdl": None,
            "bestmove": "e2e4",
            "infos": [{"multipv": 1, "cp": 0, "mate": None, "wdl": None, "pv": ["e2e4"]}],
        }

    def quit(self):
        return None


def test_heuristic_markdown_contract_with_fake_engine(
    runtime_module,
    sample_pgn_path: str,
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.setattr(runtime_module, "UCIEngine", FakeEngine)
    output_md = tmp_path / "contract-output.md"

    runtime_module.main(
        sample_pgn_path,
        cause_mode="heuristic",
        max_seconds=2,
        output_md=str(output_md),
    )

    text = output_md.read_text(encoding="utf-8")
    assert "## Significant Swings" in text
    assert "```text" in text
    assert "Ply   Turn Move" in text
    assert "- [Critical]" in text
    assert re.search(r"expected score \d\.\d{2} -> \d\.\d{2} \([+-]\d+\.\d pts\)", text)
    assert "  Cause: " in text
