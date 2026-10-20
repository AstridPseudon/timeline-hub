Implemented and marked complete.

- Ported full cap/fade fixture and pinned public evaluator tests.
- Settled product golden: opacity `0.5` at frame 105; raw opacity `1` is diagnostic only.
- Preserved authored `hold: 5`, effective cap `4s`, editor clamp, and half-open frame 120 exclusion.
- Updated product docs and ORCH/design handoff with MAIN pixel references.
- No Runtime, pin, schema, renderConfig, or clamp-default changes.

Tests:

- `pytest ...`: **52 passed, 3 xfailed**
- Ruff check: **passed**
- `git diff --check`: **passed**
- Fixture/handoff JSON and identity checks: **passed**
- No full suite run.

The managed production render join remains a strict unresolved xfail. Report, commit message, and `DONE` marker were written to the requested paths.