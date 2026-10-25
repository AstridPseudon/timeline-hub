#!/usr/bin/env bash
set -euo pipefail

readonly PYTHON=${D138_PYTHON:-/home/user/work/venv-agent/bin/python}
readonly HERE=$(cd -- "$(dirname -- "$0")" && pwd)

die() {
    printf 'd138-cli22: %s\n' "$*" >&2
    exit 1
}

bind_id() {
    test "$#" = 1 || die "one .../d66 path is required"
    case "$1" in */d66) ;; *) die "D66 output must end in /d66: $1" ;; esac
    local parent=${1%/d66}
    local id=${parent##*/}
    [[ "$id" =~ ^[A-Za-z0-9._-]+$ ]] || die "invalid central request ID: $id"
    test -n "$id" || die "empty central request ID"
    printf '%s\n' "$id"
}

case "${1:-}" in
    --source-check)
        test "$#" = 1 || die "--source-check takes no positional arguments"
        PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/check.py"
        ;;
    --controls)
        test "$#" = 1 || die "--controls takes no positional arguments"
        test -n "${TMPDIR:-}" && test -d "$TMPDIR" || die "TMPDIR must be private scratch"
        PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/test_recipe.py"
        ;;
    --bind-check)
        test "$#" = 3 || die "--bind-check requires two synthetic .../d66 paths"
        first=$(bind_id "$2")
        second=$(bind_id "$3")
        test "$first" != "$second" || die "central IDs collided: $first"
        test "$2/$first.xml" != "$3/$second.xml" || die "XML paths collided"
        printf 'binding: PASS (%s and %s have distinct per-ID artifacts)\n' "$first" "$second"
        ;;
    *)
        die "usage: $0 --source-check | --controls | --bind-check PATH/d66 PATH/d66"
        ;;
esac
