PASS_SOURCE — F-D85.

Updated only [test_recipe_m2_shot_pool.py](/home/user/work/wt/agt-F-M2-pool-2353/tests/editing_conformance/test_recipe_m2_shot_pool.py), migrating assigned callers to genuine Runtime bootstrap/`commitTimeline` with full v2 request fields and authenticated history. Original assertions and refusal behavior were preserved.

Validation:

- Ruff: pass
- mypy (`--follow-imports=skip --ignore-missing-imports`): pass
- In-memory compile: pass
- `git diff --check`: pass
- No pytest, service, build, or functional execution run per D85.

Retained first exception: `ambiguous or unexpected fork materialization` from detached `AuthenticatedRedo`/`MediaRealm`; resolved as a fixture-caller seam.

Working blob: `413c1c60bed04141673e61274a2771c52c6437ab`  
SHA-256: `7a35066fc572bc774f0d06047983914b8cdeeb84c697f6ce54d4d375861f4e41`

Commit message and `DONE` marker created. Functional qualification remains for the later affected-node MAIN batch.