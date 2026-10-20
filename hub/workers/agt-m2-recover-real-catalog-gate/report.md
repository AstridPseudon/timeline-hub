## Report

- Added a bounded real HTTP qualification test in [test_timeline_checkout_history_runtime.py](/home/user/work/wt/agt-m2-recover-real-catalog-gate/tests/sdk/test_timeline_checkout_history_runtime.py:107).
- Pinned the test to Runtime `ca1f1b6df9a4df9a7febd03c4d3b3f9cd2260b99` via KEEP checkout `/home/user/work/wt/rt-pin-ca1f1b6d`.
- Public producer/client and production code remain unchanged.

Tests:

- `python3 -m pytest -q tests/sdk/test_native_timeline_facades.py tests/v10/test_domain_cli_projects_timelines.py` — **124 passed, 1 skipped**.
- Central real HTTP lane — **12 passed, 1 failed**.
- Failure: after catalog recover, accepted-history read returns `409 conflict`, `reason=history_unavailable`, “timeline has untracked writes.” Archive/recover events are not accepted by Runtime’s history integrity guard.

This blocks qualification of the exact Runtime candidate and likely prevents fresh `TimelineSession` restore after catalog visibility changes. The assertion is intentionally retained; no weakening or skipping.

Created:

- `commit-msg`
- `BLOCKED`

No `DONE` marker was created.