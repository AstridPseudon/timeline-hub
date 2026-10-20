# Bundle 2 clip scalar contract

Worker: agt-m2-clip-scalar-fields. Base: 84db8bde. Source worktree: `/home/user/work/wt/agt-m2-clip-scalar-fields`. Branch: `tl/agt-m2-clip-scalar-fields`. M2 remains HELD until PLAN records M1. This is source for review/composition, not an official artifact freeze.

## Operation and exports

`clip.set`, version `"1"`, schema_version `1`. Singleton `select` is exactly `parent/clip:RAW_ID` or `occurrence:OCCURRENCE_ID/clip:RAW_ID`. Shared shot editing is unsupported. IDs are raw stable clip identities, never the App's merged display row identity.

Python capture: `astrid.sdk.timeline._clip_scalar_commands.capture_clip_set(bundle, select, *, values=None, clear=())`. The registered handler is `astrid.sdk.timeline._clip_scalar_commands.clip_set`, wired by `astrid.sdk.timeline.commands.operations`. Existing `_scalar_commands._clip_basis` is a mechanically extracted shared identity reader; existing params captures/goldens are unchanged.

Closed args: required `values` object and `clear` array, with at least one requested key. `values` supports **hold only**, as a positive finite number in SOURCE seconds. `clear` supports only `hold`, `asset`, `transition`, with unique keys. Values and clears must be disjoint. Unknown args/fields, null, nonfinite numbers, booleans, empty strings for hold, and unknown intentions refuse.

```json
{"schema_version":1,"op":"clip.set","version":"1","select":"occurrence:f2-occurrence/clip:f2-agent-clip","args":{"values":{"hold":4},"clear":[]}}
{"schema_version":1,"op":"clip.set","version":"1","select":"occurrence:f2-occurrence/clip:f2-agent-clear-clip","args":{"values":{},"clear":["asset"]}}
{"schema_version":1,"op":"clip.set","version":"1","select":"parent/clip:f2-transition-clip","args":{"values":{},"clear":["transition"]}}
```

The capture adds the normal original-state claims. Frontends must capture on their original authored bundle, retain that command, and send it through the existing commit door. No new DTO/ABI/endpoint/session or legacy save implementation is introduced.

## Preserved App meaning

Source inspected: `/home/user/work/app/tests/e2e/local/support/harness.ts`, `seedThreeProducts`, and `/home/user/work/app/tests/e2e/local/three-products.spec.ts`, the task-update and concurrent-draft cases. Exact original raw rows are retained in the fixture, including child holds 3 at local starts 3 and 6, and parent transition on `parent/clip:f2-transition-clip` at 15: `{"type":"crossfade","duration":0.5}`. Child hold changes 3→4; child clear removes the **asset** field; parent clear removes the **transition** field. App registry file/type/content_sha256 shapes are retained with deterministic synthetic immutable media IDs. The fixture also adds a shared occurrence to prove isolation and retains opaque/null source closure data from the established conformance fixture.

Asset absence is legal in the raw TimelineClip schema. Clearing asset retains the full clip, its clipType, registry and every other leaf. Alternate raw selectors asset_id/media_id/object_id make asset clear refuse, including null aliases, so removal cannot expose another selection. Asset SET is always refused: use the composer's occurrence.swap-media operation and its exact selected-media create-or-require policy. Scalar undo restores the original value through generic inverse, not a media swap.

Canonical transition is INCOMING. This v1 only removes it; it does not read or modify a successor/predecessor, adjacent clip or transition registry. Transition SET is intentionally outside this initial bounded operation. The historical App fixture spells it `crossfade`; the built-in element declaration is `cross-fade` at `/home/user/work/wt/agt-m2-clip-scalar-fields/astrid/packs/rendering/rendering/elements/transitions/cross-fade/element.yaml`. No alias normalization, general transition feature or unguarded transition SET has been invented. The existing validator at `astrid/core/timeline/validators/timeline.py::_validate_clip_transitions` still describes/checks a successor; fixing that pre-existing outgoing interpretation is outside this scalar-clear patch. The exact fixture is preserved rather than renamed.

Clear means ABSENT, never empty string or null. The raw JSON schema permits empty asset/transition strings, but neither is a SET this operation accepts. Raw asset/hold/transition null values are schema-invalid. Tests distinguish the schema from the recorder's ability to retain/restore previous tagged states; malformed historical values are not presented as valid authoring SETs.

## Hold timing and guards

Hold is source seconds; duration is hold / existing positive speed. At, speed, trim windows, occurrence maps, occurrence duration and other timing intentions are never rewritten. Clearing hold requires a surviving explicit from/to window with positive unambiguous duration. Contradictory duration codecs, unsupported time maps and non-null dynamic timing intentions refuse. Existing static fixed_start is preserved.

Parent rational fps is pinned; differing child fps refuses. Source seconds remain exact. The consumed half-open interval and rounded frame endpoint must fit the occurrence's explicit duration_ms and the next active same-lane occurrence. Boundary frames use the same half-toward-positive-infinity compiler helpers, so an exact endpoint remains legal at 30000/1001 fps and speed 2. Only translation occurrences (source_offset absent/0, speed absent/1) are supported. Consumed occurrence fields and existing move.blockers membership/order are recorded. No new shared query implementation is needed.

All writes are explicit recorded leaves, including unchanged writes and absent→absent clears. Original owner/source/element/selected media identities and content_sha256 are guarded. Unrelated parameter leaves, tracks and other occurrences remain independently editable. Server replay, intervening-write/ABA checks, staged coalescing, inverse and redo use the existing generic engine; there is no per-operation undo.

## Exact source artifacts for composer

Canonical candidate schema: `/home/user/work/wt/agt-m2-clip-scalar-fields/astrid/core/timeline/schema/edit-command.schema.json`

SHA-256 of exact schema bytes: `cdab9bf609b901fab591a45e262719e05945435b8e1b260d109f2538a509be24`.

Portable golden: `/home/user/work/wt/agt-m2-clip-scalar-fields/tests/editing_conformance/fixtures/recipe_m2_app_clip_scalar_fields.json`

SHA-256 of exact golden bytes: `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06`.

Golden keys: `bundle`, `commands`, `records`, `after_bundle`. The commands are ordered child hold, child asset clear, parent transition clear. `execute(bundle, commands)` and replay must reproduce exact records and after_bundle; generic inverse/redo round-trip the original bundle. The official normal artifact freeze/pin remains owned by the source-opargs manager after composition/review; the schema SHA above is a source candidate, not that future composed artifact.

Tests: `/home/user/work/wt/agt-m2-clip-scalar-fields/tests/editing_conformance/test_recipe_clip_scalar_fields.py`, `/home/user/work/wt/agt-m2-clip-scalar-fields/tests/sdk/test_timeline_clip_scalar_provider.py`, `/home/user/work/wt/agt-m2-clip-scalar-fields/tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`.

Direct actual Runtime proof against unmodified `/home/user/work/runtime` at `9f9b25c000485e919f30f1411831fe2d5a3c1316` passes with its official installed validation, without overrides. It uses RuntimeService on a throwaway realm, API-ingested synthetic media, fixture-only initial publication, then native commit/reopen/exact retry/inverse/redo/ABA. It opens no sockets. No full suite, browser/App journey, CLI ingress or full composer candidate is qualified by this worker.

## Successor source: source-hold after native fixed move (2026-10-20)

Worker `agt-m2-hold-after-move`, base `7b54ca92`, branch `tl/agt-m2-hold-after-move`. This section supersedes the blanket non-null `for` refusal described above **for this successor source only**. Bundle 2's current schema freeze, packaged artifacts, DTO/ABI and pins remain immutable. M2 integration remains HELD; the orchestrator owns review/composition and any successor artifact qualification.

Absolute successor handler: `/home/user/work/wt/agt-m2-hold-after-move/astrid/sdk/timeline/_clip_scalar_commands.py` (SHA-256 `fd54c4ca783188a64903b9bc36d380717a28c66a01f2708c97c0a3feff50bff3`). No command shape or version change.

Supported cases:

- Plain parent and occurrence-owned `clip.move` followed by explicit `clip.set` hold SET or CLEAR, in one batch or separate accepted publications. Capture the hold command on the local result of the move, preserve its original claims across acknowledgement/materialization, then submit it unchanged.
- Each existing non-null `for` at raw clip, `app`, or `app.astrid` must be a positive finite number agreeing with the **previous** effective source duration divided by existing speed, using the existing duration helper and its numeric comparison tolerance. Every such leaf becomes an explicit recorded write to the new effective timeline duration. Multiple agreeing declarations update together; one disagreement refuses the whole edit. Absent/null declarations stay absent/null. No containers or `for` leaves are created.
- Numeric hold wins over a surviving from/to source window in main. SET stores exact source seconds; CLEAR requires the surviving positive from/to window. Existing `capture._duration`, `clip_end_frame`, `clip_start_frame` and rational fps helpers determine extent. No new duration arithmetic or timing precedence was added.
- Static boolean `fixed_start`, quantized authored start, existing speed/source windows, row order, opaque metadata and disjoint siblings are preserved. Unchanged duration writes participate in ordinary publication/ABA guards. Generic inverse/redo handles the move and hold's repeated writes; undo of the move with a later dependent hold refuses.
- Main authoring compilation, reopening its emitted closure, and `project_runtime_parent_composition` readback prove effective extent at speed two with 30 and 30000/1001 fps. Direct actual Runtime acceptance/reopen/exact retry/inverse/redo/ABA passes in scalar-only, compound and separate-publication cases against normal official `/home/user/work/runtime` source `9f9b25c000485e919f30f1411831fe2d5a3c1316`, without schema overrides or sockets.

Refused cases: different/static-independent `for`, string/object/boolean/nonfinite/nonpositive `for`, non-boolean dynamic `fixed_start`, non-null follow/anchor intentions (`on`, `until`, other existing relation guards), clip time maps/nesting/from_ms/to_ms, incompatible duration/duration_ms declarations, nontranslation occurrence maps, differing child fps, occurrence half-open/frame-boundary overflow, changed captured basis, intervening writes (including unchanged and ABA), and surviving later dependencies. Asset/transition SET and all other previous bounded refusals remain unchanged. Dynamic anchors have not been widened.

Absolute successor tests:

- `/home/user/work/wt/agt-m2-hold-after-move/tests/editing_conformance/test_recipe_clip_scalar_fields.py`
- `/home/user/work/wt/agt-m2-hold-after-move/tests/sdk/test_timeline_clip_scalar_provider.py`
- `/home/user/work/wt/agt-m2-hold-after-move/tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`

The no-`for` App golden remains byte-for-byte unchanged at `/home/user/work/wt/agt-m2-hold-after-move/tests/editing_conformance/fixtures/recipe_m2_app_clip_scalar_fields.json` (SHA-256 `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06`). Successor source schema `/home/user/work/wt/agt-m2-hold-after-move/astrid/core/timeline/schema/edit-command.schema.json` remains SHA-256 `cdab9bf609b901fab591a45e262719e05945435b8e1b260d109f2538a509be24`. These identical bytes do not qualify a replacement official artifact. Exact commands/results and remaining limits are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-hold-after-move/notes/report.md`.
