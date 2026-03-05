from __future__ import annotations

import importlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PGN = REPO_ROOT / "games" / "2026-02-27-fast-checkmate.pgn"


def load_runtime_module():
    try:
        return importlib.import_module("pgn_analyzer.pipeline")
    except ModuleNotFoundError:
        return importlib.import_module("analyze_pgn")


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def sample_pgn_path() -> str:
    return str(SAMPLE_PGN)


@pytest.fixture
def runtime_module():
    return load_runtime_module()
