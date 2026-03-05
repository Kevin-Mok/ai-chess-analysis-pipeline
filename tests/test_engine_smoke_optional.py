from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(
    os.environ.get("CHESS_RUN_ENGINE_SMOKE") != "1",
    reason="Set CHESS_RUN_ENGINE_SMOKE=1 to run real-engine smoke test.",
)
def test_optional_stockfish_engine_smoke(repo_root: Path, sample_pgn_path: str, tmp_path: Path):
    stockfish_available = shutil.which("stockfish") or Path("/usr/games/stockfish").exists()
    if not stockfish_available:
        pytest.skip("Stockfish not available on this machine.")

    output_md = tmp_path / "engine-smoke.md"
    cmd = [
        sys.executable,
        str(repo_root / "analyze_pgn.py"),
        sample_pgn_path,
        "--cause-mode",
        "heuristic",
        "--max-seconds",
        "2",
        "--output-md",
        str(output_md),
    ]
    result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr

    text = output_md.read_text(encoding="utf-8")
    assert "## Significant Swings" in text
    assert "```text" in text
