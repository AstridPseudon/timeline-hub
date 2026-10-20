# WC3 current014 real-consumer handoff

Implemented the WC3 native media replacement deletion in the Agent worktree.

Reviewed delta/source pairing:

- Current014 candidate: `e86f44d04e0a5f183d82d4d1ac307951dd32c44e`.
- Donor reviewed: `tl/agt-m2-wc3-explicit-pin-type-guard`, `76c6c591` (native adapter plus explicit pending-pin type guard).
- Prior review reports: `agent-review-wc3-media-swap-final.md` and `agent-review-wc3-exact-retry-final.md`.
- Runtime used for real-provider integration: `/home/user/work/wt/rt-pin-a0dca169`, `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`.

Changes:

- `RemoteTimelines.replace_parent_media` now dispatches only to the native `TimelineSession` adapter; the old whole-closure writer remains absent/held.
- Pending replacement matching requires both pins omitted (`None`, `None`) or both exact five-field mappings: `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`. Mixed, malformed, or unrelated pins refuse before POST and preserve outbox state.
- Preserved current selected-P1/F1/save-core/Root/AM/read facades and existing outbox/history carriers.
- Restored the real parent-media conformance transport reads so the native adapter is exercised against managed media and the a0 provider.
- Added an exact replay assertion: after accepted-but-lost ACK and later head movement, replay uses the original body/key/base and returns the original receipt with one acceptance before the suffix is journaled.

Evidence:

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/test_timeline_clip_replacement.py tests/sdk/test_timeline_sync.py::test_lost_ack_reload_retries_exact_request_before_sending_suffix` — 22 passed.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_native_frontends.py` — 154 passed.
- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_parent_media_swap.py` — 22 passed.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline_media_replacement.py tests/test_timeline_clip_replacement.py tests/sdk/test_timeline_sync.py tests/editing_conformance/test_commit_runtime_parent_media_swap.py` — passed; `git diff --check` passed.
- Central named suite `ordinary014-consumer-integration` was requested once and stopped during collection: 15,618 deselected and 2 errors from missing `vibecomfy` imports, before target tests ran. No full suite was requested.

The direct integration command uses the real a0 Runtime provider and managed-media service; the central generated-client named lane did not reach collection, so that lane remains unverified in this worker.
