# ORCHREPORT — vw-m3-app-delivered-theme-seam

**Audit and UNAPPLIED mounted prototype complete. No repository changes. Actual ordinary-preview theme delivery is still missing upstream.** FINAL PLAN06:07 is authoritative: existing Agent export theme wins, App implicit preview changes intentionally, explicit themes survive, no copied policy literals. No public DEFAULT_THEME, authored config/film, package/pin, data/loader/provider, owner-film list, or earlier rejected patch was changed.

## Source and delivery finding

Assigned App/integration base: `b8064ecf16c97a579d0bf945cef5df15a2085185`, still installed public0.0.8. Audited public10/root source: `d48b13beb2f2919d3372f4221154c13e6426ef03`, plus independent accepted canvas ground line `eeddb47c0c824a6639a310c9a6c4f70631f64ff2`. Used only frozen git reads and private source snapshots; neither candidate was checked out/applied in any repo. Public10 artifact: 58,008 bytes, SHA256 `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`; all 77 extracted files match archive bytes after tests.

Agent source: `384918908aa8c75229c2b6ccdd8fda03b7ce24a1`. Existing `_resolved_theme_for_render(timeline_path, runtime_theme_path)` in `astrid/packs/rendering/shared/rendering_backend/__init__.py:89` returns `{id, visual}` using builtin or materialized runtime theme plus authored overrides. Export `astrid/packs/rendering/rendering/renderers/remotion/run.py:1103` puts this into `merged_props.theme`; Root passes props into public TimelineComposition and builds registries from that theme. The props JSON is attempt-private and deleted at line1362. It is not an ordinary-preview readable artifact.

| Existing boundary | Actual contents and consequence |
| --- | --- |
| App `src/integrations/runtime/dataProvider.ts:1263` `readTimelineInOrder` | Reads scoped canonical inspection + immutable parent revision.payload; returns config/clips, registry and head. No resolved theme or prepared-props reference. |
| `loadTimeline` at line822 / `data/DataProvider.ts` `LoadedTimeline` | Config, numeric configVersion, optional head and bundle. No resolved theme. Authored theme/overrides are not a full resolved value. |
| `lib/timeline-data.ts` `TimelineData` | Config/resolvedConfig, registry, output, factual editProjection, head and typed data. No theme result. `buildTimelineData` resolves assets/config, not Agent themes. |
| `data/shotCompositionProjection.ts:575` | Copies authored base theme/overrides into projected config, not Agent resolution. Immutable graph/candidate must be selected before resolving/delivering theme. |
| `components/PreviewPanel/useVideoEditorPreviewComposition.ts` | Selects command projection when complete; otherwise cached canonical graph/error; local canonicalDraft takes precedence over server canonicalComposition. Returns source/status/config/error only. |
| `useVideoEditorPreviewSurface.tsx` | Chooses factual editProjection/canonical draft/head labels for selected config, compiles transitions, passes config/revision to RemotionPreview. No Agent-theme input. Existing legacy saveStatus fallback remains at lines93–112; this prototype adds no inference and does not expand that fallback. |
| `runtime/astrid-element-host.ts` | Component/sequence/capability/readiness host. No prepared Root props/theme read. |
| Generic Runtime document/object reads | Client `getDocument`, `getProjectObjectLocation`, `getObject`; provider `projectObjects.read` checks project/object identity and digest/size. These can read an existing referenced object, but no resolved-theme document/object/descriptor producer or consumer exists. No new object naming convention or getter is invented. |

The SDK source/capture result also lacks theme. The reviewed inactive scene transport consumes supplied Root props and returns frame rows; it cannot supply the missing value. Agent peer independently confirms all of these gaps in `handoff-vw-m3-resolved-theme-common-source-ORCHREPORT.md` and DESIGN.md.

## Smallest proposed seam and owners

Agent source/materialization owner must retain/factor the already-computed whole theme beside the **same exact prepared config**, within the existing export/source preparation lifetime. A local result member `theme: Theme` (or the existing `props.theme` when returning actual prepared props) is sufficient at that boundary. **There is no currently returned preparation result/browser read connecting that value to App.** App data/loader/provider owner must approve how an existing authorized read/result carries it before App source selection can use it. This report proposes no new Runtime method, wire DTO, provider, endpoint, scene operation, persistence authority, or config field.

At the App local boundary, use the existing source selection and mailbox:

`same prepared config + full theme + source revision/candidate` → `selected preview config + factual previewRevision` → `RemotionPreview PreviewDelivery {config, compiledTransitions, resolvedTheme, revision, generation}` → `Player.inputProps` → `TimelineRenderer` canvas + existing ThemeProvider/component theme props.

Pair project/timeline, immutable head or exact local candidate/generation, and host/materialization source before delivery. A server head is never proof that a displayed local suffix is committed. A failed request for R2 leaves the cached R1 config/theme/label together; unavailableTarget describes the failed request. New theme identity participates in generation even when config identity stays fixed; metadata-only notices never advance theme/config/compiledTransitions. The existing keyed surface remount scopes delivery to project/timeline/source/attachment; the producer must discard stale async results before supplying props. Theme type/shape alone establishes no source authority. Do not persist resolvedTheme into TimelineConfig, commands, outbox, or a film.

The Agent peer's narrower alternative is a generated default-only JSON resource from the native resolver, transported through the existing bound `@astrid` Tool build-source read and native regeneration check. Its manifest inclusion/build invocation/release pairing still need owner implementation. A frozen handoff JSON is test evidence only. This would cover implicit builtin only, not arbitrary runtime pins or per-config merges.

## Bounded consumer prototype

`handoff-vw-m3-app-delivered-theme-seam-UNAPPLIED.patch` touches only RemotionPreview and TimelineRenderer, against public10+d48 plus the independent eeddb47c ground line. It does not include the ground line itself. It adds optional public `Theme` local props, schedules the whole value with config/compiledTransitions/revision, includes theme in metadata guards, and uses the exact delivered value for canvas and existing component theme props. A supplied value is already fully resolved: no second merge, slug lookup, or copied default. No prop means existing local fallback remains; **this inactive proposal does not yet change ordinary App implicit preview to the final policy**.

Seven new mounted cases use real Agent outputs, including the peer's actual implicit and full authored visual results. Complete RuntimeTheme comparisons use the real public10 ThemeProvider/useTheme. Tests cover paused delivery, theme-only arrival, playing newest-pair selection, M1 metadata-only unavailable/recovery, implicit canvas+component delivery and complete authored visual preservation without config writes. Tests preserve original behaviors and add no skip/xfail/it.fails. The old partial ThemeProvider test mock retained stale `.visual` while changing aliases; replacing it with the actual public provider made whole-value assertions meaningful. composeAnimations and unrelated media/Player boundaries retain their existing test doubles.

**Additional evaluator limitation found:** public10 `compositions/playerEvaluation.ts::compilePlayerTransitions` still resolves its theme locally, and `preparePlayerTrack` passes `resolveTimelineRenderTheme({})` into `prepareCompositionScene`. These existing call arguments must consume the same source-resolved value when actual production wiring is authorized. This 2-file prototype proves canvas/element delivery, not evaluator-wide theme parity or theme-dependent transitions. Nested shot inheritance/merges, installed custom theme pins and runtime-host deployment pairing remain unqualified. No tests claim otherwise.

## Exact verification

All generated source overlays, scripts, patches and logs are outside the repository. Paths below expand to the actual commands:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
D=$ORCH/design
W=$ORCH/workers/vw-m3-app-delivered-theme-seam
cd "$W/offline-app"

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python "$D/handoff-vw-m3-app-delivered-theme-seam-source.py"
# PASS. Actual native resolver, implicit + authored color override; hashes recorded.

/home/user/work/app/node_modules/.bin/vitest run --config "$D/handoff-vw-m3-app-delivered-theme-seam-vitest.config.mjs" src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
# PASS: 132 tests / 7 files, 10.64s; final-targeted.log. No filtered/skipped cases.

/home/user/work/app/node_modules/.bin/tsc --noEmit -p "$D/handoff-vw-m3-app-delivered-theme-seam-tsconfig.json" --pretty false
# PASS: actual five native outputs assign to public10 Theme/RuntimeTheme; types.log.
# This is a bounded public-type probe, not project typecheck.

/home/user/work/app/node_modules/.bin/eslint --config /home/user/work/wt/vw-m3-app-delivered-theme-seam/eslint.config.js src/tools/video-editor/compositions/TimelineRenderer.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx --max-warnings 0
# PASS, no diagnostics; lint.log.

python "$D/handoff-vw-m3-app-delivered-theme-seam-postflight.py"
# PASS: unapplied patch whitespace/applicability, restored product exactly matches
# published patch, public10 77/77 bytes unchanged, Agent source hashes match frozen
# git objects, assigned worktree clean. postflight.json.

cd /home/user/work/wt/vw-m3-app-delivered-theme-seam
git diff --check
git status --short
# PASS; status empty.
```

Red-before: restored the two external product files to public10+ground baseline, ran the same first two suites with `-t 'actual Agent implicit|complete Agent explicit|full Agent authored|defers config, actual theme|changes theme on the same|keeps theme while an M1|newest playing config and resolved'`, then restored proposed files in `finally`. Exit1: **6 failed / 1 passed / 59 name-filtered**; red.log. The explicit existing local-theme case already passed. Earlier setup failures involved missing snapshot tsconfig/vendor/virtual admissions/@astrid aliases; two new whole-value assertions exposed the partial test mock described above (91pass/2fail plus two setup errors). They were fixed in the external harness; no product fallback/refusal or old behavior expectation changed. Earlier 65pass,117pass and132pass/11.16s runs are superseded by final132pass/10.64s.

Peer source worktree was recycled after its completion. To avoid a stale path, final tests reran against our own frozen Agent384918 git-archive snapshot with matching native resolver hashes; no other worktree was changed. Exact public10 distribution aliases use the immutable package bytes, not a package source shim. jsdom mounting doubles Player/media and empty admission discovery; no browser/renderer, SSR, sockets, source admission, full suite, install or network. No actual Player/export pixel/audio, custom runtime themes or nested-merge parity claim.

## Handoff and next actions

All flat artifacts live in the absolute `$D` directory above with prefix `handoff-vw-m3-app-delivered-theme-seam-`: ORCHREPORT.md, COORDINATION.md, UNAPPLIED.patch, UNAPPLIED-tests.patch, both modified test files, source.json/source.py, prepare.py, prototype.py, vitest.config.mjs, type-probe.ts/tsconfig.json/types.log, targeted.log, final-targeted.log, red.log, setup-and-mock-diagnostics.log, lint.log, postflight.py/postflight.json. Peer common-source values/design/report remain their own flat artifacts. The source JSONs are external generated test inputs, never proposed static per-film product authority.

Reproduce after cleanup: run prepare.py, prototype.py, source.py with PYTHONPATH=$W/agent-source; copy the two flat test files back to their original relative source paths and peer common-source-values.json to `$W/offline-app/agent-theme-common.json`, then run the commands above. No dependency install is needed. Temporary caches, patch-check and source snapshots are removed after verification; flat reproducible artifacts remain.

Recommended: Agent source owner + App owner choose the existing-read connection or bounded implicit-only generated resource, retaining source-release pairing. Then wire that result at the actual selected config boundary, thread it through the existing evaluator calls too, and qualify explicit runtime pins/nested merges before claiming common-theme parity. Keep M1 factual labels/mailbox behavior; address legacy saveStatus inference separately with its owner. The manager records the intended implicit-preview change in owner-film differences. No policy disagreement and no permission request; the bounded audit is complete, while actual producer/read implementation remains the explicit next prerequisite.
