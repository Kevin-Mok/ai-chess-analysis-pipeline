# Chess Highlights

## Overview
Two rapid games that show tactical conversion and comeback play: a 15-move checkmate on Chess.com and a resilient Lichess win against a higher-rated opponent.

## Highlight Games
| Date | Opponent | Platform | Result | Why it matters |
| --- | --- | --- | --- | --- |
| 2026-02-27 | Woaheee | Chess.com | Win (White, 1-0) | Clean tactical finish with a direct king attack and forced mate. |
| 2026-03-03 | gaju33333 | Lichess | Win (Black, 0-1) | Comeback win against 1101 after early pressure and material swings. |

## Key Moves and Turning Points
- [**15. Qxe7#** (Chess.com analyzer)](https://www.chess.com/analysis/game/live/165298129986/analysis?move=29): immediate checkmate after queen infiltration.
- [**18...Nxb2** (Lichess)](https://lichess.org/nujVa4n7#36): wins queenside material and flips initiative.
- [**26...Qxe2** (Lichess)](https://lichess.org/nujVa4n7#52): tactical conversion of central pressure into a clear advantage.
- [**34...Qxc7** (Lichess)](https://lichess.org/nujVa4n7#68): forces queen simplification and leads directly to resignation.

## Study/Analysis Links
- [Chess.com game](https://www.chess.com/game/live/165298129986?move=0)
- [Chess.com analysis](https://www.chess.com/analysis/game/live/165298129986/analysis)
- [Lichess game](https://lichess.org/nujVa4n7)
- [Lichess study chapter](https://lichess.org/study/9tKdUwCn/7y3AQeFe)

## How to View the Games
Open either PGN from `games/2026-02-27-fast-checkmate.pgn` or `games/2026-03-03-comeback-vs-gaju33333.pgn` in Chess.com or Lichess analysis boards, or import into any PGN viewer.

## Engine Analysis
- Generate analysis with `python3 analyze_pgn.py <pgn-path>`.
- Markdown is written automatically to `analysis/<game-name>.md`.
- Output is POV-oriented to `SoloPistol` by default; override with `--pov-player "<name>"`.
- Use `--output-md "<path>"` for a custom output file, or `--output-md -` to print to stdout.

Visual highlight:

![Lichess comeback highlight](media/2026-03-03-lichess-comeback.gif)

## Next goals
- Reduce early opening inaccuracies in Sicilian structures.
- Convert winning positions with fewer time-pressure blunders.
- Add one annotated highlight game each week.
