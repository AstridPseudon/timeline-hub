## Report

- Recovered opacity candidate `c7533012` and App writer census.
- Verified Main path: `ClipPanelBody.tsx:437-443` writes top-level `clip.opacity`, raw range `0..1`.
- `clip.set-params` is invalid because it targets `params.opacity`.
- Candidate schema change conflicts with the frozen approved S2 schema; reverted it. No Agent product files changed.
- Published private contract/golden in [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-opacity-native-writer-slice/report.md).

Tests:

```text
python3 -m pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/sdk/test_timeline_current_union_schema.py
119 passed, 2 warnings
```

Agent tree: `a760ecca`; canonical schema SHA restored to `a6f1aaa9…190ef`. App consumer remains on the snapshot writer pending Runtime/App agreement and schema generation. `DONE` and commit message files created.