# ExecPlan: Analyzer Refactor With Pre-Lock Behavior Tests

## Goal
Lock current analyzer behavior with regression tests, then refactor `analyze_pgn.py` into multiple modules without changing CLI/output behavior.

## Plan
- [x] Add pytest-based behavior contract tests against current implementation.
- [x] Capture targeted CLI snapshot data (stable option-head subset).
- [x] Run tests on the current monolith to establish baseline.
- [x] Refactor analyzer code into `pgn_analyzer/` modules.
- [x] Keep `analyze_pgn.py` as a compatibility wrapper entrypoint.
- [x] Re-run regression tests and smoke checks after refactor.
- [x] Update README for required trigger-path sync.
- [x] Document verification and rollback notes.

## Review
- Dev dependencies were added in `requirements-dev.txt`: `pytest` and `chess`.
- Baseline lock checks before refactor:
  - `.venv/bin/python -m pytest -q` -> `3 passed, 1 skipped`
- Refactor outcome:
  - Added package modules:
    - `pgn_analyzer/constants.py`
    - `pgn_analyzer/common.py`
    - `pgn_analyzer/engine.py`
    - `pgn_analyzer/forensic.py`
    - `pgn_analyzer/pipeline.py`
    - `pgn_analyzer/cli.py`
  - `analyze_pgn.py` now delegates to `pgn_analyzer.cli.run_cli()`.
- Post-refactor verification:
  - `.venv/bin/python -m py_compile analyze_pgn.py pgn_analyzer/*.py`
  - `.venv/bin/python -m pytest -q` -> `3 passed, 1 skipped`
  - `.venv/bin/python analyze_pgn.py games/2026-02-27-fast-checkmate.pgn --cause-mode heuristic --max-seconds 2 --output-md /tmp/refactor-check.md` -> completed and wrote markdown.
- Rollback plan:
  - Restore previous `analyze_pgn.py` monolith and remove `pgn_analyzer/`, then rerun `.venv/bin/python -m pytest -q`.
