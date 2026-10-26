# Validation

Read-only source checks and pure controls:

- `node evidence/pure-route-control.mjs` → `PASS_PURE_PROSPECTIVE_ONLY`; builder blob, source tuple, normal/preflight recipe sizes and hashes verified. Candidate checkout reported unmaterialized.
- `node evidence/check-source.mjs` → `PASS_SOURCE_BLOBS_AND_TUPLE`; candidate, Agent, Runtime, and Composition commit/tree identities and all listed candidate blobs verified. Runtime helper verified at 67,914 bytes, SHA-256 `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
- `node evidence/synthetic-controls.mjs` → `PASS_FAITHFUL_INTERCEPTS_ONLY`; the exact observation value reached the intercepted service process, Playwright launch, and native argv/cwd capture. Request-test, wait-test, browser, and Runtime/App request effects were intercepted and not executed.
- Candidate source review read-only: the prior mounted-capture review passed its 6/6 lifecycle controls and the prior route review passed the finite builder controls. This packet did not rerun those suites.

Not run by instruction: request-test, wait-test, row CAS, registration, checkout request/materialization, installation, collection, browser, Runtime/App request, native D66, body production, full suite, or product tests. No source changes were made in the Composition worktree.
