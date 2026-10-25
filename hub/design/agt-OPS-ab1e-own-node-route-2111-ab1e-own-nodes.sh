#!/usr/bin/env bash
set -euo pipefail

# D134 source/dry control for the normal named-nodes recipe.  The normal
# service row remains the existing authoring-current8ea-nodes command shape,
# with only the immutable Runtime path and suite name changed.  This helper is
# intentionally not a service installer and never starts a provider or test.

ROOT=${AB1E_AGENT_ROOT:-$(pwd -P)}
RUNTIME=${AB1E_RUNTIME_ROOT:-/home/user/work/wt/rt-pin-ab1e4f61}
EXPECTED_RUNTIME_SHA=${AB1E_EXPECTED_RUNTIME_SHA:-ab1e4f6141987706132916e2da16477f5a019464}
EXPECTED_RUNTIME_TREE=7d8e77b2f5a4af79305c9212ce5174d3ea9fd657
PYTHON=/home/user/work/venv-agent/bin/python
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
EVIDENCE=${AB1E_EVIDENCE:-/tmp/ab1e-own-nodes}

die() {
    printf 'ab1e-own-nodes: %s\n' "$*" >&2
    return 1
}

verify_runtime() {
    test "$(pwd -P)" = "$ROOT" || die "PWD is not the Agent snapshot: $(pwd -P)"
    test -d "$ROOT/astrid" || die "Agent snapshot has no astrid package: $ROOT"
    test "$(git -C "$ROOT" rev-parse --show-toplevel)" = "$ROOT" || die "Agent root is not a git worktree"
    test -z "$(git -C "$ROOT" status --porcelain --untracked-files=all)" || die "Agent snapshot is dirty"
    test "$(realpath "$RUNTIME")" = "$RUNTIME" || die "Runtime path is not canonical: $RUNTIME"
    test "$(git -C "$RUNTIME" rev-parse HEAD)" = "$EXPECTED_RUNTIME_SHA" || die "Runtime SHA mismatch"
    test "$(git -C "$RUNTIME" rev-parse HEAD^{tree})" = "$EXPECTED_RUNTIME_TREE" || die "Runtime tree mismatch"
    test -z "$(git -C "$RUNTIME" status --porcelain --untracked-files=all)" || die "Runtime checkout is dirty"
    test -z "${PYTHONNOUSERSITE:-}" || die "PYTHONNOUSERSITE is forbidden"
}

verify_dependencies() {
    test -x "$PYTHON" || die "missing Agent Python: $PYTHON"
    test -x "$NODE" || die "missing Node executable: $NODE"
    test "$("$NODE" --version)" = v20.19.4 || die "unexpected Node version"
    command -v ffmpeg >/dev/null || die "missing ffmpeg"
    command -v ffprobe >/dev/null || die "missing ffprobe"
    test -d "$RUNTIME/runtime_protocol" || die "missing Runtime protocol source"
    test -d "$PROFILE/node_modules" || die "missing Remotion profile node_modules"
    test "$(realpath "$PROFILE/node_modules")" = "$PROFILE/node_modules" || die "Remotion node_modules is not canonical"
    test -d "$SCHEMA" || die "missing canonical schema site-packages"
}

verify_origins() {
    local output=${1:-}
    "$PYTHON" -P - "$ROOT" "$RUNTIME" "$SCHEMA" "$output" <<'PY'
import os
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
runtime = Path(sys.argv[2]).resolve()
schema_root = Path(sys.argv[3]).resolve()
output = sys.argv[4]
import astrid
import astrid_runtime_client
import astrid.core.timeline.banodoco_schema as local_schema
import banodoco_timeline_schema as shared_schema
import runtime_protocol

actual = {
    "astrid": str(Path(astrid.__file__).resolve()),
    "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
    "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
    "local_schema": str(Path(local_schema.__file__).resolve()),
    "shared_schema": str(Path(shared_schema.__file__).resolve()),
}
expected = {
    "astrid": str(root / "astrid/__init__.py"),
    "runtime_protocol": str(runtime / "runtime_protocol/__init__.py"),
    "astrid_runtime_client": str(root / "astrid_runtime_client/__init__.py"),
    "local_schema": str(root / "astrid/core/timeline/banodoco_schema.py"),
    "shared_schema": str(schema_root / "banodoco_timeline_schema/__init__.py"),
}
if actual != expected:
    raise SystemExit(f"module origin mismatch: actual={actual!r} expected={expected!r}")
if output:
    Path(output).write_text("\n".join(f"{key}={value}" for key, value in actual.items()) + "\n")
else:
    print("origins-ok")
PY
}

verify_common() {
    verify_runtime
    verify_dependencies
    verify_origins "${1:-}"
}

mode=${1:-run}
case "$mode" in
    --dry-positive)
        test "$#" = 2 || die "--dry-positive requires exactly one inert stub"
        verify_common "${AB1E_ORIGINS_BEFORE:-}"
        test -x "$2" || die "inert stub is not executable"
        "$2"
        ;;
    --dry-poison)
        test "$#" = 2 || die "--dry-poison requires exactly one inert stub"
        EXPECTED_RUNTIME_SHA=0000000000000000000000000000000000000000
        verify_common "${AB1E_ORIGINS_BEFORE:-}"
        die "poisoned Runtime unexpectedly passed preflight"
        ;;
    run)
        shift
        verify_common "${AB1E_ORIGINS_BEFORE:-}"
        for arg in "$@"; do
            case "$arg" in
                -k|--deselect|--skip*|--xfail*|--runxfail|--ignore*|--continue-on-collection-errors)
                    die "unsupported selector/guard weakening: $arg" ;;
                *test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba*)
                    die "exactmissinginput: selector hardcodes missing /home/user/work/wt/rt-pin-8ea0766f at tests/timeline/test_authoring_media.py:916" ;;
            esac
        done
        set +e
        "$PYTHON" -P -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45 "$@"
        rc=$?
        set -e
        verify_common "${AB1E_ORIGINS_AFTER:-}"
        exit "$rc"
        ;;
    *)
        die "usage: $0 [run [pytest selectors...]|--dry-positive STUB|--dry-poison STUB]"
        ;;
esac
