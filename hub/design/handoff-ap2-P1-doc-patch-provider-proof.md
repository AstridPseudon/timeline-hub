# Handoff: AP2 P1 real R1 doc.patch provider proof

Base: `8a66b1ac88b88ee437e42ba4b7d14ad67930d360`.

Fixture assembly used available collection commit `250db8c8d9f5bda5f0130ecf3fe46bf78e298641` (the brief's `250db2...` spelling is not a local object) and vector commit `309cb2d321cc74c06aabcee4998375a53403c8c6`. Imported bytes match source SHA-256; the harness report contains the complete hash list.

Added only `tests/sdk/test_p1_doc_patch_provider.py` plus the explicitly permitted imported fixture/test files. The provider test executes all eight vectors via real R1 `execute`, and uses `DetachedRealm`/`DetachedPort` + `RuntimeCommitService` where the source fixture can form a Runtime document. It checks exact intended parent/list deltas, opaque preservation, JSON round-trip, created-ID inverse, disjoint/same-field behavior, and membership/order refusal atomicity.

Acceptance result:

- Required combined command: **7 failed, 31 passed, exit 1**. Failures are retained evidence: trim lacks expected derived hold/metadata cleanup; four occurrence-root vectors are rejected by current R1 command schema; membership removal reports `value_conflict` instead of expected `selection_changed`.
- `ruff`: pass.
- `mypy --follow-imports=silent`: pass.
- `git diff --check`: pass.
- `tests/editing_conformance/test_doc_patch_v2.py`: 62 passed.
- `tests/sdk/test_timeline_commit_provider.py` with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`: 111 passed.

Case dispositions and exact commands/log summaries are in the harness `report.md`. This is provider/detached-service evidence only; no H3 GO. Missing chain evidence remains Runtime HTTP + App/UI/outbox + split/trim/intervening edit + lost-ack/restart/idempotency end to end.
