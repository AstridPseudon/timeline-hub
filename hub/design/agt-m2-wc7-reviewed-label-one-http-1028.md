# WC7 attached parent track-label HTTP proof

## Result

APPROVE. Independently reviewed the exact 15-line fail-closed guard in
`e1e09496a17d676851c5232d7c0c6bb82450464` (`native_checkout.py`) before
adding the HTTP case. The guard admits only a native captured parent
`track.set` label command: exact resolved target, target-id read, scalar
binding, label expectation, and direct authorship are all required. An
arbitrary label-shaped outbox record is refused before flight/request
creation. No capture, auth, basis, target/ref, rationale, empty/clear, or
pending-flight behavior was relaxed.

## Change

Added one compact real Runtime HTTP fixture case in
`tests/editing_conformance/test_native_sheet_current_runtime.py` for the
single new selector `parent/track:plate`. It exercises attached
`Checkout.publish` through durable lost-ACK, outbox reload, exact original
idempotency key/body and captured guard retry, accepted-state reload, and
guarded inverse. The retired `publish_parent_composition` writer is patched
to fail, and an unrelated clip is asserted unchanged.

Source before the uncommitted test edit: `e1e09496a17d676851c5232d7c0c6bb82450464`.
Final central snapshot tree: `ab72b17e9c4aa44c718580e56eb64912a3cd36af`.

## Evidence

- Local targeted safety lane:
  `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_native_checkout.py::test_parent_track_label_publish_uses_the_existing_captured_outbox tests/sdk/test_timeline_native_checkout.py::test_parent_track_label_publish_retries_the_original_request_after_lost_ack tests/sdk/test_timeline_native_checkout.py::test_parent_track_label_publish_keeps_original_capture_on_conflict tests/sdk/test_timeline_native_checkout.py::test_parent_track_label_publish_rejects_uncaptured_label_shaped_record`
  Result: **6 passed** in 1.61s.
- Final central named service:
  `agt-m2-wc7-reviewed-label-one-http-1028-gate13-current-b92-integration-1021102837-6778`
  (`gate13-current-b92-integration`, appended new selector), result:
  **8 passed** in 54.34s. Its all-at-once preflight verified Runtime
  `b92d3e7a05eec65c142294ef4873edd059e9b31d` / tree
  `6abc2f117391de8e7e35c0283f575a002199894d`, normal95 source
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, C13 environment, current
  client imports, and contract `0.2.14`.
- Ruff on the touched implementation/tests: **All checks passed**.
- `git diff --check`: **passed**.

One initial central request targeted the integration checkout instead of this
worker, so the new selector was absent and the harness correctly reported
zero tests (`agent-gate13-current-b92-integration-1021102645-11928`, exit 4).
It was not used as product evidence; the corrected worker-targeted run above
is the final evidence.

No full, browser, render, or other broad suite was run. No blocker remains;
owner merge is the next step.
