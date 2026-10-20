# App independent duplicate: identity review

2026-10-20. Design only; no product, schema, pin, dependency or integration changes.

## Finding and recommendation

An independent copy must reserve a new **occurrence ID and authoring shot ID**, and rederive exactly the copied occurrence's root **`stable_deep_link` and `output_identity`**. Do not copy those two root values from the source. Preserve unknown nested namespaces literally, including identically named keys and strings equal to old IDs.

`output_identity` is a deterministic occurrence-qualified final-video lookup key, not an allocated task/output/object identity. Clearing it would violate App's contract. Existing App **and Agent** factories already define it exactly. The deep link also has an existing factory, but **cannot be derived solely from project/timeline/occurrence**: it additionally needs the destination shot and its final pinned revision. Native revision IDs come from compiled content; App must not reuse its old random `*-copy-*` revision convention for the native op.

Recommend that Agent explicitly declare these two root paths as derived fields of independent duplication and reuse its existing exact factories, with the deep link derived against the actual compiled shot revision. This is a narrowly defined semantic addition, not permission to normalize other fields. Keep the strict xfail until the copied authoring row **and** immutable compiled closure satisfy it. No reason was found to refuse ordinary independent copying on the theory that `output_identity` is an immutable external task ID.

The existing candidate does **not** implement this recommendation. Its only args are `occurrence_id` and `shot_id`; no complete derived-identity helper is wired into that op. Agent must own the implementation/recording boundary for the final revision. If the orchestrator retains the candidate's requester-supplied-replacements approach instead, the maximum additional surface needed is two closed, exact replacement fields (`stable_deep_link`, `output_identity`), computed with the same factories and validated against a deterministic compiled candidate. The requester must first obtain the compiled destination revision; an arbitrary supplied string or source-revision substitution is insufficient. Do not duplicate the compiler's hash formulas in App. This review does not choose or implement a new cross-repo schema.

M2 merges remain held until the global M1 record. Candidate `occurrence.duplicate` is not in the frozen Runtime union and is not ready for an App pin/caller change.

## Sources inspected

| Source | Pinned context / relevant location |
|---|---|
| PLAN, App STATUS, `design/m2-occurrence-duplicate.md`, `design/opaque-remap-contract.md` | Shared orchestrator documents; read before tracing. PLAN wins. |
| App worktree | `c8566f12d114c538db8136b8c580a1e663af1ad1`, initially clean; same base as App STATUS. Paths below are relative to this App tree. |
| Agent integration, read only | `4a75f68f32049a69fd86135c645fa64c51175c14`; `astrid/core/timeline/{shot_composition,authoring_bundle}.py`. |
| Native candidate, read with `git show` in `/home/user/peteromallet/astrid-agent` | `e445e3db0350fc80525f78ace81cd50769879351` (`hub/tl/agt-m2-occurrence-duplicate-b`); native op, compiler, golden and recipe tests. No checkout or mutation. |
| Frozen App R4 reference | `8f0c2484463e9b666d184a744d52e252984e551a`; canonical editor duplicate positive and older pack-command tests. |
| App main reference | `580508eed1bf6ed95caaf476c9d69a4672472a2f`; checked to distinguish already-retired pack admission from this review's work. |

## Live call and exact formats

`ShotGroupContextMenu.tsx:150` emits “Duplicate shot” with `canonicalIdentity`; `TimelineCanvas.tsx:797` carries that identity. `AstridTimelineEditor.tsx:390–420` calls `duplicateIndependentShot`, supplies four IDs, calls `runtime.shots.shotComposition.publish`, refetches, and displays “Independent shot duplicated”. It is still the old graph publication path, not native command adoption. `dataProvider.ts:248–299` publishes that graph through `publishParentComposition` and loads the receipt's exact accepted revision.

`shotCompositionEditor.ts:631–661` deep-clones the graph and source revision, changes shot/revision/internal-revision IDs, sets the new revision rows to `publish: true`, adds a new occurrence, and calls `withOccurrenceIdentity` (`:94–109`). This helper spreads the occurrence and overwrites only its root identity and two derived strings. Nested values are not searched. The source's `at_ms`, duration, placement and other data carry over; `reorderOccurrences` (`:551`) sorts by time, old ordinal, then insertion index and renumbers ordinals. Copying is not an append-in-time gesture or ripple edit.

The old handler chooses one random eight-character UUID suffix (timestamp fallback):

| Old graph reservation | Format |
|---|---|
| Shot | `${sourceShotId}-copy-${suffix}` |
| Shot revision | `${sourceRevisionId}-copy-${suffix}` |
| Internal revision | `${sourceRevisionId}-timeline-copy-${suffix}` |
| Occurrence | `${sourceOccurrenceId}-copy-${suffix}` |

`shotComposition.ts:64–85` defines these exact strings, with each segment encoded by JavaScript `encodeURIComponent`:

```text
stable_deep_link = project/{P}/document/{T}/shot/{S}/revision/{R}/occurrence/{O}
output_identity  = project/{P}/document/{T}/occurrence/{O}/output/final-video
```

Here `T` is App's parent document ID / native timeline ID. The wire spelling is **`document`**, without a leading slash. `output_identity` has no task, attempt, revision, timestamp or object digest component. App validation (`shotComposition.ts:194–205`) requires equality with both factories, not just nonempty strings. `shotCompositionAdapter.ts:206–226` carries them as `stableDeepLink` / `outputIdentity` on the prepared occurrence.

Agent already defines the matching functions at `shot_composition.py:353–373`: `stable_occurrence_deep_link(P,T,S,R,O)` and `stable_output_identity(P,T,O)`. Its `quote(..., safe="-_.!~*'()")` explicitly matches `encodeURIComponent`; its contract validator also checks exact equality (`:620–624`). This disproves a technical claim that Agent has no existing format/factory; permission to change the native op's declared fields still belongs to its owner.

## Actual examples from pure probes

The App probe called the live `duplicateIndependentShot` on `shotComposition.fixture.json`, using the IDs already used by the original duplicate test. Both graphs parsed successfully; the source retained five occurrences.

```json
{
  "before": {
    "occurrence_id": "occ-1", "shot_id": "shot-alpha", "revision_id": "rev-a",
    "ordinal": 0, "at_ms": 0, "duration_ms": 2000,
    "stable_deep_link": "project/project-001/document/document-primary/shot/shot-alpha/revision/rev-a/occurrence/occ-1",
    "output_identity": "project/project-001/document/document-primary/occurrence/occ-1/output/final-video"
  },
  "after": {
    "occurrence_id": "occ-independent", "shot_id": "shot-alpha-independent", "revision_id": "rev-independent",
    "ordinal": 1, "at_ms": 0, "duration_ms": 2000,
    "stable_deep_link": "project/project-001/document/document-primary/shot/shot-alpha-independent/revision/rev-independent/occurrence/occ-independent",
    "output_identity": "project/project-001/document/document-primary/occurrence/occ-independent/output/final-video"
  }
}
```

Factories on both sides produced this encoding for `P="p /é", T="film?#", S="s!'()", R="r/a", O="o%1"`:

```text
project/p%20%2F%C3%A9/document/film%3F%23/shot/s!'()/revision/r%2Fa/occurrence/o%251
project/p%20%2F%C3%A9/document/film%3F%23/occurrence/o%251/output/final-video
```

For the **native candidate's actual golden** (`recipe_m2_occurrence_duplicate.json`), the new `shot-copy` / `occ-copy` compiles to:

```text
shot_revision_id = authoring-shot-revision-44fbac89c5e00d8c893cd59c66716b3d5ca1366e54bb1ed008c5118fe74f8dc5
stable_deep_link = project/project-1/document/film/shot/shot-copy/revision/authoring-shot-revision-44fbac89c5e00d8c893cd59c66716b3d5ca1366e54bb1ed008c5118fe74f8dc5/occurrence/occ-copy
output_identity = project/project-1/document/film/occurrence/occ-copy/output/final-video
```

That golden itself has no derived identity fields. A bounded in-memory probe added the strict xfail's synthetic `deep:occ-0` / `out:occ-0` values to its copied placement and ran the **candidate's own compiler**, read from the pinned git object. Both stale strings survived into `publication.parent_composition.occurrences`. This confirms the compiler does not currently repair the op's copied values. It is not Runtime acceptance evidence.

## Native reservations, derivations and opaque boundary

Candidate `native_occurrence_duplicate.py:29–45` calls `_copy_shot_for_placement` and creates a new shot with copied internal timeline, then copies the occurrence, removes `revision_id` / `shot_revision_id`, and replaces `occurrence_id` / `shot_id`. It leaves the two derived strings unchanged. Its args are closed; App cannot send replacements today without a reviewed contract change.

| Field/location | Required treatment |
|---|---|
| `args.occurrence_id`, `args.shot_id` | Reserve once, require absent and distinct from source, retain for retry/rebase. Only caller-reserved native identities. |
| New occurrence root `stable_deep_link`, `output_identity` | Explicitly rederive for the destination. Exactly these two paths need the additional semantic declaration. Do not clear to null/empty or carry source values. |
| New occurrence revision pin | Compiler writes actual `shot_revision_id`; the old graph's random shot/internal revision IDs are not native inputs. |
| New shot item IDs | Existing `_copy_shot_for_placement` exact derivation and collision check; no caller reservation or new scheme. |
| Child track/clip IDs | Copy unchanged in the independently owned internal timeline. Address as `occurrence:<new occurrence>/clip:<raw clip>` etc.; App projected clip IDs are `${occurrenceId}:${rawClipId}` (`shotCompositionProjection.ts:334–346`). |
| Placement, duration, source bindings, media selections, settings, provenance, unknown fields | Preserve source values except declared structural/derived fields. No invented task/asset/provenance rewriting or byte copying. |
| Nested `app`, `metadata`, namespaced data, secondary IDs, null/absence/list order | Preserve byte-for-byte JSON values, even when keys look like identities or values equal source IDs. Whole-document canonical serialization/digests may differ; do not rewrite opaque content. |

`authoring_bundle.py:255–294` computes each native item ID using `_identity("shot-item-placement", P,T,newOccurrence,newShot,sourceItem)`. `_identity` (`:157–170`) returns `kind + "-" + sha256(UTF8(NUL.join([kind, canonicalJSON(part)...])))`; canonical JSON is sorted, compact, UTF-8/non-ASCII-preserving. The actual probe yielded:

```text
item-1 -> shot-item-placement-6b31174529ec92ede9c37ad5e078cfde47f010300e35ba5f9007e3ac63775a8b
item-2 -> shot-item-placement-fca361e14e588ba27d1acff9071a0282d66e6dd87cccfc6d711c263d2506ca8c
```

Inputs were `P=project-1,T=film,O=occ-copy,S=shot-copy`, source shot `chapter-shot`. The probe verified source immutability, equal `item_id`/`id` mirrors, and declared item dependency links. A nested `metadata["org.example.notes/v1"]` containing `source_item_id: "item-1"`, `output_identity: "out:occ-0"`, `stable_deep_link: "deep:occ-0"`, null and ordered values stayed exact.

The opaque-remap contract permits only top-level shot `items` authoritative `item_id`/fallback `id` (equal mirror only), and `source_item_id` / `source_item` at that item's descriptor location: object `metadata`, otherwise item root. No recursive suffix remapper. The old `shotCompositionEditor.ts:129` recursive remapper is used by a separate shared-shot revision-edit branch (`:303–318`), **not** by `duplicateIndependentShot`; it is not a suitable native duplicate model or authorized change in this task.

Content-addressed native internal and shot revisions use existing compiler `_identity("authoring-timeline-revision", P,T,S,internalPayload)` and `_identity("authoring-shot-revision", P,S,shotPayloadWithInternalPin)` (`authoring_bundle.py:884–904` in integration; candidate has a few extra lines for recorded creates). The compiler supplies the placement's pin (`:1014` in integration). The deep link must follow that value, including on later edits; substituting the source revision would leave a stale pointer.

## Consumers and the readback trap

| Consumer | Assumption / consequence |
|---|---|
| `LocalTimelineShotBrowser.tsx:212–255` and `toolRoutes.ts:32–53` | Full deep link is encoded into route hash; selection accepts exact stable link or occurrence ID extracted from trailing `/occurrence/<encoded-id>`. A copied source deep link opens/selects the source. Stale revision links may continue resolving by occurrence suffix, which does not validate the pin. |
| `AstridTimelineEditor.tsx:380–386,722` | Popup keeps parent canvas route and passes `stableDeepLink` as `shotRef` to the canonical editor. |
| `shotCompositionProjection.ts:631–635` | Managed output matches if occurrence ID **or output identity** matches. Reusing the source output key risks false association; returning no new final-video output for the copy is correct. |
| `useFinalVideoAvailable.ts:267–296` | Scans succeeded render outputs, requires occurrence-qualified match in canonical mode, keys result by occurrence ID. It must not inherit source rendered output merely because content bytes are shared. |
| Agent `sdk/project_render.py:445–477` | Managed-output task/run/attempt, object and association identity are separate fields. Occurrence-qualified output metadata is carried through when present; existing output records remain immutable. |
| Runtime `conformance/responses/managed_outputs_200.json` | Managed output has `association_id`, `task_id`, `attempt_id`, `object_id`, digest, output port and selector, separately from optional provenance. The similarly named historical migration helper is unrelated to the App factory. |
| App `dataProvider.ts:2077–2098` | Raw accepted parent occurrence is spread, then **both root strings are unconditionally recomputed** from project/timeline/new occurrence and actual shot revision. An App reload can look correct even if the stored canonical row is wrong. |
| Agent `shot_composition.py:327–334` and `shot_composition_projection.py:580–588` | Normalization/projection uses `setdefault`; stale present strings survive. Missing-field projection defaults use a different `astrid://...` link / parent-revision key, so deleting fields and relying on generic projection is not a proven App-compatible fix. |

Therefore the strict xfail identifies a real raw-row defect, even though App's read adapter can hide it. Verify the accepted immutable **raw parent**, not just the prepared App occurrence. The task did not uncover a need to mutate any historical output association. Reusing immutable media references does not allocate or transfer output/task identity.

`rg -n duplicateLinkedOccurrence --glob '!package-lock.json' --glob '!*.md' .` found only its definition and import/call in `shotCompositionEditor.test.ts`. There is no active non-test caller, dynamic string reference found, or UI intent for linked duplicate. Preserve its existing positive test; do not add a linked command or UI during this migration.

## Original positives to keep, and missing qualification

| Existing test/source | Positive behavior / limits |
|---|---|
| `shotCompositionEditor.test.ts:124` (also frozen R4 `:79`) | Linked copy remains same shot/revision with distinct occurrence; independent copy creates new shot, revision and internal-revision identity. Keep the combined positive even though linked has no live caller. It does not prove Runtime acceptance. |
| `shotComposition.test.ts:17` | Repeated linked occurrences remain distinct; independent fixture copy has different link/output identity; pinned revisions, timing, audio scope, provenance and ordered generation inputs survive. |
| `shotCompositionEditor.test.ts:146` | Local graph move undo/redo. This is not an accepted native duplicate undo test. Preserve and add real duplicate history coverage. |
| `shot-group-pack-commands.test.ts:196` | Deep-copy nodes, registry references, final-video replacement lineage, no shared objects, nested parameter independence. Preserve original assertions when adapting to canonical ownership. Immutable ordinary media reuse remains valid. |
| Same file `:320`; `AstridTimelineEditor.document-shots.test.ts:194` | Explicit active non-default timeline/version, refresh, no relational shot action; pack failure is visible with no success toast. These are mocked older paths, not native acceptance or zero-old-publication proof. |
| Frozen R4 pack test `:185`, main pack test `:250` | R4 admitted retired `duplicate` family with explicit final-video lineage; current main already refuses that family. This review changed neither. PLAN separately defers generation duplication; independent canonical occurrence copy must not resurrect the retired task route. Report the distinction instead of describing current refusal as proof of independent-copy acceptance. |
| Output and navigation tests run below | Managed output belongs only to occurrence-qualified owner; valid deep link opens on refresh. Existing behavior must stay positive. |
| Candidate recipe tests, read only | Source/metadata/internal preservation, shared-source sibling isolation, deterministic replay, reserved/derived collisions, source change/ABA refusal, exact in-memory reload/inverse/redo, legacy migration refusal, portable golden. Strict identity xfail remains. Prior reported 32 pass/1 xfail was **not rerun here**. |

Required additions before adopting/removing the old canonical duplicate writer:

1. Native capture from an actual App closure with both valid root strings; assert the reserved IDs, exact new strings, final compiled revision, source/sibling isolation, item map and unchanged child track/clip IDs. Keep source `at_ms`/placement semantics. Assert unknown root and nested namespaces (including same-named fields and old-ID strings), explicit null versus absence, list order, media/transcript pins and content after copy/reload.
2. Real Runtime `/v1` acceptance, renderer off, immutable raw parent/shot/internal readback, fresh App reload and opening **the copy** via its deep link. Check raw root fields before the App adapter can overwrite them. Source final output remains attached only to source; a future copy output is attached only to copy.
3. Lost acknowledgment, restart and exact persisted request/key retry produce one accepted duplicate with the same reserved and derived IDs; changed request under the same key refuses. A later disjoint edit survives replay; dependent/conflicting edits follow guarded conflict behavior with local draft retained.
4. Accepted history undo removes only the copied roots and restores exact original canonical closure/opaque data; redo recreates exact copied IDs/content; second undo stays exact. Collision, missing dependency, changed source and ABA/ref publication guards refuse atomically without partial publication. Undo must not purge immutable historical rows/media.
5. The actual context-menu gesture emits `occurrence.duplicate` through commit session/outbox, uses accepted revision for refresh/history, and emits **zero** whole-graph `publishParentComposition`/legacy save, bridge/task-duplicate, placement fallback, relational or Supabase timeline writes. Mounted mocks and no-relational assertions alone do not establish this.

Never delete positives or rewrite them to expect refusal. If the replacement temporarily cannot provide a passing behavior, retain its original expectation and use a strict expected failure naming the restoration requirement. The current Agent strict xfail's `!=` checks are necessary but insufficient: add exact factory equality, valid escaped inputs, raw compiled closure, reload and undo cases; do not make it pass merely by clearing the fields. Its synthetic `deep:occ-0` / `out:occ-0` inputs do not establish an external immutable-ID format.

## Verification performed here

From `/home/user/work/wt/app-m2-duplicate-identity-review`:

```bash
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/data/shotComposition.test.ts src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/hooks/useFinalVideoAvailable.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx
```

**6 files, 71 passed, 10.83 s, exit 0.**

```bash
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/lib/shot-group-pack-commands.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts
```

**3 files, 64 passed, 3.75 s, exit 0.** Total **135 passed**; no test changes.

Two bounded pure probes passed: live App copy/factory/validation and read-only native golden compiler/item-codec preservation. Exact executable commands are in `workers/app-m2-duplicate-identity-review/probes.md`. Initial exploration failed when applying the newer candidate golden to the older integrated compiler (recorded new-shot source mapping unsupported), when invoking tsx CLI's sandbox-blocked IPC listener, and when reading the compiler publication as `parent_revision` instead of `parent_composition`; corrected probes above succeeded. None is claimed as native Runtime acceptance.

No full suite requested or run. No localhost/browser/socket suite, real Runtime duplicate acceptance/restart, App duplicate gesture end-to-end, generated Runtime union/client, new schema, pin or M2 merge was qualified. Existing tests do not close those gaps. Only requested documentation/worker notes were written; App source tree remains unchanged.
