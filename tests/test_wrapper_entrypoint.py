from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_wrapper_entrypoint_help(repo_root: Path):
    cmd = [sys.executable, str(repo_root / "analyze_pgn.py"), "--help"]
    result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    assert "Analyze PGN and stream WDL markdown output." in result.stdout
    assert "--output-md OUTPUT_MD" in result.stdout
