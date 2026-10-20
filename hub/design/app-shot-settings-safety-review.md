# Shot settings safety review and compatible consumer gate

2026-10-20. Worker `app-m2-shot-settings-safety-review-gate`; App base `8212ee44d` over `1be0efdde`. Reviewed PLAN, the absolute writer-gap design, and the writer-gap worker's 62-pass report. Result: the bounded repair is qualified with a six-line product follow-up for two additional root-preservation defects. This is not native command adoption, D01/Gate 6 closure, or current cross-repository qualification.

## Findings and repair

The original repair preserves complete raw settings during an unrelated prompt edit and refuses compound edits whose normalized form omitted authored content. Review found two remaining counterexamples through the actual component persistence callback:

1. An unchanged form still published a new shot with `settings: {}`, turning an absent or null authored root into an object and copying a shared shot unnecessarily.
2. A prompt edit replaced a non-object authored settings root (array, string, false or zero) with `{prompt: ...}`, silently losing the unrepresented root.

New permanent tests first produced **7 failures / 11 passes**. `ShotEditorView.tsx:174-179` now returns without publication when there are no changed form fields and visibly refuses changes over an unrepresented non-null root before building or publishing anything. The refusal uses the existing error presentation and entity store; tests assert the complete edited draft, original clean snapshot, dirty/error state, unchanged source graph and zero publisher calls. This is preservation/refusal at this form boundary, not a global schema restriction or unknown-field ban.

Absent/null roots remain distinct on an unchanged form. An actual prompt edit can initialize either root with exactly the authored prompt, without materializing defaults. Existing scalar null/removal and ordinary compound edits remain; added positive tests prove compound null/removal when the form contains the complete authored value. Clearing a compound value whose form omitted raw content still follows the existing visible refusal policy. An unchanged displayed default cannot express an intentional unchanged write/clear: explicit write intent remains an Agent contract gap.

Only the component and its test changed: six product lines and twelve additional test cases. All original ten component tests, including all five original positive/stale-head cases, remain unchanged; neighboring tests are unchanged. No passing expectation was rewritten as a refusal, skipped, or weakened.

## Source and whole-value review

- `ShotEditorView.tsx:145-204`: load normalizes only the selected occurrence's display form; save captures its editing composition/head before queueing, compares structurally using existing `equal`, then overlays changed roots onto raw settings. Added nested-key-reordering coverage proves JSON object insertion order does not cause a false compound clash. Arrays remain ordered.
- The existing component tests invoke the real adapter, graph builder and `toRuntimePublication`, with UI/provider children mocked only to expose the actual callbacks. They compare whole edited revisions and outgoing shot/internal payloads, not a list of unknown keys. Fixtures include arbitrary non-namespaced roots, nested unknowns, explicit null/absence, zero/false, duplicate ordered entries and own prototype-named keys. Parent config/envelopes, unchanged history, unaffected occurrences and input immutability are checked.
- `shotCompositionEditor.ts:217-383`: edits append immutable revisions and repin only the selected occurrence. Sharing is by shot ID, including distinct pinned revisions. Shared copies receive independent shot/internal/clip identities. `remapItems` changes declared item IDs and source links only: object metadata owns source links, otherwise the item does; unrelated ID-looking literals remain opaque. The unchanged neighboring opaque-remap corpus verifies complete expected revisions and this exact contract.
- `shotCompositionAdapter.ts:318-347`: visual projection is admission data; the original graph is forwarded. `dataProvider.ts:2210-2304`: the outgoing encoder sends raw internal `.timeline`, raw shot payload fields apart from publication/identity envelope fields, and parent/occurrence envelopes. Derived preview config is not substituted into authored roots.
- The name callback and `updateCanonicalShotName` still write `provenance.name`. `localTimelineShotModel.ts:152-161` still prefers root `revision.name`; a root name can mask a rename. This known precedence/ownership contract gap is unchanged and must be settled by Agent/App management before native adoption.
- Read-side `runtimeGraphToContract` still unwraps `internalPayload.timeline ?? internalPayload` and normalizes assets and several known fields. The outgoing component proof does not certify arbitrary wrapped historical child payloads through that normalization.

## Exact tests and results

Worktree: `/home/user/work/wt/app-m2-shot-settings-safety-review-gate`. Ignored dependency symlink resolves physically to `/tmp/app-m2-coherent-deps8/node_modules` (ROOT8). No dependency install or package change.

RED before product follow-up, exit 1, **7 failed / 11 passed**:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx
```

Final scoped run, exit 0, **5 files / 74 passed**, 8.74s:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionEditor.opaqueRemap.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/shared/state/createEntityStore.test.ts
```

Both exit 0; ESLint emitted no output:

```sh
./node_modules/.bin/eslint src/tools/travel-between-images/pages/ShotEditorView.tsx src/tools/travel-between-images/pages/ShotEditorView.test.tsx
git diff --check
```

Logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-settings-safety-review-gate/notes/{red,targeted,lint}.log`.

## Exactly one real compatible consumer gate

The existing App-owned `tests/integration/runtimeRestore.test.ts` cleanly exercises restore and exact immutable closure readback. It has no settings-save case. Adding a settings publication on its tracked timeline would require legacy tracked-writer compatibility: current Runtime `publish_parent_composition` explicitly refuses it with `timeline_commit_required`, as required by its existing test. I did not change guards, authority, harness seeding or product contracts to force such a case. Used the explicitly authorized fallback exactly once after the final source edits:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-shot-settings-safety-review-gate restore-opaque-m1-compat-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m2-shot-settings-safety-review-gate-restore-opaque-m1-compat-integration-1020073245-2832 1
```

**PASS, exit 0, 1 file / 1 test**, 12s service time (8.28s Vitest). App source tree `29a7b4c695e19d8a5de086192da680c7b189a5e4`. Exact executed command:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python npx vitest run --config config/testing/vitest.runtime-restore.integration.config.ts --maxWorkers=1
```

Those two read-only historical leases were checked before and after: Agent `4a75f68f32049a69fd86135c645fa64c51175c14`, Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`. The service's generic `ext` metadata lists integration heads; the command's explicit environment selects these historical leases. This result must never be presented as CURRENT qualification.

Result and full log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-shot-settings-safety-review-gate-restore-opaque-m1-compat-integration-1020073245-2832/`.

The gate proves App `RuntimeDataProvider` exact immutable parent/child reads, an intervening Agent move, restore with the actual revision/publication head pair, accepted receipt and exact closure readback through the real Runtime door. It **does not exercise settings UI, the settings/name direct writer, settings-save acceptance, restart/outbox/inverse, or arbitrary wrapped historical payloads**. It complements the 74 scoped outgoing-consumer tests; it is not a settings save-to-readback proof.

## Handoff

No blocker to this bounded safety task. No evidence required deviating from PLAN. Preserve the direct writers until the Agent-owned field/capture/ownership/name contract and native consumer journeys qualify their replacement. Manager should review this six-line follow-up with the original two-file repair, keep the name/root precedence and read-normalization gaps explicit, and apply normal current-tuple qualification before claiming current Runtime compatibility.

No full suite was requested or run; full 11559 was left alone. No build, browser, tsc, install, native operation/DTO, generic serializer or other worktree change. No commit/merge/checkout/rebase/push/ref deletion. Draft retention remains in memory, not crash safe. KEEP, worker notes and commit message are supplied; DONE is created after final artifact checks.
