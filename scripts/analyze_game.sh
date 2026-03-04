#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANALYZER="${ROOT_DIR}/analyze_pgn.py"
GAMES_DIR="${ROOT_DIR}/games"
ANALYSIS_DIR="${ROOT_DIR}/analysis"

usage() {
    cat <<'EOF'
Usage:
  scripts/analyze_game.sh <game-name-or-path> [extra analyze_pgn.py args...]

Examples:
  scripts/analyze_game.sh 2026-03-03-comeback-vs-gaju33333
  scripts/analyze_game.sh scratch-games/my-quick-test
  scripts/analyze_game.sh games/2026-03-03-comeback-vs-gaju33333.pgn
  scripts/analyze_game.sh /abs/path/to/game.pgn --cause-mode heuristic
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ "$#" -lt 1 ]]; then
    usage
    exit 1
fi

target="$1"
shift

resolve_pgn_path() {
    local t="$1"
    local path
    local matches=()

    if [[ -f "$t" ]]; then
        realpath "$t"
        return 0
    fi

    if [[ -f "${ROOT_DIR}/${t}" ]]; then
        realpath "${ROOT_DIR}/${t}"
        return 0
    fi

    if [[ -f "${GAMES_DIR}/${t}" ]]; then
        realpath "${GAMES_DIR}/${t}"
        return 0
    fi

    if [[ -f "${GAMES_DIR}/${t}.pgn" ]]; then
        realpath "${GAMES_DIR}/${t}.pgn"
        return 0
    fi

    while IFS= read -r path; do
        matches+=("$path")
    done < <(
        find "${GAMES_DIR}" -type f -name "*.pgn" \
            | awk -v q="$t" '
                {
                    file=$0
                    n=split(file, parts, "/")
                    base=parts[n]
                    sub(/\.pgn$/, "", base)
                    if (index(base, q) > 0) {
                        print file
                    }
                }
            '
    )

    if [[ "${#matches[@]}" -eq 1 ]]; then
        realpath "${matches[0]}"
        return 0
    fi

    if [[ "${#matches[@]}" -gt 1 ]]; then
        echo "Ambiguous game name '${t}'. Matches:" >&2
        printf '  - %s\n' "${matches[@]}" >&2
        return 2
    fi

    echo "Could not find PGN for '${t}'." >&2
    return 1
}

pgn_path="$(resolve_pgn_path "$target")"

if [[ "${pgn_path}" == "${GAMES_DIR}/"* ]]; then
    relative_pgn="${pgn_path#${GAMES_DIR}/}"
    output_md="${ANALYSIS_DIR}/${relative_pgn%.pgn}.md"
else
    output_md="${ANALYSIS_DIR}/$(basename "${pgn_path}" .pgn).md"
fi

mkdir -p "$(dirname "${output_md}")"

cmd=(
    python3
    "${ANALYZER}"
    "${pgn_path}"
    --output-md
    "${output_md}"
)

if [[ "$#" -gt 0 ]]; then
    cmd+=("$@")
fi

echo "Running analysis..."
echo "  PGN: ${pgn_path}"
echo "  OUT: ${output_md}"

"${cmd[@]}"

echo "Done."
echo "Output: ${output_md}"
