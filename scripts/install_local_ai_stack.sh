#!/usr/bin/env bash
set -euo pipefail

# Installs a fully local (zero-cost) AI stack for enhanced chess swing analysis:
# - Stockfish (via apt package)
# - Lc0 engine (built from source)
# - llama.cpp CLI (built from source)
# - Lc0 best network
# - Local GGUF model for llama.cpp

INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local}"
LC0_BRANCH="${LC0_BRANCH:-release/0.32}"
LC0_NET_TARGET="${LC0_NET_TARGET:-/usr/local/share/lc0/best.pb.gz}"
LLAMA_MODEL_PATH="${LLAMA_MODEL_PATH:-$HOME/models/gemma-3-1b-it-Q4_K_M.gguf}"
LLAMA_MODEL_URL="${LLAMA_MODEL_URL:-https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf}"

run_root() {
    if [[ "${EUID}" -eq 0 ]]; then
        "$@"
    else
        sudo "$@"
    fi
}

need_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Missing required command: $1" >&2
        exit 1
    fi
}

need_cmd git
need_cmd curl
need_cmd cmake

if [[ "${EUID}" -ne 0 ]]; then
    sudo -v
fi

echo "[1/5] Installing system dependencies..."
run_root apt-get update
run_root apt-get install -y \
    stockfish \
    build-essential cmake ninja-build meson git curl pkg-config python3 python3-pip \
    libopenblas-dev libeigen3-dev zlib1g-dev \
    libboost-program-options-dev libboost-filesystem-dev libboost-thread-dev \
    ocl-icd-opencl-dev opencl-headers

tmp_root="$(mktemp -d)"
cleanup() {
    rm -rf "${tmp_root}"
}
trap cleanup EXIT

echo "[2/5] Building and installing lc0..."
git clone --depth 1 -b "${LC0_BRANCH}" https://github.com/LeelaChessZero/lc0.git "${tmp_root}/lc0"
(
    cd "${tmp_root}/lc0"
    ./build.sh
)
if [[ ! -x "${tmp_root}/lc0/build/release/lc0" ]]; then
    echo "lc0 build failed: binary not found at build/release/lc0" >&2
    exit 1
fi
run_root install -d "${INSTALL_PREFIX}/bin"
run_root install -m 0755 "${tmp_root}/lc0/build/release/lc0" "${INSTALL_PREFIX}/bin/lc0"

echo "[3/5] Building and installing llama-cli..."
git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "${tmp_root}/llama.cpp"
cmake -S "${tmp_root}/llama.cpp" -B "${tmp_root}/llama.cpp/build" \
    -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS
cmake --build "${tmp_root}/llama.cpp/build" --config Release -j"$(nproc)"
if [[ ! -x "${tmp_root}/llama.cpp/build/bin/llama-cli" ]]; then
    echo "llama.cpp build failed: binary not found at build/bin/llama-cli" >&2
    exit 1
fi
run_root install -m 0755 "${tmp_root}/llama.cpp/build/bin/llama-cli" "${INSTALL_PREFIX}/bin/llama-cli"

# Install llama.cpp shared libraries required by llama-cli runtime.
mapfile -t llama_libs < <(find "${tmp_root}/llama.cpp/build" -type f -name 'lib*.so*' | sort)
if [[ ${#llama_libs[@]} -eq 0 ]]; then
    echo "llama.cpp build failed: no shared libraries found under build/" >&2
    exit 1
fi
run_root install -d "${INSTALL_PREFIX}/lib"
for lib_path in "${llama_libs[@]}"; do
    run_root install -m 0755 "${lib_path}" "${INSTALL_PREFIX}/lib/$(basename "${lib_path}")"
done
run_root ldconfig

echo "[4/5] Downloading Lc0 network..."
best_net_url="$(
    curl -fsSL https://lczero.org/play/networks/bestnets/ \
    | grep -oE 'https://storage\.lczero\.org[^" ]+\.pb\.gz' \
    | head -n 1
)"
if [[ -z "${best_net_url}" ]]; then
    echo "Could not discover a best-network URL from lczero.org." >&2
    exit 1
fi
curl -fL --retry 3 "${best_net_url}" -o "${tmp_root}/best.pb.gz"
run_root install -d "$(dirname "${LC0_NET_TARGET}")"
run_root mv "${tmp_root}/best.pb.gz" "${LC0_NET_TARGET}"
run_root chmod 0644 "${LC0_NET_TARGET}"

echo "[5/5] Downloading local GGUF model..."
mkdir -p "$(dirname "${LLAMA_MODEL_PATH}")"
curl -fL --retry 3 "${LLAMA_MODEL_URL}" -o "${LLAMA_MODEL_PATH}"

echo
echo "Install complete. Verifying:"
if [[ -x /usr/games/stockfish ]]; then
    echo "stockfish: /usr/games/stockfish"
elif command -v stockfish >/dev/null 2>&1; then
    echo "stockfish: $(command -v stockfish)"
else
    echo "stockfish: not found in PATH (unexpected)"
fi
echo "lc0: $(command -v lc0)"
echo "llama-cli: $(command -v llama-cli)"
ls -lh "${LC0_NET_TARGET}" "${LLAMA_MODEL_PATH}"
