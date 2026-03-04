# SoloPistol vs Woaheee (SoloPistol POV)

- White: `SoloPistol`
- Black: `Woaheee`
- POV: `SoloPistol` (White)
- Turn labels: `me` = `SoloPistol`, `op.` = `Woaheee`

## Significant Swings

- Config: threshold=20.0 pts, scope=pov, max-events=8, cause-mode=forensic

- [Major] 4. Bd3 (me): W/L/D 89.7/0.0/10.3 -> 22.5/0.0/77.5, eval 1.35 -> 0.71, expected score 0.95 -> 0.61 (-33.6 pts)
  Impact: me=negative (-33.6 pts), op.=positive (+33.6 pts)
  Best: d4 (Stockfish+Lc0) | Played: Bd3 | Opportunity cost: 0.64 pawns worse
  Engines: Stockfish=0.43 pawns worse, Lc0=0.86 pawns worse, confidence=Medium
  Evidence: SF PV d4 Nf6 Be2 exd4 Nxd4 d6 | Lc0 PV d4
  Cause: Minor inaccuracy; the played move is playable but less precise than engine preference.
  Lesson: Aim for higher-precision candidate filtering when multiple reasonable moves exist.


- [Major] 5. O-O (me): W/L/D 83.8/0.0/16.2 -> 12.1/0.0/87.9, eval 1.25 -> 0.57, expected score 0.92 -> 0.56 (-35.8 pts)
  Impact: me=negative (-35.8 pts), op.=positive (+35.8 pts)
  Best: Nxd4 (Stockfish+Lc0) | Played: O-O | Opportunity cost: 0.46 pawns worse
  Engines: Stockfish=0.36 pawns worse, Lc0=0.57 pawns worse, confidence=Medium
  Evidence: SF PV Nxd4 exd4 Nb5 d5 O-O dxe4 | Lc0 PV Nxd4
  Cause: Minor inaccuracy; the played move is playable but less precise than engine preference.
  Lesson: Aim for higher-precision candidate filtering when multiple reasonable moves exist.


- [Major] 9. Ne2 (me): W/L/D 90.1/0.0/9.9 -> 0.1/3.4/96.5, eval 1.36 -> -0.33, expected score 0.95 -> 0.48 (-46.7 pts)
  Impact: me=negative (-46.7 pts), op.=positive (+46.7 pts)
  Best: d4 (Stockfish+Lc0) | Played: Ne2 | Opportunity cost: 1.18 pawns worse
  Engines: Stockfish=1.52 pawns worse, Lc0=0.84 pawns worse, confidence=Medium
  Evidence: SF PV d4 b5 | Lc0 PV d4
  Cause: Minor inaccuracy; the played move is playable but less precise than engine preference.
  Lesson: Aim for higher-precision candidate filtering when multiple reasonable moves exist.


- [Critical] 15. Qxe7# (me): W/L/D 100.0/0.0/0.0 -> 0.0/0.0/100.0, eval M+1 -> M+0, expected score 1.00 -> 0.50 (-50.0 pts)
  Impact: me=negative (-50.0 pts), op.=positive (+50.0 pts)
  Cause: forensic analysis failed (Timed out waiting for 'readyok' from Lc0.). Falling back to heuristic.
  Cause: Likely cause: forced mating threat appeared against POV.

```text
Ply   Turn Move    Win% Loss% Draw%    Eval
-------------------------------------------
1.    me  e4       1.9   0.3  97.8    0.18
1...  op. e5       3.4   0.2  96.4    0.29
2.    me  Nf3      2.2   0.2  97.6    0.21
2...  op. Qe7     48.9   0.0  51.1    0.93
3.    me  Nc3     40.4   0.0  59.6    0.86
3...  op. Nc6     89.7   0.0  10.3    1.35
4.    me  Bd3     22.5   0.0  77.5    0.71
4...  op. Nd4     83.8   0.0  16.2    1.25
5.    me  O-O     12.1   0.0  87.9    0.57
5...  op. Nxf3+   18.6   0.0  81.4    0.67
6.    me  Qxf3    20.5   0.0  79.5    0.69
6...  op. Nf6     19.6   0.0  80.4    0.68
7.    me  Bb5      4.2   0.1  95.7    0.36
7...  op. c6       3.0   0.1  96.9    0.30
8.    me  Ba4      2.2   0.2  97.6    0.24
8...  op. g6      90.1   0.0   9.9    1.36
9.    me  Ne2      0.1   3.4  96.5   -0.33
9...  op. Bh6      1.0   0.3  98.7    0.11
10.   me  d4       0.8   0.4  98.8    0.06
10... op. Bxc1     0.7   0.4  98.9    0.03
11.   me  Raxc1    1.0   0.3  98.7    0.11
11... op. exd4     2.9   0.1  97.0    0.32
12.   me  Nxd4     1.6   0.2  98.2    0.21
12... op. Nxe4   100.0   0.0   0.0    2.60
13.   me  Rce1   100.0   0.0   0.0    2.55
13... op. Nd2    100.0   0.0   0.0    8.21
14.   me  Qe2    100.0   0.0   0.0    4.23
14... op. Nxf1   100.0   0.0   0.0     M+1
15.   me  Qxe7#    0.0   0.0 100.0     M+0
```
