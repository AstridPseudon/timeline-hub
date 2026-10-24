PASS_SOURCE — changed only [tests/sdk/test_timeline_capture_projection.py](/home/user/work/wt/agt-F-capture-projection-2328/tests/sdk/test_timeline_capture_projection.py).

- Replaced stale Runtime pin and synthetic `seed_trusted_parent` setup with genuine semantic bootstrap plus `publish_authoring_candidate` → `commit_timeline`.
- Preserved all 9 selectors, decorators, parameters, assertions, and behavior checks; only Runtime-generated identity lookups changed.
- Baseline blob: `c2d999609d4fa810bf1fe972e67805d571760fce`; candidate blob: `f46957c25c2e8bb5adc68ede7613ad627cbdfe70`.
- AST census unchanged: projection golden 7 asserts, expansion golden 1, canonical image 19, candidate parameterized node 2; all call/body counts unchanged.

Checks:

- Ruff baseline: PASS
- Ruff candidate: PASS
- Mypy candidate: PASS
- `python3 -m py_compile`: PASS
- `git diff --check`: PASS

No pytest, service, build, render, or functional body execution was performed per D85/D86. Protected review and the single later batched rerun remain with the manager. Commit message and `DONE` marker were created.