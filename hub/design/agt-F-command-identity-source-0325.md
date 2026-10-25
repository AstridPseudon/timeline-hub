## F-D86 report

- Traced occurrence48 (48 errors), M2placement16 errors, and recipe3 (3 errors).
- Confirmed all share Runtime’s strict claim failure: `validate_claims()` compares `schema_version/op/version/select/args` and `created`; the surfaced failure is wrapped at `service.py:2518`.
- Agent producer/test files are byte-identical to actual Agent `cef8a5be`; no Agent source correction is justified.
- Static paths preserve authored args, media pins, physical source identity, created claims, topology, opaque fields, inverse/retry/refusal guards, and C0 request fields.
- Exact mismatch remains `UNKNOWN`: exported evidence omits the private submitted-vs-produced command pair. The existing Runtime SWAP owner should inspect those pairs; strict equality must not be weakened.
- Ordinary-script comparator remains MAIN-owned and untouched.

Checks:

- In-memory compile: PASS, 11 files.
- Ruff: PASS.
- Mypy 1.17: PASS, 11 files.
- `git diff --check`: PASS.
- No pytest, collection, fixtures, services, probes, or debug execution run.
- Worktree unchanged and clean.

Recommended next evidence: existing MAIN private captures for one representative each of occurrence add/swap, placement create/unplace, and shot-pool/promotion, comparing submitted `commands[]` with provider `records.commands[].command`, including `created`.