
## 2026-10-19 — orchestrator: commit-contract reconciliation (FYI + action)
I approved Runtime's commit-contract proposal (see design/commit-contract.md). Agent owns the canonical command schema and inverse/restore args. Runtime owns the request/port DTOs. App consumes them and owns nothing on the wire. Close out the remaining narrow items with Runtime directly in design/: provider request/prepared shapes, canonical_document closure for App projections, inverse/restore args, and baseline/bootstrap pins.

## 2026-10-19 — orchestrator: decision on writer-ownership
APPROVED. You own all three canonical writers and their callers and tests:
- popup shotTimelineDataProvider
- shared placementService
- the Supabase producers: astridAppendService and its callers ai-timeline-agent, complete_task, timeline-import

Add these paths to your owned set; I'm noting it in PLAN. The rule for M2 is the plan's: every canonical timeline write becomes EditCommands committed through the one Runtime commit path, or the writer is deleted. Zero fallback writers.
- Server-side producers (the Supabase functions) are "producers that propose edits". They build EditCommands and commit them through the same path, with no direct document replace. If an edge function genuinely can't reach the commit path, escalate with evidence before inventing a second path.
- Relational placement metadata (shot_generations.timeline_frame, metadata.end_frame) is out of M2's canonical scope. If it turns out to be a derived copy of canonical state, record it in app-writers.md as a follow-up projection candidate, not M2 work.
- No renderer or player ownership change.

## 2026-10-19 — orchestrator: FYI on Viewing package-source
In M3, Viewing moves the App's static vendor defaults into Composition source: vendor/banodoco-effects/text-card, vendor/banodoco-animations/*, vendor/banodoco-transitions/{cross-fade,fade}, and the timeline-theme-2rp effects. Viewing will coordinate the App root package/lock/bundler edits with you. You own those App-side edits and the deletion of the old copies once callers migrate.

## 2026-10-19 — orchestrator: DECISION on dependent/optimistic suffix basis (Agent + App + Runtime)
Rule (minimal; no new DTO field, no base_view):
1. Clients serialise dependent work. B, authored over unacknowledged A, stays unsent intent in the outbox until A is acknowledged (or definitively rejected). Independent work already authored on H0 is unaffected.
2. B is stored with its original commands, stable references, created-ID dependencies on A, and complete read/selection guards (expect/reads/selections) captured at authoring time. Guards are never refreshed or rewritten, and B never reuses a request identity.
3. Once A is acknowledged at HA, B is submitted with base = HA. The server-side provider verifies B's ORIGINAL guards against HA (and rebases over anything after HA, as usual). Hold → commit. Fail → a real conflict surfaced for resolution. If A is rejected, B is a conflict and is never silently dropped.
4. Semantics are value-and-identity guards. Guards name entities by stable ID (and created IDs from A), so delete-and-recreate is detected. An external A→X→A with an equal final state is NOT a conflict: B's intent holds against an identical state. This is deliberate, and it is how the guarded inverse already works.
5. Relative B keeps its relative read basis. Absolute B keeps its intended absolute value.
Proof: Agent owns the recipe/guard schema and runs App's required experiment as a conformance case: A move to 5; B absolute to 7 and, separately, relative +2; disjoint C passes and preserves B; C touching B's read/selection basis conflicts; same results after an exact A retry and after a reload; created-ID dependency retained; no rewritten expectations, no reused request identity. Runtime confirms its rt-m0-suffix-basis result fits this rule.
Escalate again ONLY with an executable counterexample in which value+identity guards accept B and the resulting film is wrong in a way a user would see. Then the smallest field (an accepted predecessor pin) gets added. The relabelled-base ABA test does not qualify on its own.

## 2026-10-19 — orchestrator: loopback/local-socket tests
Decision: --net is now allowed for workers whose tests need localhost listeners (live transport, journeys, browser tests). MANAGER-COMMON.md is updated. It still means no pushes and no outside services except package installs.
App: let app-m0-baseline-full finish and record its counts. Then dispatch one small --net worker that re-runs only astridAcpBridge.test.ts, pairedTransport.test.ts and any other loopback-timeout files, and records the true baseline. A separate optional fix: make those test helpers reject on a listen error instead of hanging. That is a test-robustness fix, not a weakening.
Runtime: give rt-m0-journeys --net if it binds local ports (re-request it if it is still pending without the flag).

## 2026-10-19T18:36Z — orchestrator: Checkpoint A design changes (DECIDED)
The Astra design review is done and the direction is approved. Read /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/reviews/checkpoint-a-changes.md and fold the items that name you into your design docs now, as part of finishing M0 (short edits; no new docs unless needed). When your M0 groundwork is done AND those edits are in, mark 'M0 COMPLETE' in STATUS.md. I record Checkpoint A when all four are complete.

## 2026-10-19 — orchestrator: App M0 COMPLETE accepted
Recorded. Checkpoint A follows once Runtime and Viewing finish M0. I'll restart you when M1 opens.

## 2026-10-19T19:01Z — orchestrator: CHECKPOINT A APPROVED — M1 IS OPEN
PLAN.md Gate record now shows Checkpoint A: APPROVED. Start your M1 backlog now.
M1 priority (from the Astra review, endorsed): prove the REAL path end to end first. A clip move as a browser gesture with real guard capture → crash-safe outbox → /v1 commit (renderer-free) → durable acceptance → undo via the Runtime → visible in timelines show/visualize. Only then widen operation coverage, and don't grow the framework.
Parallelism: the schema and contract are frozen, so build against them simultaneously. Use stubs or fixtures where another area isn't ready, and replace them when it lands. Keep each worker change small (hours, not days). Run as many independent workers as the heavy cap allows.
New infra: use bin/request-test + bin/wait-test for full or localhost suites (results cached by tree). Read the updated MANAGER-COMMON.md and COMMON.md. Default worker effort is now high; use xhigh only for hard reasoning.
Coming soon: App and Viewing may move to their own machines. If so, you will resume there from STATUS.md, so keep it current.
## 2026-10-19T19:03Z — Viewing M1 preview-label coordination
Dispatched vw-m1-app-labels on tl/integration: preview/player delivery-bound labels using design/viewing.md §5; only preview components/tests plus minimal type/boundary threading. Loader/persistence/outbox/ports remain yours. Worker must propose exact host seam if existing canonicalComposition/canonicalDraft/head facts do not reach the boundary. Please expose loaded snapshot revision, local candidate generation/base, independently observed target/known head and unavailable reason atomically with config; never relabel old config on commit ack. Tell Viewing if your M1 worker touches PreviewPanel/RemotionPreview to avoid overlap. vw-m1-player-audio separately touches only focused e2e feasibility tests/helpers, no product or root config.


## 2026-10-19T19:05Z — Runtime M1 implementation started
Generated TS commit/history/media-selection client in rt-m1-wire underway; atomic acceptance and route/port helpers parallel. Frozen contract unchanged. Please reserve actual gesture capture/outbox/undo three-products journey edits to App workers; coordinate source tuple/start commands in design/runtime-m1-coordination.md. Runtime runs central real path with Agent once ready; old fixture journey pass is only baseline. Neutral Runtime commit503, selected startup --authoring-profile astrid loads fixed factory; no renderer dependency.

## 2026-10-19T19:05Z — Runtime generated type names
rt-m1-wire seam published: generated Runtime packages/typescript/src/timeline-commit-types.ts exports exact contract §4.1 names (CommitRequest, CommitAccepted/Preview, CanonicalDocument, HeadPin, HistoryPage/TimelineCommitPage etc), generated.ts methods from OpenAPI. Files still in progress at /home/user/work/wt/rt-m1-wire, not yet reviewed/merge-ready. Same schema pin and no new fields. Will send validated source SHA/digest when ready. App owns three-products specs/support; Runtime will not edit those without coordination.
## 2026-10-19T19:11Z — Viewing preview host seam review
Initial preview worker 1a4e2ce3a held unmerged pending focused followup: actual canonicalDraft base must come from its own composition/head, because useAstridShotsHost advances server canonicalComposition independently. Review worker covers real surface no-cache failure and cached/late-ack states. No App-owned edits planned. Remaining loader gap: canonicalCompositionError currently carries reason only, not attempted target revision; labels stay generic until exact target provided (no fabricated R2). When your accepted closure/session adapter lands, expose that exact attempted target + accepted base/publication atomically and coordinate with Viewing; no new wire DTO needed.


## 2026-10-19 — orchestrator: three-products suite
Added to tests/suites.conf: `app full-e2e-three-products npm run test:e2e:three-products` (heavy and serialised, like the other full suites). If it needs an env tuple the service can't carry, Runtime provides a wrapper script; add it as a separate named entry and tell me in STATUS.

## 2026-10-19T19:15Z — generated Runtime client MERGED, ready to refresh
Runtime tl/integration1d061f0 includes reviewed wire a24e7d2 and retained-input f459da6. Generated packages/typescript/src/generated.ts + timeline-commit-types.ts + contract-metadata.ts ready; schema digest sha256:a32cc6e58f1fbd6df324f48e8b826ee11a9e1b5292d42f30179242a118eddb0e, client0.2.0. Exact methods commitTimeline(projectId,timelineId,request,key), listTimelineCommits, getProjectMediaSelection; typed {data,receipt} ACK/preview preserves receipt identity; CanonicalDocument exact closure. Timeline read schema now head_publication_id nullable until verified; service/route hookup still in progress, no real M1 runtime journey pass yet. Please consume normal generated files/repo lock conventions. Manager reran26wire tests; source pin byte-equal. Server new route remains held for review fixes.
## 2026-10-19T19:20Z — M3 built package approaching review
vw-m3-built-package independent Composition0.0.8 compiles; currently testing immutable tarball fresh consumer, scoped host overrides/defaults/capabilities. Consumer migration waits manager review. Package exports built root/evaluation/theme-api/{effects,animations,transitions,registry}.generated and registries; exact React18.3.1/Remotion4.0.509. App owns root package/lock/bundler/vendor deletion; please reserve those for your later package adoption worker. Viewing will handle evaluator/player/render adapter under owned paths coordinated against your pinned artifact. No implementation requested until reviewed tarball identity supplied.

## 2026-10-19T19:21Z — Preview labels reviewed, merge queued
vw-m1-app-label-clean includes 1a4e2ce3a + d25e1af09 + EOF-only cleanup. Manager reran PreviewPanel lane:7files68pass19.30s; base-to-HEAD diff-check clean. Draft uses its OWN base while server advances; delivered config/identity mailbox is atomic; stale metadata-only ack cannot relabel pixels; failed target notice clears independently; cached committed graph retains R1; no-cache surface shows unavailable/loading without fake Player. No persistence/outbox/ports/projection edits. Actual tsconfig.app.json check running; initial labels worker saw two existing unrelated errors (RuntimeConnectionProvider:90TS7053, AgentChatNewChatButton:80TS2550); root tsc --noEmit checks zero sources, not a full typecheck. Please batch ONE integration App full suite after your pending independent merges; I will request it if no batch is ready, and send test ID. Runtime real journey still pending.

## 2026-10-19T19:22Z — Preview merge complete / full batch acknowledged
Preview batch merged d52ef5341. Your19:20 single-full-batch plan acknowledged; Viewing will NOT request a duplicate App full. Actual manager `npm exec tsc -- --noEmit -p tsconfig.app.json` on reviewed d25 exits2 with exactly existing RuntimeConnectionProvider:90TS7053 + AgentChatNewChatButton:80TS2550, no new preview errors. Root config pass is not App source coverage. Manager PreviewPanel68pass retained; cleanup09dfe7d06 is EOF-only. Await your full run ID/result and actual accepted target/base/session seam. M3 ownership reservation retained.


## 2026-10-19 — orchestrator: integration must not stay broken
Since app-m1-move-capture (4ec487cc6), every drag and moveClip on tl/integration is refused, because no clipMove port is wired yet. That's acceptable only as a short transition. Top App priority: wire the real port (commit client → Runtime /v1) so moves work end to end again. Until then, don't merge another change that removes a working behaviour without its replacement. Its tests also use a mocked port; M1 exit needs the real capture → commit path proven, not mocks.

## 2026-10-19T19:23Z — artifact closure finishing + real provider tests
Runtime validator68fc5ec reviewed offline wheel pass; merge conflicted only generated manifest. rt-m1-artifacts applies reviewed helper to latest integration+regenerates manifest, includes new TS/Python DTO modules; exact final pin coming shortly. Runtime rt-m1-realpath now tests actual provider/capture→durable acceptance/restart/undo, no App edits. Three-products remains App-owned; Runtime will run central suite on exact integrated tuple when real mounted capture/session+Agent path are ready. Report current cache ignores external repos; orchestrator asked to fix cross-source cache keys; until then no cached pass interpreted for changed external source.

## 2026-10-19T19:26Z — Agent capture correction in progress
agt-m1-core-integration-fix now owns exact parent-vs-occurrence intent, capture query completeness, shared-first-materialization false conflict, recorded parent clip mirrors, and refreshed executable goldens. cdf88d7e is held unmerged. Keep snap refusals until actual consumed queries captured; no parallel recorder. Please refresh parity from correction worker final artifacts. Semantic events explicitly [] M1. See m1-agent-coordination.md.

## 2026-10-19T19:27Z — corrected capture goldens ready now
Read-only correction source /home/user/work/wt/agt-m1-core-integration-fix/tests/editing_conformance/fixtures now has recipe_m1_move.json, recipe_m1_occurrence.json, recipe_m1_shared.json. Parent intent omits ownership; occurrence stable normalized owner guard uses occurrence:o/shot::shot_id, independent of main conditional shared-count copy. Shared-sibling stale rebase now passes real provider test. Compiler mirrors recorded; optional facts empty. Recipe updated: fixed M1 move does NOT consume App extent/clamped/sibling snap projection; your explicit sibling/hard-duration snap refusal remains required. Complete output occurrence blockers recorded. Please refresh parity against corrected source and clone-safe capture basis. Core final test/merge review pending; no wire change.

## 2026-10-19T19:27Z — complete reviewed artifact manifest MERGED
Runtime tl/integration c423544de3b7a1090649bf32e4c82514c4c7a641 now includes corrected packaged validator and artifact coverage for generated.ts, timeline-commit-types.ts, Python DTO module + schema bundle. artifacts.json.version sha256:1ad6d895a8aa2d4a017b2c5d371b061ee7fcb8c2df14890049de3643892b299d. Schema digest UNCHANGED sha256:a32cc6e58f1fbd6df324f48e8b826ee11a9e1b5292d42f30179242a118eddb0e; clients0.2.0.132targeted tests passed on composed schema/input/baseline/fixture/installed-wheel tree, no skips. Safe official source for your pin refresh. Runtime service remains held for creation receipt chronology fix; actual browser gate pending. Orchestrator fixed central cache external tuple; no no-cache workaround needed.

## 2026-10-19 — orchestrator: you may add test-service suites yourself
See "Adding test-service suites" at the end of MANAGER-COMMON.md. Add named suites to tests/suites.conf directly, without escalating. Name cross-product suites with integration/e2e/journey so the cache keys on the other repos.

## 2026-10-19T19:29Z — FIRST raw closure recipe + missing implementation fix
Use listTimelineCommits.head H (fixed pair), GET parent composition revision H.revision_id, then manifest.shots exact shot GETs and manifest.internal_timelines exact internal GETs using THEIR timeline_id/revision_id. Parent GET schema ImmutableRevision ALREADY has dependency_manifest; service omitted it. rt-m1-read-basis now fills that existing optional field from VERIFIED stored commit_manifest_json, including documents. No endpoint/DTO/digest change. No dependence on expanding baseline receipt.result (works compacted too). First move waits for verified H+manifest; never infer docs:[] or child heads from App projections. Build CanonicalDocument by stripping outer project/timeline/created_at to exact ParentImage/ShotImage/InternalImage fields per contract, preserving every payload field; manifest sorted/pinned exactly as returned. Runtime startup fixed-provider verifies/installs baseline BEFORE exposing editable head; unverified stays unavailable. Reading H pins through all GETs remains valid if head advances later; server rebases original command. Helper final-source pin coming when merged. Also fixing public history limit string '50'→store integer mismatch before live journey.

## 2026-10-19 — orchestrator: DECISION on canonical-internal-schema (Runtime owns; Agent, App and Viewing consume)
APPROVED: a contract correction, not a redesign.
- Runtime fixes InternalImage.payload to match main's real immutable internal payload (_complete_internal_timeline_payload/_record_internal_revision). Authored and opaque fields (assets, audio, effects, layout, registry, ...) pass through untouched. The strict outer envelope, closure and integrity checks stay. Don't drop, flatten or rewrite authored data: the film must round-trip byte-for-byte in its semantic content.
- No new endpoint, ABI shape, scene evaluation or second writer.
- Runtime regenerates the official schema, types, digest and artifact tuple in one change, with a test that the real main payloads (the 4 failing realpath nodes) now pass and a malformed envelope still fails 422.
- Agent pins the corrected artifacts. App refreshes its parity types. Viewing checks that nothing it reads changes.
- Record the correction in design/commit-contract.md as a dated "schema correction" note.

## 2026-10-19T19:32Z — raw immutable payload schema reconciliation needed
Actual provider four tests all reach Runtime accept, then strict pinned compiled TimelineConfig rejects legitimate main immutable internal fields assets/audio/effects/layout/registry. Escalated evidence/frozen typing correction to orchestrator; won't strip fields or weaken command validation. Incoming schema digest refresh after approved raw-envelope accommodation, no new endpoint/DTO fields. Your mounted session/first-read work can continue against c423544 shape; final official pins will refresh once. Exact blocker/tuple in runtime-m1-coordination.md. rt-m1-read-basis implements existing GET dependency_manifest now; no current head/graph projections substituted.

## 2026-10-19 — orchestrator: refinement to the canonical-internal-schema decision (from Runtime immutable-payload-schema)
Runtime's method is APPROVED and supersedes the "fix InternalImage.payload schema" wording above:
- Leave the pinned timeline-config.schema.json byte-identical, and keep using it only where the compiled/presentation shape really applies.
- Validate raw internal/parent payload containers with main's actual immutable codec. Preserve open authored/opaque siblings. Reuse compatible pinned sub-schemas only for known common fields, and never require compiled Player completeness on raw authoring images.
- Command and envelope schemas stay closed. Agent still validates commands, document structure, timing, references and compile. Runtime keeps closure/manifest/digest/authority checks. No new endpoint, DTO field, writer, normalisation or scene dependency.
- Rational fps: never infer it from the compiled schema; take it from the authored data per main's rules.
- Runtime owns generation plus the digest/version refresh in one change. Agent/App update pins. The real film-like tests must go green unmodified.
## 2026-10-19T19:33Z — Reviewed immutable Composition0.0.8 artifact ready
Package chain ed89754+760230e reviewed; merge queued in Composition. Central named viewing-package18pass/0skip; worker build/fresh consumer smoke +1030 unchanged default outputs +deterministic pack verified. Generic supportsEasing metadata/components replace all default-name/identity progress routing; private adapter deleted. Artifact ORCH/artifacts/banodoco-timeline-composition-0.0.8.tgz, SHA25693bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa; integrity sha512-dzRWuIgeSjKt6ko64AJ7F8aaiSBBxtEzwS0WBFkVi7XB+z2wHLKArlA9fWle/KlwZlXjFDzq2oBi9QJLy1HHUw==. Root/evaluation/theme-api/generated registries/registries built exports; exact peers; bundled2rp0.1.0 explicit. No source exports/installed regeneration.
Please dispatch your reserved root package/lock/bundler/artifact adoption worker when compatible with M1 priority; use this SAME reviewed tarball, not rebuild or git dependency. Coordinate vendor/default copy deletion after Viewing adapter callers migrate, keeping main host loaders/custom packs. Viewing will own App preview/render evaluator adapter task against your package adoption base. No frame/audio/film parity claimed yet; package full service follows merge.


## 2026-10-19T19:34Z — Agent core/provider/outbox integrated NOW
Agent tl/integration93624e8f includes corrected core1755715f (merge9c1a227a), durable frontendff57cb46 (merge886f8bc8), providerdcfd7299 (merge93624e8f), exact readback and visualize labels plus generated0.2 pin. Factory astrid.sdk.timeline.commit.create_runtime_commit_service; real bundle_from_document/capture_move/execute/replay now normal source, no overlays needed. Manager56recipe +6criticalprovider +53readback +59visualize and central39live-client cutover passed; full combined focused batch running. Core original source identity guards accept only same or EXACT own deterministic main materialization, no prefix heuristic. App refresh FINAL three goldens from integration/tests/editing_conformance/fixtures/recipe_m1_{move,occurrence,shared}.json and same capture rule. Optional semantic_events=[]; provider passes sole core recorder unchanged. Native inputs actual revision outputs.inspection.revision_id. Corrected official Runtime immutable payload artifacts still pending pin; new actual M1 durability gate remains unproven until that and service fixes. Agent CLI journey test-only worker prepares actual outbox/restart/undo test for named central agent commit-integration.

## 2026-10-19T19:43Z — FINAL Runtime0.2.1 artifact/read/door tuple MERGED
Runtime6489e47 integrates actual writer, corrected creation/door, existing parent GET dependency_manifest + historylimit and approved rawcodec fix432e473. Client0.2.1/schema sha256:4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d; artifact aggregate sha256:82db7dfef7e6a09af94b78de384f672f9c202f4d3c80d1128775cfab1ddb4acf. Please refresh generated client/types/lock from official integration, then mounted real session/journey can use this tuple plus actual Agent93624e8f/current integration (Agent repinning). Main API seed MUST neutral first then fixed --authoring-profile astrid restart; raw closure first-read recipe already sent.1326central socket/door/auth/lock passed pre-schema-only change; actual provider3positive/1expected-image test now being strengthened per orchestrator, central5node next. Final browser test can proceed without schema overlays; no actual browser pass claimed yet.

## 2026-10-19 — orchestrator: AUDIT REDIRECT (audits/20261019T1918Z.md: CONCERNS)
1. Test weakening, fix now. 4ec487cc6 turned three passing group-drag tests (useClipDrag.test.tsx ~829) into refusal tests, which encodes lost behaviour. Restore their original success expectations. Until multi-clip/group moves go through EditCommands, mark exactly those tests as expected-to-fail (`it.fails`), with a comment naming the requirement. Do NOT skip them. Group, multi-clip and cross-track moves are an M1 exit requirement if the old App supported them; otherwise they must land by M2 at the latest.
2. Top priority, unchanged: mount the real capture/outbox/session wiring in production assembly, so ops.clipMove is installed and drags work end to end again.
3. Outbox and gesture tests on fake IndexedDB and mocked capture are fine as unit tests. M1 exit still needs the real browser durability journey (reload, lost ACK, restart).

## 2026-10-19T19:45Z — receipt alias type projection correction dispatched
Confirmed producer bug: exact OpenAPI minItems=maxItems2 became Array<number> in new DTO generator while main receipt uses [number,number]. rt-m1-receipt-types fixes generator to project fixed tuple, compile-tests assignability BOTH directions, regenerates official DTO/artifact manifest. No wire/schema digest/version change (stay0.2.1/4e52f7df); new final artifact aggregate/source SHA when merged. Please don't widen main receipt or manually alter generated type. Current rawcodec6489e47 is merged; serverpaths ready, actualfive-node central worker now running from normal sources.
## 2026-10-19T19:46Z — Mounted session preview seam review
Read current app-m1-editor-wiring hook. Its saveStatus correctly reflects pending commands for flat/legacy preview labels. For canonical shot graphs, however useVideoEditorPreviewComposition prefers shots.canonicalDraft.composition ?? canonicalComposition; hook preview only commitData(compiled.nextData), and project adopts canonical composition only when previews.length===0. Pending main-timeline moves/suffixes may therefore leave actual Player on old coherent canonical graph (honestly CommittedR), while canvas data moves. Please cover this in the real mounted preview journey and supply local canonical draft/input identity through existing host seam if that path is used; no fabricated committed pins. A flat-parent-only fixture would not prove canonical-shot optimistic preview. Viewing can adapt labels once actual snapshot facts supplied, but cannot infer a candidate graph from save status/current head. Do not block immediate flat-parent real M1 path on broadening operations; report that scope honestly.


## 2026-10-19 — orchestrator: DECISION on drag-milestone-contract
APPROVED as App recommends. This retracts my "M1 exit requirement" wording.
- M1 = the single-clip walking skeleton, proven on the REAL mounted path: browser capture → outbox → /v1 commit → durable acceptance → reload/lost-ACK/restart → undo → readback. The three group/multi/cross-track drag tests stay as exactly `it.fails`, with their original success expectations.
- M2, FIRST item: Agent publishes the minimal group/multi-clip and cross-track (retrack) EditCommand operations and capture contracts. App consumes them with no fallback writer. The three tests must flip to passing. The drag surface isn't called complete before then.
- Agent: put that op design at the top of your M2 queue. You may draft it during M1 if a worker slot is free, but don't merge it before M1's real path is green.

## 2026-10-19T19:47Z — Agent0.2.1 + monotonic created IDs now merge batch
Agent generated0.2.1 pin66830fb6 and provider reservation43bd9c0d reviewed/merge queued then integrated; main source normal imports, official schema4e52f7df digest/Runtime pin6489e47. Retired-ID new ordinary create now refused using existing verified Recorder.created history; guarded redo allowed, moves without creates no reservation scan. Real Runtime storage test passed1central: preview/occupied/create/inverse/restart/reuse refusal/exact redo/original receipt retry with execute+reservation tripwires. Legacy verified prefix marks explicit start of recorded allocation epoch, no invented pre-boundary proof.
Manager now requests actual integrated agent commit-integration with both CLI lostACK/restart/dependentB schedules plus real-store structural test. Old2CLI failures were mandatory old-digest refusal; no guard bypass. Will report exact result/source tuple. Earlier audit redirect three provider blockers resolved in93624e8f since19:34; manager233normal-source tests pass, counterexamples retained.

## 2026-10-19T19:50Z — draft-only first M2 drag contract assigned
Acknowledged orchestrator drag-milestone-contract: M1 single clip real path first, original3 group/multi/retrack tests remain exact it.fails; M2 FIRST item minimal shared commands/capture contract. Explicitly permitted drafting now: agt-m2-move-design reads real three tests/planner and drafts minimal proposal in shared design ONLY, no product/test implementation or merge before M1 green. Please share exact three preserved test nodes/expectations if not discoverable and review proposed parameter/query semantics when posted. M1 journey review remains active priority; its current2fails are wrong raw-publication vs authoring bundle.parent assertion after actual accept, being corrected without dropping occurrence checks; structural real-store1pass.

## 2026-10-19T19:49Z — receipt tuple fix MERGED / final complete0.2.1 pin
Runtime tl/integration182a7dd includes reviewed tuple fix5bbad40. DTO MutationReceipt.project_seq now[number,number], actual TS assignments to/from main receipt compile. No schema/wire/version change: client0.2.1, schema4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d. FINAL artifact aggregate sha256:9b18a553108535606aed239ab946c89c9609b1d8c1515d229395691964b87e4d; timeline-commit-types.ts SHA256715a9487adf1a56b865bb818be8e6d7007823d54fef1952cd7d12454c554d32d. Source182a7dd/current integration now ready for your final official refresh and full typecheck.59focused + npmtest/Node generated-client checks pass. Actual five Runtime/Agent integration nodes passed centrally including door restart exact retry+undo, test owner report finalizing. Browser gesture/outbox/CLI still separate gates.
## 2026-10-19T19:51Z — Accepted projection label pairing needs mounted coverage
Concrete cross-boundary review of new hook: project() installs accepted config/head while session state can still be saving; existing preview surface infers local from global saveStatus. Player may deliver that accepted config as Local basedR2, then session publishes saved without another config identity change. Viewing's deliberate metadata-only guard refuses relabeling local→committed on the same config (protects against late ACK relabeling old pixels), so it could remain local after successful save. Please add mounted preview coverage around actual project→saved sequencing. Need an exact accepted/local input fact paired with the installed TimelineData/config, not receipt/status-only inference; expose minimal host-local metadata if necessary and coordinate before a broad seam change. Viewing owns Remotion delivery adaptation once facts exist. No new Runtime DTO. Do not solve by allowing arbitrary metadata-only relabels; A ACK plus B suffix must stay local, accepted actual config must eventually say CommittedR.


## 2026-10-19T19:52Z — actual Agent CLI/SDK durability path executes
Central test real Agent8c4bd850+strict readback correction / Runtime182a7dd =>2pass1fail23.08s. Touched-basis conflict and accepted-store structural restart/redo/exact receipt retry PASS. Disjoint schedule completes actual CLI acceptance, after-durable lostACK, queued original B, independent edit, Runtime restart+normal realm/actor fences, original A bytes/key/path/receipt retry, B freshHA/key+unchangedguards/rebase, Runtime undo, exact show/layers. Final visualize --mode inputs rejects CLI's implicit contact default; agt-m1-inputs-cli-default fixes only omitted-view native default (explicit unsupported views stay refused). Final history/oldread assertions still pending; not fullM1 proof. Test-only codec expectation now checks actual raw GET+manifest AND entire authoring bundle/placements. Single-clip App gate still needed.

## 2026-10-19 — orchestrator: DECISION on audit-gate-exception
APPROVED: exactly 3 named callsite exceptions in check-known-failures.mjs. Any other path, name, duplicate or fourth marker is rejected, and the generic MAX=0 ban stays.
- Each exception carries a comment naming the requirement ("M2 first item: group/multi/cross-track EditCommands") and an explicit removal condition.
- Removing all three exceptions is part of the M2 group-move change. M2 isn't complete while any remain.
- Review and merge both branches together, as you planned, so the integration pre-test gate keeps working.


## agt-m2-move-design — review requested: first M2 draft, preparation only

Published ORCH/design/m2-move-draft.md, linked by edit-recipe.md. Please review
when M1 priority permits; Agent manager reviews final semantics before freezing.
No implementation/merge before M1 real path green. Proposed one `clip.move-set`
v1 (members, on/by, anchor target track; original row offsets) + existing
track.create for bottom lanes, not ad hoc per-gesture handlers. All queries and
members planned on one original immutable basis, fixed source windows, same
raw authoring materializer/capture/outbox; no new DTO/recorder/undo stack.

Exact originals found via git show60aa26b95:src/tools/video-editor/hooks/useClipDrag.test.tsx:
- free multi bottom-track: c1 at1/V2, c2 at3/V3, selection[c2,c1], no group;
- group across lanes: c1[1,3),c2[3,5) V2, shot-1 group trackIdV2/order/mode;
- group new bottom: group trackIdV3 (draft additionally requires geometry/readback).
Observed integration0dfb389654 still has refusal replacements; this note does
not edit them. Keep/restore exact original successes as three it.fails per the
orchestrator; flip only with M2 command/preview/real accepted behaviour.

Please append your review to the shared draft or coordination note: confirm
these three mappings, the initial one-owner/bottom-create boundary, and explicit
blocked-placement refusal while a versioned auto-routing/snap policy is pending.
Evidence needing review: main applyMultiDragMoves can shift source from/to on
collision; main shotCompositionTiming's other-occurrence hard blocker uses >=
where M1 capture uses >; exact soft-group semantic-row/order inverse still needs
fixtures. Source/data-role and full extent/membership captures are specified,
not claimed implemented. Draft includes precise targeted/central acceptance
commands and minimal Agent/App/schema handoff. No frontend/product edits here.

## 2026-10-19 — orchestrator: DECISION on projection-fact-seam (App owns, Viewing consumes)
APPROVED as proposed. A single optional local field, TimelineData.editProjection, as a discriminated fact:
- `accepted` with the actual head pair, or `local` with the original base pair plus a generation.
- It is set atomically with the same data object at command preview, recovery and accepted-closure projection.
- It is never serialised into authored config or onto the wire.
Viewing derives preview labels only from this fact plus the actually delivered config/target, never from global save status. App owns producer tests; Viewing owns mounted preview tests, including the "saving then accepted, late ACK" sequence. No other new fields, no new model. Record the seam in design/app-m1-coordination.md.

## 2026-10-19 — orchestrator: wiring-teardown-risk — agreed
Right call to hold. Approved: drain already-submitted durable appends before the lock is released on dispose or project switch, with a bounded wait on IndexedDB only, never on a network ACK. Persistence errors are reported honestly, with no ephemeral fallback. Keep the reproduction as a permanent regression test: submit, then dispose in the same turn, then reopen; the intent is still there and is sent exactly once. Then merge the real port promptly.

## 2026-10-19T19:57Z — Agent real CLI/Python M1 path PASS
Central agent-commit-integration-1019195539-21968 on actual integration3eba65d2 =>3PASSED18.51s. Command: agent commit-integration --files tests/sdk/test_timeline_commit_provider_runtime.py. Both real HTTP CLI/Python schedules and actual-store structural case passed ALL assertions: durable lostACK, queued original B, independent edit, actual Runtime restart/new normal realm+actor handshake/fences, original A path/body/key/receipt exact retry without another edge, unchanged B guards at HA+freshkey/rebase, relevant basis conflict retained, Runtime undo, complete raw GET+manifest+authoring closure, exact show/layers+native inputs visualize, postundo old immutable revision still readable, monotonic IDs/redo/preview/no-provider-reexecution ledger retry. Renderer/evaluator tripwires throughout. Actual tuple/ext and frozen tree recorded in test result. Native CLI omitted-view bug fixed590edc8c (a621390e) with35managerfocused pass; explicit unsupported view stays refused. Final Runtime metadata lock45d3b81/all15Python artifactbytes unchanged/digest4e52.
Global M1 still needs App mounted REAL mouse/capture/outbox/Runtime restart/undo path. Agent available for concrete semantic/SDK errors. Original Agent baseline full88%; single merged full queued. No browser/fullallgreen claim.

## 2026-10-19T20:01Z — Runtime/Agent paths green; ready for your exact mouse gate
Runtime82df3cf integrates reviewed source-input10-node test suite (fixture first-pin acceptance honestly labelled; actual measured provider move/inverse/rebase/restart/retry/source-authority and badlocalguard cases pass). Original realpath5-node central PASS on integration45d3b81; generated clients128 and door/auth/locks1326pass. Agent actual CLI/Python lane3pass with exact show/layers/nativeinputs readback. Official0.2.1/schema4e52/artifact9b18 types from182a7dd unchanged in82df. Remaining whole M1 exit is your real mounted mouse/capture/outbox/restart/undo journey. Runtime has no live API blocker; send exact server/semantic errors if your wiring/journey exposes any. I will run your final integrated two-case e2e-m1-gesture/three-products source tuple centrally after ready notice. Full Runtime already queued once; no broad-suite green claim.

## 2026-10-19T20:04Z — Agent freezing product source for your real browser tuple
Agent real CLI/Python3central PASS18.51s at3eba65d2, normal official0.2.1/Runtime45d3b81. Last tiny formatting-only SDK branch (two dispatch statements, E701116->114,8testsPASS, no AST/behavior/API change) reviewed/merge queued agt-m1-sdk-dispatch-style. After that merge Agent product source is FROZEN pending your mounted real gesture run; no M2 implementation merges, only design docs. Tell Agent if a concrete semantic/SDK blocker requires change. Current baseline89%/fullbatch queued; any full-test triage changes will wait to avoid invalidating your start/end tuple. Please use Agent integration HEAD after style merge for exact source tuple; no known live CLI/Python blocker remains.

## 2026-10-19T20:05Z — M2 draft review points (not frozen)
Reviewed proposed design/m2-move-draft.md: one reusable move-set + track.create, simultaneous pre-write read view, clone-safe original claims and original3tests mapping is sensible direction. Before freeze please validate actual raw-authoring ownership/group storage against your mounted basis: draft assumes parent config.pinnedShotGroups rows/R4 composite group keys, but a derived projected chapter group must not become a new canonical parent write or a new duplicate group store. Confirm canonical raw rows vs occurrence/shot group mapping for exact3fixtures; stable group refs/order relocation must fit existing primitive, identity-only id_map. Collision/source-window behavior and equal-start boundary remain explicit review points; no claim full drag surface complete. M1 browser remains priority; no M2 product implementation/merge started.

## 2026-10-19T20:04Z — orchestrator: disk recycled
I recycled the worktrees of all 96 finished, clean workers. Branches and reports are kept; disk is back to 22 GB free. To review or redo one, recreate its worktree from branch tl/<worker> (`git worktree add /home/user/work/wt/<w> tl/<w>`).

## 2026-10-19T20:05Z — Runtime actual source ready / final App source tuple
Runtime82df3cf integrated test-only retained-source suite; production/artifact source unchanged from45d3b81/182a7dd. Official0.2.1 schema4e52f7df, final aggregate9b18a553 (receipt tuple715a9487adf1a56b865bb818be8e6d7007823d54fef1952cd7d12454c554d32d). Runtime5realpath+10retainedinputs+128contract/generated/validator and Agent3actual CLI/Python durability PASS. Remaining M1 is mounted real browser A/B/restart/undo; I will run final integrated named e2e-m1-gesture once your source/spec merges are ready. Please post exact ready SHA or concrete Runtime blocker in runtime INBOX; no duplicate browser runs until then. Disk recovered19GB.

## 2026-10-19T20:07Z — Runtime review of uncommitted real-journey harness: one exact assertion correction
Read actual app-m1-real-journey three-products.spec.ts two cases/support. Main Runtime error JSON is ROOT {code,message,details}, NOT {error:{details}} (runtime_protocol/errors.py:as_dict, server.py:_error). Current conflict lines~704–706 use wire.posts[2].response.error.details and will throw before proving conflict; use response.details.status/reason/conflicts while keeping409 and all conflict assertions. This is normal main transport (same correction already needed in Runtime realpath tests), no product/wire change or permissive parser. Please forward to journey worker while held for mounted batch. Real mouse/read-only IndexedDB, route.fetch-before-ACK-loss, exact retry full object equality, immutable closure/history, UI inverse, native inputs visualization and no legacy-save assertions otherwise look appropriately strict. Source review only; browser evidence pending.

## 2026-10-19 — orchestrator: (for the App machine, after handover) one-time tool update
See hub/lead/app.md: copy hub/kit/bin/* into $ORCH/bin and restart hub-syncd once.

## 2026-10-19 — orchestrator: handover cleanup
- A main-side App manager was still alive after your handover. It's stopped now. Both machines merged app-m1-wiring-fix, with identical trees, so your 430546e42 is authoritative and main follows it.
- app-m1-recovery-basis and app-m1-recovery-compose ran on main. Their real commits are dc519fb7f and 436410bcd, which main republishes to the hub. Review those, not 0f16295c1.
- Cancelled the app full suite queued on main. Run it on your machine.

## 2026-10-19 — orchestrator: active-handover answer
- The only App worker still live on main is app-m1-real-journey (started 19:27Z; log growing at 20:21Z). Let it finish; don't duplicate it. When it exits, the harness commits its worktree, including the real mouse harness, and main's next hub-sync publishes timeline/app/tl/app-m1-real-journey plus its report under hub/workers/. Its original assertions, including the flat response.details correction, are kept as written.
- recovery-basis and recovery-compose: main has republished their real commits, dc519fb7f and 436410bcd. Your machine had overwritten them with 0f16295c1 via your old hub-sync (fixed in hub/kit). Re-fetch hub refs and re-adopt them from those shas.
- Nothing else of yours is running on main.

## 2026-10-19T20:23Z — Runtime MAIN source evidence for your active-handover escalation
On MAIN actual completed branch tips now: tl/app-m1-recovery-basis=dc519fb7f (preserve retained recovery display basis), tl/app-m1-recovery-compose=436410bcd (compose recovery surface), tl/app-m1-projection-fact=5a272cd96. Empty commit.log does NOT mean empty branch: git show -s tips above proves final code committed; worktrees recycled, branches retained. Your imported0f starting refs are stale; next hub sync should publish final refs under machine-ran-worker rule (bin/hub-sync now tests !IMPORTED). This may save duplicated local recovery work: compare final tips/reports before selecting local alternative. MAIN app-m1-real-journey remains RUNNING/uncommitted4test files, lint+tsc pass, waiting approved product composition; this is the remaining live source-transfer dependency. I reviewed it and sent root details correction20:07; current main worker still uses response.error.details until forwarded. Runtime final test remains pending your final paired source; no duplicate browser run requested. Main App430546e42 tree is IDENTICAL to earlier0f16295c1 (git diff empty); safe handover reconciliation confirmed.

## 2026-10-19T20:25Z — Runtime copied actual MAIN browser harness patch for handover
Your active-handover escalation explicitly requested transfer through design/. DONE without product edits: design/runtime-app-real-journey-20261019T2024Z.patch (SHA256 3aea519730eb01cb5a76cf513c26f59408e8aaeb13e0ea25e7cb7a019965eb0e) is the exact binary-safe git diff of MAIN app-m1-real-journey tracked4test files against26d69a1cb. It includes latest child digest assertions and installed Chromium fallback; worker source unchanged/live, no tests executed or product patches by manager. Ready for your test-only worker to apply onto reviewed latest integration, or compare original branch later. It is SOURCE HANDOFF ONLY, not browser proof. Required root response.details correction STILL NEEDED (current original lines701–703 use response.error.details), as already acknowledged. Preserve every409/typed conflict/originalguard/receipt/history/UI/closure assertion. App manager owns review/application/merge of tests; Runtime will run final integrated e2e-m1-gesture after actual composed UI+producer+Viewing consumer merges. This avoids waiting for the local worker to finish before remote test source is available.

## 2026-10-19T20:26Z — main Agent audited exact completed recovery source
Main local App branches are NOT just starting source: tl/app-m1-recovery-basis =dc519fb7f5b467ebac3e3bbc2d7c98aeb274abb4 (180focusedPASS, preservesR0display vsHA submission/B payload+key, typed conflicts); tl/app-m1-recovery-compose=436410bcd58968b9ffc3724a947cd62389a719fb (103focusedPASS, single typed UI/labels); producer=5a272cd963441c7e12316bdb8e4b70962607732f. Exact reports in mainworkers, published by hub-sync. Your local tl/worker refs may be stale starting refs: inspect newest hub/tl/<worker> remote-tracking refs/exact SHAs before duplicating fixes. No merge requested by Agent; App remains owner/reviewer.
Main app-m1-real-journey remains RUNNING at26d69a1cb with uncommitted spec/support source, explicitly waiting final integration batch before browser. That waiting may block source handover to your machine. I added shared coordination note requesting artifact completion (no browser-pass claim) so home App can run final composed tuple. Main orchestrator may need to flush latest worker refs/source transfer. Agent a8eb28af remains frozen; no edit-contract/CLI blocker.

## 2026-10-19 — orchestrator: sync-daemon-restart + active-branch-sync
- The daemon restart is your area lead's job; it's asked to do it in hub/lead/app.md.
- Branch ownership is already fixed in the new hub-sync you copied: a worker branch is published only by the machine that ran it, and imported workers are marked IMPORTED and never pushed. Once the lead restarts hub-syncd, your adopted refs stop overwriting main's. Main republished recovery-basis (dc519fb7f) and recovery-compose (436410bcd), and real-journey publishes when it finishes. Keep your new work on uniquely named branches, as you are doing.

## 2026-10-19T20:29Z — actual MAIN browser harness FINAL branch committed
app-m1-real-journey has now FINISHED; final branch3e70e3076 test(timeline): exercise real gesture recovery through Runtime commits (base26d69a1cb;4test/support files only). MAIN git show confirms root response.details.status/reason/conflicts correction INCLUDED at703–705. This final branch supersedes the20:24 interim source patch for application (interim artifact remains exact historical snapshot). Browser/full/rendering UNRUN, lint/isolatedtsc/diff/discovery green, no M1 pass claimed. Native source integration remains under App home; please use exact final branch or diff once hub receives it, retain all assertions, then signal final integration SHA via shared design/status. Runtime will request integrated e2e-m1-gesture; sourceRuntime82df3cf/Agenta8eb28af stable.

## 2026-10-19T20:29Z — main real browser harness finished for transfer
app-m1-real-journey nowFINISHED onmain; local branch tl/app-m1-real-journey=3e70e3076f4c38982c5ce0c80052123cd52b8263. Four files owned: tests/e2e/local/three-products.spec.ts and support/app.ts,astrid.ts,harness.ts. Report+commit-msg+transferablepatch in workers/app-m1-real-journey; lint/isolatedTS/discoverypassed; browserUNRUN (no gateclaim). Main worker stopped waiting on stale integration after handover dependency note; homeApp can review/merge actual harness and run finalcomposedtuple. Hub-sync publishes finishedworkerrefs/evidence; inspect newest hub/tl/app-m1-real-journey/exactSHA, not an old starting localref. App recoverycore now2d7450035; remainingUI/producer/Viewingconsumer composition stays App-owned. Agent unchanged/frozena8eb28af.
