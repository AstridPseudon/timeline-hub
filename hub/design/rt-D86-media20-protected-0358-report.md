## F-D86 source review — PASS_SOURCE

Restored the original guarded `doc.patch` transition setup in [test_commit_runtime_parent_media.py](/home/user/work/wt/rt-D86-media20-protected-0358/tests/editing_conformance/test_commit_runtime_parent_media.py).

- Genuine `occurrence.add-media` allocation remains unchanged.
- Transition preserves exact value `{type: crossfade, duration: 0.5}`.
- Uses canonical `internal-revision:<id>` provenance and `clips/id:clip-2`.
- Uses explicit `ABSENT` previous-value guard.
- All original IDs, opaque fields, media refs, created claims, branches, decorators, parameters, 67 assertions, and 7 raises remain byte-identical to `tl/rt-D86-media20-transition-return-0352`.
- Candidate SHA256: `e04abad83ad5136ab5ec1ba2ce11d56a425799120d726791051405bcfcb2036d`
- Original SHA256: identical.

### FAIL_SOURCE

The pre-patch source used `capture_clip_set(values={'transition': ...})`. Current schema permits only `hold` in `values`; transition is only valid for clearing. This was the source-level cause of the unsupported-transition path.

### Checks

- In-memory AST/topology/input checks: PASS
- In-memory schema validation: PASS
- `/home/user/work/venv-agent/bin/ruff check ...`: PASS
- `/home/user/work/venv-agent/bin/mypy --follow-imports=skip --ignore-missing-imports ...`: PASS
- `git diff --check`: PASS
- Functional pytest/collection/service execution: intentionally not run per task.

No product, schema, generated, pin, dependency, or other test files changed. Proposed D72 disposition: retain as an existing faithful fixture-repair entry; functional proof remains unverified until the later approved Main-source change. Commit message and `DONE` marker are present.