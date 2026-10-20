# Runtime catalog/history proof review

## Verdict

**BLOCK at the qualification gate, for the permanent negative test only.** The Runtime product implementation is security/data-safety sound in this review, but the required HTTP proof is not yet admissible: the untracked negative test updates `timeline_shots`, while the committed `music-documents` film fixture has zero rows in that table after the real move. Its `assert changed.rowcount > 0` therefore fails before the intended refusal is exercised.

This is not a discovered Runtime bypass. The minimal fix is test-only: mutate a populated retained projection in the real film (for example `project_shots.name`) and assert the existing refusal (`history_unavailable`, with the existing `unaccounted_shot_projection` reason), or provide a normal fixture with an authenticated non-empty `timeline_shots` projection. Do not seed accepted history with SQL.

## Exact product inventory reviewed

Base: `601d533d91e3726c4f7ae74723e8eff4adbe2f90`.

The leased product worktree was reviewed with the three modified tracked files and both untracked files included. The final harness must verify these exact SHA256s before merge:

| File | SHA256 |
| --- | --- |
| `runtime_protocol/service.py` | `db7442b0c2c87a8d07b6605ce5601cf8d1e9bffef98e40b22525f904cd5bf4d0` |
| `runtime_protocol/timeline_commit_baseline.py` | `36076f4a0ffa26e6544ec9704000a22a6bd46370cacb6577ea9f5dadac346e31` |
| `runtime_protocol/timeline_commit_store.py` | `170fac1a19f99659c03157d236a63e056affd40bfecf840ddf2e2b299b05822a` |
| `runtime_protocol/timeline_catalog.py` | `4fcc2bd80f6e2bac13931dc2ddf14fb82513606ade8886283052177b8e5eeec56` |
| `tests/test_timeline_catalog_history_integration.py` | `e6dd7870729646f707add6f8cbb40005c21ab778a99f3c975be27319306cb69d` |

## Review findings

- `timeline_catalog.timeline_resource` is structurally identical to the old `RuntimeService._timeline_resource` function after normalizing `self.store.conn` to the new `connection` parameter. The AST comparison returned `projection_ast_equal=True`; the service now delegates to this function without changing the projection.
- `verify_catalog_tail` does not whitelist an event kind by itself. The caller first verifies the complete timeline hash chain and project identity. Each archive/recover event then requires exact payload keys, project ID, integer version progression, one matching receipt at the exact stream position, aggregate/stream/event identity, strict project-sequence ordering, the correct command kind, and the exact normal request hash. It checks the stored full projection (or only the existing expired-result hash) against current state and final visibility/version. Legacy `head_publication_id` null is accepted only for a verified `legacy_unknown` publication boundary.
- The baseline ledger guard exempts only receipt transaction IDs returned by that proof, plus the pre-existing display-only rename rule. Unknown events, malformed/missing/ambiguous catalog receipts, target-version recover facts, and unrelated scoped ledger writes still fail closed.
- On a catalog tail, recorded heads reuse the existing canonical closure equality and existing shot projection/text-binding checks. The retained flat `timeline_revisions` shots/references snapshot is compared with live state, so a catalog receipt cannot launder film projection drift. No provider replay, evaluator, DTO, table, journal, or film-history edge was added.
- Reads and acceptance are serialized by the existing store mutex. Acceptance calls the same head proof from `_check_head` inside the existing SQLite transaction; no new external-writer synchronization was introduced.
- Expired catalog responses are handled by their existing exact result hash; when a later rename prevents reconstructing the old name, the code remains fail-closed. Receiptless and otherwise unproven legacy facts remain refused.

## Focused evidence

These were review probes only; no product file was modified.

1. With the real Agent provider (`afcb326c`), a real `clip.move` acceptance followed by archive/recover preserved the canonical head, accepted history, and closure; exact archive/recover retries returned the original receipts without writes. Result: **PASS**.
2. With the same real provider and move, changing populated `project_shots.name` before genuine archive/recover caused `head` to refuse with `history_unavailable` / `unaccounted_shot_projection`; the catalog receipts did not launder the write. Result: **PASS**.
3. The projection extraction comparison returned `projection_ast_equal=True`. `git -C /home/user/work/wt/rt-m2-history-after-catalog-visibility diff --check` passed.

## Qualification status and limits

The primary's corrected central request `rt-m2-history-after-catalog-visibility-catalog-history-agentafcb-integration-1020192212-3733` was still `queued` at review time. It must not be reported as a passing HTTP test. I did not rerun the real HTTP lane, the primary's 128 baseline checks, or its 37 service checks. The separate Agent facade retry issue remains outside this Runtime review; the corrected fixture uses the existing generated transport for the exact retry.

After the test-only negative correction, rerun that single central HTTP request against the exact inventory above. Only then can this review be upgraded from qualification BLOCK to product-hash-tied APPROVE.
