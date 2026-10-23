# Agent G3 corrected-current join

Base `8e7fbea7cf3ce9dbf7d0deffb60c858bdd104afa` was joined with corrected U4a `7d356202826ce60ff676d6e46151187aad9f4a70` (parent `fc515591b39aba8b7c297f4934c4760b88bcd8ef`). Actual merge-tree conflicts were `astrid/sdk/timeline/commit.py` and `runtime.lock.json`.

Resolution retained current `commit.py` for the G3 emitter/history/publication and R2 whole/per-step/physical/ABA behavior. `runtime.lock.json` and `astrid_runtime_client/generated.py` were aligned to the corrected U4a wire artifacts; generated acceptance now accepts valid `merged` replies with receipts. All 15 lock-mapped files compare byte-for-byte with `7d356…`; source pin is `780da6d605033ca71dbe2ad48c10ec2870ea4865`. The six approved V4 live-scenes deletions remain absent. No G4/P4 imports, V2 policy changes, obsolete `21482` pin, arbitrary restoration, or new deletion was introduced.

Results: original media manifest reload/inverse/redo `1 passed`; focused G3/G2/R2/R3/meta tests `149 passed`; vendor/artifact tests `37 passed`; artifact manifest and vendor lock checks passed; Ruff baseline `2150/2150`; direct valid-merged generated-client probe passed; `git diff --check` passed. Normal mypy was blocked by the shared venv missing `types-PyYAML` and incompatible NumPy stubs under Python 3.13. Full suite not run.

