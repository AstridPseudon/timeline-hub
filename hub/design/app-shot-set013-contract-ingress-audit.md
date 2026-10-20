# Current S2 shot.set ingress audit

2026-10-20. **Source audit complete; neither settings nor name writer is ready for retirement.** S2 already supplies occurrence-owned root-name/scalar-settings semantics. The remaining work is App capture/authority/session wiring and compound-setting semantics, with one concrete native/payload-schema discrepancy below. This report supersedes the old assumption that no native shot-field operation exists; it does not claim accepted current Runtime/UI journeys.

## Exact current source, qualified first

| Input | Exact identity |
| --- | --- |
| App audited/tested | `/home/user/work/wt/app-m2-shot-set013-contract-ingress-audit`, HEAD `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Agent | `/home/user/work/wt/app-m3-agent013-current-pair-source`, HEAD `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` |
| Runtime source/schema | `/home/user/work/wt/app-m3-runtime013-producer-source`, HEAD `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| Normal App client | `0.2.13`; schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`; artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Command S2 | Agent canonical schema byte-equal to Runtime `contract/schemas/edit-command.json`; SHA256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`; 48 definitions / 22 EditCommand clauses. `operations()` enumerates 20 registry operations; inverse/restore account for the two other clauses. |
| Primary test dependencies | Private individual-package-link overlay, Composition extracted privately from App's locked `0.0.12` archive: SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular members. React/DOM `18.3.1`, Remotion/media `4.0.509`, Vitest `4.1.5`, Node `/opt/node22/bin/node` `v22.22.0`. |

All **13 App locked files** matched their lock hashes and exact Runtime producer bytes. The Agent source keeper's 15-file count describes Agent's lock, not App's. This is focused current-source/public12 qualification, not primary Root/Player/browser release qualification. No historical safety tuple was substituted for current S2. See worker `identity.json`.

PLAN, deletion ledger D01-app-shot-raw-normalization and prior settings/raw-reader reports were read. `75df44e99` integrated the safety repair. At the audited App HEAD, its `dataProvider.ts`, `shotCompositionEditor.ts`, and `tests/integration/runtimeRestore.test.ts` are byte-unchanged; the component differs only in the canonical route-identity helper, and its test only changes `localProject/localTimeline` to `project/timeline` in setup. No inventory or repository source/test file was edited for this audit.

## Existing native contract and golden

Authoritative files under the exact Agent source:

- `astrid/core/timeline/schema/edit-command.schema.json:$defs.ShotSetArgs` and `EditCommand`'s shot.set clause.
- `astrid/sdk/timeline/_shot_commands.py:12,44`: `shot_set` and `capture_shot_set`.
- `tests/editing_conformance/test_recipe_shot_set.py` and `fixtures/recipe_m2_shot_set.json` (SHA256 `d7179b08eede890e301bae6874380b2a8067570479dc2605c7344776871dcfe4`).

The actual generated App boundary is `src/integrations/runtime/timeline-commit-types.ts:25,103,115,119`, type **`ShotSetArgs`**. There is no callable `nativeShotSetArgs` helper in these exact App/Agent/Runtime sources. A future App builder must implement the existing contract; a type name is not a capture implementation.

Wire shape: `schema_version: 1`, `op: "shot.set"`, `version: "1"`, `select: "occurrence:<raw-occurrence-id>/shot"`, `args: {values, clear}`, `intent: {ownership: "occurrence"}`. Both args keys are required. At least one set/clear is required, settings values cannot be an empty object, unknown args/fields, duplicate clears and set/clear overlap refuse. Root `settings` replacement/clear and `provenance` writes are not operations in this contract. No shared-shot intention or global shot selector is supported.

| Settable settings roots | Value type, also nullable |
| --- | --- |
| `videoControlMode`, `prompt`, `negativePrompt`, `dimensionSource`, `generationMode`, `selectedModel`, `motionMode`, `selectedPhasePresetId`, `textBeforePrompts`, `textAfterPrompts`, `generationTypeMode` | string |
| `batchVideoFrames`, `batchVideoSteps`, `customWidth`, `customHeight`, `guidanceScale`, `amountOfMotion` | finite JSON number; schema does not supply UI enum/range policy |
| `enhancePrompt`, `turboMode`, `advancedMode`, `smoothContinuations`, `ltxHdResolution` | boolean |

The 22 settings roots clear through `settings.<key>`. `name` sets a string at **raw payload root `name`**, or clears through `clear: ["name"]`; name null is invalid. Set null, clear absence, false, zero and empty strings are distinct. Strings are not normalized or enum-constrained by ShotSetArgs.

Unsupported set **and clear**: `steerableMotionSettings`, `phaseConfig`, `pairConfigs`, `shotImageIds`, `loras`, `structureVideo`, `modelSettingsByModel`, arbitrary unknown settings keys, and nested subpaths. Unmentioned compound/unknown data survives unchanged. A mixed supported/unsupported batch refuses atomically; migrating only its scalar half loses behavior and is not acceptable.

Capture reads the occurrence ID and shot ID, fixes `shot.owner` to `occurrence:<id>`, and records exact `shot.source` dependency pins when present: source shot/revision/digest, internal timeline/revision/digest and item map. Selected raw occurrence ownership, not a projected clip/group ID, resolves the editable shot. The authoring bundle isolates shared shots per occurrence; native tests cover shared/unshared compilation and exact inverse. Runtime request project/timeline and revision/publication authority come from the verified command basis, not this selector alone.

The unchanged portable golden sets root name `Renamed`, explicitly writes unchanged prompt `Old`, writes `turboMode: false`, clears a present-null `negativePrompt`, and records original root name `Opening`. Command fields include `resolved`, exact `expect`/`authorship`, reads, `bindings: {"shot.owner":"occurrence:occ-1"}`, empty selections/created, and occurrence-only intent. Native execution equals the exact golden command/after bundle/compiled shot revisions. The suite also checks deterministic replay, guarded inverse/redo, unchanged writes/ABA, disjoint rebase, source/owner/container conflicts and unsupported batches. Do not replace those captures with normalized-form diffs.

## Native output through actual App reader/form

The native probe produced real `compile_authoring_candidate(...).publication` output. An in-memory transport supplied those immutable records to actual `RuntimeDataProvider.shotComposition.loadAtHead`, actual composition parser/adapter, and `selectCanonicalShotModels`. No socket, fake provider validator, alternate reader or bypass of parser validation was used. This tests source behavior; the transport does not establish server acceptance or authenticated commit authority.

| Native name action, original legacy name `Legacy` | Native capture/execute/inverse | Pinned Runtime ShotPayload schema | Actual App pipeline |
| --- | --- | --- | --- |
| set `Renamed`, root originally present or absent | success, exact inverse | valid | displays `Renamed`, preserves provenance name |
| set `""` | **success**, exact inverse | **invalid: name minLength 1** | **fails** `shot_revisions[0].name: must be a non-empty string` |
| set two spaces | success, exact inverse | valid | preserves raw spaces; display falls back to `Legacy` |
| clear present or absent root | success, exact inverse | valid | root absent, displays preserved `Legacy` |

The reader keeps payload root name and rawJson; the model prefers nonblank root name, then provenance name/title, metadata name/title, stable shot ID. Re-encoding the read rows, explicitly marked as outgoing rows only within the probe, preserves the raw payload exactly. Already-read rows are normally omitted from outgoing publication unless marked `publish`, as designed.

**Concrete Agent question:** S2 native name tests positively require `name: ""`, while Runtime2c4's `contract/schemas/shot-composition.json:$defs.ShotPayload.properties.name` requires minLength 1 and the App matches that restriction. Which contract is to be reconciled by its owner? Preserve the native positive expectation until an authorized contract change; do not call this end-to-end success or rewrite it to an expected refusal. No schema or test was altered here. Nonempty UI rename does not require choosing an answer to this separate gap.

The actual current name callback was invoked on a graph read from native output. It successfully published `provenance.name = "Legacy callback rename"`, retained root `name = "Renamed"`, and the resulting App model still displayed `Renamed`. Thus the old writer remains masked when a root name exists; current S2 root-name writing is already the chosen canonical direction, not a fresh ownership/field decision.

Settings probes inject each raw shape into the transport record before the actual reader: absent, null, scalar `17`, array `[1,null]`, and object with unknown nested values/duplicate entries. Actual `ShotEditorView` persistence callbacks then load/save the form. Unchanged forms publish nothing for all five. Prompt change initializes absent/null with exactly `{prompt}`, preserves the object's null/unknown siblings, and visibly refuses scalar/array replacement before publication. Native settings set/clear probes separately confirm exact inverse and unchanged unknown nested values for all 22 fields (66 set/null/clear cases), plus the five-container/action matrix. Native name-only edits preserve even scalar/array settings; prompt changes there refuse. Absent/null clear does not materialize a settings object.

## Live call graph and authority gap

All following App paths refer to the audited App worktree.

| Path | Current behavior and missing seam |
| --- | --- |
| `components/ShotEditor/hooks/editor-state/useNameEditing.ts:55` → `ShotEditorView.tsx:331` | UI emits trimmed nonempty changed strings only; no name clear/null UI. `onUpdateShotName(newName)` runs after typing. It does not carry a capture from `handleNameClick`; a refreshed prop callback is not an original raw edit basis. |
| `ShotEditorView.tsx:142-208` → `VideoTravelSettingsProvider.tsx` → `hooks/settings/useShotSettings.ts:98` → `shared/settings/hooks/useAutoSaveSettings.ts:146` | Custom loader obtains a prepared composition and normalizes only the form. Save receives a whole form snapshot; comparison overlays changed roots onto raw settings and retains safety guards. `updateField/updateFields` exist upstream, but touched paths, explicit clears and unchanged authored writes are lost before this persistence callback. |
| `ShotEditorView.tsx:185,345` → `shotCompositionEditor.ts:394,535` → adapter publish → `dataProvider.ts:248` | Settings replaces the guarded assembled settings root; name edits provenance. Queue uses explicit project/parent. Both still publish whole graph snapshots with expected revision; neither enters the native command outbox. Name base is the composition prop at save; settings base is the ref captured by load/last own publication. |
| `VideoEditorProvider.tsx:875,909` → `useTimelineState.ts` → `useTimelineSave.ts:99` → `useTimelineCommandSession.ts:53,114` | Mounted editor authority is scoped by explicit project/timeline/user/provider generation. Session loads recoverable actor identity and verified canonical raw basis, owns revision/publication pair, outbox, dependent suffix, exact request/key, undo, accepted projection and stale-read guards. No default-timeline inference is needed or valid. |
| `commitSession.ts:240-324`; `useTimelineCommandSession.ts:236` | Only move and parent-track-label capture/finish/submit ports exist. They enforce original local generation/basis and prepared payload ownership. There is no shot capture/finish/submit port, nor a generic public native enqueue to reuse safely. |
| `AstridTimelineEditor.tsx:383,717` → `LocalTimelineShotBrowser.tsx:290` → `ShotEditorView` | Embedded popup passes exact selected occurrence/deep link, parent ID, canonical adapter/composition and publication/draft callbacks. It does **not** pass the mounted command-session capture authority. Publication callback updates local override and `runtime.shots.adoptCanonicalComposition`; that is accepted display coordination, not permission to mint an outbox capture. |
| `useAstridShotsHost.ts:49-130`; `ShotTimelinePreview.tsx:406-450,559` | Existing `CanonicalShotTimelineScope` uses project, parent, occurrence and popup editorSessionId. Begin/end/projection/clear callbacks guard popup draft lifetimes. These callbacks currently belong to child timeline preview; settings/name do not report their own capture lifecycle through them. Draft scope token is distinct from command outbox actor/owner authority. |
| `AstridTravelRoute.tsx:35` → standalone `LocalTimelineShotBrowser.tsx:84-143` | Standalone route resolves an explicit discovered project/timeline and constructs its own Runtime provider/adapter. It receives no mounted parent session. Discovery may choose a timeline before writing the explicit route; the audit never uses that default to infer a shot's command owner. |

There is no `globalShotEditor` symbol or global shot command session in this exact source. Global shot selection/settings caches do not confer canonical write authority. Standalone/global navigation must acquire or be passed a correctly scoped session explicitly; borrowing whichever editor happens to be active risks the wrong project/timeline or a second outbox lifetime.

Settings support also cannot be inferred from individual scalar type names: `useShotSettings.ts:243` couples `advancedMode`/`motionMode` changes to `phaseConfig`; `useVideoTravelSettingsHandlers.ts:157-184` couples frames/steps to `modelSettingsByModel`; generation mode/model changes also update compound data. Their full positive behavior must survive. Prompt/negativePrompt are genuinely simple existing callbacks (`...Handlers.ts:147-153`), but the current shared autosave snapshot still discards intent.

## Smallest next PR and retirement boundary

**Recommend one bounded App PR: nonempty canonical rename in the mounted editor only.** Reuse S2 `shot.set`, root name and occurrence ownership. Add a small capture/finish implementation proven against the existing native golden/records, expose its typed port on the existing command session/store, and pass it down the embedded browser rather than resolving a global editor. Capture raw field presence, selected occurrence/source pins, exact displayed revision/publication, local generation and dependent local basis when editing begins (`handleNameClick`), then finish/submit the trimmed string through that same port. An unchanged explicit write must retain intent where the callback represents one. Reject stale/mismatched owner or missing authority without guessing another timeline or recapturing at save. Keep the draft visible until acknowledged; current void name callback/error toast alone is not durable retry or sufficient draft retention.

Project accepted closure through the existing session projector and canonical adoption callback; do not use a normalized settings form or preview config as capture/publication data. The nested publication/draft callbacks must be tied to the originating project/parent/occurrence/editor lifetime. Do not start a second outbox in the popup or bypass pending local edits/recovery/legacy-save fences.

Standalone name and the full settings writer remain unchanged until their real authority/field-intent seams are migrated. This PR is a bounded consumer migration, not global name-writer deletion or D01 closure. For a later prompt slice, intercept explicit `handleBatchVideoPromptChange`/negativePrompt intent before generic snapshot autosave and preserve pending compound batches atomically; do not silently drop unsupported roots or turn passing compound edits into refusals.

Neither old writer is removed by this audit. Retirement needs actual current Runtime accepted raw reload, renderer-independent save, undo/redo, lost ACK/exact retry/restart, dependent edits, original positive/malformed/draft controls and **zero legacy traffic for the migrated consumer**. No such journey was run here. `75df`'s referenced malformed `metadata: []` exact HTTP422 and tracked settings/name HTTP409/draft controls are byte-unchanged; the prior historical-compatible `16622` pass remains historical evidence only. No success-to-refusal conversion, skip, xfail, schema relaxation or fallback activation was made.

## Exact probes and results

Artifacts: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-set013-contract-ingress-audit/` (W below). Commands ran from the assigned App worktree. Private qualification config imports the unchanged repo config, disables test cache and puts Vite's directory under W; private extracted Composition and individually linked read-only dependencies are supplied through this worker's own ignored node_modules link. No shared node_modules/venv/runtime/cache writes or installation occurred. That worktree link is restored after qualification.

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-set013-contract-ingress-audit
AGENT=/home/user/work/wt/app-m3-agent013-current-pair-source
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider "$AGENT/tests/editing_conformance/test_recipe_shot_set.py"
# native-targeted.log: exit 0, 61 passed in 2.00s.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AGENT" /home/user/work/venv-agent/bin/python "$W/native_probe.py"
# native-probe.log/native-results.json/native-cases.json: exit 0; 66 field checks,
# 15 container/action observations, six name outputs with inverse, exact golden.

ASTRID_CHECKOUT="$AGENT" node node_modules/vitest/vitest.mjs run --config "$W/qualification.config.ts" --no-cache --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/integrations/runtime/shotCompositionRuntime.test.ts src/tools/travel-between-images/pages/localTimelineShotModel.test.ts
# app-targeted-final.log: exit 0, 3 files / 60 passed, 8.58s.

ASTRID_CHECKOUT="$AGENT" node node_modules/vitest/vitest.mjs run --config "$W/probe.config.ts" --no-cache --maxWorkers=1
# app-probe-private-cache.log: exit 1, 1 failed / 2 passed, 4.51s.
# Failure intentionally retained: native-success empty name fails actual App parser.
# Passes: actual old rename masking; actual reader/form five-root settings matrix.

ASTRID_CHECKOUT="$AGENT" node node_modules/vitest/vitest.mjs run --config "$W/matrix.config.ts" --no-cache --maxWorkers=1
# app-matrix-private-cache.log: exit 0, 1 observational probe (3.44s), six outcomes recorded in
# app-name-results.json. This records the empty-name failure; it does not qualify it.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$W/schema_probe.py"
# runtime-schema-results.json: pure pinned-schema validation, exit 0;
# empty name invalid, other five name cases valid. No Runtime process launched.

git diff --check
git status --short
# exit 0; clean source tree.
```

Private probe setup errors (unavailable historical Node20 path; runner-loader `__dirname`/module resolution; an initial TS rather than TSX probe; missing slash in copied child mocks and omission of an encoder publish marker) were corrected solely in worker artifacts. `app-probe-startup-failure.log` and `app-probe-fixture-failure.log` retain the latter failures. Final failing name expectation was not rewritten as refusal; the separate observational matrix records all remaining cases without parser bypass.

Final cache audit found an initially inherited `.vite-temp` symlink in the private overlay. The shared target remained empty with its unchanged 08:32 directory timestamp; no config was written there. The private link was replaced with a real private directory and all App probes were rerun for the final results above. Shared cache metadata/entries match exactly before/after that final run (`shared-cache-before.json`, `shared-cache-after.json`).

No full suite, build, tsc, browser, localhost/socket, install or test-service request. No product, repository test, lock, generated client, ledger or inventory edits. No git mutation. Audit is complete; native consumer cutover and the empty-name contract reconciliation remain unverified/outstanding work for their owners.
