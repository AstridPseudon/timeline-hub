HOLD — candidate `689e55de` against parent `e2c7bdcb`.

Finding: `RemoteTimelines.recover()` now refuses every call (`astrid/sdk/remote.py:1609-1624`). The settled contract requires no-version/current-version recover to remain catalog unarchive; only non-current historical recovery should refuse (`runtime-timeline-visibility-restoration.md:5-19`). The changed CLI test now incorrectly asserts refusal for the no-version case (`tests/v10/test_domain_cli_projects_timelines.py:1755-1771`).

Positive revision restore is correctly routed through `TimelineSession.restore()` and `timeline.restore` with exact revision/digest, outbox, retry, and CLI commands-file paths. Legacy Agent forwarding wrappers are physically removed; only the generated vendor symbol remains, with no Agent callers.

Tests:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_native_timeline_facades.py tests/v10/test_domain_cli_projects_timelines.py tests/sdk/test_timeline_checkout_history_runtime.py` — **187 passed, 2 skipped**
- `git diff --check` — passed
- Existing worker HTTP evidence: `commit-integration` — **12 passed**; not rerun.
- Direct probe confirmed no-version recover returns `retired_route` without forwarding.

Recommended fix: preserve existing catalog recover behavior for absent/current version, add its positive visibility/idempotency/head-preservation assertion, and retain refusal only for non-current historical versions.

Markers written:

- `.../workers/agt-review-recover-retirement-mapping/commit-msg`
- `.../workers/agt-review-recover-retirement-mapping/commit-msg.txt`
- `.../workers/agt-review-recover-retirement-mapping/DONE`