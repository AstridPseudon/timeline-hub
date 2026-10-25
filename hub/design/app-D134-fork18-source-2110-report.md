## D134 root-008 report

Status: **UNAPPLIED / NOTRUN**

- Read PLAN and traced the registered provider, producer/history ABI, retained failures, and passing current comparator.
- Mapped all 18 exact node IDs, inputs, topology, opaque values, and predicates in `evidence/predicate-map.json`.
- No faithful caller/setup correction is supported within the two owned files without changing ABI, authored inputs, or predicates.
- Both owned files remain byte-identical to base `96a6b2deea46eb33ba5184203a10e966cc5e9179`.

Validation:

- `ruff check ...`: PASS
- `mypy ...`: PASS — no issues in 2 files
- Python 3.11 AST parse/compile: PASS
- `git diff --check`: PASS
- Outside-scope blob equality: PASS
- Pytest, collection, replay, browser/service, and protected review: **NOTRUN** as required.

Missing evidence is an authenticated current Runtime ABI-1 fork record with canonical predecessor/output closure, including `recorder_abi`, bindings, and history boundaries. Root classification remains UNKNOWN; this is not product-fault proof.

Evidence is under the worker `evidence/` directory. `DONE` marker and D134 commit message are present.