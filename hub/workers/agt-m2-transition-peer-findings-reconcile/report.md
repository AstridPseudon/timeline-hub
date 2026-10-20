Implemented and verified the transition reconciliation.

- Enforced Main adjacency and shortest-neighbor fit.
- Added retained-P1 authority for same-reference selected-pack `clip.set`; P2 substitution now refuses atomically.
- Preserved clear semantics, schema, and inverse machinery.
- Added executable counterexamples and published [reconciliation report](/home/user/work/wt/agt-m2-transition-peer-findings-reconcile/ORCH/design/agent-transition-eb115-peer-reconciliation.md).

Tests:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_selected_param_authority.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_clip_scalar_provider.py tests/sdk/test_timeline_current_union_schema.py
```

Result: 183 passed. No full/browser/socket suites run. No blockers. Commit message and `DONE` marker created.