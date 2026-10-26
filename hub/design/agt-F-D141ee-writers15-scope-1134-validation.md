# U2 F D141ee writers15 validation

Result: `PASS_EVIDENCE`. This is source-only evidence, not a behavior PASS, REG0, or ship claim.

- Disk: the required fresh sustained 5-second trace is in `disk-trace.txt`; available bytes were `6992437248`–`6992699392`, above the `4000000000` stop line.
- Git: Agent HEAD is `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf`, parent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, pristine `64197afa297f86f1e738238d5e80aff6d33e303a`; Runtime supported cut is `95d98f038320d5d46bd679ac000ab3e15825c935`. The worktree remained clean and no refs were changed.
- JSON: `python3 -m json.tool evidence/per-id.json`, `python3 -m json.tool evidence/source-manifest.json`, and `python3 -m json.tool evidence/restoration-manifest.json` all pass. The assigned manifest and this map each contain exactly 15 IDs: 4–18, no duplicates or omissions.
- Static source: `git show`/`git grep`/AST source reads compared every pristine body/assertion set to the current parent and then traced each row through the supported commitTimeline chain. No import, test, typecheck, lint, browser, render, request, CAS, service-body, or full-suite execution was performed in this worker.
- Retained restoration evidence: prior review is `PASS_SOURCE_RESTORATION`; exact restored targeted invocation recorded `15` failures and `40` collection errors, with `0` executed in the 55-node independent invocation because of collection errors; the unaffected 15-node invocation executed and failed all 15. The two authoring-bundle rows collected as ImportError (`promote_approved_authoring_candidate` missing). These retained summaries are not re-run evidence.
- Current replacement evidence is source/selector mapping only. It does not convert changed assertions into original-behavior PASS. The three unresolved owner-scope rows are 8, 12, and 13.
- Raw reviewer-private XML under the removed temporary control paths is not claimed to exist. Only retained JSON/log summaries supplied to this worker are cited.

Checked source/replacement coordinates include Agent `astrid/packs/timeline/cli.py`, `astrid/packs/timeline/cli_native.py`, `astrid/sdk/timeline/sync.py`, `astrid/sdk/workspace_client.py`, `astrid/sdk/timeline/commit.py`, `astrid/sdk/remote.py`, `astrid/packs/rendering/shared/runtime_stitch.py`, `astrid/core/timeline/authoring_bundle.py`, and Runtime `runtime_protocol/server.py` plus `runtime_protocol/service.py`.
