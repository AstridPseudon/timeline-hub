#!/usr/bin/env bash
set -euo pipefail

# Private author/reviewer check for the D73 receiving recipe.  It is not a
# service installer and does not create a checkout, manifest, or test result.

readonly PYTHON=${D73_PYTHON:-/home/user/work/venv-agent/bin/python}
readonly HERE=$(cd -- "$(dirname -- "$0")" && pwd)

die() {
    printf 'd73-exact-nodes: %s\n' "$*" >&2
    exit 1
}

bind_id() {
    local output=${1:?D66 output directory is required}
    case "$output" in
        */d66) ;;
        *) die "D66 output must end in /d66: $output" ;;
    esac
    local parent=${output%/d66}
    local id=${parent##*/}
    [[ "$id" =~ ^[A-Za-z0-9._-]+$ ]] || die "invalid central request ID: $id"
    [[ -n "$id" ]] || die "empty central request ID"
    printf '%s\n' "$id"
}

bind_check() {
    test "$#" = 2 || die "--bind-check requires two synthetic .../d66 paths"
    local first second
    first=$(bind_id "$1")
    second=$(bind_id "$2")
    test "$first" != "$second" || die "central IDs collided: $first"
    test "$1/$first.xml" != "$2/$second.xml" || die "XML paths collided"
    printf 'binding: PASS (%s -> %s.xml; %s -> %s.xml)\n' "$first" "$first" "$second" "$second"
}

source_check() {
    PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/check.py"
}

controls() {
    # Bounded source controls are independent of missing receiving inputs.
    test -n "${TMPDIR:-}" && test -d "$TMPDIR" || die "TMPDIR must be private scratch"
    PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/test_recipe.py"
}

case "${1:-}" in
    --bind-check)
        shift
        bind_check "$@"
        ;;
    --source-check)
        shift
        test "$#" = 0 || die "--source-check takes no positional arguments"
        source_check
        ;;
    --controls)
        shift
        test "$#" = 0 || die "--controls takes no positional arguments"
        controls
        ;;
    *)
        die "usage: $0 --bind-check PATH/d66 PATH/d66 | --source-check | --controls"
        ;;
esac
