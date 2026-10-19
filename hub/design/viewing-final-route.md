# App final render route and transition compatibility

2026-10-19. Evidence/design only; PLAN decisions 5/9 and gate 6 apply. Product files, pins, vendors and integration worktrees are unchanged.

## Result and next bounded change

**The mounted Render button reaches the real Runtime task authority; the current frame harness deliberately bypasses it. The final render input still carries incoming App transitions into an outgoing Composition interface without translation. Do not retire the existing App host path yet.**

- **Source proven:** `TimelineRenderControls` → chrome `startRender` → `useRenderState.startAstridRender` → save barrier → catalog-backed `rendering.render` admission → Runtime freezes the canonical closure → generic host materializes its CAS snapshot → Agent `RenderService` → `rendering.remotion` → public `TimelineComposition`. Scoped ordinary media also uses this task path; old router-header comments describe an earlier split.
- **Executed:** original worker's six existing suites: **137 passed**. Final scratch probes: **20 passed** (6 base-host, 6 current-host, 8 public-route cases). These are unit/DOM/planner observations with mocked media/Remotion clocks, not rendered pixels or recorded sound.
- **Counterexample:** `[a@0,b@1(transition=fade/.4s)]`, 30 fps, reaches the local payload unchanged. Public `prepareCompositionScene` gives neither clip a ramp; adding `c@2` makes **c** fade instead of b. Explicitly moving b's declaration to a and adding `incomingPolicy:'preroll-crossfade'` fixes only the fitting adjacent case. First clips, gaps, substantial overlaps, oversized fades and legacy endpoint mounts remain different (table below).
- **Smallest harness PR:** adapt the existing frame spec to `DirectHarness` plus the existing real generic pack-host bootstrap, use a real canonical/media fixture, remove `localBrowserRender=1`, click the same mounted button, and compare captured Player frames with its downloaded task output. Reuse capture/comparator helpers and one admitted closure. Do not add a fake render handler, invoke a render CLI as the test oracle, or introduce another renderer. App owns spec/fixture/door wiring; Agent owns launcher/readiness setup; Runtime owns canonical admission/readback. Run centrally only after manager scheduling.
- **Smallest semantic correction recommended for review:** extend the existing public planner's explicit App compatibility policy to consume clip-owned incoming declarations, including a first clip and nonadjacent/oversized windows, plus explicit legacy/canonical mount-end behavior. Keep all calculations in Composition and let both hosts supply the same policy. A declaration shuffle in App's local payload alone cannot fix Runtime-owned render bytes. Preserve omitted-policy own-span/clamped-clock behavior and half-open intervals. No correction is implemented here.

**Not proven:** mounted App → real generic host → final MP4 on this fixture, audiovisual parity, either planted parity failure, or a 0.0.9 consumer migration. Separate CPU qualification completed **8 passed in 137.83s**; it does not close those gaps. No rerender is needed for this report.

## Evidence appendix: pinned sources

| Item | Exact identity |
| --- | --- |
| This worktree / original unit-test App base | `c7a98922e3c6835b7a114e30c74bf495936f982f` (`hub/tl/vw-m3-app-adapter-batch`) |
| Current-host source snapshot used by original probes | App `85be65a0a6fcf5dbf3575d95fecfdc445e2edc02` |
| Agent inspected | `4ffbb8b081a57eb5f6d8962c30d02b30660491ae` |
| Runtime inspected | `ff0ae58daf1f5f8b89f3e5ad27d0c864f962f243` |
| Composition integration source, not the candidate probe | `7aa384a9f3c815f78ce88ff9b47de5adee7bf34a` |
| Public candidate probed | Composition `63ab6e0bca736a725d2bb0f056596a35f0a0c7d1`, version `0.0.9`; scene-guards artifact SHA256 `bd2c33095e54b1bb80a2b20b2ec21b6fdd8019a8d625150966672902ea69ff52` |
| Current App/Agent 0.0.8 tarball bytes | Both SHA256 `93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa` |
| Earlier repaired frame harness inspected | App worker `vw-m3-frame-fixture-restart`, commit `c16ca3090e136e9bad5541b0b27e2c3154c2928a` |

Original evidence is preserved under `workers/vw-m3-app-route-contract/probes/` and its `log.txt`; no original files were overwritten. The 0.0.9 config aliases only the artifact's declared public exports, not Composition source. `CurrentVisualClip.tsx` is the original worker's read-only-source snapshot of `85be65a0a`, with imports redirected for the scratch runner. The route/projection files have no changes between the two App pins relevant to this trace; current `85be65a0a` removed the partial Player adapter and retains the native wrapper. Neither pin was checked out over another worker.

### Mounted action and actual wire request

App paths/lines at the listed base (also inspected at `85be65a0a`):

1. `components/TimelineRenderControls.tsx:56` calls `chrome.startRender()`; `hooks/useTimelineState.ts:680` wires render state into the editor. `hooks/useRenderState.ts:1033` routes the action and `:1135` prefers managed admission for a scoped editor even when the shape router calls it browser-renderable. `:278` reads the explicit browser-proof URL flag.
2. `useRenderState.ts:838` requires project/timeline scope and a durable `flushPendingSave()` returning a positive acknowledged version. It builds the local payload at `:900`, admits at `:925`, then polls the same Runtime task and reads its result. No availability or render failure silently falls back once scoped admission is attempted.
3. `lib/renderRouter.ts:854` locally calls output projection then sequence materialization (`:861`, `:889`). **This local `payload.timeline` is not posted as render authority.** `enqueueAstridRuntimeRenderTimeline` (`:960`) reads `rendering.render` from the ready capability catalog, takes its definition digest/storage estimates, and calls the common task-admission client. Normal media/effects select `rendering.remotion`; live-scene selection has a separate explicit threejs branch (`:675`).

The real request shape is:

```ts
{
  project: projectId,
  capability_id: catalog.capability_id, // rendering.render
  capability_digest: catalog.definition_digest,
  schema_version: '1',
  input_object_ids: [], // Runtime derives the complete closure's managed inputs
  spec: {
    family: 'rendering.render',
    params: {
      timeline_ref: timelineId,
      expected_version: acknowledgedVersion,
      selector: 'rendering.remotion',
      output_name: filename,
      // Present when canonicalComposition metadata is available:
      canonical_project_id, canonical_parent_document_id,
      canonical_head_revision_id, canonical_occurrence_ids,
    },
    output_policy: {format: 'mp4', destination: 'download', filename},
  },
  storage_estimate: {scratch_bytes: catalog.estimated_scratch_bytes,
                     output_bytes: catalog.estimated_output_bytes},
  settlement_effect: {},
}
```

The request uses the existing per-export operation/idempotency identity (`renderRouter.ts:925`). A browser fixture must exercise this client and door, rather than manufacture its own digest or task output.

Runtime `runtime_protocol/store.py:1693` freezes managed render inputs, refuses caller-supplied snapshot/document paths, loads the current canonical parent with content-integrity validation (`:1784`), and follows its pinned shot/internal revisions via `load_closure`/`admit_closure`. At `:1816` it validates **all supplied canonical project/document/head/occurrence metadata**, then checks `expected_version` and returns the frozen config/registry plus authority (`:1935`). The authority carries parent revision/content digest, dependency digests, snapshot digest and object IDs. Subsequent rendering uses this snapshot, not mutable child heads.

**Correction to earlier design prose:** `design/viewing.md:149` says no canonical-head guard was found. Runtime `ff0ae58` now has that guard. Sending the field without checking readback still is not end-to-end evidence; the harness should assert the admitted authority matches the displayed fixture closure and rejects a changed head.

Agent `astrid/core/execution/generic_host.py:6620` hydrates and hashes the CAS snapshot, then `:6713` writes attempt-local `timeline.json`/registry and materializes authorized media. `astrid/packs/rendering/pack.yaml:1021`/`:1045` declares the actual `rendering.render` child:

```text
{python_exec} -m astrid.packs.rendering.actions.render.run
  --timeline {timeline} --assets {assets_registry} --out {out}/{output_name}
  --selector rendering.remotion --timeline-authority {timeline_authority}
  [other admitted optional input flags]
```

`actions/render/run.py:472` creates the `RenderRequest`, `:493` calls `RenderService.render`; the Remotion backend (`rendering/renderers/remotion/run.py:1196`) runs the provisioned Node/Remotion CLI with `render TimelineComposition --props ... --output ... --concurrency=1 --bundle-cache=false`. `remotion/src/Root.tsx` imports the public package and supplies host registries/fonts. This internal command is the production executor invocation, **not** a proposed test-side CLI oracle. The separate legacy `task_adapter.py` is not the common task path traced above.

### Bootstrap reuse and smallest real harness PR

Existing real Runtime startup is in App `tests/e2e/local/support/harness.ts:471`. Its effective commands (templates from source, **not executed here**) are:

```sh
PYTHONPATH="$RUNTIME_CHECKOUT:$ASTRID_CHECKOUT" "$PYTHON" -m runtime_protocol.cli create \
  --root "$REALM_DIR" --display-name 'Direct Journey'
PYTHONPATH="$RUNTIME_CHECKOUT:$ASTRID_CHECKOUT" "$PYTHON" -m runtime_protocol.cli start \
  --root "$REALM_DIR" --support-root "$SUPPORT_DIR" --port 0 --display-name 'Direct Journey' \
  --door-origin "$APP_ORIGIN" --door-port "$DOOR_PORT" \
  --door-credential-file "$PRODUCT_CREDENTIAL_PATH" --door-audit-log "$AUDIT_PATH" \
  --authoring-profile astrid
```

Reuse the harness's real provisioning, authoring restart, discovery, App origin/credential and managed-media APIs. `AstridCli.host()` (`support/astrid.ts:268`) currently starts `astrid.core.dev.cross_client host`; that code registers **f2.marker**, not rendering. It cannot qualify export. Use existing `astrid.sdk.host_bootstrap.ensure_pack_host` and its launcher-owned source/boot handoff instead, with the real `astrid-pack-host` credential/scopes. Discovery alone lacks some launcher source/boot fields: add a narrow harness setup bridge owned by Agent, reusing the existing bootstrap rather than fabricating them or launching against an ambient realm.

The existing launcher (`host_bootstrap.py:1548`) starts:

```text
{host_python} -m astrid.core.execution.generic_host run
  --pack-root {source}/astrid/packs --runtime-endpoint {endpoint}
  --runtime-discovery-file {support}/discovery.json --credential-file {worker_file}
  --executor-id astrid-pack-host --ready-file {ready_file} --support-root {support}
  --source-checkout {source} --source-checkout-digest {source_digest}
  --source-closure-digest {closure_digest} --runtime-instance-id {instance}
  --register --source-inventory-identity {inventory_identity}
  --boot-manifest-path {manifest} --boot-manifest-hash {hash}
  --capability-matrix {source}/config/astrid-beta-capabilities.json
  [existing additional managed pack roots / validation-launch flag]
```

Retain these existing launch checks. The matrix marks `rendering.render` required, `requires_remotion:true`, resource `render`, binaries Node/ffmpeg (`config/astrid-beta-capabilities.json:807`). Host setup resolves the concrete Remotion project, Node and Python schema root (`host_bootstrap.py:453`), then runs its existing render validation. The provisioned browser selection is `ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`; no installation, full-Chrome fallback or independent renderer is needed. Require a ready catalog entry with the real definition digest and fail the harness if that capability is unavailable.

The existing spec at `c16ca309` (`tests/e2e/timeline/player-export-frame-parity.spec.ts:30`) uses `localBrowserRender:'1'`, fake Runtime reset/publication and already clicks the actual Render button. Keep its Player seek/readiness/capture, export decoder and strict RGB comparator. Replace only fixture publication and environment authority with the real APIs, remove the flag, and let the existing UI polling/download complete. Record admitted task ID/closure and output provenance, media/fonts/package/tool versions once per run; assert the fixture parent/shot/internal pins and admitted snapshot stay identical before and after the action. Use the exact same pinned tarball bytes on both consumers. Candidate 0.0.9 is uninstalled/unqualified here; pin changes remain owner-scheduled after M1.

The first PR can prove one ordinary-media positive round trip and its picture-only planted mismatch without changing product semantics. Retain original transition/other behavior expectations for subsequent coverage; unresolved mismatches remain failures or the prescribed requirement-linked strict expected failures. Audio capture/positive comparison and its independent gain negative control remain required for gate 6. Do not claim this smaller harness PR alone finishes that gate.

### Incoming/outgoing translation and exact boundary observations

`data/timelineOutputProjection.ts:90` filters output tracks/clips without rewriting transitions. `sequences/materialize.ts:101` substitutes sequence params and spreads the rest unchanged. `data/shotCompositionProjection.ts:416` explicitly retains the child transition; `:424` adds canonical timing bounds. Runtime's independently authoritative expansion also deep-copies the transition (`runtime_protocol/visual_seam.py:178`, `:210`), adjusts position/clip length and adds canonical occurrence timing. Its incoming-transition seam predicate (`:357`) validates a topology; it does not transpose declarations for Composition.

Composition candidate `TimelineComposition.tsx:174`/`:184` reads `fromClip.transition`, creates outgoing declarations, and passes them to the common track planner. `lib/transition-spans.ts:74` requires incoming start in `[outEnd-1,outEnd]` and `0<T<=min(outDuration,inDuration)`. The opt-in changes incoming content/opacity only after those checks; first/gap/oversized transitions cannot become active through it. Default `fade` is a dip with outgoing fade-out; opt-in turns it into an incoming-only ramp. `lib/transitions.tsx:38` accepts bundled ID `cross-fade`, while untranslated App alias `crossfade` throws when resolved. The App public declaration helper already knows aliases; direct final Composition resolution does not perform that App adapter step.

For the executed fixtures below, fps=30, outgoing a has own span `[0,30)`, incoming b duration=30 frames. `T=12` unless noted. Host results are identical in the base wrapper's retained host branch and the `85be65a0a` snapshot. These are mounted intervals; a zero-opacity mounted layer need not produce a visible pixel.

| Case | Actual App host b mount / midpoint | Candidate public result after an explicit outgoing declaration with opt-in |
| --- | --- | --- |
| Adjacent b starts 30 | `[18,61)`, frame 24 opacity .5, local/content frame 6; frame 60 mounted, 61 absent | `[18,60)`, frame 24 opacity .5, outgoing stays 1; frame 60 absent |
| First b starts 60, no predecessor | `[60,91)`, frame 66 opacity .5, local frame 6; frame 90 mounted, 91 absent | No boundary/declaration slot; own `[60,90)` with no transition |
| Gap: b starts 60 after a ends 30 | `[48,91)`, frame 54 opacity .5, local frame 6; frame 90 mounted, 91 absent | Pair rejected by planner; b own `[60,90)`, no ramp |
| Overlap: b starts 15 | `[3,46)`, frame 9 opacity .5, local frame 6; frame 45 mounted, 46 absent | Pair rejected by planner; b own `[15,45)`, no ramp |
| Oversized: b starts 30, T=60 | Start clamps to 0 but duration stays 91: `[0,91)`, frame 30 opacity .5, local frame 30 | Pair rejected (`T>30`); b own `[30,60)`, no ramp |
| One-frame overlap: b starts 29 | Source formula gives start 17; not separately mounted in host probes | Public planner accepts, anchors to outgoing end 30, b starts 18; no claim of equivalence |

The oversized row records actual existing behavior, not a suggested new default. In `85be65a0a:compositions/VisualClip.tsx:640`, host `from=max(0,round(at*fps)-T)` uses T only when a predecessor exists; legacy duration is own duration+T+1. Inner `:557` fades the incoming visual from local frame 0 even without a predecessor. It advances video/content from this draw origin. Unknown/custom transition implementations must retain their current host behavior until publicly supported.

For canonical `occurrenceStartMs=1000,occurrenceDurationMs=1000`, host b ends at **60 excluded**, as the executed 59/60 probe asserts. `VisualClip.tsx:648` caps transition mounts at occurrence end and removes the legacy extra endpoint. In the same probe an ordinary legacy cut b@30 still mounts at frame 60 (`duration=31`). Thus even **no-transition legacy cuts** cannot be assumed equivalent to public own-span mounts. Candidate default queries remain half-open; do not change that default to match the old overlap workaround.

Recommended public correction scope: one explicit App host policy in the existing public preparation path, consumed by actual render and scene/track queries, that (a) identifies incoming ownership and aliases, (b) computes from the incoming clip's start even for first/gap/overlap/oversized cases, (c) advances its content while leaving gain untouched, and (d) applies explicit legacy endpoint versus canonical occurrence caps. API spelling belongs to the existing Composition owner; no new registry/framework is warranted. The current `preroll-crossfade` outgoing-pair policy stays valid for its stated cases. Keep the native path until public behavioral and real pixel/audio tests demonstrate equivalence; do not put a private timing mirror in the App adapter or Runtime.

### Executed commands and limits

Original worker cwd: `/home/user/work/wt/vw-m3-app-route-contract`. In the following exact commands, `ORCH` expands to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch` and `P=$ORCH/workers/vw-m3-app-route-contract/probes`.

```sh
node_modules/.bin/vitest run --config "$P/vitest-008.config.mjs" \
  src/tools/video-editor/lib/renderRouter.test.tsx \
  src/tools/video-editor/sequences/materialize.test.ts \
  src/tools/video-editor/data/timelineOutputProjection.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx > "$P/host-unit.log" 2>&1
# exit 0; 6 files, 137 passed, 5.70s

node_modules/.bin/vitest run --config "$P/vitest-009.config.mjs" \
  "$P/host-boundaries.test.tsx" "$P/current-host-boundaries.test.tsx" \
  "$P/public-route.test.tsx" > "$P/boundaries.log" 2>&1
# final exit 0; 3 files, 20 passed, 3.90s
```

Command counts: original worker **5 Vitest invocations**: one existing-test run and four evolving scratch-probe runs. The first probe run had one import/setup failure (`@testing-library/react` resolution from outside the repo; 7 public tests passed). The scratch import was bound to the existing installed package; subsequent probe invocations exited 0, ending at the 20-test run above. No product test expectations were weakened. Final log replaces earlier scratch output, but the original worker transcript preserves the failure and intermediate commands. These two final commands are the evidence totals; intermediate reruns are not additional independent coverage.

Resumed worker: **0 test/build/browser/render/install/full-suite commands and 0 central test submissions**. Reused existing evidence under the recovery/quiet instruction. Read-only source verification and report checks only. `git diff --check` exits 0 and the worktree has no tracked changes. No lint/typecheck is claimed for this documentation-only task.

Separately inspected central result: `tests/vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223448-19007/{summary,log.txt,snap,ext}`, exit 0, **8 passed in 137.83s**, Agent snapshot tree `d3508cb5158c80b34e90e6de8b5430423e3a692f`; external tuple Runtime `ff0ae58`, App `85be65a0a`, Composition integration `7aa384a9`. Its command was `flock -x /tmp/timeline-viewing-browser.lock "$ORCH/workers/vw-m3-cpu-profile-proof/setup-run.sh"`. This is a separate CPU backend qualification, not an App task-route/0.0.9/player comparison. No old CPU result was rerun or removed.
