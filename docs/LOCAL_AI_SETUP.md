# Local AI Setup (Zero-Cost)

This project can generate higher-confidence swing explanations using local tools only:

- `stockfish` (table pass + forensic baseline)
- `lc0` + network weights (second-opinion forensic engine)
- `llama-cli` + local GGUF model (optional rewrite layer)

## One-command install

Run:

```bash
bash scripts/install_local_ai_stack.sh
```

The script installs dependencies (with sudo), builds `lc0` and `llama-cli`, downloads an Lc0 network, and downloads a local GGUF model.

## Default installed paths

- Stockfish: `/usr/games/stockfish`
- Lc0 binary: `/usr/local/bin/lc0`
- Lc0 weights: `/usr/local/share/lc0/best.pb.gz`
- llama-cli: `/usr/local/bin/llama-cli`
- GGUF model: `~/models/gemma-3-1b-it-Q4_K_M.gguf`

`analyze_pgn.py` auto-detects these paths.

## Usage examples

Forensic mode (default):

```bash
python3 analyze_pgn.py games/2026-03-03-comeback-vs-gaju33333.pgn
```

Forensic mode with explicit Lc0 paths:

```bash
python3 analyze_pgn.py games/2026-03-03-comeback-vs-gaju33333.pgn \
  --cause-mode forensic \
  --lc0-path /usr/local/bin/lc0 \
  --lc0-weights /usr/local/share/lc0/best.pb.gz
```

Forensic + local LLM rewrite:

```bash
python3 analyze_pgn.py games/2026-03-03-comeback-vs-gaju33333.pgn \
  --cause-mode forensic-llm \
  --llama-model ~/models/gemma-3-1b-it-Q4_K_M.gguf
```

## Troubleshooting

- If forensic mode fails with missing `lc0`, install via `scripts/install_local_ai_stack.sh` or pass `--lc0-path`.
- If forensic mode fails with missing weights, pass `--lc0-weights` to a `.pb.gz` network file.
- If `forensic-llm` cannot find `llama-cli` or model, the script falls back to deterministic forensic text.
