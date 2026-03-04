#!/usr/bin/env bash
set -euo pipefail

# Targeted repair script for llama-cli runtime dependencies only.
# It does NOT install/rebuild stockfish or lc0.
#
# What it does:
# 1) Builds llama.cpp (CPU + OpenBLAS)
# 2) Installs llama-cli to /usr/local/bin
# 3) Installs required shared libs to /usr/local/lib
# 4) Runs ldconfig
# 5) Verifies no missing libs in ldd output

INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local}"
LLAMA_REPO="${LLAMA_REPO:-https://github.com/ggml-org/llama.cpp.git}"
LLAMA_BRANCH="${LLAMA_BRANCH:-master}"
LLAMA_SRC_DIR="${LLAMA_SRC_DIR:-}"

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
need_cmd cmake
need_cmd ldd

if [[ -z "${LLAMA_SRC_DIR}" ]]; then
    workdir="$(mktemp -d)"
    trap 'rm -rf "${workdir}"' EXIT
    LLAMA_SRC_DIR="${workdir}/llama.cpp"
    git clone --depth 1 -b "${LLAMA_BRANCH}" "${LLAMA_REPO}" "${LLAMA_SRC_DIR}"
else
    LLAMA_SRC_DIR="$(realpath "${LLAMA_SRC_DIR}")"
    if [[ ! -d "${LLAMA_SRC_DIR}" ]]; then
        echo "LLAMA_SRC_DIR does not exist: ${LLAMA_SRC_DIR}" >&2
        exit 1
    fi
fi

echo "[1/4] Building llama.cpp..."
cmake -S "${LLAMA_SRC_DIR}" -B "${LLAMA_SRC_DIR}/build" \
    -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS
cmake --build "${LLAMA_SRC_DIR}/build" --config Release -j"$(nproc)"

cli_bin="${LLAMA_SRC_DIR}/build/bin/llama-cli"
if [[ ! -x "${cli_bin}" ]]; then
    echo "Build failed: ${cli_bin} not found" >&2
    exit 1
fi

mapfile -t shared_libs < <(find "${LLAMA_SRC_DIR}/build" -type f -name 'lib*.so*' | sort)
if [[ ${#shared_libs[@]} -eq 0 ]]; then
    echo "Build failed: no shared libs found under ${LLAMA_SRC_DIR}/build" >&2
    exit 1
fi

echo "[2/4] Installing llama-cli and shared libs..."
run_root install -d "${INSTALL_PREFIX}/bin" "${INSTALL_PREFIX}/lib"
run_root install -m 0755 "${cli_bin}" "${INSTALL_PREFIX}/bin/llama-cli"
for lib in "${shared_libs[@]}"; do
    run_root install -m 0755 "${lib}" "${INSTALL_PREFIX}/lib/$(basename "${lib}")"
done

echo "[3/4] Refreshing dynamic linker cache..."
run_root ldconfig

echo "[4/4] Verifying runtime linkage..."
ldd "${INSTALL_PREFIX}/bin/llama-cli" | sed -n '1,120p'
if ldd "${INSTALL_PREFIX}/bin/llama-cli" | grep -q 'not found'; then
    echo "FAIL: llama-cli still has missing shared libraries." >&2
    exit 1
fi

echo "OK: llama-cli runtime libs are resolved."
