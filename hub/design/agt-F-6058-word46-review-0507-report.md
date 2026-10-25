## PASS_SOURCE — F-D86

Reviewed source commit `a8bf1e51c644bbb3ee8593a3ef888362d6dd0666` against `tl/integration` parent `d540651f9accd2a5e0c96daa9e097aeab71dffe0`.

- Exact one-file diff: `tests/editing_conformance/native_word_anchor_fixture.py`, `4 insertions / 6 deletions`.
- Removed historical Runtime `80973d34…` fallback.
- Subprocess now uses the parent-selected `use_runtime()` path, same interpreter, explicit Agent+Runtime `PYTHONPATH`, and current registered provider path.
- Runtime provider registration and canonical `commitTimeline` route remain unchanged.
- 46-case membership conserved: 37 word selectors + 9 cohort selectors.
- Seed bytes, MIME, transcript text/IDs, pins, timing/FPS, topology, opaque values, assertions, refusal/retry/inverse/ABA/no-write guards unchanged.
- No product or other test files changed.

Checks:

- Candidate and parent Ruff: PASS.
- Candidate and parent mypy: PASS.
- Parent/candidate in-memory AST compile: PASS.
- `git diff --check`: PASS.

No pytest, imports, collection, fixtures, services, probes, or functional suites were run. The historical inner subprocess exception remains UNKNOWN; functional qualification requires the central MAIN46 run on the current tuple.

Required commit message and `DONE` marker created.