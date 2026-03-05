from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

OPTION_HEAD_RE = re.compile(r"^(--[a-z0-9-]+)(?: ([A-Za-z0-9_{}.,-]+))?")
SNAPSHOT_PATH = Path(__file__).resolve().parent / "fixtures" / "help_option_heads_snapshot.txt"


def _extract_option_heads(help_text: str) -> str:
    heads = []
    for line in help_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("--"):
            continue
        match = OPTION_HEAD_RE.match(stripped)
        if not match:
            continue
        option = match.group(1)
        metavar = match.group(2)
        if metavar:
            heads.append(f"{option} {metavar}")
        else:
            heads.append(option)
    return "\n".join(heads)


def test_cli_help_contract_snapshot(repo_root: Path):
    cmd = [sys.executable, str(repo_root / "analyze_pgn.py"), "--help"]
    result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stderr
    help_text = result.stdout
    assert "Analyze PGN and stream WDL markdown output." in help_text
    assert "--cause-mode {heuristic,forensic,forensic-llm}" in help_text
    assert "--output-md OUTPUT_MD" in help_text
    assert "effective minimum is 0.50" in help_text

    observed = _extract_option_heads(help_text)
    expected = SNAPSHOT_PATH.read_text(encoding="utf-8").strip()
    assert observed == expected
