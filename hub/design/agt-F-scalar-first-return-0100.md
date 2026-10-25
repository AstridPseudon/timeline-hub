Implemented the bounded F-D86 correction in [test_commit_runtime_clip_scalar_fields.py](/home/user/work/wt/agt-F-scalar-first-return-0100/tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py:36):

```python
value_at(Closure(bundle).payload(physical), physical, path)
```

This uses the genuine `(root, ref, path)` contract and resolved physical closure identity.

Checks:

- In-memory AST compile: pass.
- AST conservation: assertions 14→14; branches/loops/with blocks unchanged.
- Seed command registration mapping: pass.
- Ruff baseline/candidate: pass.
- `git diff --check`: pass.
- Mypy baseline/candidate: both exit 2 on the same NumPy/Python-version environment diagnostic.
- No pytest, collection, fixture, service, build, or browser execution performed.

Source SHA-256:

- Candidate test: `3ff8e7792e2f9ba3e4b052f431bbea28cbea8d4bd3daf2250a87ea4e3ec707ee`
- `_doc_patch.py`: `15cc750407eb3b057900befd95cd2bd30c28f41acda9bb2f31e5c2f48f5ad00f`

Commit message and `DONE` marker are written. Evidence is under 50 MB. Recommended next step: one fresh protected review, then normal Agent merge and later affected-main functional qualification.