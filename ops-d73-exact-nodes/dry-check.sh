#!/usr/bin/env bash
set -euo pipefail

# Private author/reviewer check for the D73 receiving recipe.  It is not a
# service installer and does not create a checkout, manifest, or test result.

readonly EXPECTED_LAUNCHER_SHA=9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd
readonly EXPECTED_SELECTED_SHA=8243f3b9fe71b218b3b6a402c10d099e15c848b91b82770383e91a2dd3a72b86
readonly EXPECTED_FORK_SHA=3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4
readonly EXPECTED_CONTROL_SHA=0c2c70bd5e26598beebd31f4c7a0a3c1bf48bdc5e9f32ff93c6b54bf15b4b600
readonly PYTHON=${D73_PYTHON:-/home/user/work/venv-agent/bin/python}

die() {
    printf 'd73-exact-nodes: %s\n' "$*" >&2
    exit 1
}

sha256() {
    sha256sum "$1" | awk '{print $1}'
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
    local agent=${D73_AGENT_HOME:?D73_AGENT_HOME must name the receipt-backed Agent checkout}
    local receipt=${D73_AGENT_RECEIPT:?D73_AGENT_RECEIPT must name the receiving receipt}
    local runtime=${D73_RUNTIME_HOME:?D73_RUNTIME_HOME must name the Runtime receipt checkout}
    local manifest=${D73_MANIFEST:?D73_MANIFEST must name the rendered four-repository manifest}
    local commit=${D73_AGENT_COMMIT:?D73_AGENT_COMMIT must come from the source receipt}
    local tree=${D73_AGENT_TREE:?D73_AGENT_TREE must come from the source receipt}

    test -r "$receipt" || die "Agent receipt is not readable: $receipt"
    test -r "$manifest" || die "manifest is not readable: $manifest"
    test "$(realpath "$agent")" = "$agent" || die "Agent path is not canonical: $agent"
    test "$(realpath "$runtime")" = "$runtime" || die "Runtime path is not canonical: $runtime"
    test "$(git -C "$agent" rev-parse HEAD)" = "$commit" || die "Agent commit mismatch"
    test "$(git -C "$agent" rev-parse HEAD^{tree})" = "$tree" || die "Agent tree mismatch"
    test -z "$(git -C "$agent" status --porcelain --untracked-files=all)" || die "Agent checkout is dirty"
    test "$(git -C "$runtime" rev-parse HEAD)" = ab1e4f6141987706132916e2da16477f5a019464 || die "Runtime commit mismatch"
    test "$(git -C "$runtime" rev-parse HEAD^{tree})" = 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657 || die "Runtime tree mismatch"
    test -z "$(git -C "$runtime" status --porcelain --untracked-files=all)" || die "Runtime checkout is dirty"

    test "$(sha256 "$agent/tools/p4-d73-pinned-launch.sh")" = "$EXPECTED_LAUNCHER_SHA" || die "reviewed launcher hash mismatch"
    bash -n "$agent/tools/p4-d73-pinned-launch.sh" || die "launcher shell syntax failed"
    "$PYTHON" -m json.tool "$manifest" >/dev/null || die "manifest JSON parse failed"
    test "$(sha256 "$agent/tests/sdk/test_timeline_selected_schema_runtime.py")" = "$EXPECTED_SELECTED_SHA" || die "selected source hash mismatch"
    test "$(sha256 "$agent/tests/editing_conformance/test_occurrence_fork_source_baseline.py")" = "$EXPECTED_FORK_SHA" || die "fork source hash mismatch"
    test -f "$agent/tests/sdk/test_p4_d73_pinned_launcher.py" || die "reviewed control test is missing"
    test "$(sha256 "$agent/tests/sdk/test_p4_d73_pinned_launcher.py")" = "$EXPECTED_CONTROL_SHA" || die "control test hash mismatch"

    grep -Fq 'run -- -m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45' "$(dirname "$0")/README.md" || die "pytest argv guard missing"
    grep -Fq 'test_native_rebase_after_v2_and_selection_removal_uses_original_object' "$(dirname "$0")/README.md" || die "selected selector missing"
    grep -Fq 'test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]' "$(dirname "$0")/README.md" || die "pin selector missing"
    grep -Fq 'test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]' "$(dirname "$0")/README.md" || die "element selector missing"
    grep -Fq 'test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart' "$(dirname "$0")/README.md" || die "HTTP selector missing"
    grep -Fq 'test_current_runtime_retained_fork_then_emitter' "$(dirname "$0")/README.md" || die "fork selector missing"
    printf 'source: PASS (%s, %s)\n' "$commit" "$tree"
}

controls() {
    source_check
    local agent=${D73_AGENT_HOME:?D73_AGENT_HOME is required}
    local runtime=${D73_RUNTIME_HOME:?D73_RUNTIME_HOME is required}
    cd "$agent"
    PYTHONPATH="$agent:$runtime" "$PYTHON" -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_d73_pinned_launcher.py
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
