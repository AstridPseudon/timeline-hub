# D08 current-root audit: no qualified deletion

No product or test changes. Base is App `0ea988bdd2907c876b82fd2620820e3fb6d6ea84`, the held public12 root. No deletion earned qualification in this audit; the authorized no-deletion fallback applies. This does not claim that future consumer adaptation is impossible. `exact.patch` and `filelist.txt` are intentionally empty.

Read PLAN, COMMON, viewing deletion ledger, current viewing INBOX through 11:54, and `design/viewing-main-image-cap-actual-reference.md`. The latter records physical MAIN opacity **0.5** at frame105 for the 5s image / fade1 / cap4 fixture. Nothing changes that reference or introduces raw-opacity1 expectations or renderConfig.

## Active callers and replacement gaps

- **Native fade math is already removed.** `compositions/playerEvaluation.ts:27` calls public `clipOpacity`; `VisualClip.tsx:301` uses that adapter for effects. Existing node: `playerEvaluation.test.ts::evaluates authored opacity and object/array fades on the native content clock`. Do not replay the older deletion. The no-effects `clip.opacity ?? 1` branch is active; replacing it wholesale with public clipOpacity also introduces public [0,1] normalization for inputs the current branch passes to CSS. This audit supplies no new behavior qualification for that change.
- **Host transition interpolation/timing is active.** `VisualClip.tsx:566` resolves the host catalog and invokes contributed progress/params or static CSS renderers; `VisualClipSequence` at :691 retains playing native/custom subtree clocks. `playerEvaluation.ts:95` shares only qualified silent-image boundaries in its fallback branch. Exact positive nodes: `VisualClip.test.tsx::passes transition progress and params to contributed renderer`, `::handles object-style renderer (static CSSProperties)`, and `VisualClip.evaluation.test.tsx::preserves the mounted image fade pair with outgoing opacity one and the legacy incoming clock` / `::retains the host path for video transitions without freezing or extracting its audio`. Public outgoing plans differ for the legacy fade/video cases. Public incoming vectors already serve qualified canonical tracks; treating every native fallback as canonical or replacing arbitrary host CSS contributions is not a qualified deletion.
- **Host identity guards are active.** `TimelineRenderer.tsx:1296` checks actual host/sequence/live/clip-type registrations before selecting native plans. Exact positive: `TimelineRenderer.sequence.test.tsx::retains host bounds and neighboring timing when an injected component overrides a compiled media name`. `playerEvaluation.test.ts::keeps undeclared custom and typed component internals unknown and present` protects unknown internals. Removing the guards substitutes native semantics for another registered owner.
- **Audio curves already use public evaluation.** `AudioTrack.tsx:353` compiles the public envelope and :362 evaluates `audioEnvelopeAt` with the authored/render offset. `AudioTrack.test.tsx::keeps boosted callbacks in authored time across occurrence bounds, trim and speed` protects this active callback. Public `applyAudioEnvelope` needs actual PCM source/backend integration; it is not a drop-in replacement for this Remotion volume callback. No audio policy or readiness changes made.
- **There is a genuine duplicate trim helper, outside ownership.** Definition: `lib/config-utils.ts:43`, matching public `evaluation.computeMediaTrim`. Active owned callers: `VisualClip.tsx:317` and `AudioTrack.tsx:295`. Original tests: `lib/config-utils.test.ts::omits trimAfter when source out is not greater than source in` and `::clamps invalid trim, speed, and volume values to safe playback props`. Changing the two imports alone would leave the duplicate definition; deleting it requires the helper owner's grant. No unowned file edited.
- **Preview metadata is an active candidate, not proven dead.** `components/PreviewPanel/RemotionPreview.tsx:282` aggregates independently rounded App-normalized durations on the delivered output projection. Public root `getTimelineDurationInFrames` exists, but direct raw inputs use public duration semantics (`speed ?? 1`, raw hold/trim); App's current helper uses `getConfigTimelineClipDuration` with hold-like classification, valid-trim and positive-speed sanitization. Preserve `RemotionPreview.test.tsx::parks a paused playhead on the last frame after a duration shrink without resuming` and `::excludes source video/audio and their extent without mutating the authored timeline`. A mapped-input replacement needs targeted clock/rounding/invalid-input qualification; this audit does not supply it. No MAIN helper reset or aggregate replacement claimed.
- **Marker lookup/effect-layer intervals remain active.** Public evaluation has no matching marker-color query for `AudioReactiveColour.test.tsx::keeps source-order tie behavior for duplicate frames`; EffectLayerSequence also owns provider snapshot dispatch and pass-through of children, not scene culling. Those features stay.

The companion replacement-test map gives one-line original-node -> existing public replacement / exact remaining gap entries. Every named test node above was inspected, **not executed**. Original positive assertions remain byte-identical; no refusal rewrite, skip or xfail.

## Checks actually run

From `/home/user/work/wt/vw-m3-d08-qualified-current-cut`:

```sh
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d08-qualified-current-cut-audit.py
git diff --check
git status --porcelain
```

All exit0. Archive SHA256 is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; version0.0.12 and77 regular members verified in memory. Static public declaration checks pass. All43 tracked composition files equal HEAD, and the entire worktree is clean. No archive extraction, Node public evaluator execution, installed-package/current-API qualification, browser, render, socket, full suite, install, network or shared dependency/cache write. A standalone arithmetic sampling probe ran via `node --input-type=module -`; it found no rounding difference for the sampled existing-adapter round trips and establishes no general clock equivalence or behavior-test pass.

**Behavior tests: none run.** No source delta was proposed. No physical parity, audio parity, current API, M3, Gate6 or owner-pair activation claim. The clean f816 peer graph was inspected read-only but not used to execute tests; polluted App/scene graphs were not used for environment qualification.

## Recommendation and handoff

Keep the unqualified paths. If pursuing the small trim deletion, obtain the `lib/config-utils.ts` helper-owner grant, replace both owned callers with public computeMediaTrim, delete the helper, and run the original trim tests plus the visual/video/audio clock tests against the exact public12 package. Alternatively qualify the preview metadata candidate with the same delivered output projection and the existing native-clock adapter before deleting its aggregate. Both are future owner decisions, not permission inferred by this audit.

No external blocker is asserted: the assigned fallback audit is complete. The manager owns ledger updates and any gated App port. Harness commit-msg is prepared; there are no product changes to commit. No merge/publish performed.

Flat artifacts: `handoff-vw-m3-d08-qualified-current-cut-REPORT.md`, `-exact.patch` (empty), `-replacement-test-map.txt`, `-filelist.txt` (empty), and `-audit.py`, all under this report's absolute design directory.
