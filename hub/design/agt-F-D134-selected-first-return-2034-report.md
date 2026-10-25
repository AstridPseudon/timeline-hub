## D134 report

Changed [test_timeline_selected_schema_runtime.py](/home/user/work/wt/agt-F-D134-selected-first-return-2034/tests/sdk/test_timeline_selected_schema_runtime.py):

- Restored original ABI-1 request controls and `rebased` assertions.
- Rebuilt HTTP setup through the registered provider with the exact retired parent shape; `config.clips` remains absent.
- Preserved all seven UNKNOWN cases unchanged.

Validation:

- Python 3.11 compile: PASS.
- Ruff: PASS.
- Mypy: known baseline failure only (`types-PyYAML` missing).
- Diff check and source conservation: PASS.
- Three local nodes executed but current Runtime returned `merged`; assertions remain `rebased` per C0 compatibility rules.
- HTTP node unverified: central service deselected it for `lanes-integration`; no retry.

Evidence is under [evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-selected-first-return-2034/evidence). Commit message and `DONE` marker were created.