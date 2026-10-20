# Deletion ledger — Runtime rows

Current source: Runtime `9f211fcdb66023a577a14111f99c87fb32ef573c`.
This area ledger records deletion/retention decisions only; it is not a
combined ledger or a product implementation plan.

| id | what | contradicts | replaced by | ms | status | evidence |
|---|---|---|---|---|---|---|
| D04 | Runtime legacy canonical timeline publication bodies | one edit path | `/v1` commit; direct legacy writes refuse | M2 | HELD | Current clip replacement parity is independently **APPROVED** at `1f75756c` (`13 passed, 10 deselected, 1 strict xfail` centrally; the xfail is the existing parent-owned `clip.swap-media` ownership/schema case). D04 stays held: one-parent ownership remains strict-xfail, and both App D01 and Agent whole-candidate migrations remain held. |
| D11 | R4 control docs under `docs/projects/timeline-r4/` | ceremony | one architecture page | M4 | DELETED from integration surface; historical archive KEEP | No R4 docs path is present in the integration surface. The frozen historical archive is retained and unchanged. This is not a claim that the archive was deleted. |
| RT01 | Generic Document writes to reserved canonical timeline IDs/kinds | service bypass | ordinary Documents; canonical edits through commit | M2 | DELETED | Reserved canonical-document refusal remains; ordinary source-document writes remain. Existing authority/cutover tests preserve both sides. |
| RT02 | Direct film shot/item/text-binding mutation bodies | one writer and coherent projections | native commands plus accepted projections | M2 | FILM WRITERS RETIRED; native/consumer gates OPEN | Film-scope direct writers remain retired. The unplaced catalog capabilities are tracked separately in RK02; no other CRUD was restored. Native replacement and consumer qualification remain open. |
| RT03 | Direct timeline reference/placement mutation bodies | one timeline writer | guarded film EditCommands | M2 | DELETED | Timeline-scoped reference/placement writers refuse before mutation; project-catalog reference operations are retained only under RK01. |
| RT04 | Unsupported canonical task effects and pre-replay snapshot publication | one writer; refusal writes nothing | closed supported effects and persisted admission comparison | M2 | DELETED | Existing effect-authority, task-replay, and render-admission tests cover the closed set and keyed comparison. |
| RT05 | Retired timeline CRUD operations in contract/OpenAPI/generated clients | retired routes advertised as callable | server-side `410 retired_route` refusal handlers | M2 | DELETED from contract and clients | `ba76bd4` removed the retired operation schemas/client methods; refusal handlers and raw-request tests remain. |
| RT06 | Commit-path duplicate validators/dead helpers | one contract and authority | shared validation helpers and one refusal table | M2 | MERGED | `5bb7fdd`; commit integration was `9 passed`. The default-filter full result is baseline-only and is not used as current-green evidence. |
| D13 | Render admission without producer custody | accepted current producer attempt only | producer guard/checkpoint and historical selector | M2 | MERGED primitives; registered replacement OPEN | Historical/authority primitives are present. Prior full `16608` is corrected to `5533 passed / 8 failed / 18 skipped / 24 xfailed`, with the audit race fixed by `16ac`. The later full `16434` is the separate `81f8`/tree `0e3a5b9` state: `5523 passed / 14 failed / 18 skipped / 22 xfailed`; its seven storage-floor visual failures were independently reproduced as exactly `7 passed` in the private floor environment. This is not current/CAS full-green evidence. |
| RT07 | Legacy `publish_timeline_render` direct document writer / pre-settlement registered publication | producer writes outside the sole commit path | native registered requester → settled proposal → requester outbox → `/v1` commit | M2 | OPEN | The actual Agent native two-test central pass is claimed, but independent review and current-cohort qualification are still pending. Do not close until the actual source tuple proves the registered path, lost-ACK/restart/exact retry, and accepted revision chain. |
| RT08 | Blanket identity-only `id_map` admission without source-bound allocation join | source-bound materialization authority | closed authenticated source/owner join | M2 | OPEN; private review only | The private `7b` carrier review is not public adoption. No public schema/pin/DTO/endpoint claim is made; current source/cohort review remains required. |
| RK01 | Project reference catalog state: kind/name/version/archive, ordered associations/primary/links | outside accepted film state | project-scoped catalog infrastructure | M2 | KEEP | Catalog CRUD and project isolation remain valid. These operations are not timeline placement or film-state mutation. |
| RK02 | Genuine unplaced project-shot catalog promotion and exact UTF-8 text bindings | outside accepted film history | existing project-scoped catalog operations; film selection/placement/pins remain commands | M2 | KEEP; MERGED on current9f | Promotion restoration is merged in `81f8c7e`; text restoration/current replay resolution is merged through current `9f211fc`. The original two promotion positives and original four text-binding positives remain active. This is the owner14:32 decision; it restores no other CRUD, endpoint, command, DTO, table, or accepted-film history path. |

## Original-positive mapping

The RK02 retention is deliberately narrow and traceable to the original
behavior tests:

| capability | original positive tests kept active |
|---|---|
| Unplaced catalog promotion | `test_candidate_promotion_is_atomic_fixed_point_and_byte_stable_on_replay`; `test_candidate_provenance_is_verified_before_promotion` |
| Unplaced catalog text bindings | `test_set_is_deterministic_project_scoped_and_replays`; `test_set_rebind_and_event_order`; `test_invalid_utf8_and_size_are_zero_write`; `test_identity_digest_is_sha256` |

The later exact-retry/restart and authority tests strengthen these mappings;
they do not replace or invert the original positives. No other retired film
CRUD positive is restored by RK02.
