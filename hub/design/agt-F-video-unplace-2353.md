## PASS_SOURCE — F-D85

Migrated the Runtime video-unplace fixture from retired `_publish` setup to genuine bootstrap, semantic captures, registered provider, and v2 `commit_timeline` metadata. Test bodies/assertions remain AST-identical.

Changed only:

- `tests/editing_conformance/test_commit_runtime_video_unplace.py`

`test_recipe_m2_video_unplace.py` unchanged; hash `11a68fba…d23b70b`. Candidate commit-test hash: `e605c09f…c93b8bc`.

Checks passed:

- Ruff candidate and baseline
- Mypy candidate and baseline-shadow
- In-memory compile
- AST conservation
- `git diff --check`

No pytest, service, build, or functional execution run per D85.

Exact 12 selectors are preserved. Existing rollup log entry: `handoff-agt-F-rehearsal-rollup-return-2320-rehearsal-rollup.tsv`, lines 135–197. Recommend the later affected-node qualification batch on integrated main.

Commit message written; `DONE` created.