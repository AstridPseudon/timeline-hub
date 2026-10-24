#!/bin/bash
# D83 finite-batch recipe. The registry owns the service launch; this file supplies
# one finite seven-selector invocation through the existing D73 pinned launcher.
set -euo pipefail

manifest=${1:?usage: p4-r2-d83-unprofiled.recipe.sh MANIFEST EVIDENCE REQUEST_ID [run|probe STUB]}
evidence=${2:?usage: p4-r2-d83-unprofiled.recipe.sh MANIFEST EVIDENCE REQUEST_ID [run|probe STUB]}
request_id=${3:?usage: p4-r2-d83-unprofiled.recipe.sh MANIFEST EVIDENCE REQUEST_ID [run|probe STUB]}
mode=${4:-run}
stub=${5:-}

# This batch is intentionally unprofiled. A caller-provided profile directory
# is removed before dispatch and is never forwarded to the service.
unset P4_LIVE_PROFILE_DIR
[ -f "$manifest" ]
[ -d "$evidence" ]

manifest_value() {
  awk -F= -v wanted="$1" '$1 == wanted { sub(/^[^=]*=/, ""); print; exit }' "$manifest"
}
format=$(manifest_value format)
batch_id=$(manifest_value batch_id)
timeout_seconds=$(manifest_value timeout_seconds)
profile_mode=$(manifest_value profile_mode)
scope=$(manifest_value scope)
original_p4_test_hash=$(manifest_value original_p4_test_hash)
agent_path=$(manifest_value agent_path)
python=$(manifest_value python)
runtime_path=$(manifest_value runtime_path)
[ "$format" = p4-d73-v1 ]
[ "$batch_id" = p4-r2-d83-unprofiled-seven ]
[ "$timeout_seconds" = 45 ]
[ "$profile_mode" = unprofiled ]
[ "$scope" = actual-integrated-head ] || [ "$scope" = source-candidate-donor2 ]
[[ "$original_p4_test_hash" =~ ^[0-9a-f]{64}$ ]]
case "$python" in /home/user/work/venv-agent/bin/python) ;; *) exit 2 ;; esac
case "$runtime_path" in /home/user/work/*) ;; *) exit 2 ;; esac

case "$mode" in
  probe)
    [ -n "$stub" ]
    exec "$agent_path/tools/p4-d73-pinned-launch.sh" "$manifest" dry -- "$stub"
    ;;
  run)
    exec "$agent_path/tools/p4-d73-pinned-launch.sh" "$manifest" run -- \
      -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration \
      --junitxml="$evidence/$request_id.xml" \
      tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back \
      tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo \
      tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document \
      tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo[False-None] \
      tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo[False-public-element] \
      tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo[True-None] \
      tests/core/test_timeline_element_publication_runtime.py::test_public_helper_restart_exact_retry_later_head_inverse_redo[True-public-element]
    ;;
  *)
    echo "D83 recipe: mode must be run or probe" >&2
    exit 2
    ;;
esac
