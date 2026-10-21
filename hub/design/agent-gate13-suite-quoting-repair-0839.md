# Gate13 current b92 suite quoting repair

## Scope and change

Repaired only the Agent-owned gate13-current-b92-integration command in
ORCH/tests/suites.conf line 149. The artifact-count guard changed from a
single-quoted Python payload containing literal backslashes:

    -c 'import json; print(len(json.load(open(\"...\"))[\"artifacts\"]))'

to the same shell quoting with ordinary Python double-quoted literals:

    -c 'import json; print(len(json.load(open("..."))["artifacts"]))'

No preflight guard, hash, path, environment isolation setting, test selector,
test body, product source, or assertion was changed. The suite remains
registered exactly once. The three selectors remain exactly unchanged and
expand to seven cases.

## Preflight and propagation evidence

The existing failed result was:

- agent-gate13-current-b92-integration-1021083128-8324
- Agent snapshot tree 93862f0accf8bbe2331ed551b69839b47f7b8e1b
- Result: exit 1 before pytest, 0/7 executed
- Cause: Python SyntaxError: unexpected character after line continuation
  character from the artifact-count guard

A planted mismatch was run against the repaired command by changing only the
expected artifact count from 76 to 77 in a private in-memory command variant:

    CMD=$(awk '$1=="agent" && $2=="gate13-current-b92-integration" {$1=$2=""; sub(/^ +/,""); print; exit}' "$ORCH/tests/suites.conf")
    BAD=$(printf '%s' "$CMD" | sed 's/ = 76 && test -x/ = 77 \&\& test -x/')
    (cd /home/user/work/agent && bash -c "$BAD")

Result: exit 1, no output. The mismatch propagated nonzero through the
preflight chain.

The positive repaired preflight and collection used the current integration
worktree:

    CMD=$(awk '$1=="agent" && $2=="gate13-current-b92-integration" {$1=$2=""; sub(/^ +/,""); print; exit}' "$ORCH/tests/suites.conf")
    COLLECT=\${CMD/ -m integration / --collect-only -m integration }
    (cd /home/user/work/agent && bash -c "$COLLECT")

Result: all retained preflight guards passed and exactly 7 tests collected in
1.88 seconds. This included Runtime b92/tree 6abc2f..., normal95 producer
and clean checkout guards, lock/schema/artifact hashes, the 76-artifact count,
C13 tool paths, env isolation, and the exact Agent/runtime import checks.

Collected cases:

1. test_http_connected_rational_move_is_lossless_across_native_frontends[python]
2. test_http_connected_rational_move_is_lossless_across_native_frontends[cli]
3. test_http_connected_rational_move_is_lossless_across_native_frontends[sheet]
4. test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[python]
5. test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[cli]
6. test_http_connected_occurrence_move_preserves_shared_source_across_native_frontends[sheet]
7. test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable

No local test body, full suite, private suite, install, render, browser, or
transcript/document replay was run.

## One corrected central run

Exact request and wait command:

    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent gate13-current-b92-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

Result ID: agent-gate13-current-b92-integration-1021083835-1139

Result: exit 1, 7/7 executed, 7 failed in 13.88 seconds. The first
failure was:

    tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_connected_rational_move_is_lossless_across_native_frontends[python]

All seven failures stopped at the Runtime health contract check. Runtime
reported schema digest
sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816;
the Agent client expected
sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4.
The stopped-renderer case reached the same health mismatch before its
renderer-off assertions. No case reached product assertions.

## Decision and status

The minimal repair was to remove the literal backslashes inside the existing
shell single-quoted Python payload. This preserves the guard chain and avoids
changing any product or test behavior.

The quoting defect is repaired and proven by negative propagation plus
positive collection. The corrected central run is not a Gate1/3 pass because
the current Agent/Runtime integration reports a schema-digest mismatch in all
seven authorized cases. No rerun was made because the brief allows exactly
one corrected central run. Follow-up should diagnose the digest mismatch
against the existing pinned b92/normal95 contract; that work is outside this
suite-only repair.

