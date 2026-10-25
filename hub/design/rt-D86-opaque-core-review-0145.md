## Verdicts

- **A — PASS_A (source-only):** Candidate blob `5ae20ab0…` restores genuine shared occurrence-1/2 topology via `occurrence.delete` → guarded `doc.patch` → `occurrence.place-shared` → guarded authored-data/order patch. Opaque matrix, assertions, branches, parameters, decorators, and test bodies are preserved. Only the requested test changed; create/fork files remain untouched.
- **B — SOURCE_EXACT / sourcefacts only:** Exact target blob `91b8d15…`; no edits. Retain both findings: lost-ACK replay is refused for sequential metadata mismatch, and the optional-session case returns `merged` while the source assertion expects `rebased`. No behavioral PASS claimed.

## Evidence

- A source SHA-256: `5ae20ab0a747a16debdd5415516a07f1e6f35118a16a2afdcfbdf1b4716ea770`
- B Git blob: `91b8d15affa7f21f46eef6cfef32a0f30e9d651a`
- AST parse/in-memory compile: PASS.
- AST authored-test/predicate conservation: PASS.
- Ruff baseline/candidate: PASS.
- Pinned mypy A baseline/candidate: PASS.
- B mypy is source-identical, but environment lacks `types-PyYAML`; not green locally.
- `git diff --check`: PASS.
- No pytest, collection, fixtures, services, browsers, builds, or full suites run.

The supplied rehearsal XML was read; its broad batch was `39 failed, 30 passed, 176 errors`, automatic `NO-GO`, and was not treated as qualification.

Commit message written and `DONE` marker created. Proposed log entry:

`F-D86 opaque/core protected review: PASS_A for opaque source; B SOURCE_EXACT with retained lost-ACK and merged-vs-rebased findings; functional qualification pending MAIN.`