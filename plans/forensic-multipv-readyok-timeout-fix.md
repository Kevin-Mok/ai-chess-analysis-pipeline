# ExecPlan: Forensic MultiPV readyok timeout fix

## Goal
Prevent forensic analysis from failing with `Timed out waiting for 'readyok' from Lc0` when running with `--forensic-multipv 3`.

## Plan
- [x] Identify timeout source in UCI engine wrapper.
- [x] Implement robust ready synchronization around `setoption MultiPV`.
- [x] Validate with a local forensic run using MultiPV 3.
- [x] Update README to reflect behavior change.
- [x] Summarize risks, verification, and rollback notes.

## Notes
- Keep behavior deterministic.
- Keep diff surgical (no unrelated refactors).

## Review
- Validation command completed successfully:
  - `python3 analyze_pgn.py games/3.4-play-well.pgn --cause-mode forensic --forensic-multipv 3 --output-md analysis/3.4-play-well.md`
- Forensic phase completed all `8/8` events with no fallback errors.
- `analysis/3.4-play-well.md` no longer contains:
  - `Timed out waiting for 'readyok' from Lc0`
  - `Falling back to heuristic`
- Risk: forensic fallback still exists for true engine failures, but transient MultiPV synchronization timeouts are reduced.
- Rollback: revert changes in `analyze_pgn.py`, regenerate analysis artifact.
