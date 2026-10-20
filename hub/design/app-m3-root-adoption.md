# App M3 source candidate and gated root adoption

## Current candidate — label/initial/public10 refresh (2026-10-20)

Worker/branch: `app-m3-label-release-refresh` / `tl/app-m3-label-release-refresh`.
Base: `126658391742d62cf8b10f6421d0bea529ba6502`.
**Final source SHA: `903f2755043f880ef628ea65356700fe4d4b847d`** — manager verified final harness branch. Exact reconciliation and commands: `workers/app-m3-label-release-refresh/report.md` and `static-review.py`.
This section supersedes the candidate/pin instructions in the historical sections below. **Source-only; all M2/M3 integration merges remain HELD until PLAN records M1.** Corrected full `app-full-m1-opaque-integration-1020025341-10022` completed18336PASS/6EXACTOLDFAIL and was accepted03:17; globalM1stillawaitsAgentfull. At source preparation time, no test, typecheck, build, install, browser/discovery, socket or test-service request was made here.

- Exactly eight App paths changed: the three absent native M1 fixture files from `ea3461e0c..c8566f12d`; exactly four official Runtime pin files from `f5e438652..823d078daa27081dabc360037de1aaaa2bb1a408`; and Viewing `910773b31`'s new 353-line `useVideoEditorPreviewComposition.initialRead.test.tsx`, unchanged (18 mounted cases, UNRUN here). No wider ordinary-control source was imported from `f5e438652`.
- Read-only reconciliation: 16 of the 17 existing Viewing paths match both `df6ba7120` and `910773b31`, including the two existing audioFade deletions. The remaining command-projection test stays at this base's **175 lines**, retaining the 15 initial public-vector/committed-label lines missing from Viewing's 160-line copy. No existing Viewing path was overwritten.
- `useTimelineCommandSession.ts` matches the reviewed producer byte-for-byte: blob `39db2c89b352174914e6915286b633a1bcf5aa1b`. Keep/Use latest, `loadLatest`, read-generation, recovery, initial-source fences and all four cold/ordinary/conflict label cases remain unchanged. All existing e2e files, including restored original M1 and mixed journeys, remain byte-identical to base. Current M1 opaque product code matches `c8566f12d` exactly.
- All 13 Runtime-locked files match both their declared hashes and native producer bytes. New frozen qualification pair: **Agent `027bd16d96010544331c953c0e1014e161786e71` + Runtime `4c145dc62192f0e942e3ee3922a11488aefe9b41`**, client **0.2.3**, schema `a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6`, aggregate artifact `0f3d217ba0f3ca51d580bf3938fb3df1361a561de5acae7a911d21a9eea8bd9e`. The official generated exports are copied intact; no hand-written DTO extension. Frozen Bundle1 Agent `3bf9e5368a956ef562c77e1beb0a745addf23daf` / Runtime `6be970633cc82ab412428151e6bf42f3e7fc3081` refs and historical qualification remain intact.
- Root package/lock/config/vendor paths and the shared dependency environment remain unchanged, at Composition **0.0.8**. Public10 tarball identity was checked read-only: **58,008 bytes**, SHA-256 `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`, matching its sidecar. No compiler shim, metadata-only relabel, raw-loader accepted stamp, params/scalar/trim/popup/delete/UI port or vendor retirement was added.

Validation: scoped ESLint on all five changed TS/TSX files **PASS (0 warnings)**; `node scripts/quality/check-known-failures.mjs` **PASS (3 authorized / 0 forbidden)**; `git diff --check` **PASS**; read-only `python .../workers/app-m3-label-release-refresh/static-review.py` **PASS**. The fixture exporter was parsed only, never executed. **Mounted/public10/cold-label, all other tests, project typecheck/build, full suites and actual picture/audio parity are UNRUN on this candidate.** Predecessor pass counts below are historical evidence only.

After the M1 record and quiet-window release, a separately assigned root qualifier owns the following, together:

1. Resolve the harness SHA above and use this entire candidate. Perform the seven root/lock/config/vendor steps preserved below against the exact public **0.0.10** tarball, with App+Agent adoption coordinated. Retain the **new 0.2.3 four-file pin and exact frozen pair above**; the older instructions to keep 0.2.2 are historical. Preserve old tarballs, unrelated vendors, shared peers and the bundled-theme identity assertion; no fallback to private exports/source aliases. Do not import the separate unqualified ordinary-controls candidate.
2. On the finished actual 0.0.10 installation, run `node --test config/vite/timelineCompositionPackage.test.mjs` (version assertion updated by the root qualifier), preserving all export/shared-peer checks. Central `targeted --files "..."` must include the new initialRead and preserved commandProjection files, all existing Viewing test paths in `dd376d5e0..df6ba7120`, preview neighbors (`RemotionPreview.test.tsx`, `useVideoEditorPreviewComposition.test.tsx`, `useVideoEditorPreviewSurface.lifecycle.test.tsx`), `useTimelineCommandSession{,.projection}.test.tsx`, `useTimelineCommit.test.tsx`, and the command session/outbox/move/label/authoringBundle/opaque fixture neighbors. Use `$ORCH/bin/request-test <root-qualifier-worker> targeted --files "$FILES"`, then `$ORCH/bin/wait-test "$R"`; this worker requested none.
3. Run the actual serialized project check: `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false`. Report exact diagnostics against the two known baseline errors, not a root-empty config result. Run the hosted build through a central build lane with the exact paired Agent source (`env ASTRID_CHECKOUT=/home/user/work/wt/app-m2-bundle2-agent-source npm run build:hosted`); the suite owner must pin that environment before requesting it.
4. Central browser qualification must run **all four** `track-label-command.spec.ts` cases through `playwright.track-label.config.ts`, plus restored M1/closure, mixed/recovery and restore-integration journeys. The suite owner must register/review a new 0.2.3/public10 label lane: use `TIMELINE_BUNDLE_AGENT_HEAD=027bd16d96010544331c953c0e1014e161786e71`, `TIMELINE_BUNDLE_RUNTIME_HEAD=4c145dc62192f0e942e3ee3922a11488aefe9b41`, `ASTRID_CHECKOUT=/home/user/work/wt/app-m2-bundle2-agent-source`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m2-bundle2-runtime-source`, existing venv Python paths and `npm exec -- playwright test --config playwright.track-label.config.ts`. Keep leases and preflight/start/end source checks. The existing `e2e-m2-label-bundle1` lane is frozen to 0.2.2 and **cannot qualify this pin**. Likewise pin the exact source pair explicitly in the central `e2e-m1-closure`, `e2e-m1-mixed` and `restore-integration` qualification environment; do not substitute default integration heads or relabel old results.
5. Actual Player/export frame and audio parity with independently planted mismatches remains OPEN. Any later full suite needs a separate explicit brief and at most one final-tree request; no full qualification is requested by this source task. Keep all original assertions and classify failures honestly. Root adoption and branch proof do not authorize M2/M3 integration before the PLAN M1 record.

## Preserved prior release-source handoff

Worker/branch: `app-m3-release-source-compose` / `tl/app-m3-release-source-compose`.
Base: `d347cfff47` (`tl/app-m2-conflict-label-compose`). This candidate supersedes the earlier source-prep starting point below; that handoff is preserved verbatim.
**Source-only, held until the M1 record. No M2/M3 merge or install qualification is claimed.**

- Applied only `214981bbc..7d15151f2` (20 paths), `2bfde69ea..7cee9939c` (4 authoringBundle paths), and `d347cfff47..bccebd3f7` (one cold-label spec addition). Exactly 25 source/test paths changed.
- Eighteen source-prep paths match `7d15151f2` exactly, including two audioFade deletions. The session hook and its mounted test required bounded reconciliation: one accepted-closure projector now serves initialization and later acceptance, while the base's `loadLatest`, read-generation/session fences, Keep/Use latest/recovery callbacks and cleanup remain byte-identical. The mounted test only adds the exact reviewed initial-projection case; every base assertion remains.
- All four opaque paths match `7cee9939c` exactly. Native item/source links alone are remapped; foreign metadata remains opaque. No authored fields, DTOs, schemas, generated files, new abstractions or unrelated writer/parameter/deletion changes.
- All 67 other existing e2e files are byte-identical to base, preserving both original M1 gesture bodies and the concurrent journey. The entire base label spec is an unchanged prefix, and its four cases now match `bccebd3f7` exactly, including opaque/root/recovery/metadata/publication checks.
- Viewing uses the reviewed public `clipOpacity` import and preserves `expect(entry.source).toBe('bundled:2rp@0.1.0')`. No synthetic DrawPlan mutation or private opacity math was added.

Final dependencies for **one separately authorized root/vendor install qualifier after M1**:

| Dependency / scope | Required action or fixed value |
|---|---|
| App source | This composed worker tree, based on `d347cfff47`; qualify the whole candidate together. |
| Composition artifact | Use only `ORCH/artifacts/banodoco-timeline-composition-0.0.10.tgz`, 58,008 bytes, SHA-256 `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`; copy identical bytes to App `vendor/artifacts/`. |
| Public API | Actual 0.0.10 exports, including `compileCanonicalTransitions`, `clipOpacity`, public registries and bundled 2rp defaults. No 0.0.8/0.0.9 substitution, alias to source or compiler shim. |
| Shared peers | React/React DOM 18.3.1; Remotion, `@remotion/media`, `@remotion/layout-utils` 4.0.509. Installed peers match. Preserve Player/web-renderer/Three versions; ensure layout-utils production availability as described below. |
| Runtime | Keep the base's 0.2.2 contract/generated metadata, frozen Bundle 1 source pins and leases unchanged; no Runtime root/generated refresh in this batch. |
| Root/lock/config/vendor | Perform the existing seven-step handoff and all 13 default-directory deletions below in that single qualifier. Coordinate Agent's adoption of the same frozen artifact. Preserve unrelated vendors and host components. |
| Required proof | Actual 0.0.10 package-resolution/shared-peer tests, all affected source/preview suites and neighbors, serialized typecheck/build; central browser cold-label plus all original label/M1/concurrent/recovery journeys. Frame/audio parity and planted mismatches remain separately required. |

Validation on this composed tree:

- Five isolated command suites: **285 passed / 5 files**, 11.59s.
  `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts`
- Two isolated session-hook suites, which do not import the new public-0.0.10 viewing path: **38 passed / 2 files**, 6.77s.
  `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`
- Scoped ESLint on all 21 changed TS/TSX paths: **PASS**, no warnings. `npm run check:known-failures`: **PASS**, exactly 3 authorized markers / 0 forbidden. `git diff --check`: **PASS**. Exact lint arguments and verification results are in this worker's commit message.
- Read-only endpoint/path/base comparisons and artifact size/digest/public-declaration/peer checks: **PASS**. Root, lock, config, vendor, generated and pin files remain byte-identical to base. Shared `node_modules` still resolves Composition **0.0.8**.

**UNRUN:** all tests executing the new public-0.0.10 or preview path, actual Runtime/browser cold-label qualification, package-resolution suite, project typecheck/build, full suite and pixels/audio parity. No install, network, browser, new skip/expected-failure, fallback/mock/shim for missing 0.0.10 exports, or Git mutation was performed. The passing isolated fixtures do not qualify real cold-label behavior, public 0.0.10 execution or pixels. Keep M2/M3 merges held until M1; then dispatch the single root/vendor qualifier against this candidate.

## Preserved source-prep handoff

Source-prep worker: `app-m3-source-batch-compose`, branch `tl/app-m3-source-batch-compose`.
Qualified starting point: `214981bbc` (`tl/app-m2-label-browser-qualify`, Bundle 1).
This is a **source-only candidate, not merge-ready**. PLAN has not recorded M1. No package installation, root/config/lock change, vendor deletion, network, full suite, browser, build or project typecheck was performed. Shared `node_modules` remains the symlink to `/home/user/work/app/node_modules`, with Composition **0.0.8**.

## Composed source

- Applied only the cumulative 17-path Viewing delta `dd376d5e0..df6ba7120`. Sixteen paths match the reviewed endpoint byte-for-byte, including the two reviewed audioFade deletions. The command-projection test has additional integration assertions described below. Kept the M1 exact assertion `entry.source === 'bundled:2rp@0.1.0'`; only its surrounding obsolete description changed.
- Applied only the three-file initial-projector delta `70f7fd522^..70f7fd522`. Reused the existing accepted closure projector for clean bootstrap; kept this base's guarded track-label port unchanged. Did not import ancestor-only Use latest/Keep/read-generation changes absent from the qualified base.
- Inspected `hub/tl/vw-m3-app-read-projection-fact` (currently `b23108926`): its executable producer/surface/mailbox/native-omission case is already included in the cumulative reviewed Viewing delta. Extended that same test to pass the actual verified initial basis, without commands or graph, through the public `compileCanonicalTransitions` export and actual preview surface. It expects the concrete vector `{fps:30, tracks:[{trackId:'V1', clipIds:['a','x','c'], incomingTransitions:[null,{T:12},null]}]}`. The original raw/native omission, local, accepted, late graph, exact config/vector pairing and revision assertions remain. The accepted lookup now selects publication `p1`, because bootstrap also installs accepted `p0`.
- Initial-projector tests retain invalid closure/head/scope/bundle refusal, delayed local/recovery/accepted/head/unmount fences, persisted original B basis and late A versus C ordering. Added existing-local/existing-accepted bootstrap guards. No additional skip, `it.fails`, fallback package, compiler mock, authored field, config field or wire field was introduced.
- Original e2e journeys, metadata/recovery code, schemas, Runtime/Agent generated sources, root configuration and all vendors are unchanged from `214981bbc`.

## Exact dependency check (read-only, passed)

Artifact: `ORCH/artifacts/banodoco-timeline-composition-0.0.10.tgz`, where ORCH is the real absolute directory containing this document.

- SHA-256: `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`.
- Size: **58,008 bytes**. The adjacent `.sha256` file matches the digest.
- Tar metadata declares `@banodoco/timeline-composition@0.0.10`, public ESM/declaration export maps, and no schema/theme npm dependency. Public declarations contain `compileCanonicalTransitions` and `clipOpacity`.
- Exact required installed peers already match: React/React DOM **18.3.1**; Remotion, `@remotion/media`, `@remotion/layout-utils` **4.0.509**. App's Player/web-renderer/Three peers remain at their current main versions. App currently declares layout-utils directly in devDependencies; preserve production-install availability when qualifying the package closure.
- These checks read tar members and installed package metadata; they do not load or execute 0.0.10. Composition 0.0.8 cannot supply this candidate's new public imports. Frozen 0.0.9 is historical and must not be used as a fallback.

Reproduce artifact identity from the real ORCH directory:

```sh
sha256sum artifacts/banodoco-timeline-composition-0.0.10.tgz
stat -c %s artifacts/banodoco-timeline-composition-0.0.10.tgz
tar -xOf artifacts/banodoco-timeline-composition-0.0.10.tgz package/package.json
```

## Future root/vendor batch (only after the M1 record)

Coordinate the App and Agent pin adoption to this same immutable artifact. The manager owns a separate install/proof task; none of the following edits were made here.

1. Copy the exact artifact into App `vendor/artifacts/banodoco-timeline-composition-0.0.10.tgz` and verify digest/size again. Retain existing 0.0.8 and any frozen 0.0.9 artifact. Do not repack, rebuild or modify the approved tarball.
2. In `package.json`, replace `dependencies['@banodoco/timeline-composition']` with `file:vendor/artifacts/banodoco-timeline-composition-0.0.10.tgz`. Remove `dependencies['@banodoco/timeline-theme-2rp']`: its defaults are bundled and the App theme selection already uses its existing host metadata. Keep the independent timeline-schema/timeline-ops and official Runtime Bundle 1 pins unchanged. Preserve the five exact shared peer versions; if the production install omits devDependencies, move layout-utils's existing exact declaration to dependencies rather than introducing another copy.
3. Regenerate `package-lock.json` using the normal App npm install in the separately authorized dependency environment. Expected lock changes: root dependency spec; `node_modules/@banodoco/timeline-composition` version/resolved/integrity to the exact 0.0.10 file artifact; removal of the `node_modules/@banodoco/timeline-theme-2rp` link and `vendor/timeline-theme-2rp` package record. Account for npm peer/dev flag changes if layout-utils is moved. Keep unrelated locked dependencies and Runtime artifacts stable. Verify SRI against the same tar bytes. Do not change shared node_modules during the held source-prep task.
4. Remove the three now-obsolete App default `@workspace-effects`, `@workspace-animations`, `@workspace-transitions` aliases from `config/vite/vite.config.ts`, `config/testing/vitest.config.ts`, `config/testing/vitest.boundary.config.ts`, `config/testing/vitest.edge.aliases.ts`, and `scripts/astrid-landing/public-host-browser/vite.config.ts`. Remove the obsolete `@banodoco/timeline-theme-2rp` dedupe entries in Vite, main/boundary Vitest and public-host configs. Keep normal package export resolution, Composition dedupe and the React/Remotion peer aliases. No alias to Composition source or a second ThemeContext.
5. Reconcile `config/testing/vitest.astrid-renderer.config.ts`'s three rendering-pack aliases with the coordinated Agent source adoption: package defaults must resolve from 0.0.10; retain any separately admitted host-element support needed by actual Agent consumers. Its `renderingElements` helper becomes removable when no alias uses it. Remove the stale `@workspace-animations/*` path from `tests/e2e/fake-runtime/tsconfig.json` and update the stale launch comment if consumer import checks confirm it is unused (current source scan finds no imports).
6. Update the version assertion in `config/vite/timelineCompositionPackage.test.mjs` from 0.0.8 to 0.0.10. Preserve every public-export realpath/shared-peer assertion, including the new `./registries` export. Keep the exact bundled-theme identity assertion in `TimelineRenderer.test.tsx`. The old `vendoredTimelineCompositionAliases.test.ts` still requires vendored source files: migrate its package/declaration/default-resolution coverage to actual public exports before deleting the obsolete source tree, without dropping behavior coverage or teaching a behavior test to expect refusal. This source-prep task deliberately leaves it untouched.
7. Delete the 13 duplicate default implementation directories below, including their obsolete JSX mirrors/schema/default/meta files, after public registry behavior is qualified. Then remove the obsolete App `vendor/timeline-composition/` source mirror and unused `vendor/timeline-theme-2rp` package shell only after the remaining file-based contract checks migrate. Keep unrelated vendors and host-installed custom component support.

The 13 default deletion paths (all relative to App; each contains its `component.tsx`):

| # | Delete directory | Canonical packaged implementation |
|---|---|---|
| 1 | `vendor/banodoco-effects/text-card/` | `builtins/effects/text-card/` |
| 2 | `vendor/banodoco-animations/fade/` | `builtins/animations/fade/` |
| 3 | `vendor/banodoco-animations/fade-up/` | `builtins/animations/fade-up/` |
| 4 | `vendor/banodoco-animations/scale-in/` | `builtins/animations/scale-in/` |
| 5 | `vendor/banodoco-animations/slide-left/` | `builtins/animations/slide-left/` |
| 6 | `vendor/banodoco-animations/slide-up/` | `builtins/animations/slide-up/` |
| 7 | `vendor/banodoco-animations/type-on/` | `builtins/animations/type-on/` |
| 8 | `vendor/banodoco-transitions/cross-fade/` | `builtins/transitions/cross-fade/` |
| 9 | `vendor/banodoco-transitions/fade/` | `builtins/transitions/fade/` |
| 10 | `vendor/timeline-theme-2rp/src/effects/art-card/` | `builtins/themes/2rp/effects/art-card/` |
| 11 | `vendor/timeline-theme-2rp/src/effects/cta-card/` | `builtins/themes/2rp/effects/cta-card/` |
| 12 | `vendor/timeline-theme-2rp/src/effects/resource-card/` | `builtins/themes/2rp/effects/resource-card/` |
| 13 | `vendor/timeline-theme-2rp/src/effects/section-hook/` | `builtins/themes/2rp/effects/section-hook/` |

## Validation and pending proof

Executed on this source candidate:

- `git diff --check`: PASS, exit 0.
- Scoped ESLint below: **18 files, PASS, exit 0, no warnings**.
- Read-only source comparisons: PASS. Sixteen Viewing paths match reviewed endpoint; original e2e/root/lock/config/vendor unchanged; current label-port guard block and bundled identity assertion preserved.
- Read-only artifact/sidecar/public declaration and five shared peer checks: PASS. Shared installed Composition remains 0.0.8.

Exact executed scoped lint command:

```sh
node_modules/.bin/eslint \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/compositions/AudioTrack.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.tsx \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/VisualClip.tsx \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/playerEvaluation.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.ts \
  --report-unused-disable-directives --max-warnings 0
```

**Intentionally UNRUN here:** all Vitest/runtime tests requiring 0.0.10, package-resolution test, project tsc/build, full suite, localhost/browser/live tests. No shim or mock substitutes for missing 0.0.10 exports. Historical reports (Viewing 291 tests/17 files under 0.0.10; initial-projector 360 tests under 0.0.8) are predecessor evidence only, not results for this composed tree.

After root adoption, run the changed existing test files plus `RemotionPreview.test.tsx`, `useVideoEditorPreviewComposition.test.tsx`, `useTimelineCommit.test.tsx`, the command session/label/opaque-draft neighbors and package-resolution/shared-peer lane against the actual 0.0.10 installation. Recheck original three-products, mixed opaque recovery, restore and label browser journeys through the central test service; do not run browsers locally. Serialize project typecheck/build per current orchestrator policy, and use central service for any full or socket/browser suite, at most one final full request on the finished tree. Preserve original assertions and classify failures rather than adding skip/fails markers.

Actual Player/export frame and audio parity, including independent planted picture and audio mismatches, remains OPEN. Source adoption, endpoint media conformance and package checks do not prove this gate. The source candidate cannot be called merge-ready until the manager completes the root batch, actual 0.0.10 targeted proof and real parity requirements.
