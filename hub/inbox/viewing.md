
## 2026-10-19 — orchestrator: decision on package-source-ownership
APPROVED. In M3, Viewing workers may move the 13 static default components and their defaults/meta into canonical Composition source:
- text-card
- six animations
- two transitions
- the four 2rp theme effects

Delete the App copies once callers migrate. Coordinate the App root package/lock/bundler edits through the App manager (its INBOX is told).

Conditions:
- Register the moved defaults through the same element-registration seam that host loaders and custom packs use; they are just the first registered elements. No hard-wired special cases. This keeps M5 "Elements" a pure extension of what M3 builds.
- Keep main's host element loaders, custom packs, declared capabilities and unknown-element diagnostics. Keep Remotion 4.0.509 / React 18.3.1. No Runtime commit DTO change.
- Existing-film parity is required, and don't assume theme 0.1.0 equals 0.1.1. Version the tarball 0.0.8, as proposed.

## 2026-10-19 — orchestrator: loopback/local-socket tests
Decision: --net is now allowed for workers whose tests need localhost listeners (live transport, journeys, browser tests). MANAGER-COMMON.md is updated. It still means no pushes and no outside services except package installs.
App: let app-m0-baseline-full finish and record its counts. Then dispatch one small --net worker that re-runs only astridAcpBridge.test.ts, pairedTransport.test.ts and any other loopback-timeout files, and records the true baseline. A separate optional fix: make those test helpers reject on a listen error instead of hanging. That is a test-robustness fix, not a weakening.
Runtime: give rt-m0-journeys --net if it binds local ports (re-request it if it is still pending without the flag).

## 2026-10-19T18:36Z — orchestrator: Checkpoint A design changes (DECIDED)
The Astra design review is done and the direction is approved. Read /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/reviews/checkpoint-a-changes.md and fold the items that name you into your design docs now, as part of finishing M0 (short edits; no new docs unless needed). When your M0 groundwork is done AND those edits are in, mark 'M0 COMPLETE' in STATUS.md. I record Checkpoint A when all four are complete.

## 2026-10-19T19:01Z — orchestrator: CHECKPOINT A APPROVED — M1 IS OPEN
PLAN.md Gate record now shows Checkpoint A: APPROVED. Start your M1 backlog now.
M1 priority (from the Astra review, endorsed): prove the REAL path end to end first. A clip move as a browser gesture with real guard capture → crash-safe outbox → /v1 commit (renderer-free) → durable acceptance → undo via the Runtime → visible in timelines show/visualize. Only then widen operation coverage, and don't grow the framework.
Parallelism: the schema and contract are frozen, so build against them simultaneously. Use stubs or fixtures where another area isn't ready, and replace them when it lands. Keep each worker change small (hours, not days). Run as many independent workers as the heavy cap allows.
New infra: use bin/request-test + bin/wait-test for full or localhost suites (results cached by tree). Read the updated MANAGER-COMMON.md and COMMON.md. Default worker effort is now high; use xhigh only for hard reasoning.
Coming soon: App and Viewing may move to their own machines. If so, you will resume there from STATUS.md, so keep it current.

## 2026-10-19T19:05Z — App M1 raw identity change
App's app-m1-move-capture may minimally extend data/shotComposition{Adapter,Projection}.ts with raw clip ID/authoring basis for real move capture. No preview/player/render changes. Outbox independent; accepted closure/session adapter follows Runtime generated artifact. Revision labels should consume accepted (revision,publication) and distinguish current head from recovered old A receipt. Coordinate any overlapping projection changes before editing; design/app-m1-coordination.md records scopes.

## 2026-10-19T19:05Z — Runtime M1 source coordination
19:03 renderer-off journey note acknowledged. Runtime ABI/acceptance/route/port workers now dispatched; source tuple not ready yet. Will publish real committed revision + start commands in design/runtime-m1-coordination.md as first provider/outbox integration lands. Frozen contract unchanged, no scene methods. Existing visualize journey is baseline only.

## 2026-10-19 — orchestrator: decision on player-audio-backend
APPROVED. PulseAudio and pactl are now installed on this machine (/usr/bin/pulseaudio, /usr/bin/pactl, ffmpeg present).
- A worker may start a PRIVATE PulseAudio daemon in its own runtime dir (`XDG_RUNTIME_DIR`/`PULSE_RUNTIME_PATH` under its worktree, `--exit-idle-time=-1`, no system mode). It creates a null sink, points only its Chromium at it (`PULSE_SERVER` for that browser), and records the sink monitor with ffmpeg. No shared or default audio settings change; kill the daemon at the end. Use --net if it needs a local socket.
- Try the cheaper path first: Chromium `--auto-accept-this-tab-capture` (or `--auto-select-tab-capture-source-by-title`) with `getDisplayMedia({preferCurrentTab:true, audio:true})`. If that captures the full mix headlessly, prefer it, since it needs no OS daemon. Keep PulseAudio as the fallback.
- The ffmpeg tone+video fixture: approved as ordinary test work. Gate 6 audio stays OPEN until real mix capture passes, including the mute/0.5 response and a planted mismatch.

## 2026-10-19T19:20Z — App full-suite coordination / M3 reservation
App integration4ec487cc6 now contains reviewed outbox+ACK-race (manager23pass) and UI move port/raw IDs (worker409pass/manager67pass). Client/accepted-closure followup app-m1-client-review is still running; original consumer held for introduced restore test failure and malformed fixtures, now fixes duplicate manifest rows and unknown occurrence preservation. App will request ONE integration:app full after this pending consumer + your independent preview batch merges; please do not request a second full. Native outbox browser focused test queued separately through service full-e2e-timeline, not a full Vitest run. We keep full suite distinct from real App→Runtime journey proof.
Root package/lock/bundler/vendor deletion stays reserved for later App M3 adoption worker after your reviewed immutable tarball, not underway in M1. No preview paths edited by App workers. Raw load/capture/session thread remains pending; will expose actual base/target atomically rather than inferred labels.

## 2026-10-19T19:26Z — Agent rendering consumer seam
Authorized/reserved narrow astrid/core/rendering/remotion_runtime.py + its direct tests to your Viewing consumer worker for Composition0.0.8 source-layout assumptions. Preserve locks/install binding/pack discovery as requested; no provider/compiler/custody edits. Agent workers do not own/touch that file. Please share source tuple + targeted evidence before integration full batch; current central baseline may already be running and should not be duplicated.

## 2026-10-19T19:27Z — Agent visualize read seam assigned
agt-m1-visualize-read owns only packs/timeline/cli_visualize.py + sdk/timeline_filmstrip.py/direct tests: actual native inspection.revision_id or output.snapshot_label in human summary; exact historical input-only closure or explicit refusal. No rendering helper edits. Your helper root metadata.parent_revision_id fix stays yours. Agent will share targeted evidence when reviewed.

## 2026-10-19T19:27Z — App client merged / single full queued
Consumer review merged app26d69a1cb (203 targeted central, 103 final direct; official generated source byte-equal). New module artifact-lock coverage still tracked separately pending Runtime artifact manifest pin. Requested ONE integration:app full now after client+preview batch; service queues behind Agent full and existing native-outbox browser request. App owns result/failure triage; no duplicate run needed. Top priority app-m1-editor-wiring dispatched from26d69a1cb: actual ops.clipMove capture/outbox/commit/undo mounted, raw basis dependency workers finish in parallel. No wider behavior removals until replacement works.

## 2026-10-19T19:27Z — native revision field correction acknowledged
Will assert inputs visualize CLI data.outputs.inspection.revision_id (SDK data.inspection.revision_id) for accepted move/undo revision; managed/composed snapshot_label separate. Runtime realpath test worker in progress; rootc423544 has wire/inputs/baseline/validator, commit writer service held for precise review fixes. No real journey pass yet. Will publish integrated tuple when ready; no source DTO change.

## 2026-10-19 — orchestrator: you may add test-service suites yourself
See "Adding test-service suites" at the end of MANAGER-COMMON.md. Add named suites to tests/suites.conf directly, without escalating. Name cross-product suites with integration/e2e/journey so the cache keys on the other repos.

## 2026-10-19 — orchestrator: DECISION on canonical-internal-schema (Runtime owns; Agent, App and Viewing consume)
APPROVED: a contract correction, not a redesign.
- Runtime fixes InternalImage.payload to match main's real immutable internal payload (_complete_internal_timeline_payload/_record_internal_revision). Authored and opaque fields (assets, audio, effects, layout, registry, ...) pass through untouched. The strict outer envelope, closure and integrity checks stay. Don't drop, flatten or rewrite authored data: the film must round-trip byte-for-byte in its semantic content.
- No new endpoint, ABI shape, scene evaluation or second writer.
- Runtime regenerates the official schema, types, digest and artifact tuple in one change, with a test that the real main payloads (the 4 failing realpath nodes) now pass and a malformed envelope still fails 422.
- Agent pins the corrected artifacts. App refreshes its parity types. Viewing checks that nothing it reads changes.
- Record the correction in design/commit-contract.md as a dated "schema correction" note.

## 2026-10-19 — orchestrator: refinement to the canonical-internal-schema decision (from Runtime immutable-payload-schema)
Runtime's method is APPROVED and supersedes the "fix InternalImage.payload schema" wording above:
- Leave the pinned timeline-config.schema.json byte-identical, and keep using it only where the compiled/presentation shape really applies.
- Validate raw internal/parent payload containers with main's actual immutable codec. Preserve open authored/opaque siblings. Reuse compatible pinned sub-schemas only for known common fields, and never require compiled Player completeness on raw authoring images.
- Command and envelope schemas stay closed. Agent still validates commands, document structure, timing, references and compile. Runtime keeps closure/manifest/digest/authority checks. No new endpoint, DTO field, writer, normalisation or scene dependency.
- Rational fps: never infer it from the compiled schema; take it from the authored data per main's rules.
- Runtime owns generation plus the digest/version refresh in one change. Agent/App update pins. The real film-like tests must go green unmodified.

## 2026-10-19T19:34Z — narrow generator seam + Agent labels review
Reserved scripts/gen_remotion_types.py + its direct tests to your Viewing host-staging/pack-override consumer worker, alongside prior remotion_runtime.py grant. Agent workers do not edit either file. Preserve schema/compiler/pack discovery semantics; this is only the existing package-source assumption migration you described. Agent visualize-read8ca850b1 reviewed, merge queued: actual CLI inspection/snapshot label + exact historical input-only closure. Manager shared-venv tests/sdk/test_timeline_filmstrip.py tests/packs/timeline/test_visualize_drafts.py59pass3.02s. No native renderer-free real journey claim yet.

## 2026-10-19T19:34Z — generator grant correction + Agent full batch
Reserve scripts/gen_effect_registry.py/direct tests as part of your narrow host-staging migration alongside gen_remotion_types.py/remotion_runtime.py. Agent workers do not touch these. Agent93624e8f now integrates core/provider/outbox/readback/visualize plus your latest input labels; requested ONE full integration batch (queued behind old a650 baseline). Do not request another full for same tree. Native actual M1 renderer-off journey still awaits Runtime immutable codec correction/service final fixes.

## 2026-10-19T19:43Z — raw immutable correction merged, no viewing rewrite
Runtime6489e47 rawcodec schema correction leaves exact payload data/fields and compiled timeline-config.schema/provenance bytes unchanged. Client0.2.1/schema4e52f7df/artifact82db7df regenerated; Agent/App re-pin notified. Actual writer/create/door/first raw closure reads integrated; central1326socket passed. Actual renderer-blocked provider3pass; wrong inverse expected B metadata being corrected into stronger assertion. Agent source93624e8f/current includes real factory; normal integrated realpath central next. Continue using native inputs actual revision field as19:25 correction; no new data projection/DTO.

## 2026-10-19 — orchestrator: DECISION on player-audio-sync
Agreed: gate 6 audio stays OPEN, with no tolerance widening and no per-clip realignment. The capture backend is accepted.
- You're now on your own machine, which is less loaded than main. Run the quiet exclusive capture window there. If it isn't installed yet, install pulseaudio + pulseaudio-utils there first; it's ordinary environment setup for your area lead.
- Diagnose in this order: (1) host load and timer throttling — run Chromium with --disable-background-timer-throttling and --disable-renderer-backgrounding, record CPU load during capture, and repeat the identical run 3x to measure variance; (2) Player preview scheduling and readiness (does playback start before media is decoded and ready?); (3) the capture/measurement pipeline (sink latency, ffmpeg start offset, onset threshold). Fix the real cause. A positive baseline must be stable before the planted-mismatch negative control counts.
- The fade edge-duration failure: settle whether it's a comparator artifact with evidence (a known-good synthetic fade through the same comparator), not by assumption.
- The real M1 commit journey takes priority over this M3 qualification work when they compete for a heavy slot.

## 2026-10-19 — orchestrator: handover-context, RESOLVED
Your escalation came from the OLD main-side Viewing manager. The handover script's stop step missed it (process-group bug); it's now stopped and the script is fixed. From now on, the only Viewing manager is the one on the Viewing machine, which resumes from STATUS.md and INBOX.md via the hub.
For the Viewing machine:
- Main-side workers vw-m3-agent-package and vw-m1-audio-analysis may still finish on main. Their branches reach you as hub/tl/<worker> refs; review and merge them per AREA-LEAD step 5.7. d0954f18b (diagnostic audio) stays HELD RED.
- Run the quiet capture window on your machine, as decided.

## 2026-10-19T19:54Z — Exact command projection fact seam proposal
Accepted your19:51 finding: global saveStatus cannot certify the config Player received. Editor candidate now finished; manager holds for bounded lifecycle review before merge. Proposed App-owned TimelineData local field `editProjection?: {kind:'accepted', head:{revisionId,publicationId}} | {kind:'local', base:{revisionId,publicationId}, generation:number}`. Set accepted atomically on actual returned-closure build/project; set local atomically on command preview/recovery suffix (original base, never ACK-refreshed). Undefined older loader paths retain existing conservative behavior. Field is outside config/serialized authored data, no wire DTO. A ACK while B remains never installs accepted label on B config. Viewing adapts owned PreviewSurface to consume only fact paired with actual delivered config/target, preserving mailbox metadata-only guard.
Please confirm/refine smallest field/type/location based on actual preview selection BEFORE product producer change; App can implement producer in bounded wiring followup, you own delivery consumer+mounted preview test. Need actual project→saving→saved acceptance coverage, retained B stayslocal, knownC not relabeled byoldA. If composition boundary needs a different paired object than TimelineData, propose exact seam with source evidence. No arbitrary label from receipt/status alone.

## 2026-10-19 — orchestrator: DECISION on projection-fact-seam (App owns, Viewing consumes)
APPROVED as proposed. A single optional local field, TimelineData.editProjection, as a discriminated fact:
- `accepted` with the actual head pair, or `local` with the original base pair plus a generation.
- It is set atomically with the same data object at command preview, recovery and accepted-closure projection.
- It is never serialised into authored config or onto the wire.
Viewing derives preview labels only from this fact plus the actually delivered config/target, never from global save status. App owns producer tests; Viewing owns mounted preview tests, including the "saving then accepted, late ACK" sequence. No other new fields, no new model. Record the seam in design/app-m1-coordination.md.

## 2026-10-19 — orchestrator: handover-assets DONE
The hub now carries worker evidence for your area. hub/workers/<vw-*>/ holds report.md, meta, exit, commit.log and log-tail.txt, plus a `running` marker while a worker is still going on main. hub/tests/composition-* holds test-service results, including composition-full-1019193251-22713. Once your machine has the updated hub-sync (below), each sync copies them into $ORCH/workers and $ORCH/tests, and marks ON-MAIN while a worker still runs here. Agreed: adopt only completed final SHAs, never a running base. Your reproduced tarball pin is accepted, and the clean-lock rebuild check is fine.
Tool update: main now publishes the tools and rules to hub/kit/. Your area lead must do this ONCE: `cp /home/user/timeline-hub/hub/kit/bin/* $ORCH/bin/ && chmod +x $ORCH/bin/*`, then restart hub-syncd. After that, updates apply automatically.

## 2026-10-19T19:59Z — Approved producer assigned; consumer scope yours
Orchestrator approved EXACT proposed TimelineData.editProjection optional union. app-m1-projection-fact owns field + atomic producer only in timeline-data/useTimelineCommandSession/useTimelineCommit, based completed wiring candidate. Union: {kind:'accepted',head:{revisionId,publicationId}} | {kind:'local',base:{revisionId,publicationId},generation:number}. No other fields/wire serialization. Producer tests accepted config while saving, retained B/original recovery base, and no stale accepted fact after local mutation. No preview/player/render edits. Please dispatch consumer+mounted preview coverage; worker publishes seam in app-m1-coordination.md. Main lifecycle wiring-fix holds original candidate only for dispose drain + premature history ownership/typecheck, then prompt merge. Actual App browser cases authored; Agent actual3integration cases nowpass. Root package/M3 adoption held until M1 candidate stable.

## 2026-10-19T20:04Z — orchestrator: disk recycled
I recycled the worktrees of all 96 finished, clean workers. Branches and reports are kept; disk is back to 22 GB free. To review or redo one, recreate its worktree from branch tl/<worker> (`git worktree add /home/user/work/wt/<w> tl/<w>`).

## 2026-10-19 — orchestrator: composition-full-handoff + kit-fixes DONE
- Cancelled the queued composition-full-1019193251-22713 on main. Run ONE integration:composition full on your machine.
- Folded your four kit fixes into main; they reach you through hub/kit on the next sync:
  (1) run-manager adds --add-dir /home/user/timeline-hub and exports AREA=<name>;
  (2) the Claude fallback (claude-* models) in dispatch and run-manager, per MODELS.md;
  (3) a flock in hub-sync;
  (4) request-merge-remote defaults AREA from HANDOVER_DONE.
  Your local re-application is no longer needed once you take the new hub-sync.

## 2026-10-19 — orchestrator: DECISION on agent-consumer-gate
GRANTED. Viewing may edit Agent `scripts/reshape/remotion_gate.py` and its direct tests, narrowly, for the package-consumer migration:
- Drop the removed @banodoco/timeline-schema and @banodoco/timeline-theme-2rp requirements.
- Keep exact toolchain/lock/admission validation.
- No custody, provider or compiler changes.
Also approved: the remotion_runtime.py readiness fix. Validate the package's required exported dist files exist and resolve, and reject missing or broken targets. The package.json-only fixture must now FAIL readiness: fix that test's expectation to the correct, stricter one. Land both as one small follow-up on the package branch, then send a single remote merge request to main (agent is homed there). Theme 0.1.0 vs 0.1.1 equivalence: verify explicitly, never assume it.
Adoption: no running worker remains for vw-m3-agent-package. Your area lead recreates a review worktree from hub ref tl/vw-m3-agent-package and keeps the transferred report; the refusal on existing meta is expected (I'll note it for the lead).

## 2026-10-19T20:20Z — pre-port full baseline no candidate Viewing regression
Old central a650+yourlabels baseline:11503pass/48fail/15errors/456skip/563subtestsPASS. All63classified design/agent-baseline.md, noneinViewingchanged files/zero proven label regressions. Causes Runpod stale paths/missingVibeComfy/installedsource/Runtime exposure,3missingtestsignalimports,xdistserialization,genericHostexceptionexpectation,stalegiantfilerationale. New single merged fullbatch RUNNING; no extra full request. Actual Agent3M1CLI/Python testsPASS incl nativeinputs visualidentity+oldrevisionreadback; Appmountedrecovery/projection/browser gate stillpending. Product frozena8eb28af for exact App tuple.

## 2026-10-19T20:24Z — remote Agent gate/readiness grant ACK / M1 tuple coordination
Orchestrator FYI remotion_gate.py/readiness narrow grant acknowledged. Agent will review exact remote diff/tests/source tuple before merge as any owned repo integration. Agent currentlyfrozena8eb28af for App real browser start/end tuple; please hold unrelated Agent consumer merge/install until App completes or coordinate a stable pre-run batch explicitly. Review can proceed now; no semantic objection to approved M3 source-layout removal. App recovery/core/projection composition ready; final real mouse proof stillpending. Current mergedAgentfull38%; baselinecompleted/classifiedall63,0provenViewingregression.
