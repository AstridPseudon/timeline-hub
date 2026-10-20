# App transition explicit-contract review

## Verdict

**MISMATCH — do not approve or activate this unpublished proposal yet.**

The paired destination `clip.set` shape is the correct existing carrier for
the App transition family, and the explicit removal/legacy-clear split is
directionally correct. Two semantic gaps remain against Main and the review
brief:

1. The proposal records a same-lane predecessor but explicitly says that
   adjacency, successor/shortest-clip fit, and the corresponding neighbor
   validation are not authoring constraints. Main's `ElementAdapter` rejects
   non-adjacent transitions and rejects a duration larger than the shorter
   adjacent clip. This is a user-visible acceptance mismatch, not an
   implementation detail.
2. The proposal's new `clip.set` selected-pack path can accept a caller's
   later P2 `schema_source` for the same unchanged element reference. The
   existing P1 authority fence is implemented for `clip.set-params` in the
   selected-parameter resolver, but the `clip.set` transition resolver only
   verifies the supplied pin and selected descriptor. A same-reference update
   must retain the recorded first P1; a genuine reselection must be a separate
   explicit producer action.

No App source was changed, no artifact or pin was activated, and no generated
client/schema was regenerated.

## Reviewed identities and scope

- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`.
- Agent peer ACK: `eb115db81ac2c24b182fe6873fbd883da851571e`.
- Agent source tree: `10ea4f3adb085adf7589239f852248cc9811eeb4`.
- Agent schema SHA-256: `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.
- App review tree: `e245a4791` (clean before and after review).
- The Agent ACK identifies the proposal as source-only and unpublished; frozen
  public 0.0.13, ordinary, private, and project-data counterparts remain out
  of scope.

I reviewed the peer handoff, the Agent candidate source/schema and its
transition tests, the App adapter and producers, and the prior `263+59+5`
direct-check plus P1/P2 retained-pin probe evidence referenced by the peer
handoff. The latter probe evidence was not rerun here; no claim is made that
it was newly reproduced by this worker.

## Main behavior comparison

The current App adapter is literal and destination-oriented:

- `src/tools/video-editor/runtime/element-adapter.ts:175-189` resolves the
  explicit or next clip and requires same-track adjacency.
- `:231-243` checks the positive integer frame duration against the shorter
  adjacent clip.
- `:345-367` writes `elementRef` and the incoming `transition` to the `to`
  clip in one resulting config image. The stored duration is authored seconds
  (`durationFrames / fps`), with the selected element revision retained.
- `:369-406` updates the incoming destination and preserves the existing
  transition object by spread; App producers must provide a complete raw
  transition when changing a field so opaque top-level keys and nested params
  are not lost.
- `:408-412` is the old literal remove path and removes both `transition` and
  `elementRef` without an identity guard. The native consumer must narrow this
  behavior: only an explicit paired clear may remove the associated transition
  reference, and it must refuse a mismatched effect/reference rather than
  deleting it.
- `:487-514` performs one provider CAS save after applying the operation; it
  is not yet the durable command-session/outbox consumer.

The legacy scalar clear is intentionally different. `ClipTransitionSection.tsx`
uses `clear: ['transition']` for ordinary “None” (`:111-120`), and the
existing scalar behavior tests show that this removes only the transition and
preserves an unrelated `elementRef`/opaque sibling. The proposal's
transition-only clear preservation is therefore required and correct.

The current UI already demonstrates the raw-field producer rule for ordinary
updates: `ClipTransitionSection.tsx:269-275`, `:301-310`, and `:325-334`
spreads the existing transition and params before changing duration, reset,
or one parameter. A native migration must preserve that exact recipe rather
than send a partial object and hope the provider merges unknown fields.

## Exact mismatches and required correction

### 1. Neighbor acceptance policy

The candidate `astrid/sdk/timeline/_clip_scalar_commands.py` records
`transition.predecessor` and reads neighbor fields, but its `_transition_set`
does not enforce Main's same-track adjacent pair or shortest-clip frame fit.
The proposal text explicitly says gaps, overlaps, and oversized windows are
authorable and leaves window policy to compilation. That disagrees with the
actual App adapter and this review brief.

The corrected native recipe must, for a destination `TO` clip:

- resolve the recorded same-lane predecessor as the `FROM` clip;
- guard membership, collection order, owner/track, and the predecessor/target
  source and timing identities;
- require the Main adjacency relation (same track and the existing 0.001
  second comparison); and
- require the positive authored duration to fit the shorter pair after the
  retained FPS conversion, matching Main's `durationFrames <=
  min(fromDuration, toDuration) * fps` check and tolerance.

Parent and occurrence targets must use the stable owner-qualified command
select and the existing occurrence source/owner binding. No flattened App clip
ID or cross-occurrence inference is acceptable. If canonical incoming policy
is intended to supersede Main's fit rule, the orchestrator must explicitly
change that settled contract; this review does not authorize that deviation.

### 2. Same-reference selected-pack authority

In the candidate source, `_transition_set` calls the selected schema path for a
supplied `schema_source`, while `commit.py`'s selected-source authority check
is scoped to `clip.set-params`. Thus a transition update with the same
`elementRef` can be presented with a later P2 pin and be resolved against P2.
That violates the requested P1/P2 rule even though inverse records can retain
the pin used by the accepted command.

The native floor must use an existing authority/binding primitive to require
the recorded first P1 for ordinary same-reference transition updates and
retries. It must not infer “latest” from the catalog or dependency manifest.
A separately captured explicit reselection may choose P2 and must record that
new selection as its own intent; it must not be smuggled into a duration/param
update. The inverse must continue to resolve the exact accepted first-P1
dependency and refuse if that proof is unavailable.

### 3. Removal distinction

The candidate's explicit `clear: ['transition', 'elementRef']` pair and
kind/id/revision guard are the right native shape. The App consumer must use
it only for the element-library transition removal path, and the native
handler must clear both canonical and legacy stored reference spellings when
the pair is valid. If the stored reference is an unrelated effect, stale
revision, wrong id, or opaque value, refuse atomically and preserve the draft.

The existing ordinary panel “None” path must remain
`clear: ['transition']`; it must not infer or clear either element reference.
No null sentinel, whole-document fallback, manufactured no-op guard, second
history framework, or new DTO is needed.

## Exact App consumer recipe after the native floor exists

Use the existing clip command session/outbox and its owner-qualified scalar
port. Do not call `AstridElementOperationAdapter`'s direct provider save for
this family.

1. **Apply from `ElementsLibraryPanel`.** Capture the selected `FROM` and
   `TO` rows from the raw authoring bundle. Resolve `TO` as the incoming
   destination and preserve its parent/occurrence owner. Check/record the
   exact predecessor and Main adjacency/fit facts. Emit one `clip.set` v1:

   ```json
   {
     "values": {
       "transition": {
         "type": "<element id>",
         "duration": "<duration_frames / retained fps>",
         "revision": "<element revision>",
         "params": "<literal params when present>"
       },
       "elementRef": {
         "id": "<element id>",
         "kind": "transition",
         "revision": "<element revision>",
         "packId": "<owner when present>"
       }
     },
     "clear": []
   }
   ```

   The default duration must match Main's catalog default frame count (8 when
   no descriptor default exists), converted using the captured rational FPS.
   Selected project-pack elements carry the exact original `schema_source`
   and immutable snapshot; built-ins do not invent one.

2. **Update from the transition panel.** Capture the full raw destination
   `transition` plus both `elementRef`/`element_ref` spellings and the exact
   owner. Change only the requested duration or parameter; carry every other
   transition key, unknown nested value, null/absent distinction, and existing
   parameter key forward. Send the matching `elementRef` in the same SET. A
   same-reference selected-pack update reuses recorded P1, never the current
   catalog's P2. Missing or mismatched identity is a visible refusal with the
   draft retained, not a guessed reference.

3. **Associated remove.** Capture the destination and validate the original
   transition `type`/`revision` against the stored transition element ref.
   Send only `clear: ['transition', 'elementRef']`; the native record must
   restore exact prior presence on inverse and clear the legacy alias when the
   paired identity is valid. A mismatched effect/ref or unavailable P1 is an
   atomic refusal.

4. **Ordinary “None”.** Keep the existing `clear: ['transition']` producer.
   It must preserve unrelated effect/component references and all opaque clip
   fields. This is intentionally separate from associated transition removal.

For all four paths, capture/finish/submit must retain the existing command
claims, original input, owner binding, selection/order records, preview,
outbox retry identity, and visible refusal behavior. Runtime activation waits
for the corrected Agent record/bundle/inverse/replay golden and matching
generated Runtime artifact; no public pin or version change is implied here.

## Evidence and tests

Reviewed candidate evidence:

- Agent transition conformance additions in
  `tests/editing_conformance/test_recipe_clip_scalar_fields.py` cover paired
  SET, opaque fields, explicit paired removal, legacy transition-only clear,
  mismatched identity refusal, and inverse/replay.
- `tests/sdk/test_timeline_transition_schema.py` covers exact selected-pack
  schema validation and redo, plus first-selected document inverse behavior.
- The peer handoff cites the existing `263+59+5` direct checks and P1/P2
  retained-pin probe; these were treated as supplied evidence, not rerun here.

Focused App controls run on the unchanged worktree:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs ./node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/commands/ordinaryScalarMember.test.ts
```

Result: **3 files, 51 tests passed**. No source, dependency, cache, pin,
browser, socket, or full-suite operation was performed.

## Recommendation / blockers

Agent/Runtime should correct and qualify the two native gaps above while
keeping `clip.set` v1 as the carrier. The matching Runtime prerequisite is
the generated schema/client/acceptance artifact from that corrected Agent
source, including parent/occurrence owner handling, Main neighbor membership
and frame-fit rejection, paired-clear guards, opaque-field records, and the
recorded P1 authority/inverse proof. App should then qualify one real
ElementsLibrary apply, one panel update, associated remove, legacy clear,
refusal, exact retry, reload/undo, and zero legacy traffic before retiring
the direct adapter writer. Until then, the transition consumer is blocked;
the frozen refs remain unchanged.
