# M2 canonical group migration candidate — HELD

PLAN option A is settled. Canonical shot/occurrence ownership is the single editable representation; parent `config.pinnedShotGroups` is migration input only. No M2 integration before PLAN's M1 record. This is a distinct successor to reviewed Agent `a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83`, branch `tl/agt-m2-group-official-root-proof`. Harness commit is pending worker exit; the base commit is not the final source identity.

## Bounded implementation

`timeline.migrate-groups` v1 selects `parent`, takes closed `groups:[{legacy_shot_id,shot_id,occurrence_id}]`, and requires a mapping for every legacy group in authored order. The caller supplies the destination IDs. The handler uses the current native recorder, collection order guards, root creation, source capture and inverse machinery. It does not allocate IDs, manufacture history or publish outside the ordinary provider.

The exact two-clip fixture is c1 at 0 and c2 at 2, hold 2, lane V1. Conversion creates shot `new-shot`, occurrence `new-occ`, a 4000ms interval starting at 0 on V1, and removes only consumed parent rows and the structural legacy array. Full legacy group/mode/snapshot/null/opaque metadata and ordered `{legacy_clip_id,clip_id}` mapping remain under occurrence `provenance.group_migration`. Complete child/track/registry bytes, ungrouped rows/order, rational 30000/1001 fps and immutable source pins survive. The canonical graph walker exempts only the actual token path `occurrences[index].provenance.group_migration.legacy_group`; collision keys and structural legacy data elsewhere still refuse. No sanitizer is used.

Interleaved/reordered membership, duplicate legacy shot identities, missing/duplicate/shared members, occupied destinations, ambiguous aliases, divergent mirrors/registries, nonempty legacy items without an explicit mapping, follow timing and unrepresentable timing refuse atomically. No fixture normalization is authorized. Ordinary edits on a legacy basis refuse; a sole recorded migration or authenticated migration inverse is the admission path. Historical reservation scans may read exact legacy boundaries, without granting ordinary edit admission.

The current staged inverse is retained. A one-line mirror refresh in its existing reconstructed-write loop is necessary to validate destination child bindings without querying a stale derived parent clip mirror. The old 99d inverse implementation was not imported. Pure compiled reload/inverse/exact raw legacy restoration/same-ID redo and detached-provider disjoint-work/ABA/dependency guards pass.

## Source versus official artifacts

Candidate canonical schema: `/home/user/work/wt/agt-m2-group-official-root-proof/astrid/core/timeline/schema/edit-command.schema.json`, SHA256 `47f67cd701ba3d2210d8b3c1f754e00eeace6078e37f610bc7b286ea17df2930`. Standalone review copy: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-official-root-proof/notes/edit-command.group-candidate.schema.json`. Removing only its appended migration condition and `MigrateGroupsArgs` restores the exact ordinary Bundle2 schema bytes, frozen SHA256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`. All 16 existing conformance fixtures, including M1 and label goldens, remain byte-identical to a31.

Normal pin delta is exactly Agent `f423074778f4220df808799a4f7b308e56885397` (all six files), consuming Runtime `d691ddadb4ef3f5881a25fa893b4fb812211f102`, client 0.2.3, schema digest `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6`. This artifact contains frozen ordinary 472622 root guards. It is not a group release: migration closed args/typed exports still need a newly reviewed normal generation from the distinct candidate. No Runtime schema override, Runtime edit or fake pin was used.

The direct source pair proves official root-key admission and real CAS/normal segments transcript setup, retained v1 reads after v2/reopen, negative literal `lines` admission, and canonical-document envelope validation. Two positive real migration tests now reach the provider and fail in `_check_reservations`: the Runtime-owned 99-line helper's genuinely stored setup record has `created:[]`, while its command omits `created`; the reviewed identity scan requires exact agreement. Do not infer accepted migration, undo/redo, retry/restart or browser success. Do not weaken the production guard to accept the helper. Runtime owner should supply a reviewed helper successor with complete capture fields through genuine storage acceptance, followed by rerunning the original positive tests. A later provider failure is not inferred.

Helper comes unchanged from explicit Runtime archive `7c6e4eabf88d914d9c98c0097b06ea298ba11866`, `tests/timeline_trusted_bootstrap.py`, SHA256 `c3cdaa6b904f374cee7c17f6d61ba196909bca1e9bab0f6e200d8efe6e227c82`. Runtime code is d691; only the test helper module is imported from that archive. No SQL or invented accepted edge is added by Agent.

## Next bounded delta and exact App outcomes

Neither a canonical group placement/retrack command nor a derived App legacy group view was already ported on a31. They remain the explicit next delta, after this migration candidate and provider setup boundary are reviewed. The first step is movement on existing lanes plus a read-only view derived from canonical occurrence ownership and child ordering. Retrack must change occurrence placement and its occurrence-owned child tracks atomically. It must preserve relative starts, source windows, mode/opaque provenance, stable refs and guards; no editable parent soft tags, persisted duplicate order map or display-ID parsing. Broader free moves/new-track creation stay separate.

All three original App `it.fails` assertions in `src/tools/video-editor/hooks/useClipDrag.test.tsx` are untouched and unrun:

| Original test | Exact visible outcome still required |
|---|---|
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` | V1,V2,V3 once; clip-1 at 1 on V2 and clip-2 at 3 on V3, hold 2 each; no pinned override; selection `[clip-2,clip-1]`, secondary ghosts, one transaction. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` | V1 empty; V2 ordered clip-1 `[1,3)`, clip-2 `[3,5)` with original effect IDs; both metadata lanes V2; derived group retains legacy shot-1, mode images, ordered members; selection `[clip-1,clip-2]`, one transaction. The old override assertion maps to a derived compatibility view, never a parent writer. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` | One config gesture exposes the same ordered images group on newly created V3. The fixture drop at 3 additionally requires clip spans `[3,5)` and `[5,7)` through accepted readback; those geometry assertions are not in the original test and must be added without weakening its existing assertions. |

No App/browser or full-suite pass is claimed. Detailed exact commands and counts are in the worker `notes/report.md`.
