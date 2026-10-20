**HOLD — independent refreshed-root source review complete.** The eight new mobile expected failures remain rejected. Independently, two ordinary counterexamples expose a render-facing source-clock defect and a desktop label-display defect. Do not treat the preceding worker’s scoped green counts as approval of this entire root. No product/assertion edit, mobile decision, KEEP request, integration change, Git mutation, install, full/build/browser/socket run, or project typecheck was made.

**Exact reviewed source.** Compared `667498cc49b4ec2b1ccd3a515eb87311c5126c93` (tree `74d6c8033b1e006e8dbd4accc361b4e1288093e9`) with frozen `35ebae007d848ff22d8da89461bdb66efc93472f` (tree `d15621214a629e070ad4df3c0252cddae4f07060`). Read PLAN first, `app-refresh-public12-compiler-root-port.md`, and `app-refresh-main-overlap-review.md`. This review worktree remains at `35dbb0eb12d75dc2c1becf7a9d8ac914758c05c7`; its source was not substituted for the candidate. Tests used a private Git-archive export of the frozen candidate and read-only `/tmp/app-coherent-deps12/node_modules`. All 5,797 regular exported source files remained byte-identical afterward. The export and temporary dependency links are removed after review; `notes/prepare-source.py` reproduces them without an install.

**Independent source findings — exact candidate lines.**

1. **P1: the rendering input is already clamped before the public compiler sees it.** `hooks/useTimelineCommandSession.ts:82` and `data/canonicalCompositionState.ts:61` call `projectCanonicalComposition` with the default clamp. `data/shotCompositionProjection.ts:440–449` shortens source `to`/`hold`; `compositions/playerEvaluation.ts:20–23` then uses that shortened duration, and `compositions/VisualClip.tsx:301` evaluates the authored fade on it. The external ordinary counterexample uses the existing prepared-shot fixture with a five-second image, one-second `fade_out`, and four-second occurrence cap. At frame 105 / 30fps the raw public clock returns opacity **1**, while the actual default projection returns **0.5**. Both public draw plans exclude frame 120 correctly: the error is moving the authored fade earlier, not an off-by-one end. This is a synthetic projector/evaluator counterexample, not decoded pixels or Runtime acceptance. The clamp predates this port; its unresolved composition with the new evaluator violates the requested raw rendering input boundary. The current regression at `TimelineRenderer.sequence.test.tsx:302` starts from a manually supplied unclamped config and therefore misses the production callers.

   Smallest follow-up: preserve raw source timing on the rendering/preview projection into the existing public compiler, which already accepts the occurrence end cap. Keep the editor/read projection’s existing clamped-behavior assertions; do not rewrite `shotCompositionProjection.test.ts:481` to erase that existing behavior. Add the end-to-end projection-to-evaluator regression beside the existing suite. No new timing policy, local fade math, or authored timing rewrite is justified.

2. **P2: an untouched desktop focus session hides a remote rename after blur.** `components/TimelineEditor/TrackLabel.tsx:321–323` declines to clear the draft while the capture is active. If the label changes during that interval, `finishNameEdit` at `:343–356` clears only the capture/error, leaving `nameDraft` set. Its `[track.label]` effect has already run, so the old label remains indefinitely until another prop change or remount. The ordinary external test focuses “Original”, supplies “Remote”, and blurs without typing: no finish callback occurs, but the textbox still displays **Original** instead of **Remote**. This is independent of phone/tablet controls and of the eight known markers. Release the clean finished draft to current props while retaining genuinely dirty/refused input and its original capture; add this positive desktop case without weakening the existing refusal tests.

**Known mobile HOLD — no decision made here.** Candidate `TrackListRenderer.test.tsx:683` uses `it.fails` for three positive row cases on each of phone/tablet (six cases); `TimelineCanvas.test.tsx:2508` adds forwarding positives for both (two cases). `node scripts/quality/check-known-failures.mjs` exits **1**, reporting **3 authorized drag markers and 2 forbidden source sites**. The latter expand to the known eight cases; they are not eight new source sites. Original MAIN row/canvas assertions remain intact, including agent-only touch settings. Escalation 1013 must map NEW MAIN’s intentional phone/tablet behavior to the old unmerged c866 touch-capture requirements. The manager/owner must reconcile those requirements and tests explicitly before the guard can pass. Neither importing a mobile UI nor accepting/expanding failure markers nor rewriting positives into absence assertions is authorized by this review.

**Deletion closure and package findings.**

- The frozen diff has **163 paths**, not the brief’s 149; this matches the source worker’s final allowlist. It deletes **94 files**: **92 vendor files / 3,278 lines**, plus local `audioFade.ts` and its test. All 13 duplicate built-in implementation directories, the Composition source mirror and 2rp package shell are absent. Public tests resolve the default effect, six animations, two transitions and four bundled 2rp effects through normal registries; custom registry overrides and unknown-component diagnostics remain exercised. No replacement vendor evaluator or second theme constant was added in the changed product paths.
- The **six production/test bundler configurations covered by the package guard** resolve every public Composition subpath and shared peers to installed public modules; all seven guard checks pass. `package.json`/lock point to the same immutable public12 archive; layout-utils is available as a production dependency; old archives/unrelated vendors remain.
- **Residual cleanup, preexisting and outside those six guarded configs:** `examples/embed-demo/vite.config.ts:10–35` still looks for private `typescript/src` files and chooses committed theme/registry stubs when they are absent. Public12 ships only `dist`, so this example selects the stubs even with the package installed. `tests/e2e/fake-runtime/tsconfig.json:12` retains the retired workspace-animation alias and `launch.mjs:4` its stale comment. `supabase/functions/complete_task/deno.json:6–7` retains mappings into the deleted vendor trees. No live `complete_task` Composition import or fake-runtime workspace-animation import was found, so those two stale mappings are not claimed as a reproduced deployed failure. The unchanged embed example is an actual fallback configuration, but was not built. Do not claim repository-wide zero fallback/deletion closure; have the owners remove/reconcile these residuals before that M4 claim. These findings do not invalidate the narrower six-config resolution pass.

**Boundaries independently checked.**

- **Product size:** exactly **27 changed `src/` product paths**, excluding tests/support/fixtures/generated contracts/vendor source: **15,096 → 15,912 lines**, **+1,021/−205, net +816**. This is the changed-path census, not the whole App Timeline core or the four-repo target. Exact paths are in `notes/audit.json`.
- **Composition identity:** **58,444 bytes**, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; **all 77 regular archive members byte-equal installed files**. React/DOM 18.3.1 and Remotion/Player/media/layout-utils 4.0.509 match. Entire public `DEFAULT_THEME` equals read-only Agent `BUILTIN_DEFAULT_THEME`, including all nested values. Public-default, complete explicit visual theme, explicit 2rp, nested override and mutation-isolation tests pass. No App-local Agent default literal was introduced. This is source equality, not Agent package qualification.
- **Runtime pin:** only `runtime.lock.json` and its three normally generated TypeScript files change. All **13 locked files** equal the producer’s source bytes and hashes at **`94114269d1ce23ab3224d7eca5a85138ce2b5fed`**, and the normal producer-aware check passes. This is the affected **DEVELOPMENT-ONLY 0.2.9 producer**. Runtime P1 republication and the matching safe Agent/App pair remain required; byte equality confers no safe/current release or browser claim.
- **MAIN preservation:** **28 protected files byte-identical** to the refreshed base: provider/digest/two-reading boot, auth/App root, canonical URL/bootstrap metadata CAS, chat/proxy, render/admission/download cohort and tests, shell/mobile single portal and lifecycle tests, ShotEditor/raw-settings defense, save barrier, and provider client. Preview adds compiler/config/vector delivery to the existing deferred mailbox without restoring the old remount generation. `useTimelineState` exposes the existing command session ports; no download owner is reintroduced.
- **Label/outbox:** `trackLabelCapture.ts:36–46` uses existing recording primitives and complete original claims. `commitSession.ts:274–318` checks the displayed head/unique raw parent identity, retains the original typing basis and tests its guards against current bytes. The same outbox persists exact body/key before send; `pump(false)` at `:136`/`:238` blocks append-triggered retry of unknown A while retaining B. Explicit retry/recovery/flush remain. Rejected-prefix resolution is an owner-fenced transaction, and Keep is confined to one parent-label intent with no suffix; unknown results do not offer replacement. Real guarded conflicts retain local work. These are in-process transport/storage tests, not server rebase proof.
- **Initialization/provenance:** `useTimelineCommandSession.ts:64–68` validates scope/head, authoring closure validation precedes use, and `:99–111` pairs projection facts only after generation/local/head/clean checks. Disposal, delayed asset reads, observations, prior local/accepted projections and retained outbox basis are covered. Opaque roots, `__proto__`/constructor/prototype keys, explicit null/absence, ordered arrays, raw settings and transition revisions retain existing assertions. Undo emits `timeline.inverse` for the accepted publication (`commitSession.ts:468`), rather than rewinding accepted Runtime history. The test helper’s saved-document inverse is an in-process server stand-in, not real guarded undo evidence.
- **Gate 5:** TypeScript AST extraction confirms **all six migrated case bodies and 21 helper bodies** equal `04346844f^`; one case and one helper are added. This reference is the previously reviewed migrated journey, not the older pre-migration writer assertions. All original refreshed MAIN row/canvas assertions are preserved; **63 changed TS/TSX files parse**. Syntax parsing does not type-qualify NEW source.

**Exact commands and results.** All commands below ran against the exported frozen candidate. `N` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-refreshed-root-independent-review/notes`. The private config imports the unchanged repository config, uses its aliases, and sets cacheDir under `N`. No shared dependency/cache/venv mutation was requested. To reproduce after cleanup, first run `python "$N/prepare-source.py"`, then `cd "$N/source"`.

```sh
node node_modules/vitest/vitest.mjs run --config ../vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/AudioTrack.test.tsx \
  src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx \
  src/tools/video-editor/compositions/installed-themes.test.ts \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts
```

**PASS, exit 0: 13 files / 403 tests**, 41.25s. `notes/focused.log`.

```sh
node node_modules/vitest/vitest.mjs run --config ../vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx
```

**PASS, exit 0: 8 files / 169 tests**, 18.39s. `notes/neighbors.log`. Distinct existing-suite evidence totals **21 files / 572 passing tests**, no expected failures in these selections.

```sh
node node_modules/vitest/vitest.mjs run --config ../counterexamples.config.ts --configLoader=runner --no-cache --maxWorkers=1 ../counterexamples.test.tsx
node config/vite/timelineCompositionPackage.test.mjs
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime029-producer-source
node scripts/quality/check-known-failures.mjs
python "$N/audit.py"
node "$N/ast-audit.cjs"
git -C /home/user/work/wt/app-m3-refreshed-root-independent-review diff --check 667498cc49b4ec2b1ccd3a515eb87311c5126c93 35ebae007d848ff22d8da89461bdb66efc93472f
```

- External ordinary counterexamples: **RED, exit 1, 2/2 failed behavior assertions**, 3.08s; `notes/counterexamples.log`. No tracked tests or assertions were changed. An earlier runner attempt could not resolve the outside-root test library; an own-notes dependency link fixed resolution. A preliminary scene-layer opacity probe returned `null` for undeclared evidence and was corrected to use the actual public clip-opacity evaluator; only the final explicit 1-versus-0.5 result is claimed.
- Package guard: **PASS, exit 0, 7 checks**; `notes/package-guard.log`. Resolves build configurations; no build executed.
- Normal Runtime check: **PASS, exit 0**; `notes/runtime-check.log`.
- Failure-marker guard: **FAIL, exit 1**, exactly the known two forbidden sites; `notes/known-failures.log` / `notes/known-failures-explicit.log`.
- Independent census/artifact/pin/theme/protected-file audit and AST preservation/parse audit: **PASS, exit 0**; `notes/audit.{json,log}` and `notes/ast-audit.{json,log}`. The first AST helper hit this sandbox’s Node child-process EPERM; read-only Git input was supplied by Python before the successful AST-only run.
- Frozen diff whitespace check and final review-worktree status: **PASS**, no output/no changes. No build output or temporary files are left in the review worktree.

**Exact remaining holds / next steps.**

1. Source owner fixes the raw render-input clock and clean desktop draft defects with unchanged original expectations plus permanent focused regressions. This review makes neither edit.
2. Manager/owner resolves escalation 1013 and removes the unauthorized-marker condition through the agreed behavior mapping; the three original drag markers are the only existing authorization. Do not use the known eight failures to hide findings 1–2.
3. Owners close or explicitly scope the stale example/vendor bindings before claiming complete deletion/no fallback. The six supported config/package checks already pass.
4. Runtime republishes the safe producer, then owners adopt exact normal pins and freeze the matching Agent/public12/App tuple. Existing MAIN render scope/integrity follow-ups and local-counter result provenance remain separately open: `useRenderState.ts:864` still stores the local save number and `TimelineRenderControls.tsx:250` prints it. Those files are unchanged by this root; they are not new regressions attributed to the port.
5. Manager performs the final-tuple project typecheck at the instructed time, then separately authorized build/browser/current-pair/Gate 5 and real frame/PCM parity with planted mismatches. The single OLD-c866 project typecheck cannot qualify NEW source. **No full, build, project tsc, browser, socket, real Runtime acceptance, current release, or decoded audiovisual parity was run/requested here.**

No settled PLAN decision was changed. Nothing blocked completion of this independent review; candidate source/qualification remains HOLD for the conditions above. `DONE` records review completion only; no KEEP/merge approval is requested.
