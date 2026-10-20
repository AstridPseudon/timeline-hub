# ShotSettings actual read/save/readback probe — BLOCKED

2026-10-20. Worker `/home/user/work/wt/app-m2-shot-settings-real-read-roundtrip`, base `66fe21c175a2f5bf0f5c4bae89ef6adf730691db` (safety review over writer repair). PLAN was read first. This report does **not** close the actual accepted settings/name save-to-raw-readback gap. Keep the manager's merge hold.

## Finding and candidate repair

A pure executable probe uses Runtime `4bb1d0f7`'s actual `_complete_shot_payload` and `_validate_published_shot_payload`, the committed App read converter, real name helper and outgoing encoder. It demonstrates a separate whole-shot loss: ordinary Runtime `generation_inputs: {}` becomes `[]`, and absent `dependencies`, `assets`, and `timing` become authored display defaults on name publication. The actual Runtime codec supplies that empty object; it is not an invented compatibility DTO. The settings object itself survives this particular converter unchanged.

The candidate repair adds 20 product lines in two existing files. `runtimeGraphToContract` retains the raw shot payload as local `revision.rawJson`, while keeping the existing normalized display fields and all validators. `updateCanonicalShotRevision` updates only its explicit settings/provenance/assets patch, intentional timeline/duration changes, declared shared-copy item remaps and immutable internal pin in that raw value. The existing outgoing encoder and shot digest use the retained raw payload. Prepared contracts without `rawJson` retain their previous path. There is no sidecar, new API/DTO, guard relaxation, compatibility writer, metadata service or renderer requirement.

The same pure codec/converter/name/encoder probe is RED against the committed read converter (exit 1, full-value assertion), GREEN against this worktree (exit 0). It bundles selected functions in memory solely to call the existing private converter; it does not add a product export or fake a backend. This is a bounded normalization counterexample and local repair check, **not HTTP acceptance evidence**.

## One actual HTTP run and precise blocker

Added the real callback journey to the existing included `tests/integration/runtimeRestore.test.ts`; no harness or service configuration was changed. Only UI child/provider hooks are mocked to capture the real `ShotEditorView` persistence/name callbacks, following its existing unit test. Runtime, door transport, adapter, graph helper, encoder and raw immutable HTTP reads are real. No renderer/browser is started.

The single authorized central request, after all source edits:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-shot-settings-real-read-roundtrip restore-opaque-m1-compat-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m2-shot-settings-real-read-roundtrip-restore-opaque-m1-compat-integration-1020075825-497 1
```

**FAIL, exit 1: 1 passed / 1 failed**, 50s service time, 46.19s Vitest. Exact source tree `aa09c8819f6e3d0c3fa0ac2372eeb445d94a521c`. No source changes or resubmission followed this result.

Executed command:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env ASTRID_CHECKOUT=/home/user/work/wt/app-m1-full-agent-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m1-full-runtime-source ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python npx vitest run --config config/testing/vitest.runtime-restore.integration.config.ts --maxWorkers=1
```

Historical leases were read-only and verified before/after: Agent `4a75f68f32049a69fd86135c645fa64c51175c14`, Runtime `4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136`. Physical standard dependencies: `/tmp/app-m2-coherent-deps8/node_modules` (ROOT8), selected by this worktree's ignored symlink and copied by the central snapshot service. This uses the authorized historical safety exception, **never current-tuple qualification**. The service's generic external-head metadata is not the source selection; the explicit command above is.

The old M1 restore control passed unchanged. The new test reached and passed: real Runtime acceptance of the **absent settings root** seed containing opaque data; normal HTTP raw immutable parent/shot/internal reads; exact App `rawJson` read; actual persistence load and neutral save producing no publication; exact raw immutable source readback after that neutral save. It then failed waiting for the real name callback's accepted publication: the published list remained empty for 30 seconds (`runtimeRestore.test.ts:216`).

A socket-free reproduction of the same `seedThreeProducts` geometry deterministically rejects that name graph in the existing adapter's `assertVisualSeamAdmission(..., {enforceIntent: true})`:

> Visual seam admission blocked: V1: f2-app-clip ends at frame 90, f2-transition-clip starts at frame 450

The seed places the ordinary app clip at 0–3s and its crossfade successor at 15–18s, so it is unsuitable for a whole-graph direct name/settings publication under the preserved guard. This pure reproduction explains a concrete pre-publication blocker; the HTTP test's captured error was not printed, so its underlying callback error is inferred from the matching graph rather than directly recorded. The pure reproduction with only that unrelated transition clip removed passes admission. Both probes are executable and retain the current guard.

Result/log directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-shot-settings-real-read-roundtrip-restore-opaque-m1-compat-integration-1020075825-497/`.

## Cases, controls and honest limits

- Intended positive cases in the new test: actual Runtime-admitted object settings with arbitrary nested/own prototype-named keys, explicit `negativePrompt: null`, absent known fields, and absent/null/scalar/array settings roots; neutral save; real name callback; prompt save for object/absent/null; scalar/array prompt refusal. Whole outgoing/raw immutable shot payloads, internal revision, opaque parent/occurrence values, parent config, old immutable history and fresh App reads are compared. **Only the absent-root pre-name phase executed.** Null/scalar/array/object root acceptance and accepted edited raw readback are unverified.
- Invalid input control is present for malformed known `metadata: []`, expecting HTTP 400 and unchanged head. **Not reached**, so it is not claimed as actual inadmissibility evidence.
- Final control enables the pinned M1 authoring provider, makes a tracked Agent move, invokes the real settings/name writers, expects `409 timeline_commit_required`, and checks unchanged raw head/closure plus the entity store's exact dirty/error draft and clean snapshot. **Not reached**. No legacy tracked-write refusal or other guard was changed; the original tracked M1 move/restore control passed.
- All original 74 positive/safety inputs pass unchanged; no test was skipped, deleted, weakened, or rewritten to expect missing behavior.
- The repair is not qualified for merge by this failed HTTP gate. No accepted settings/name edit, current Runtime tuple, arbitrary wrapped internal payload, native command adoption, touched-field intent, inverse/outbox/restart durability, or new shared-shot raw HTTP journey is claimed. Name still writes `provenance.name`; root-name display precedence is a separate existing gap.

## Exact local validation

Both commands exit 0:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionEditor.opaqueRemap.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/shared/state/createEntityStore.test.ts
# 5 files, 74 passed, 7.95s
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/integrations/runtime/shotCompositionRuntime.test.ts src/integrations/runtime/opaqueRootWriters.test.tsx src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts src/integrations/runtime/timelineCommit.test.ts src/tools/video-editor/data/shotCompositionAdapter.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts
# 7 files, 210 passed, 11.66s
```

Both exit 0 (ESLint emitted no output):

```sh
./node_modules/.bin/eslint src/integrations/runtime/dataProvider.ts src/tools/video-editor/data/shotCompositionEditor.ts tests/integration/runtimeRestore.test.ts
git diff --check
```

`./node_modules/.bin/vitest list --config config/testing/vitest.runtime-restore.integration.config.ts --maxWorkers=1` exits 0 and collects both real tests without opening sockets.

Executable local probes (notes path below):

```sh
node notes/raw-codec-probe.mjs --baseline  # exit 1, raw generation_inputs/default loss
node notes/raw-codec-probe.mjs             # exit 0, whole raw shot preserved
node notes/seam-probe.mjs                 # exit 1, exact visual seam blocker
node notes/seam-probe.mjs --neutral       # exit 0, unrelated crossfade removed locally
```

The raw codec JSON was produced with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m1-full-runtime-source /home/user/work/venv-runtime/bin/python`, calling the two actual Runtime codec/validation functions described above. `baseline-dataProvider.ts` is the worker's committed `66fe21c17` read source obtained by `git show`, not another checkout or mutable-head capture. Probe scripts only compile in memory; no worktree build output was created.

Logs and executable probes:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-settings-real-read-roundtrip/notes/` (`targeted.log`, `neighbours.log`, `lint.log`, `collection.log`, `raw-red.log`, `raw-green.log`, `seam-probe.log`, `seam-neutral.log`). Run the four probe commands from the worker artifact directory containing `notes`.

## Orchestrator next step

Keep this candidate unmerged. Dispatch a bounded follow-up with a new explicit central-run allowance: retain the original restore test, make the new probe's neutral seed omit the unrelated 15s crossfade in **both** parent clips/config clips (or supply a naturally adjacent neutral seed), and fail immediately with captured callback errors before waiting for accepted publication. Preserve `assertVisualSeamAdmission` and tracked-write refusal. Then execute every root/invalid/tracked case and compare accepted raw immutable payloads. The pure neutral check only validates local admission; it does not prequalify that HTTP run.

No full suite, build, browser, tsc, dependency install, product DTO/contract change, git commit/merge/rebase/checkout/push/ref deletion, or other worker/integration tree modification. KEEP exists. BLOCKED is supplied instead of DONE because the requested actual accepted round trip remains unproven. Commit message is supplied for harness handling; its creation is not merge approval.
