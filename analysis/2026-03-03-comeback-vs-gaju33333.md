# SoloPistol vs gaju33333 (SoloPistol POV)

- White: `gaju33333`
- Black: `SoloPistol`
- POV: `SoloPistol` (Black)
- Turn labels: `me` = `SoloPistol`, `op.` = `gaju33333`

## Significant Swings

- Config: threshold=20.0 pts, scope=pov, max-events=8, cause-mode=forensic

- [Major] 2... Nf6 (me): W/L/D 0.2/2.4/97.4 -> 0.0/61.5/38.5, eval -0.22 -> -1.03, expected score 0.49 -> 0.19 (-29.7 pts)
  Impact: me=negative (-29.7 pts), op.=positive (+29.7 pts)
  Best: Nc6 (Stockfish+Lc0) | Played: Nf6 | Opportunity cost: 0.70 pawns worse
  Engines: Stockfish=0.65 pawns worse, Lc0=0.76 pawns worse, confidence=Medium
  Evidence: SF PV Nc6 Nge2 Nd4 Nxd4 cxd4 Ne2 | Lc0 PV Nc6
  Cause: Minor inaccuracy; the played move is playable but less precise than engine preference.
  Lesson: Aim for higher-precision candidate filtering when multiple reasonable moves exist.


- [Major] 9... d6 (me): W/L/D 100.0/0.0/0.0 -> 0.6/0.5/98.9, eval 2.94 -> 0.02, expected score 1.00 -> 0.50 (-49.9 pts)
  Impact: me=negative (-49.9 pts), op.=positive (+49.9 pts)
  Best: d5 (Stockfish+Lc0) | Played: d6 | Opportunity cost: 5.90 pawns worse
  Engines: Stockfish=2.77 pawns worse, Lc0=9.03 pawns worse, confidence=Medium
  Evidence: SF PV d5 Bb5 d4 Bxc6 bxc6 Bxh6 | Lc0 PV d5
  Cause: The move misses a tactical continuation and concedes material in the engine follow-up.
  Lesson: Scan forcing candidate moves first, then compare resulting material before choosing a move.


- [Critical] 10... Na5 (me): W/L/D 100.0/0.0/0.0 -> 0.1/2.9/97.0, eval 2.93 -> -0.31, expected score 1.00 -> 0.49 (-51.4 pts)
  Impact: me=negative (-51.4 pts), op.=positive (+51.4 pts)
  Best: d5 (Stockfish+Lc0) | Played: Na5 | Opportunity cost: 5.36 pawns worse
  Engines: Stockfish=3.07 pawns worse, Lc0=7.65 pawns worse, confidence=Medium
  Evidence: SF PV d5 Bb5 d4 Bxc6 bxc6 Bd2 | Lc0 PV d5
  Cause: Major evaluation drop from deviating from the engine-preferred continuation (d5).
  Lesson: In sharp positions, compare your move against top engine candidates before committing.


- [Major] 11... Bd7 (me): W/L/D 55.5/0.0/44.5 -> 0.7/0.4/98.9, eval 1.00 -> 0.05, expected score 0.78 -> 0.50 (-27.6 pts)
  Impact: me=negative (-27.6 pts), op.=positive (+27.6 pts)
  Best: a6 (Stockfish+Lc0) | Played: Bd7 | Opportunity cost: 0.85 pawns worse
  Engines: Stockfish=0.90 pawns worse, Lc0=0.80 pawns worse, confidence=Medium
  Evidence: SF PV a6 Ba4 b5 Bb3 d5 e5 | Lc0 PV a6
  Cause: Minor inaccuracy; the played move is playable but less precise than engine preference.
  Lesson: Aim for higher-precision candidate filtering when multiple reasonable moves exist.


- [Critical] 13... d5 (me): W/L/D 1.1/0.2/98.7 -> 0.0/100.0/0.0, eval 0.14 -> -4.64, expected score 0.50 -> 0.00 (-50.5 pts)
  Impact: me=negative (-50.5 pts), op.=positive (+50.5 pts)
  Best: dxe5 (Stockfish+Lc0) | Played: d5 | Opportunity cost: 11.22 pawns worse
  Engines: Stockfish=4.80 pawns worse, Lc0=17.64 pawns worse, confidence=Medium
  Evidence: SF PV dxe5 Nxe5 Qc8 a4 Nc6 Bf4 | Lc0 PV dxe5
  Cause: The move misses a tactical continuation and concedes material in the engine follow-up.
  Lesson: Scan forcing candidate moves first, then compare resulting material before choosing a move.


- [Critical] 29... Qb8 (me): W/L/D 78.4/0.0/21.6 -> 0.0/100.0/0.0, eval 1.22 -> -4.46, expected score 0.89 -> 0.00 (-89.2 pts)
  Impact: me=negative (-89.2 pts), op.=positive (+89.2 pts)
  Best: Nc5 (Stockfish+Lc0) | Played: Qb8 | Opportunity cost: 15.03 pawns worse
  Engines: Stockfish=5.59 pawns worse, Lc0=24.47 pawns worse, confidence=Medium
  Evidence: SF PV Nc5 Rc1 Qf8 Qd5+ Kh7 g4 | Lc0 PV Nc5
  Cause: The move misses a tactical continuation and concedes material in the engine follow-up.
  Lesson: Scan forcing candidate moves first, then compare resulting material before choosing a move.

```text
Ply   Turn Move    Win% Loss% Draw%    Eval
-------------------------------------------
1.    op. e4       0.2   2.7  97.1   -0.25
1...  me  c5       0.1   6.5  93.4   -0.42
2.    op. Nc3      0.2   2.4  97.4   -0.22
2...  me  Nf6      0.0  61.5  38.5   -1.03
3.    op. Nf3      0.1   4.3  95.6   -0.35
3...  me  Nc6      0.0   8.8  91.2   -0.50
4.    op. Bc4      1.0   0.5  98.5    0.07
4...  me  e6       0.5   0.8  98.7   -0.03
5.    op. d3       1.0   0.4  98.6    0.07
5...  me  Bd6      0.0   7.6  92.4   -0.47
6.    op. Bg5      8.8   0.0  91.2    0.51
6...  me  Be7      0.8   0.4  98.8    0.05
7.    op. O-O      0.9   0.4  98.7    0.08
7...  me  O-O      0.8   0.4  98.8    0.06
8.    op. h3       0.8   0.4  98.8    0.07
8...  me  h6       0.7   0.5  98.8    0.04
9.    op. Be3    100.0   0.0   0.0    2.94
9...  me  d6       0.6   0.5  98.9    0.02
10.   op. a3     100.0   0.0   0.0    2.93
10... me  Na5      0.1   2.9  97.0   -0.31
11.   op. Bb5     55.5   0.0  44.5    1.00
11... me  Bd7      0.7   0.4  98.9    0.05
12.   op. Bxd7     0.9   0.3  98.8    0.10
12... me  Qxd7     0.7   0.4  98.9    0.05
13.   op. e5       1.1   0.2  98.7    0.14
13... me  d5       0.0 100.0   0.0   -4.64
14.   op. exf6     0.0 100.0   0.0   -4.36
14... me  Bxf6     0.0 100.0   0.0   -4.56
15.   op. Bxc5     0.0 100.0   0.0   -4.47
15... me  Qc6      0.0 100.0   0.0   -5.62
16.   op. Bxf8     0.0 100.0   0.0   -5.39
16... me  Rxf8     0.0 100.0   0.0   -5.46
17.   op. d4       0.0 100.0   0.0   -5.37
17... me  Nc4      0.0 100.0   0.0   -5.33
18.   op. Nd2      0.0 100.0   0.0   -2.90
18... me  Nxb2     0.0 100.0   0.0   -3.18
19.   op. Qf3      0.0 100.0   0.0   -3.11
19... me  Bxd4     0.0 100.0   0.0   -3.23
20.   op. Ne2      0.0 100.0   0.0   -3.10
20... me  Bb6      0.0 100.0   0.0   -3.86
21.   op. Rac1     0.0 100.0   0.0   -3.47
21... me  f5       0.0 100.0   0.0   -4.53
22.   op. c4       0.0 100.0   0.0   -4.65
22... me  Rd8      0.0 100.0   0.0   -5.26
23.   op. cxd5     0.0 100.0   0.0   -4.44
23... me  Qd6      0.0 100.0   0.0   -5.59
24.   op. Rc2      0.0 100.0   0.0   -5.31
24... me  Na4      0.0 100.0   0.0   -5.50
25.   op. dxe6     0.0 100.0   0.0   -5.36
25... me  Qxe6     0.0 100.0   0.0   -5.50
26.   op. Qxb7     0.0 100.0   0.0   -2.98
26... me  Qxe2     0.0 100.0   0.0   -3.24
27.   op. Rc8      5.3   0.0  94.7    0.46
27... me  Qxd2     5.2   0.0  94.8    0.46
28.   op. Rxd8+   59.8   0.0  40.2    1.06
28... me  Qxd8    52.6   0.0  47.4    1.01
29.   op. Qc6     78.4   0.0  21.6    1.22
29... me  Qb8      0.0 100.0   0.0   -4.46
30.   op. Qxa4     0.0 100.0   0.0   -4.43
30... me  Qe5      0.0 100.0   0.0   -4.61
31.   op. Qb4      0.0 100.0   0.0   -4.46
31... me  Bc7      0.0 100.0   0.0   -4.66
32.   op. g3       0.0 100.0   0.0   -4.47
32... me  f4       0.0 100.0   0.0   -5.32
33.   op. Qc4+     0.0 100.0   0.0   -5.05
33... me  Kh7      0.0 100.0   0.0   -5.27
34.   op. Qxc7   100.0   0.0   0.0    5.32
34... me  Qxc7   100.0   0.0   0.0    5.28
```
