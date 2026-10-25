## Verdict: FAIL — bounded source finding

Reviewed [test_recipe_m2_shot_pool.py](/home/user/work/wt/agt-F-M2-pool-review-0000/tests/editing_conformance/test_recipe_m2_shot_pool.py).

The migrated redo helper is not valid for all six cases:

- `build(..., genuine_runtime)` prepares `add-second` and `remove-middle` only with local `execute()`.
- Runtime remains at the empty-pool bootstrap.
- `accepted_boundaries()` submits only the final command to Runtime.
- `add-second` carries a prior pool read; `remove-middle` removes from an unseeded pool, so genuine Runtime will refuse or produce a non-equivalent history boundary.

Relevant lines: `261–265`, `281–294`, `195–205`. This must be repaired by the author; I made no semantic fix and requested no merge.

Checks:

- AST conservation: pass; original assertions, raises, parameters, decorators, branches, and untouched test bodies preserved.
- In-memory parse/compile: baseline and candidate pass.
- Ruff genuine venv: baseline and candidate pass.
- Mypy repository-config scoped check: baseline and candidate pass.
- Normal-import mypy: both blocked by the same environment errors (`yaml` stubs, NumPy/Python syntax); not treated as a full pass.
- `git diff --check`: pass.
- Scope: one changed file, one commit beyond `tl/integration`.
- Candidate SHA-256: `7a35066fc572bc774f0d06047983914b8cdeeb84c697f6ce54d4d375861f4e41`.
- No pytest, service, build, or functional execution run per D85.

`DONE` and review commit message were created.