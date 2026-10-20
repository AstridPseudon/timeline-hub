# Shot settings/name writer audit and repair

Completed on App base `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff` in `/home/user/work/wt/app-m2-shot-settings-writer-gap`. Only `src/tools/travel-between-images/pages/ShotEditorView.tsx` and its owned test file changed in the repository. KEEP exists. No integration worktree, branch, ref, package, schema, DTO, validator, or other worker was modified; no commit/merge/checkout/push was run.

## Result

Proved settings data loss and repaired it at the existing component save callee. Before repair, a prompt edit round-tripped a normalized form into a replacement `revision.settings`: arbitrary root/nested settings disappeared, an unrelated explicit null became a default, and absent defaults became authored. Name edits preserved the same opaque fixture.

The save now retains the raw settings root and overlays only changed form fields. It compares JSON values using the existing `clipMovePrimitives.equal` helper, preserving object key independence, own prototype-named keys and array order. JSON form comparisons omit undefined as the existing publisher does; an explicitly changed root undefined still removes that root via the existing builder. No new serializer/merge framework was introduced.

If a changed compound value cannot represent the complete raw authored value, the entire save refuses before publication, displays “Shot settings draft kept”, and leaves the existing entity store's edited settings, clean snapshot, dirty flag and error intact. Ordinary complete compound edits and explicit null/clear succeed. Draft retention is in the current in-memory settings store, not a new durable outbox or reload guarantee.

Both direct canonical graph writers remain; this is data safety, not native adoption or Gate 6/D01 closure. No whole-document native operation was invented. No passing behavior expectation was changed to a refusal; all five original component positive/stale-head tests remain unchanged.

## Exact trace, payload proof and gaps

Full field/ownership/capture request: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-shot-settings-writer-gap.md`.

- `ShotEditorView.tsx:145-152,154-199`: custom form load normalizes the selected occurrence's raw `revision.settings`; save captures the current editing composition/head before queueing and calls the existing graph builder/publisher. New repair is `:162-187`.
- `ShotEditorView.tsx:321-343` → `shotCompositionEditor.ts:519-533`: name changes `revision.provenance.name`, preserving other provenance; it does not write `revision.name` or a parent track label.
- `shotCompositionEditor.ts:217-374`: appends immutable shot revision, occurrence-only copy on shared shot ID, item-link remap/new internal copy for shared shots, original revisions retained, extent/blocker check and parent head advancement. No normalized timeline projection is used for these settings/name edits.
- `shotCompositionAdapter.ts:318-347`: projection is used for visual-seam validation; original graph request is forwarded.
- `dataProvider.ts:248-299,2210-2304`: real outgoing `toRuntimePublication` sends raw internal `.timeline` as the immutable internal payload and preserves raw shot/parent envelopes except reserved identity/publication fields. Production then uses existing `publishParentComposition` and receipt-pinned reload; the new tests exercise the encoder directly, not a live server.
- Read-side `runtimeGraphToContract` selects `internalPayload.timeline ?? internalPayload`, normalizes assets and some known shot/occurrence fields. Arbitrary wrapped historical child payload preservation through readback is not certified here. Future native capture must consume authenticated raw authoring images, not normalized presentation graphs.

Permanent tests at `ShotEditorView.test.tsx:108-248` call the real component persistence/name callbacks with mocked UI/provider children, the real adapter, real graph builders, and real outgoing Runtime encoder. They compare complete edited revisions and outgoing shot/internal payloads; unchanged history/other occurrences, parent config/envelopes and input immutability; raw child output/config/tracks/clips; arbitrary non-namespaced data, null, absent fields, booleans/zero, duplicate array order, own `__proto__`, `constructor`, and `prototype`. Two refusal cases connect the actual existing `createEntityStore` to the component save callback, verify error presentation/dirty draft/no publication, then prove a safe save still succeeds. The ordinary compound test preserves order and exercises null and removal.

Contract gaps handed off to Agent via the App manager:

1. A bounded shot settings/name field capture with explicit occurrence vs shared-shot ownership and original raw identities/presence; parent track labels and clip fields do not cover it. No new op name was chosen here.
2. Explicit touched-path/write/clear intent: the present normalized snapshot cannot distinguish an unchanged authored write from an untouched display default. Root/nested/ordered compound fields need an Agent-owned minimal supported contract and exact goldens, not an inferred whole-settings replacement.
3. Name precedence mismatch: `localTimelineShotModel.ts:152-161` displays `revision.name` before `provenance.name`, so a present root name masks the current rename. Manager/Agent must settle the authoritative name field and migration/clear policy; no unrelated name behavior was changed here.
4. Exact lossless inverse/rebase/created-ID guards, shared occurrence isolation, accepted raw reload and crash-safe retry/outbox/zero legacy traffic remain required before either writer can be deleted. The handoff lists precise golden and inverse guard cases.

## Commands and results

All test commands ran in `/home/user/work/wt/app-m2-shot-settings-writer-gap`, with ignored local `node_modules -> /tmp/app-m2-coherent-deps8/node_modules` (actual coherent ROOT8). Logs live in this absolute notes directory.

RED, before product change:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx
```

Exit 1: **1 failed / 6 passed**, settings preservation failed as intended; name preservation and all original tests passed. Log `red.log`.

After the initial repair, the same command passed **7/7** (`green-initial.log`). During expansion, the five-file command below exposed an object-key-order false refusal in the first comparison implementation (**1 failed / 61 passed**); this was corrected by reusing the existing structural equality helper. No expectation was weakened.

Final targeted suite:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionEditor.opaqueRemap.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/shared/state/createEntityStore.test.ts
```

Exit 0: **5 files / 62 tests passed**, 11.07 seconds (`green-final.log`; preceding green run also passed 62/62 in `green.log`). Component file has 10 tests; neighboring existing builder/remap/provider/store tests are untouched.

```sh
./node_modules/.bin/eslint src/tools/travel-between-images/pages/ShotEditorView.tsx src/tools/travel-between-images/pages/ShotEditorView.test.tsx
git diff --check
git status --short --untracked-files=all
readlink -f node_modules
```

ESLint exit 0, no output (`lint.log`); diff check exit 0; status shows only the two intended source/test modifications; dependency link resolves to `/tmp/app-m2-coherent-deps8/node_modules`. No build output or temporary worktree files remain.

No full suite, build, browser, tsc, install, socket, real Runtime acceptance, restart or native command journey was run/requested. Full 11559 was left alone. The outgoing regression does not prove accepted immutable storage/readback, arbitrary historical wrapped payloads, or a settings/name command contract.

## Decisions and next steps

Used the authorized bounded raw-root preservation plus visible kept-draft refusal; retained legacy writers and current name semantics. Did not choose cross-contract field policy or create a generic serializer. No evidence contradicted PLAN's settled decisions. No blocker to this assigned audit/repair deliverable.

App manager should review the two-file patch and escalate the exact Agent field/ownership/capture request in the design handoff. Agent should publish the minimal command schema/capture and golden/inverse fixtures, then App can qualify these consumers through the existing session/outbox and remove their direct publishes. Wrapped read-side preservation and name precedence deserve explicit manager review; neither is claimed repaired by this change.
