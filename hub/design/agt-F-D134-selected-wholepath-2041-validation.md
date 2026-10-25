# Validation

This was a read-only source/AST/hash/contract review. No pytest, HTTP, browser, provider body, full suite, or central test request was run by this worker.

- `git -C /home/user/peteromallet/astrid-agent show tl/agt-F-D134-selected-first-return-2034:tests/sdk/test_timeline_selected_schema_runtime.py`: PASS; exact first-return source inspected.
- `git diff --stat tl/agt-F-D134-selected4-2019 tl/agt-F-D134-selected-first-return-2034 -- tests/sdk/test_timeline_selected_schema_runtime.py`: PASS; 31-line repair only.
- `git show` of frozen/current Runtime `contract/commit-v2.md`: PASS; same C0 hash `4581ea85...f9bb7`.
- `git diff 5e9ad1c6f7 ab1e4f6141 -- contract/commit-v2.md`: PASS; no contract drift.
- Python 3.11 AST/source-hash comparison against pristine Agent `a30e74e901a28b39c28facba3deb00d76f186e23`: PASS; all seven UNKNOWN cases identical, assertion counts preserved.
- Source trace through Runtime `commit_timeline`/request hash, Agent `normalize_steps`/`prepared_records`, Runtime `_is_v2_request`/accept/replay: PASS; fresh omitted-control moved-head requests classify as new modern landings, while same-key exact retries use the durable ledger.
- `accepted.zip::accepted.json` read-only record inspection: PASS; `legacy-params` is `accepted` with `rebased_onto: null`, not historical `rebased`.
- Prior central targeted result: HTTP node deselected by `lanes-integration`; no retry performed.
