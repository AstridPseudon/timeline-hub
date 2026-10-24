#!/bin/bash
# Pending final P4 recipe. Fill the D73 manifest from four fresh receipts first.
set -euo pipefail
: "${P4_LAUNCHER:?set to the exact launcher from the final Agent checkout}"
: "${P4_D73_MANIFEST:?set to the rendered final four-SHA manifest}"
: "${P4_D73_EVIDENCE:?set to the final evidence directory}"
: "${P4_D73_REQUEST_ID:?set to a fresh request id}"
exec "$P4_LAUNCHER" "$P4_D73_MANIFEST" run -- \
  -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration \
  --junitxml="$P4_D73_EVIDENCE/$P4_D73_REQUEST_ID.xml" \
  tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back \
  tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo \
  tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document
