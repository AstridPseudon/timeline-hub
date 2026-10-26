# Deletion ledger — APP rows (ONLY the app manager edits this file)
See deletion-ledger.md for the rules. Add rows here for contradicting code your area must delete; keep status/evidence current.

| id | what (paths) | contradicts | replaced by | owner | ms | status | evidence |
|---|---|---|---|---|---|---|---|
| D01 | App snapshot/whole-document savers, saveTimeline compat branch, useTimelinePersistence whole-doc fallback, timeline-save-utils reconstruction, every fallback writer in design/app-writers.md | one edit path | EditCommands via the durable command session | app | M2 | in-progress | Integration41fff/Main17; finalroot b1/tree8d8a normal013/public12 independently APPROVE+projecttscPASS, currentbrowser pending. Historical-compatible full25523 18506PASS/0actualFAIL/3originalexpected remains historical only. Allwriters stillOPEN; current census app-writers.md authoritative. |
| D02 | App local durable inverse history | Runtime is the only history | Runtime history/undo | app | M2 | in-progress | Runtime history/restore UI heldd352+historyfollowup4cdf2b87: central e2e-m2-history-conflict3PASS305s (strict restore/repeatedpublications/oneCurrent); accepted undo uses Runtime session. Zero-caller createCheckpoint alias removed at b1b9dbd44 (e51f76ea6), 37 existing history/remote-boundary/authority controls passed; no tests removed. Ordinary26437 and duplicate19235 qualified native deltas do not close the shared leaves: `useTimelineOps.ts:277-321` still snapshot-saves unmigrated project-data/transcript/seam/proposal/compiler-canary operations; `useTimelineHistory.ts:248-279,302-320,493-556` plus `TimelineEditorShellToolbar.tsx:213-245` still have live checkpoint save/load/rollback and snapshot restore callers; prepared-media still uses the command-history bridge at `useTimelineState.ts:1087-1098`/`useTimelineCommit.ts:433-451`. Focused history/persistence neighbors: 5 files, 125 passed. No safe physical D02 leaf remains; whole D02 OPEN. |
| D02-app-undo-entry-label | Unused private `UndoEntry.label` metadata field (`src/tools/video-editor/types/history.ts`) | Runtime is the only accepted history; local stack stores only data needed by unsent undo/redo | no replacement field; existing `UndoEntry` snapshot/timestamp/transaction metadata remains | app | M2 | DELETED (bounded sub-entry) | Merge `bc6f9dd39` integrates candidate `5ea95846e` and removes the unused `UndoEntry.label` field (`rg -n '\\bentry\\.label\\b' src/tools/video-editor/hooks/useTimelineHistory.ts` and `rg -n 'label\\?: string' src/tools/video-editor/types/history.ts` both return no matches after the cut). Removed one private type field only; no checkpoint, snapshot restore, command-history bridge, outbox, recovery, or public `Checkpoint` API changed. Neighbor proof: `vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineHistory.test.ts src/tools/video-editor/hooks/useTimelineHistory.remote-boundary.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx` — 3 files, 38 passed; `vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts` — 2 files, 71 passed. Whole D02 remains OPEN; live checkpoint/snapshot callers are retained above. |
| D03 | Supabase canonical writers: ai-timeline-agent, timeline-import, complete_task append + registry upsert, _shared/astridAppendService.ts | one edit path (owner: purge) | retired; completion/billing/media/relational linking retained | app | M2 | DELETED | Integrated4e7c06a0e/tree36d3e637 = testedade7b5ff.85paths+485/-20191. Replacing tests canonicalWriterRetirement.test.ts +complete_task/handler.placement.test.ts +retainedhandler.test.ts; direct nonwrite/retainedfunction controls5PASS(worker+manager); unit297PASS67files,targetedge195PASS42files,smoke7PASS3files; lint/knownmarkers clean. All M1opaque paths unchanged. No hosteddeploy/Appfull/browser claim; postbatchfull pending. |
| D08a | App initial flat canonical read before command projection has no paired projection fact, retaining old host transition clock | one compiled film and honest delivered-source labels | App initial verified TimelineCommandBasis projected atomically via existing callback/editProjection | app+viewing | M3 | DELETED (bounded source cut; final Gate6 OPEN) | Physical source attribution is `70f7fd522e6fdb663e9b72ee15d37d2e4f9a040f` (`fix(timeline): project the verified initial command basis`), which replaces the clean-session raw-load path with `project(basis, [], true)`, plus `910773b3145582b287a528bb7ba3d23701ece597` (`fix(video-editor): deliver verified initial preview projections`), which pairs the canonical config/transition delivery. R31's original-branch attribution records merge `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` / tree `74130f68` and readiness continuation `b77ccaf2dbf2da85d7ba5828e5114627325cdea6`; the unchanged qualification source is App merge `c85da5427944d26242c71e503516d8d203a5f7a7` / tree `8666399f23cd10adde62e36b3429aea4bf7375de`. Original focused neighbors remain `useTimelineCommandSession.test.tsx`, `useTimelineCommandSession.projection.test.tsx`, and `RemotionPreview.mailbox.test.tsx`: 71 passed. The original `useVideoEditorPreviewComposition.initialRead.test.tsx` suite passed 18/18 once run with the protected public13 graph: `@banodoco/timeline-composition` 0.0.13 archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, all 77/77 archive members, loaded `dist/index.js` SHA-256 `364460a558df5b0b9c6633113943f3414fd1c1873cb1357d01ecf7d279a41e52` and `dist/evaluation.js` SHA-256 `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`; no source or assertion changed. This classifies r31's 3-pass/15-fail result as the wrong effective shared Composition 0.0.10 graph; historical invalid runs `23570` and `19811` remain invalid and are not green. No remaining live OLD canonical raw-clock branch was found: `useVideoEditorPreviewComposition.ts:56` is the intentional no-projection fallback for ordinary untracked/unsent editor data, not the accepted canonical path. Final guarded cold-open remains OPEN at 18Z, and physical Gate6 remains OPEN; no actual-cold or PCM parity claim. Viewing coowner disposition: bounded initial source/projection cut only; D08b/PCM remains separate. |
| D01-app-popup-add | Popup occurrence ADD canonical snapshot publication | one edit path | occurrence.add-media via same durable session | app | M2 | in-progress — successor failed before qualification | Source `6043801bb513f20046e7bd81e7eff6a7389b57e1`, tree `317e8d2002a74bcd3b68e786b501cea3ea32e585`; central result `test-app-m2-popup-add-mounted-port-real-successor-r5-e2e-popup-add-mounted-port-successor-r5-604380-tree317e-agent8130-runtime2c4-public13-9412-all75-all77-chrome141-owned-e2e-integration-1021011818-9186`: build and exact one-case discovery passed, but the unchanged ADD case failed at line 161 after the drop with zero commit POSTs; no toast/guard, commit, or verified media-selection request followed. The live legacy writer is `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:createShotTimelineDataProvider().saveTimeline` (510–672), mounted by `src/tools/travel-between-images/components/ShotTimelinePreview.tsx` (519–639). Proposed cut is only this placed-occurrence ADD writer/caller after an actual PASS of all original raw/owner/timing/opaque/registry/closure/reload/retry/inverse/zeroLegacy assertions. SWAP, unplaced catalog operations, and unsupported audio/group/native gaps remain separate. First blocker: native ADD ingress is still not observed reaching the embedded editor after import/selection; no unchanged rerun or deletion. |
| D01-app-popup-swap | Popup occurrence SWAP canonical snapshot publication | one edit path | occurrence.swap-media create-or-require registry via same durable session | app | M2 | in-progress | FrozenAgent027/Runtime4c helper parity; popup309core212PASS and734neighbors, vendorLock13PASS central6892 resolvesGitEPERM. Assetownkeyfix adds15nativefullcases/24refusals+830neighbors/3existingexpected. Runtime0.2.6a9a reviewed UNFROZEN/adapter96sourceonly. Provenlocal-vs-acceptedprojection configmismatch exactdoc; Agent/Viewing verdict needed. Actualmediaread+UI+acceptance/reload/undo/retry/0legacy UNRUN; old writer remains. |
| D01-app-placement | Shared placementService canonical mutate/CAS save | one server rebase | explicit-owner native placement operations through command outbox | app | M2 | in-progress | TOP automatic priority. Existing media fence explicitly ACKed, no guessed taskguard. Editor ingress3cb37 preadmission sameoutbox originalapproval/owner/lane/anchor/basis/IDs+exacttaskbytes/key survives reopen;688targeted/12ingressPASS, production INACTIVE pending realhostbinding. Current b1-based auto-operation-binding worker active; bounded realproxy1PASS fakeIDB is not browserdurability. Parent auto MAINpolicy waits NEXT officialS3 pair; oldanonymous remains unconfirmed/manual/gallery. Actualtask/reconnect/reload/undo/retry/0legacy unproven; writer not retired. |
| D08b | App preview audio per-frame envelope step-hold path (exact seam under audit) | one continuous gain policy | public applyAudioEnvelope per PCM source time, same compiled Agent output | app+viewing | M3 | OPEN | AppFIRST immutable13 source2b3c431f/9412ae25 pin+lock matches all77 packagebytes,9identityPASS. Same public compile/admission/apply/WAV consumer worker active from reviewed pin; public12 ownRED19PASS5FAIL retained. Must prove own13 red->green+plantedcallernegative and retain readiness/retry/mute/boost/window beforecut. No currentPCM parity/deletion yet. |
| D01-app-bootstrap | createDefaultTimeline.ts whole-config initialization and headless repair publisher | one command path | Runtime existing constrained creation/repair then guarded Agent initialization commands | app | M2 | OPEN | Bootstrap assertion restoration is integrated at b66a94006f31 (source 8ffd2164/tree 6e67c659); its private13 targeted run passed 1 file and 4 tests, with all four identity/order assertions restored. The bounded initializer cut is qualified on published014/current native activation `1557c312b999ddc0a21c1728acbc64052ef6491f`; real proof `1021034025-7782` PASS1/exit0 covers create/init, exact lost-ACK retry, reload/restart, raw readback and history2. The whole bootstrap row remains OPEN: the true null-head same-ID repair positive is still missing, and live headless callers `dataProvider.ts:295` and `dataProvider.ts:1131` remain under D04/WC10. Conversion mapping only (proposal 0047, independent review 0055 APPROVE): map the old raw total1 history assertion to raw history length exactly 2 in order, with the normal Main `parent_composition.publish` baseline first and exactly 1 native `timeline.commit` second. Assert the full raw baseline entry: receipt/publication identity, `bootstrap:<timeline_id>` key, `bootstrap` intent, null records, exact project/timeline scope, `previous: null`, and null-to-baseline head/result ancestry. Assert the full raw native entry: `timeline.commit` receipt/publication identity, `recorded` intent, exact project/timeline scope, previous exactly the baseline revision/publication, head exactly the native entry, and commands `timeline.init`, `track.create`, `track.create`, each version 1 with `select: parent`. This preserves OPEN and all existing evidence; it is not a deletion of the live headless callers. Published013 rollback `27912` is immutable historical evidence; current native activation is `1557c312`, with the `1021034025-7782` initializer proof. No Runtime redesign or browser/acceptance qualification is claimed. |
| D01-app-bootstrap-default-initializer | Bounded `createDefaultTimeline.ts` default initializer legacy whole-config publication helper (`publishEmptyTimeline`) and its callers | one command path; no legacy initializer publication | existing `RuntimeDataProvider.initializeNativeBootstrapTimeline` -> guarded `timeline.init`/`track.create` commands through the durable session | app | M2 | DELETED (bounded sub-entry) | HOME current integration merge `1557c312b999ddc0a21c1728acbc64052ef6491f` (candidate `5c53ed21f94fd944e03642d1b6e007760082143c`; current tree `cf94daef960fe1426f6f50e4000b00c0fc42867e`). The candidate physically removes exactly 28 lines from `src/integrations/runtime/createDefaultTimeline.ts`: the old `publishEmptyTimeline` publication body/helper and its create/repair callers (old lines 51-81, 93, and 121); current `initializeTimeline` (55-65) delegates to `RuntimeDataProvider.initializeNativeBootstrapTimeline`, and current initializer source has no `publishParentComposition` call. HOME native proof `1021034025-7782` is PASS1/exit0 on App `f045`/tree `642b`, Agent `6ef`, Runtime `95bd`, public13: create/init, lost ACK, exact original request/key/body, reload, restart, outbox drain, two ordered raw history rows, and raw readback all executed; all 17 activation paths in current1557 are byte-identical, with implementation325 and independent288 focused tests passing. Published013 rollback27912 remains historical; native activation is current1557. Wholebootstrap/D04 remains OPEN because the headless carrier `src/integrations/runtime/dataProvider.ts:295` still calls `this.client.publishParentComposition`; its scope is incomplete. Next action: qualify and cut that HOME-owned headless caller, then coordinate D04/WC10 closure after the remaining Agent peer callers migrate; this bounded cut does not close the whole row. |
| D01-app-duplicate | AstridTimelineEditor duplicateIndependentShot → shotComposition.publish graph writer | one command path | native occurrence.duplicate with reserved IDs and exact derived root identity semantics | app | M2 | DELETED | HOME merged candidate `d1191f4be175d37d4f677e1f7109e6f0d91fd6c7` at actual merge SHA `8c0e1f799b64e9b6f179018b7dff01479d43c85c`; exact merged tree has zero `duplicateIndependentShot` references, including production, and retains `occurrenceDuplicateCapture.ts`, `occurrenceDuplicateGesture.ts`, and their focused tests. Central command `R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-final-state-review-gate e2e-m2-duplicate-effective-graph-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"`; result `ap2-m2-duplicate-final-state-review-gate-e2e-m2-duplicate-effective-graph-three-products-1020204512-19235`, exit 0, 1 test passed/118s. Assertion conversion retained exact pre-A parent payload with literal C/S1 edit instead of post-A `agentEdit`; retained duplicate absence plus exactly one original occurrence, opaque/order, closure IDs/digests/payloads/manifest, local B undo, credentials, zero legacy, and conflict-negative coverage. No whole-App zero-writer claim. |
| D01-app-selected-param | changed selected-pack PARAM snapshot writer | retained exact schema plus one command path | Runtime exactDocumentPin retained publicread +nativePARAMcapture/outbox | app | M2 | open | Server is sole selected-PARAM validator per owner08:36: no local Ajv or semantic after guess. Source2952 APPROVE428+7 prior+8fresh mounted; pendingraw16/cancel/recovery/remount/proto/ACKcoalescing guarded. Currentroot source refresh active. Runtime013 retained exact DocumentPin publicread available; matchingAgent/browser V1max10 afterV2/removal/restart, reload/retry/inverse/0legacy still pending. Writer NOT retired. |
| D01-app-split | useClipSplitting/useTimelineCommandsService snapshot split writers | every gesture emits EditCommands | native parent split then remaining ownership/batch contracts through same outbox | app | M2 | in-progress | CurrentMainRoot sourcef665 APPROVE1551/38files+nativeparity, independentCORS21/native1 and diff review; original mirrorpreflight2e9 refuses unsupported shared divergence before capture, never fallback aftercapture. Native parent single slice source only. Real paired UI acceptance/reload/undo/retry/0legacy pending; multi/group/newtrack legacy positives retained. |
| D01-app-parent-media | TimelineCommands.addClip/prepared-media and Astrid duplicate-generation snapshot producers | one command path | official parent clip.add-media/swap captures and verified selection through durable session | app | M2 | open | design/app-parent-media-native-seam.md;11nativepositives/18refusals/exactinverse. Duplicate-generation row-local port is retained in actual App merge `c395296db97ddf7876eafa9885e9d1678446ce75`, including the HOME two-parent merge `0cc7591f0364cfded00e4d582434753ef0c6085f` (parents `facd9c65` + `1be92c689`), preserving the original Runtime MediaSelection, displayed head/projection, and preparation epoch. For this specific Duplicate generation menu gesture, no legacy registration/publish writer is reachable. Existing 26 focused source controls plus types/lint evidence remain retained (reports 0243/0250/0257). Normal catalog duplicate remains visibly unsupported (Main catalog adapter still visibly refuses), and native `afterClipId` remains visibly unsupported; no accepted workflow is claimed. FrozenBundle2 is not parent-media ADD proof; successor official pair/real Door and App acceptance, placement, reload, retry, undo, and zero-legacy evidence remain pending; broad parent-media stays OPEN. |
| D01-app-root-normalization | timeline-domain.ts cloneTimelineExtras/migrateToFlatTracks/withCanonicalClips whitelist drops arbitrary root authoring fields in display config | opaque data survives every projection/edit | generic own-JSON passthrough with unchanged known-field normalization | app | M2 | KEEP/DONE; D01 retirement OPEN | Repair066b651b/tree fecb9ea ready:20paths+462/-54, generic own-root display/edit/popuprawchild serialization;1204PASS/3oldexpected+139corpus+100liveguards+27writer+16D03, manager30PASS. Actualrestore acceptedM1compat17865PASS; CURRENT11837 firstseed410 beforeedit, owner05:15historicalcompatible safetygateAPPROVED; originalcurrent11837setup410retained. Retainedpopuprecursiveopaque remapFIXEDcc4: sharedcontexthelper,339PASS/manager64/historicalactual8483PASS. D01wholepublisherretirementstillOPEN. Publicstrictdiskvalidation unchanged. INTEGRATED f84542004 EXACTfec tree, owner05:15 permits historicalcompatgate. Normalizationwhitelist DELETED; nativepublisherretirement stillD01OPEN. Follow-uprecursivepopuphelper2f984 MERGEDcc4dff86b/tree0bf2dba;339PASS/manager64/compat8483PASS. Replacingtests authoringBundle.sharedOpaqueRemap.test.ts +shotCompositionEditor.opaqueRemap.test.ts +opaqueRootWriters.test.tsx +shotCompositionRuntime.test.ts. No queuedfollowup. |
| D01-app-unused-query-writer | hooks/useTimeline.ts unreachable snapshot save hook (saveTimelineAtHead + numeric saveTimeline) | zero legacy writers | active command session/outbox; live persistence/history disabled-write guards, retained query keys | app | M2 | DELETED | Integrated5912bfc32/currenttree1e21df7d, source d9a12c33: -81product/-50hook-onlytest. All7querykeyconsumers unchanged/no hook/barrel/public caller. Replacing useTimelinePersistence.test.tsx 3disabledsafetypositives +useTimelineHistory.test.ts disabledcheckpoint; manager2files100PASS. Worker290PASS/205liveconsumer/94sessionrecoveryPASS; oneproposal failure EXACTacceptedM1baseline10022, no newfailure. No full/browser/zero-globalwriter claim. |

| D01-app-popup-recursive-remapper | shotCompositionEditor.remapOwnedItemReferences recursive *_item_id/_item_ids suffix rewrite | unknown/namespaced authored data preserved by one explicit codec | existing shared remapItems helper, known identity/source-link fields only | app | M2 | DELETED | Integratedcc4dff86b/tree0bf2dba9590097e703bf5775f6a7fa4363184449 source2f984d63,3paths+163/-27 incl18directconsumerregressions. Fourexistingbugexpectationscorrected/originalinputskept; RED19→339PASS15files, manager64PASS. Sharedcorpus492289unchanged; all3codecs/null/order/proto/metadatafallback/secondaryid/sourceimmutability/fullshotpayload. Approvedhistorical-compatible actualrestore8483PASS8.54s4a75/4bb; CURRENT11837 stillseed410, no deployed/nativepopupacceptanceclaim. PopupwriteritselfstillD01OPEN. |

| D01-app-accepted-echo-local-history | useTimelineHistory.onRemoteData equal-signature early return retains undo/redo snapshots across new accepted publications | Runtime sole accepted history, local snapshots only unsent gestures | existing verified accepted-pair boundary + Runtime owned-publication inverse | app | M2 | KEEP/DONE; D02 retirement OPEN | Integratedb8064ecf1/treea4614cc9016761a5681c44a60907e5a70a17e91d (source98c7):9lineverifiedacceptedpairboundary, 2RED→292PASS+manager11+historical-compatible5756actualrestorePASS. All11mountedcasesinclbadclosure/delayedread/sameheadURLrefresh/unsentundo+redo/keptdurabledraft/nativependingB/Runtimeinverse controls. Onlyactualacceptedfactclosesboundary, noquery/saveStatusauthority; no wire/server/history-model change. Correctedpostbatchfull pendingnewcleansourceafterinvalid22121cancelled; CURRENTtupleproofstillopen. |

| D01-app-transition-none-serialization | legacy rowsToConfig drops own-undefined transition; partial-coverage publisher restores old raw transition | explicit None must remove the canonical transition | native clip.set clear with original owner guards, single and atomic bulk; accepted reload/inverse/0legacy qualification | app | M2 | DELETED | Merged App commit c57dcc26162642f503532f143ceb96bb185273aa, tree b02e5380cc664bf07e4703e9a388bce0442ff645. Central gate `app-m2-none-c57-immutable-browser-final-e2e-native-none-finalroot-c57dcc26-treeb02e5380-agent8130-runtime2c4-public13-e2e-integration-v3-1020175339-2382` passed 2/2: `M2 native None single: ordinary default crossfade clears raw mirrors, reloads, retries exactly after restart and undoes through Runtime`; `M2 native None bulk: one original-basis atomic clear preserves unknown revision and opaque data; real conflict retains the whole draft`. Raw absence, opaque preservation, reload, undo, lost ACK/restart exact request and receipt, 409 draft retention, and zero legacy all passed; Agent 8130, Runtime 2c4, public 13, all 77/all 75, and source/cache/peer/Chromium guards passed pre and post. Source audit: `design/app-none-c57-immutable-final.md` and `design/app-none-remaining-standalone-writer-cut.md`; current source commit ddd9e7824c7c0c08b1293132484f5ac52d1de3c3, tree 83cf9199f2f858147d8ebbfc6648f01962bbe333. The transition SET/reset/params rows and the whole D01 family remain open; the old callback fallback is gone and missing authority visibly refuses. |

| D01-app-resolved-edit-serializer | serializeResolvedTimelineEdit added as root-preserving legacy resolved-edit serializer; three legacy effect/mutation/hook callers | one native command path without parallel snapshot serializers | retire with D01 after every consumer uses native captures | app | M2 | DEFERRED | Scope triage `design/orchestrator-scope-triage-20261021T1147Z.md`: the root-preserving helper supplies no persistence authority and is not a film-data writer; the mandatory D01 cuts still remove its writer callers. Owner-film disposition is recorded in `design/owner-film-differences.md`. Root safety repair f845/cc4 preserves data, not deletion. Asset-drop follow-up integrated2d80f2d33 (4aebsource), fixesinternalstrictboundary+authoredregistrypreservation;964focusedPASS+7880historicalactualrestorePASS. InternalassertValidTimelineEditSnapshot inlegacyrunner also retireswithD01 onceallconsumerscaptureNative. Delete helper with its three callers when D01 lands; preserve original opaque-root/outgoing assertions in native replacement. |

| D08c | four dead Composition fallback registry/theme modules under compositions/fallback and lib/*.fallback | one public Composition package, no private fallback copies | existing public-package aliases, renderer dispatch and unknown diagnostics | app+viewing | M4 | DELETED | Integrated564a21805 source d80eb7b3e; exactly4files deleted/-246physical/-229nonblank. Worker+central17560:5files65PASS; public package export/shared-peer checkPASS. Replacing tests TimelineRenderer.test.tsx, .dynamic.test.tsx, .sequence.test.tsx, .public-host.qualification.test.tsx and vendoredTimelineCompositionAliases.test.ts; no tests changed, live aliases/custom loaders/schema fallback/embed demo preserved. |
| D08d | dead `src/tools/video-editor/render/renderPipeline.ts` helper and its six private middleware tests (177 product lines) | one active render route and dispatch path | retained `renderRouter` route/admission surfaces and `useRenderState` browser/worker state | app | M3 | DELETED | Merged App commit `971e62e1b80123d93bb98cb7d72075b77cb83621` from candidate `77ad1f26afcba2df339e92441a86981ee32866ef`. Zero live/public callers; the only prior import was the removed private test block. Named replacements: `renderRouter.test.tsx` pure-media browser route, preview blocking, themed worker route, admission/body, rejection, and network-error tests; `useRenderState.test.tsx` client dispatch, malformed-preview refusal, scoped admission/polling, and worker-unavailable/no-client-fallback tests. Base active-surface proof: 76 tests across `renderRouter.test.tsx`, `renderRouter.attach.test.ts`, and `timelineOutputProjection.test.ts`; independent `useRenderState.test.tsx`: 67 passed; full assertion mapping: `handoff-vw-m3-d08-dead-renderpipeline-retirement-review-MAPPINGS.md`. No full/browser/install/typecheck rerun. |

| D10-vendor-real-provenance | `vendor/astrid-browser` nine package-owned rendering component implementations; refresh manifest/provenance seam | one public Composition implementation owner; no duplicate vendored package implementations | Composition 0.0.13 public registries for the nine builtins; Astrid checkout remains authoritative for catalog/schema/custom adapters/assets | app+viewing | M3 | DELETED | Agent source deletion is merged at `f711cbd29be0b0cb1a51328ea5093b954db3c158`, using source `c1d49291a7d4b1fabdb574acc919ded351cb106a` / tree `b96f0246024d165abaf21e5b456ba6106472267f`: all nine duplicate implementations and implementation-resource declarations are gone; descriptors, schemas, defaults, catalog authority, custom resources, and assets remain. App consumer/source deletion is `e245a4791f9270177408a7745d8397ad7b6f81a1`. Its current normal refresh donor is `68b5356db21a345be294fa50c830a3b451da77cc`, merged to App `tl/integration` as `ad1b0961a315b1ba4357768f0fe72d427ecdea49`; normal generator/verifier evidence covers 149 vendor files, exactly 9 exclusions, 65 closure files, 11 Home imports, 20 affected controls, `node --test scripts/quality/astrid-public-boundary.test.mjs`, and `node scripts/build/verify-astrid-vendor-sources.mjs`. No Runtime/Composition package or lock change, no new vendor generation/pin, and no physical frame/PCM parity claim. |

| D01-app-transition-payload-loss | transition property callbacks reconstruct partial authored transition and drop revision/opaque fields | opaque authored JSON survives edits | per-clip spread plus known-key reset through existing controls | app | M2 | KEEP/DONE; D01 retirement OPEN | Integrated1be0efdde sourcefbe7a8cb;268targeted+7opaquewriterPASS, fulloutgoing21casepreservation in TransitionPreservation.test.tsx, historical-compatibleactualrestore29689PASS. No nativeSET activation; explicitNonepublication remains separateOPEN row, allwriters stillD01. |

| D01-app-shot-graph-settings | ShotEditorView shot settings/name fallback calls and gallery/list name writer | one edit path, zero snapshot writers | Agent exact shot/config scalar commands through normal App session | app | M2 | OPEN | Whole shot settings, standalone fallback, and gallery/list writer scope remains OPEN. The bounded embedded canonical shot NAME callback is tracked separately in D01-app-shot-name, and the bounded embedded canonical PROMPT writer is tracked in D01-app-shot-graph-settings-prompt; SET/reset/params and the remaining settings writer are not covered by those deletions. Native motionMode/advancedMode/turboMode and no-fallback authority route merged `157eef8cf` from reviewed `d22c048f`; r38 retained result `app-m2-settings-effective-approved-one-actual-r38-e2e-main95-settings-reviewed-current-r36-actual-b0f07-tree91da-agent6ef-vendor091-runtime95-all76-public13-all77-runnerc148-chrome141-node20-e2e-integration-1021095924-2232` is PASS with exactly one original SettingsAutoDisable browser test, `10/10` resolver checks, App commit `b0f07b852fe66ff63825a6c7f212a5606528283a`, tree `91da628c22b55172b1aa2aa9cbcf5434c4aca2d8`, command SHA `15dacc23c869deaef7a92d05d27c35c3c4e52999799c42e848367c68090d8ed3`, and retained row SHA `725f993e88948e294be31c3196629591bb55e21d28ef2e5d17114792b280a334`. This proves the current qualified scalar no-fallback route, not physical deletion of the remaining settings families. No whole D01 claim is made. |
| D01-app-shot-graph-settings-prompt | Bounded embedded canonical PROMPT snapshot writer in the placed ShotEditor path | one edit path, zero embedded canonical prompt snapshot writers | existing occurrence-owned `shot.set` capture/session/outbox path; native refusal keeps the prompt draft dirty | app | M2 | DELETED (bounded sub-entry) | Merged App cut `c85da5427944d26242c71e503516d8d203a5f7a7` from source `6abf2e3fd32aa071a272a074e57ce0d41a4f437f`, carrying the exact reviewed prompt source `cd927abfa09b6f8571cfeb282763855af3e44541` and current-preserving donor `dfb96f10a3f33abcbef733ee55d9874e3aaeba01`. The embedded prompt intent now captures before the local draft update and submits through the existing native `shot.set` path; refusal preserves the draft and does not fall through to the snapshot writer. Original r42 independent data-safety review approved the reviewed source. The retained targeted evidence is 47 + 49 + 37 controls across the prompt source, current handoff, and proof packet; the historical actual/browser packet was not run at the 18Z checkpoint, so no actual PASS is claimed. Unsupported/compound settings, standalone/catalog/manual-position writers, the remaining generic settings writer, and all other D01 scope remain OPEN. |

| D01-app-shot-name | Embedded canonical shot NAME callback through the mounted parent session | one edit path for embedded canonical names | verified native `shot.set` capture and submit through the durable command session | app | M2 | DELETED | Integrated at dcb9f9c7095b0a8438291c8949029122c7c98ad3. Native ingress is present in ddd9e7824c7c0c08b1293132484f5ac52d1de3c3. The exact real proof passed 1 browser test, 9 Composition resolver tests, and 83 focused controls; three pre-existing NAME cases were converted one-to-one and independently approved across the 22-case control set. This is bounded to the embedded canonical callback; standalone fallback, settings, gallery, and whole-row zero-writer retirement remain OPEN. |

| D01-app-shot-raw-normalization | ShotEditor normalized form and Runtime raw-shot read materialize/drop authored root settings and successor fields | opaque authored data survives every edit | raw shot payload retained through reader/digest/encoder; overlay only changed form roots; unsafe unrepresented roots visibly refuse with draft kept | app | M2 | KEEP/DONE; D01 retirement OPEN | Integrated75df44e99 source5685f7517/productc07. Three product paths +53/-1 (net52 lines); all original positive/stale-head expectations retained. Replacing ShotEditorView.test.tsx74PASS + independent24raw corpus controls, source-codec neighbors222PASS. Actual normal HTTP cachefree historical-compatible16622 PASS2/19.18s on exactApp042c/Agent4a75/Runtime4bb: originalrestore, ALL5settingsroots, acceptedname/prompt/rawimmutableclosure, referenced malformedcontainer422/validation_error, trackedsettings/name409/draftkept. Earlier unreferencednegative200 and incorrect400/actual422 failures retained; corrected ONLY newly authored negative to exact main ValidationError. No native shot.set adoption/zerolegacy/currentpair claim. |

| D01-app-ordinary-batch | useTimelineOps ordinarypatches/proposals/project-data/transcript/seam/compiler-canary snapshot ingress | one edit path, zero snapshot writers | one atomic supported native capture/submit batch through existing session | app | M2 | OPEN | Currentcensus1be useTimelineOps226-307 routes allordinarypatches tosnapshotcommitData; stagednativebatch helpers notactivated; no partialmixedpatchdrop orsequentialcanaryfiction. Process-harness conversion only (D01 remains OPEN): original `outer-controls-run.py` SHA-256 `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234` is unchanged; sidecar `outer-controls-run.phase-corrected-1150.py` SHA-256 `a4b3f89d9f15f9fbd095e5b6b658605807f7b0099e8337f0cb4dea11ebdf662e` applies only the missing `before` temp-log handling and `before` zero-temp assertion. Patch: `temps=[]` when the `before` log is absent, otherwise parse as before; `before` now asserts `not temps and not leaked`; non-before branches are byte-identical. Mapping: `before` still requires refusal/status, one shell, zero child/build, and no packet, now with exact `temps_created=0` and `temps_leaked=0`; `after`, `absent-output`, `copy-failure`, and `success` retain their original temp/cleanup/evidence assertions. No fake event, source/helper/pin/version rebinding, launch stub, or artifact-closure change; no controls executed. |

| D01-app-ordinary-batch-compiler-canary | Bounded compiler-canary sub-entry: private `src/tools/video-editor/lib/compiler-canary.ts` and its 59 private self-tests | one edit path; no private canary callers | retained source-map/navigation/SDK/project-data controls and the still-live ordinary batch path | app | M2 | DELETED (bounded sub-entry) | HOME merge `692765846` removes both private files (2,171 lines). Independent review proved zero live static, dynamic, public, registry, manifest, or SDK callers; retained `com.example.compiler-canary` values are fixture-only. All 59 removed declarations map one-to-one to `BEHAVIORGONE: private canary`; the reviewed retained-neighbor lane passed 439 tests. This does not close `D01-app-ordinary-batch`; its central ordinary snapshot fallback remains live. |
| D01-app-ordinary-batch-compiler-canary-strict-debt | Stale `eslint.strict-debt.js` entry for the removed private compiler-canary module | strict-debt inventory matches live paths | exact one-line owner-approved removal | app | M2 | DELETED | HOME merge `743d3464d1ed548986f29249bd9b4215baccf9bb` of candidate `ff04c7d2cfa02f2b4aaa2a92a634cac4c4539bb0` removes exactly two stale lines: the `eslint.strict-debt.js` compiler-canary entry and the `docs/cutover-inventory.md` compiler-canary test row. Focused config/lint/syntax and `git diff --check` passed; no threshold, caller, or product change. `D01-app-ordinary-batch` remains OPEN; the canary module sub-entry remains `DELETED692765846`. |
| D01-app-element-routes | runtime/element-adapter direct save/CAS through VideoEditorProvider + ElementsLibraryPanel ingresses | one edit path, zero snapshot writers | native exact element identity/revision/params operations through same commit session | app | M2 | OPEN | Currentcensus1be element-adapter65-112/487-523, provider320, UI72/86. Unknownextensions/readpins preserved; genericclipcommandsnotcompleteproof. No nativeelementdirecttrafficqualification yet. |

| D01-app-parent-delete | single-parent `useClipDeletion` snapshot branch | one edit path | native `clip.delete` through existing command session/outbox | app | M2 | **DELETED (bounded sub-entry)** | Current integration carries product route `d4d02913d32e0e39103d3cafb2017dd4683fa245` in merge `c0adfd0e956c43bcfde6a8459670efe13c5786af`; `src/tools/video-editor/hooks/clip-editing/useClipDeletion.ts:44-54` routes exactly one qualified parent through `genericPatchPort` before the shared fallback. Exact normal95 product: App `bc8ba8ff0dfd1a5737c9f7517108fe96db0ba27c`, tree `7eaca5202505ce003f41cba72843ed427d8a9eaa`; parent-delete source surface matches current integration. Central actual `1021025059-14549` **PASS**, one real test in 178s, 22 launcher controls passed; raw/opaque preservation, reload/restart, exact retry, inverse restore, and zero legacy traffic asserted. Local targeted deletion/neighbors: four files, 68 passed (`useClipEditing.test.ts`, `commitSession.genericPatch.test.ts`, `genericPatchCapture.test.ts`, `useTimelineCommandSession.test.tsx`). `isParentClipDeleteTarget` remains live ownership gating; shared `applyRowsEdit` fallback remains required for grouped, occurrence, multi/mixed, and unsupported paths. Original `useClipEditing.test.ts:261` and original positive/refusal/draft/raw/outbox/guard assertions retained. Whole D01/D02 remains open; no unsupported-family closure claimed. |

| D08-app-private-trim-math | lib/config-utils.ts private getSanitizedMediaTrimProps math | one public Composition trim policy | public computeMediaTrim compatibility reexport | app+viewing | M3 | DELETED | Actual App merge `9d518546df880ec515f2f424c55073193f2a2e64` (tree `9b3a0a81`, source `93cd2f7d4ea5520c9793f5f336ccc89fcfc92538`) removes exactly 16 private math lines across two files. Existing named controls in `src/tools/video-editor/lib/config-utils.test.ts`, `src/tools/video-editor/compositions/VisualClip.test.tsx`, and `src/tools/video-editor/compositions/AudioTrack.test.tsx` retain the shared visible-time, boundary, malformed-fps, and before/public-vector coverage; the recorded owner lane passed 62 controls plus 20 before/public vectors with a bidirectional signature check and all77/public12 byte parity. No clock/root/pin/PCM policy change. |
| D08-debug-track | Uncalled private `src/tools/video-editor/compositions/DebugTrack.tsx` | one active evaluator/viewer path | retained TimelineRenderer/VisualClip path and renderer/sequence/shots tests | viewing+app | M3 | DELETED | Actual App home merge `bdeb5e97eadec5ce103a15e4d5434cf8e85cf7c1` from source `6bb4de6fafe4c1e616958506506fad0594d63893`: 59 physical product lines removed, zero live callers; replacement neighbors `TimelineRenderer.test.tsx`, `TimelineRenderer.sequence.test.tsx`, and `TimelineRenderer.shots.test.tsx` passed 64 tests, with no assertions removed. Broad D08 remains open. |
| D08-rate-wrapper | App `config-utils` sanitized-playback-rate wrapper and its live import delegation | one public playback-rate evaluator | public `getSanitizedPlaybackRate` plus existing player/visual/PCM consumers | app+viewing | M3 | DELETED | Actual App merge `a12b19be56816112da9b16cd8db4c48f9c5c399b` from source `831bd7aba98c5f7076836b17299056c40aa3ca64` removes 5 physical duplicate-wrapper lines across four files. Existing named controls in `config-utils.test.ts`, `playerEvaluation.test.ts`, `VisualClip.test.tsx`, `AudioTrack.test.tsx`, `compiledAudioSourceClock.test.ts`, and `continuousPCM.lifetime.test.tsx` retain public imports and rate assertions; the current six-file rate lane passed 127 tests plus 69 rate-clock neighbors, with ESLint/diff check and no residual private wrapper callers. Broad D08 remains open. |
| D08-duration-delegation | App private timeline-duration implementation and eight caller delegations | one public Composition duration evaluator | public13 `getTimelineDurationInFrames`, with the App compatibility export retained | app+viewing | M3 | DELETED | Actual App merge `dce7eea63785f8a54ea7f14aee6c2e12c16d3bc6` from current source `e414afb56c7c573b7be0ab0b9924e4697df9c5d0` removes 6 physical local implementation lines, moves 8 callers to public13, and retains the `config-utils.ts` compatibility export plus identity assertion. Existing named duration/render/player/property neighbors, including `config-utils.test.ts`, retained their assertions; the current integration-first duration lane passed 442 tests with scoped ESLint/diff check. Viewing donors `3508231fd` and `ac8894ba1` are superseded by this landed equivalent. Per Viewing 00:58, remaining per-clip duration helpers are retained domain/host adapters: public13 whole-timeline duration differs on invalid trim/hold-kind/speed and nonzero starts, so no further exact safe deletion exists. Broad D08 remains open. |

| D01-app-original-three-drag | group/free-multi/new-track drag paths remain refused with three original success expectations marked it.fails | all existing gestures via EditCommands with visible Main behavior preserved | official guarded legacy-group migration, canonical occurrence move plus atomic child retrack, then track.create/free move-set and derived group view | app | M2 | OPEN | Current officialS2 Agent8130/Runtime2c4 lacks timeline.migrate-groups/occurrence.move/clip.move-set. Exactly3original success assertions useClipDrag.test.tsx774/1120/1230 retained; private draft goldens NOTrelease authority. Readiness design/app-original-three-drag-current-contract-readiness.md. Needs Agent/Runtime published capture+golden+paired normal artifact; then existing-lane/new-track/free-multi acceptedreload/exactguardedundo/concurrency/0legacy, markers fliponlywithpositives. |

### Test conversions retained (not product deletions)
- main.bootstrap-order.test.tsx — synchronous MAIN574 contract: sourcef203e0bb249328f742724b7c1636defdcbee3503 converts the original deferred-extension initialization case one-to-one to explicit synchronousextensioninstall -> awaitedworkspaceidentity ->render ordering. Pre-rendernegative/migrationfailure/twofontcaseskept,5PASS2files; Main e4b199066 sourceisreference. No deleted/skipped/weakenedassertions. Integrationmergepending.

| D08e | Unreferenced private FALLBACK_RENDER_RUNTIME and createRenderRuntime exports | one active render runtime path | live RenderRuntime type and existing render route/hooks | app+viewing | M3 | DELETED | Candidate `429d126a13964ed4d544f94d82673671f5efdcb8` merged to App as `35814b16a365199fc816ce1b1dc69fb007b104f1`; 14 product lines deleted and zero live references, while the live `RenderRuntime` type remains. Existing named controls `src/tools/video-editor/lib/renderRouter.test.tsx`, `src/tools/video-editor/hooks/useTimelineRenderRequest.test.tsx`, and `src/tools/video-editor/hooks/useRenderState.test.tsx` passed 140 tests; ESLint and `git diff --check` passed. No test assertions were removed. Broad D08 remains open. |

| D01-app-parent-source-window | Canonical parent Source In/Out snapshot fallback in ClipPanelBody | every film timing edit through EditCommands | existing native clip.trim capture/session/outbox via ClipSourceWindowFields | app | M2 | DELETED | Merged 3935dec38 from independently approved 93a268c17. Real browser19010 passed raw/opaque, reload, Runtime undo, lost ACK/restart/exact retry and zero legacy traffic. Original Source In controlled-reset/blur positive maps to native clip.trim success; old missing-authority case visibly refuses and preserves exact dirty draft with no snapshot call. Speed preserved; 20 targeted controls pass, only three original drag expected failures remain. Child/group/drag trim and whole D01 remain open. |
| D01-app-public-trim-native-fail-closed | Public `trimClip` source-only native capture/submit missing-or-rejected fallback in `src/tools/video-editor/hooks/useTimelineCommandsService.ts` | one edit path; native `clipTrim` owns accepted source-window writes | existing `clipTrim` capture/finish/submit with visible `mutation_failed` refusal and draft retention | app | M2 | DELETED (bounded sub-entry) | Physical source cut `eb51ff381660a90e847c70371fcb64b8eca4d113` (tree `525ce6d726ab36d743e4504fa2e1b274bfa21b41`), merged by `df4c86b08c390db932b19cac3d1ad36fb55b6f15`; the old `c3f943ddf` lines 848–873 (22 lines) no longer fall through to local `nextConfig`/`applyValidatedMutation`. Current source `5f513665a6961e3552cf47bf70303fe41f370ba3` / tree `1c28244f9de4399070bc31772aef2d1a6cfca128`. Named direct controls: `src/tools/video-editor/commands/semanticGestures.test.ts`; exact targeted command `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader bundle --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/clipTrimCapture.test.ts src/tools/video-editor/commands/clipTrimGesture.test.ts src/tools/video-editor/commands/ordinaryTrimMember.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx` — 7 files, 217 passed, exit 0; `git diff --check` passed. Existing positive native path, refusal/raw/draft controls retained; placement/group/child/mixed families remain separate. Historical `actual8788` stays UNKNOWN; the original browser packet remains a checkpoint18 requirement. No browser/full/whole-D01 success is claimed; whole D01 remains OPEN. |

| APP-A4-D37-TRACK | `src/tools/video-editor/commands/trackReorderCapture.ts` and `.test.ts` — dormant same-order `track_order` capture and exclusive tests | D52 owner latitude; dead scope may be removed when census-proven unreachable | None; no provider migration or new operation | app | S | D52 DELETED; source merge actual MERGED 2e3c/whole-tree identity qualified with receipt | Author 1118 commit `f00ee693aaaa4af3ed007b4f7a847f75ee705f12`, parent `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `7ee82efe89862de629bf48abb25cc941deed915d`; exact four-file-only deletion. Base import/export census found zero production callers and zero external references; only the module’s own test imported it. Independent review 1121 PASS. Retained neighboring tests: 85/85 passed across 6 files; serialized Node 20.20.0/npm 10.8.2 typechecks for root/app/node passed; diff check passed. Full C0 request/reply shapes and live P1–P5 paths unchanged. |
| APP-A4-D37-RAW-BIRTH | `src/tools/video-editor/commands/parentAfterAnchorCapture.ts` and `.test.ts` — dormant raw after-anchor births and exclusive raw/null-hold, subminimum, and incoming-transition tests | D52 owner latitude; dead scope may be removed when census-proven unreachable | None; no provider migration or new operation | app | S | D52 DELETED; source merge actual MERGED 2e3c/whole-tree identity qualified with receipt | Author 1118 commit `f00ee693aaaa4af3ed007b4f7a847f75ee705f12`, parent `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `7ee82efe89862de629bf48abb25cc941deed915d`; exact four-file-only deletion. Base import/export census found zero production callers and zero external references; only the module’s own test imported it. Independent review 1121 PASS. Retained D31 transcript and P1/P2/P3 specs remain byte-identical; 85/85 neighboring tests and all three serialized Node 20.20.0/npm 10.8.2 typechecks passed. Full C0 request/reply shapes and live P1–P5 paths unchanged. |

| APP-A4-D37-SESSION-CHAIN | `commands/commitSession.ts`; remaining non-label and explicit-resolution declarations in `commitSession.test.ts` | D37 reachable-writer rule | Keep implementations and behavioral tests unchanged; no provider migration | app | S | dormant: no production caller; follow-up deletion for owner review | Sol0306 current graph at a64587176d; no production caller at entry177. Keep `__tests__/commitSessionEnvironment.ts`, all five `commitSession*.test.ts`, capture/gesture dependencies and fixtures. Exact pending request/key, fresh dependent key, restart, raw closure, refusal, history and undo assertions retained. [Source audit](app-A4-dormant-protocol-sol-0306.md). |
| APP-A4-D37-NATIVE-LABEL | `commitSession.ts` native label port; `trackLabelCapture.ts`, `trackLabelGesture.ts`; remaining original label declarations | D37 reachable-writer rule | Keep implementations and behavioral tests unchanged; no provider migration | app | S | dormant: no production caller; follow-up deletion for owner review | Sol0306 current graph at a64587176d; no production value caller. Keep both label-helper tests, session environment, generic-patch and ordinary-member support. Native presence/clear, observed and unobserved remote actions, guarded history/undo and canonical closure remain unchanged. [Source audit](app-A4-dormant-protocol-sol-0306.md). |
| APP-A4-D37-EXECUTOR | `src/tools/video-editor/commands/runner.ts`, `runner.test.ts`, and retired runner/parity sections in `commands/media.test.ts`, `lib/sha256.test.ts`, and `lib/timeline-save-utils.test.ts` | D52 owner latitude; dormant executor has no production caller or value export | None; live save utilities, media behavior, types, and D31 transcript behavior retained | app | S | D52 DELETED; MERGED via `5a9ff97cf036efdd409c559dbd0334ff7a5639b8` and `d99396bca7c3853435cfa5a5991f5b1073187be4`; integrated tree `3311baa327c8963d007cfc3a1b2f04617085f3b3` | Source `3403a1d0ae784f4da98793008560acea51ece221`, tree `9ccc637f4be03611d6c362a3950be52678fad550`; reviewed 1143 PASS; `runner.ts` SHA-256 `c42ff359dbcd1883ace2cc72e91fbd23377b80d0f38ad70affde5b6d188ec119`, `runner.test.ts` `d6912b9a3d166e40462540a95568a38d783242f62b2f82cc4b7f75d54ec0cf65`; exact five-path delta, no production callers/value exports; 82 targeted tests passed, three TypeScript checks, scoped ESLint, and diff check passed; cumulative integrated proof 1157 passed Gate5 23/23, deduplicated union 608/608, task-route 20/20, edge-retirement 1/1, D39 checks 72/72, three TypeScript checks, lint, and diff check; [source](app-A4-D52-runner-delete-1137.md), [assessment](app-A4-D52-full-runner-assessment-1132.md), [integrated review](app-U3b-F-cumulative-review-1157.md) |

| APP-A4-D52-TRANSCRIPT | `src/tools/video-editor/commands/transcriptAssociateCapture.ts` and `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts` — dormant exclusive `transcript.associate` capture pair, exactly 970 deleted lines | D52 owner latitude; no production caller or Agent registry operation | None; live `useProjectTranscriptHost` → reconciliation/import → generic v2 `doc.patch` → durable outbox/Runtime commit path retained | app | S | D52 DELETED; MERGED `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f`, tree `911956d49c42021f11d21e9cf69e9e9478ab569a` | Source `8a712d39c74e92ff10886007ae5135d4f316e92e`, tree `27a5e398c14245317ca9fc7f8bb42b037bd84877`; reviewed 1217 PASS; source SHA-256 `transcriptAssociateCapture.ts=a4db541841f2c068c2984c27225c6fd14a5b557a648b6d9412b5ed5e352020a2`, test `56c1c0bb0393ec2275caf6f76af07b207c23d873e1551f687de9393364b31516`; census proved no production imports, dynamic callers, or Agent registry entry, while the three live negative assertions remain; integrated `d99396bca7..cca3deb361` is exactly the two deletions; loader-first Vitest attempt failed at startup with `__dirname` undefined, then the same run without `--configLoader=runner` passed 4 files/50 tests; `tsconfig.json`, `tsconfig.app.json`, and `tsconfig.node.json` passed; [census](app-A4-D52-transcript-census-1205.md), [review](app-A4-D52-transcript-review-1217.md), [retirement](app-A4-D52-transcript-retire-1210.md) |
| APP-A4-D52-COMPLETE-TASK | Retired `supabase/functions/complete_task/**` closure: `authContext.test.ts`, `authContext.ts`, `billing.test.ts`, `billing.ts`, `cleanupMaterializedInputs.test.ts`, `cleanupMaterializedInputs.ts`, `completionHelpers.test.ts`, `completionHelpers.ts`, `constants.test.ts`, `constants.ts`, `deno.json`, `errors.test.ts`, `errors.ts`, `generation-child-diagnostics.test.ts`, `generation-child-diagnostics.ts`, `generation-child.test.ts`, `generation-child.ts`, `generation-core.test.ts`, `generation-core.ts`, `generation-handlers.test.ts`, `generation-handlers.ts`, `generation-parent.test.ts`, `generation-parent.ts`, `generation.test.ts`, `generation.ts`, `handler.placement.test.ts`, `handler.test.ts`, `handler.ts`, `index.ts`, `orchestrator.gate.test.ts`, `orchestrator.test.ts`, `orchestrator.ts`, `orchestratorCore.ts`, `orchestratorPolicy.test.ts`, `orchestratorPolicy.ts`, `params.test.ts`, `params.ts`, `paramsGeneration.test.ts`, `paramsGeneration.ts`, `request.test.ts`, `request.ts`, `shotValidation.test.ts`, `shotValidation.ts`, `storage.test.ts`, `storage.ts`, `taskParamNormalizer.test.ts`, `taskParamNormalizer.ts`, `types.ts` — 48 files, 7,656 deletions | D52 owner latitude; retired Supabase completion path and exclusive tests contradict Runtime-owned task admission, claim, and settlement | Runtime-owned App `createTask` → `POST /v1/tasks` with idempotency key → Runtime/Worker claim and settlement; no App/Agent/Runtime `complete_task` caller remains | app | S | D52 DELETED; MERGED via `5a9ff97cf036efdd409c559dbd0334ff7a5639b8` and `d99396bca7c3853435cfa5a5991f5b1073187be4`; integrated tree `3311baa327c8963d007cfc3a1b2f04617085f3b3` | Source `664a8a08ddc1d69533677ed07092e749763ae924`, tree `94ceaa226d241d28fa597c77390573d40ed0b7f7`; reviewed 1143 PASS; key deleted source hashes `handler.ts=bbf8687c2f3720340b8b3d2179b8308ceae12afd18740b91f346ae1ad5b4ab60`, `index.ts=c027c9c5cca3653ace7d14e94a309d220dfe7192d01143f67fa2921cd341e1c9`; no production callers across App, Agent, or Runtime; live Runtime task caller qualification passed 20/20 `createTask` plus task-route tests and 1/1 canonical-writer-retirement neighbor; cumulative integrated proof 1157 passed the 48-file union 608/608, three TypeScript checks, lint, and diff check; [source](app-U3-D52-complete-task-delete-1137.md), [integrated review](app-U3b-F-cumulative-review-1157.md) |
## behaviour changes

| D50/P3 | `tests/e2e/local/three-products.spec.ts:1641` — P3 request-B `doc.patch` expectation | D50-approved C0 v2 shape requires strict `created: []` | Exact strict `created: []`; all other bytes unchanged | app | S | reviewed PASS; merged 28b0f11e1c; integrated0800 PASS | Producer: `documentPatchIntent.ts:131,216–223` → `localSaveSession.ts:167–185`; [review](handoff-ap2-P3-D50-created-review-0747.md); [source handoff](handoff-ap2-P3-D50-created-expectation-0741.md); [integrated proof](app-P2-P3-oracle-integrated-0800.md); full SHA-256 `741bcfb986fe0e80bbf81a40f741418991ed7e59cda59e578060b818e7d7cd94`→`68bb47b4dd7d3ca0b2ee962bf729c0465132cb3bfb6ce5ffaa27493b0c61d2ae`; body `c7735569a90ec9acdc2d66feed8747d3480c3b6d0e5acd3e22316ba84f9489e8`→`2b99496c7fb8a0d9b51ecb7dfdbc7041c2d3031aa60d9c80da75b754c1ec9e3f`; tail `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`→`5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`; full C0v2 request/reply unchanged |

Normal home receipt: `ap2-P3-D50-created-expectation-0741` merged at `28b0f11e1c`; integrated proof worker `app-P2-P3-oracle-integrated-0800` passed 17 controls, three types, lint and list checks. The row above records the worker-authored and independently qualified pre-merge facts; source merge is now received. No original journey or GO credit.


D53 | fullspec 26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b→95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c; guard 15b580777856fb3d4b6494fbb52f8dcc8c83712ce3ce0c7f6a1cda19431bdfd5→1c080595fbb1dd5fb6ecc7387e9bf01744e0b08e61473d3994383e226b60a9e0; author2357/review1126; MERGED602f; integrated PASS.


| D53/P3 | `tests/e2e/local/three-products.spec.ts`; `tests/e2e/local/support/gate5-fault-order.ts`; `tests/e2e/local/support/gate5-fault-order.test.mjs` — strict observed `[A,A]`, forwarded `[A]`, zero B, and real staged retry accounting | Gate5 previously counted every observed commit POST, but its `attempts===1` assertion misclassified the genuine second A retry as if B were still unsent | Exact identity/order classification with fail-closed duplicate/mismatch guards | app2 | S | **PASS; integrated `602f8b1f5`** | `602f8b1f5` tree `a3884497`, parents `2e3c8f65` and `2357df925`; D53 paths equal author commit `2357df925` (sole parent `d6ed8cbd`). Only other delta is D52 deletion `f00ee693`; no `32ba166b` or `bd08e4c3` ancestry. Full spec SHA `26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b` → `95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c`; guard SHA `15b580777856fb3d4b6494fbb52f8dcc8c83712ce3ce0c7f6a1cda19431bdfd5` → `1c080595fbb1dd5fb6ecc7387e9bf01744e0b08e61473d3994383e226b60a9e0`; protected tail unchanged `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`. Existing integrated controls remain reusable: Node 23/23, three TypeScript checks, ESLint, Playwright list 15, and `git diff --check` passed. [Finite correction provenance](design/handoff-ap2-P3-D53-ledger-wording-1154.md). |



| ID | Current behavior | C0 citation | Actual home proof |
|---|---|---|---|
| P3-history | Authenticated `recorder_abi: 2` is required for physical-binding Gate-5 history; wrong/missing ABI is rejected. | C0 §§4,7; D62 history-only `recorder_abi` | Author `471dc827…`; home merge `9f4ec08f…`, tree `c13980c7…`; 23/23 controls passed. |
| P2-parentreads | Submitted request `reads` must match authoritative history exactly; omitted reads remain absent. | C0 §§1,4,5,7 | Author `6b7b6e7a…`; integrated home `a2a6e4ab…`, tree `6cae4f2f…`; 10/10 P2 controls passed. |


D69 — Current App home `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`; D69 source `2eab0fb8f0df8972a3f02804b1ac25cc8df0f142` is merged at home, with frozen upstream `3881e9440688f774878e18806da2dc5c993a9b00` ancestral. Reverse audit: 1,403 cleared / 67 cited intentional / 4 restored / 0 remaining. Placement restoration: old RED = 5 added controls failed; new home PASS = 41/41. Exact restoration scope is `src/shared/lib/placement/placementService.ts`, `src/shared/lib/placement/__tests__/placementService.test.ts`, and `src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts`; source `61f0fb613a` before → `2eab0fb8f0` after. SHA-256 before → after: `placementService.ts` `74c12bb82895cae28902e71735662851989424c854954b0672973b2de624df0f` → `aa290545d19630ddbebfe2a0d16346d079bba17fa8c35fb3b8158e395e3c4d30`; `placementService.test.ts` `77dfb5e80a848e44e239aca27f2c82b35f4a2ea2ed97063080649258a4c672fa` → `4035cab35caf56fb27f7c31d782467d816e6e9f885af8d6bd71f25849f67ad23`; `placementService.workspaceV1.test.ts` `aeb366ef8d91c7ffbc8c8bad9f277e4cb78633e1011e9336652f33af047cb5f2` → `14d1492668ebc9e76b2a25956e4a597c67300be0b3cb084dac0923c560cce8ca`. Frozen placement declarations remain `fcf8e413ce400977be026208d424ea211f4e464cf68db8fd2d7eece5fce8dd0d` and `80bd6c080820a5855c56fdc48e9ed988627b0d7fbf8fda32afc18957d6a1183b`. C0 §§1, 4, 7 semantics remain: pre-authoring head races may re-read once; submitted Runtime 409 conflicts remain durable as one intent. No live Runtime/browser/service/original/full receipt is claimed.

D70 — Actual home is `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`; D70 merge `aaddaf12d2401760b75f6fb54e9e624883434447` is an ancestor. The approved `cc64db` line is present: mounted V1 parent move emits `label: Edit timeline`, `intent: Move ${seed.appClipId} on V1`, and `tags: []`. Full-spec SHA-256 `95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c` → `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`; setup helper `28f7f84e141022740bd4bc6cc465579a8285fae16aecbf09ec77ea9d405fb962` → `77c10439a9b1d8287853d325bec82088e65e7401542a5380f8f361d4a9feb6f4`. Gate-5 body is unchanged at `d47d55265b3905a1882ffb370df033cf92b35c3492d4bec366d8da0272b9fb20`; reset block unchanged at `980b4cbe2c1d7a05840c8419fd55991ff73783784c89df6c717e2721a212fe62`; canonical tail unchanged at `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`. C0 §§1, 4, 7 and D13 source path are proven by `timelineLocalSaveHandoff.ts:572–577`, `localSaveSession.ts:168–199`, and `three-products.spec.ts:941–1055`. This is source qualification, not a live P3/browser/service/original/full GO.

D75b/P3 — Candidate retains both automatic-recovery mounts and revises exact counts to observed `A,A,A,A,B` (5) and forwarded `A,A,B` (3), with strict request/key/body/URL/origin/order assertions. C0 §§1,4,5,7; D75b decision 2026-10-24T18:15Z. **PENDING — return review `app-P3-D75b-return-review-1839` FAIL on old control metadata; repaired controls QUALIFIED on donor HEAD, whole-path review `app-P3-D75b-wholepath-final-1843` and home qualification/merge still pending.** Clean return donor `09ae405158bba0d0c1f4bf5502649dea9c04854f`, source blob `8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b`, mounted-recovery blob SHA-256 `10e58e89c0626363c3d99ae40515f09aaabdfade67f5a6d1c2426602304f901b`, applied on parent `830252327fc37b9c68fb7fa9e3d09ad560624fb8`. The three return controls/evidence/patch are retained byte-exact in `app-P3-D75b-controls-return-1831-proposal-controls-v4.mjs`, `app-P3-D75b-controls-return-1831-proposal-evidence-v4.txt`, and `app-P3-D75b-controls-return-1831-proposed-v4.patch` with SHA-256 `e60e7661c2348e0f1e1dc98c0b4af0506d89a26a150059b42959da8ce4f299c3`, `9e8169e3b6481354587464cda0b0fdb924358bdfad742eb009922e866b92e4e9`, `d9f1dfc2c249f5354bba8cf4ace2a8c8a711836552963199b58f036a43a8d634`. No live Runtime/browser/service/original/full receipt or GO is claimed. Control-only repair `app-P3-D75b-controls-sol-1843` verified actual before SHA-256 `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`, unchanged source/mounted hashes above, exact unmodified Git patch, structural mounted assertions and repository direct tsc recipe. Required combined Node controls/helper 7/7, `--lint`, `--types`, `--hashes`, parent/working whitespace and reverse patch check all PASS on existing committed `09ae405158bba0d0c1f4bf5502649dea9c04854f`; only metadata differs. Direct root tsc does not build referenced projects or establish semantic coverage of protected tests. Prior independent mounted 3/3 and neighbors 97/97 were not rerun. Corrected byte-exact artifacts: `app-P3-D75b-controls-sol-1843-proposal-controls-v4.mjs` SHA-256 `eb2ea4bfa53c82dd4efdb73e3fb3afe2c22b47d3b57295412912d90aab6ed5f3`; `app-P3-D75b-controls-sol-1843-proposal-evidence-v4.txt` SHA-256 `408a898211b4d5e1f6b1d28a81ca8c1f4c33550fbbbc30a1b75e45942a9ca183`; `app-P3-D75b-controls-sol-1843-proposed-v4.patch` SHA-256 `79317cfe8bbfacf6f3fd0240b30f8c3c2a96d4f84726bf947855dcda82c6b33c`. No future home receipt or source behavior fix is claimed; prior artifacts remain preserved.

P2-receipt-publication — Request idempotency and receipt publication identities remain distinct; authoritative `receipt.receipt_id` governs history/head/inverse/undo joins; strict v2 and zero-legacy assertions remain retained. C0 §§4, 5 and `commit-v2.md:703–711,1565–1577`. Author `52f1ee5111be78644b4b7d625217bb5dc3b0a54d`, reviewed tree `89ae790b40f928754a53b9120d3c64319d3010cf`; actual merge `0971c645ba113fab54d1da568550542b94f75e6c`, tree `60cdf06f0688066307dd5020567d15a8563baf7e`; current qualified home `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`. Author hashes: P2 spec `2e8fc72bcf29870299a13aab50258a0528f727909125099b53a8aa13bc530a8d` → `67662468d0b4e2951b629154fb30f15764de2b797afe7788a97793872c9cd0e0`; oracle `a0bfad5dfa9c2ae14c36508543ccce00c53d459a5c4c3569198c2411407dfc5f` → `225a4c4358f9c115b04b0aea4e969a9b56fe8a0418450f20bb89eff1cdf47e90`. Current-home continuation hashes: `67662468…` → `07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c`; `225a4c4358…` → `98934eceeb9ac2ae8d6170913abf57ff4503b6f426cfd31739006bbc94d1d272`. Status: PASS for source/merge/home qualification; no live original P2 journey or GO credit.


D75b/P3 — Author app-A2-P3-recovery-current-sol-1910; clean apply app-P3-intermediate-clean-apply-1925; independent review app-P3-intermediate-recovery-review-1920 PASS; actual home e771ce1426022d1a10bab93323d40222c5ce9c3d; exact protected spec SHA-256 8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b → 736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05; one approved intermediate automatic-recovery poll only, preserving both mounts, exact 5-observed/3-forwarded identities/order, all prior waits/timeouts, and downstream B/history/undo/canonical assertions; live original qualification pending disk floor.

D82/P3 — Author app-P3-envelope-artifact-return-2005; independent qualifier app-P3-envelope-qualify-apply-2010; exact normalized recorded-command envelope correction at `tests/e2e/local/three-products.spec.ts:1820`, preserving the raw six-key submitted command, strict thirteen-key recorded command, deep equality, receipt/head/history checks, both recovery mounts, waits/timeouts, and downstream assertions; protected spec SHA-256 `736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05` → `93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b`; exact reviewed patch SHA-256 `80127a0bc4174b8a5b25d9bc34a52d01c712f76a32a1076245ad9547c0846733`; independent qualification PASS and exact clean application PASS; no product source or unrelated test change.


## FAIL — P3 same-ID gate is not gateGO

- Preflight PASS: `app-pin-f6a21c28-p3-intermediate-1933-preflight-1024193926-15980`.
- Normal same-ID run FAIL, exit 1: `app-pin-f6a21c28-p3-intermediate-1933-1024193956-14240`.
- No retry or duplicate submission.
- Readiness: 1/1 PASS, 26.282665s.
- Original Gate 5: 0/1, 1 failure, 103.105087s suite / 75.224s testcase.

Pinned heads:

- App `f6a21c285267d6475816adbda74233907ac93911`, tree `1993e3326e515e0a2801810bf087dc60886388d7`
- Agent `3b2db4bdf9014de013338521dd038ebdecd25f02`, tree `c84907010418e1c0a9ca0d46900c106ba771736e`
- Runtime `42855b6401e6683b157164bc332441ffffdffb06`, tree `d7c2f07832f6d5eba3b6c95831d1a856930edb55`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`

The actual run passed both recovery mounts’ strict five-observed/three-forwarded identity, ordering, origin, and prior-wait checks, then reached merged B and history-count assertions. It failed at `three-products.spec.ts:1820`: history’s authoritative B command contained additional `authorship`, `bindings`, `expect`, `reads`, `resolved`, and `selections` fields absent from the submitted command. No downstream history-closure, preview, Agent, undo, or canonical credit is claimed.

Source/hash checks:

- Actual protected spec hash: `736fd381…e491e05`.
- Approved before/after hashes: `8661fc91…6154315b → 736fd381…e491e05`.
- Exactly one reviewed readiness-poll insertion; D79 harness files match the author-tested commit exactly.
- Node 20 syntax check and `git diff --check`: PASS.
- Bare native-control command failed at setup because Node lacked a TypeScript loader; Node 20 with the existing `--import tsx` loader passed all 3 controls.
- Reused unchanged author evidence: D66 21/21, parser 9/9, setup 3/3, typecheck and scoped lint PASS.

No product, test, pin, generated, registry, or source edits were made. Commit message and `DONE` marker created.


# PASS — D84 placement selector review

Applied the exact published patch to:

`tests/e2e/local/three-products.p2-elements-assets.spec.ts`

The correction qualifies both helper selectors with `occurrenceId`, preserving all waits, geometry, payload, ordering, reload, undo, and closure assertions.

Evidence:

- Node20 retained control: PASS — old selector RED, corrected selectors GREEN, strict sibling/wrong-occurrence/same-bytes negatives GREEN.
- D66 source-only original list: 8 tests in 3 files.
- All 8 isolated selectors: 1 test each.
- D66 neighbor tests: 22/22 PASS.
- TypeScript: PASS.
- ESLint: PASS.
- `git diff --check`: PASS.
- Applied diff byte-identical to published patch: PASS.
- No browser/service/original/full run, per hold and task restrictions.

Hashes:

- Base HEAD: `245742dc778977a8404be2d1a7bc3b8721267416`
- Base tree: `3b83bafa9ff9e4120f5596ddd99cd12a9ddbfd17`
- Patch SHA256: `9302b5346aa661ec989518a0932f98be23a638da69b0e1d240730b09444816be`
- Spec before: `c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797`
- Spec after: `413d314d5788021bd54ae29e03813bfac91e279d5e038d6108cbb3ae18fa4133`

Protected files remained unchanged. Only the target spec is modified.

The existing ledger is outside this worktree under the orchestrator’s `design/` area; the worker rules prohibit writing there. The exact D83/D84 ledger entry should record the above before/after hashes and the preserved predicate map.

Commit message written; `DONE` marker created.
# PASS — P2 batched tour review

Reviewed `d3ecfdd7ba` against `32036b3c`, including 2323 and 2338 changes. No product/source edits made.

Predicate map:

- Parent move: exact full v2 request, project/timeline, base pair, command, UUID step, reads, patch, merge, and source.
- Transition single/bulk: exact `doc.patch`, original-derived `before` values/reads, and authored intents `Clear transitions: <ids>`.
- Undo: exact `timeline.inverse` targeting the accepted receipt, complete envelope, and strict mutation refusals.
- Existing canonical, history, reload, guarded undo, readiness, geometry, waits, ordering, and legacy-route assertions remain intact.
- Bulk `None` assertion remains unchanged.

Exact hashes:

- Tour: `07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c` → `da55dba9476ef35ebd98973b2c3c6eaeea4deaaa73d34f9b2e51eabf7da0277e`
- Oracle: `98934eceeb9ac2ae8d6170913abf57ff4503b6f426cfd31739006bbc94d1d272` → `f6a3fd098693726f9ce562e76d6cd3cd9ce07d66b8ded7b7c1bf800a8fbaf3ab`

Protected six-file map: only the tour changed; P1, popup, elements/assets, base three-products, and mounted-readiness hashes are unchanged.

Tests:

- Node oracle: 13 passed
- Node/app/root TypeScript checks: passed
- Scoped ESLint: passed
- `git diff --check`: passed
- Direct Undo RED/GREEN probe: minimal rejected; complete envelope accepted

Ledger entry: `P2-tour-batched-envelope` — C0-compliant exact parent, transition, and Undo request predicates; strict source-derived guards and authored transition intents preserved; PASS on `d3ecfdd7ba`, ready for normal merge.

No browser/full suite was run per instructions. `DONE` and commit message are present.## PASS — independent P2 popup traffic review

Reviewed `f5052b75d0` against parent `364f124b5c`. No repository source was authored during review.

The Runtime source independently confirms `POST .../inspect` is read-only: it requires `projects:read`, calls `inspect_timeline`, and reads immutable revision closure data without publication/history mutation. App canonical polling calls this exact endpoint with `{ limit: 1 }`.

Predicate coverage:

- Accepts only exact `POST /v1/projects/{project}/timelines/{timeline}/inspect` or mounted `/api/runtime/v1/.../inspect`.
- Rejects query/hash, trailing/sibling/encoded paths, wrong methods, broad prefixes, unknown routes, old save routes, and extra `/commit` routes.
- Requires all classified inspections to return HTTP 200.
- Preserves exact expected request-object equality, POST/`/commit` checks, media-import-only exclusion, canonical/digest/receipt/identity/history/reload/undo/raw-field assertions, and all waits/timeouts.
- The expected commit remains the sole actual film mutation; no synthetic request set was substituted.

Old/new witness: the pre-correction collector is genuinely RED with the seven observed inspect POSTs; the new exact classifier is GREEN. The dedicated adversarial probe also passed.

Checks:

- Node oracle: **3/3 passed**
- Old-RED/new-GREEN predicate probe: **passed**
- `tsc -p tsconfig.app.json --noEmit`: **passed**
- `tsc -p tsconfig.node.json --noEmit`: **passed**
- Scoped ESLint with `--max-warnings=0`: **passed**
- `git diff --check`: **passed**
- Worktree: clean

No browser/service/full suite was run. The retained first wire failed before reload/undo; no later credit is claimed.

Hashes:

- Popup spec: `d68b773a14eccb287fa907c1bde80fb6987c74839e3b869670555a5811534562` → `ab66f693430d62ec537f18d1d6aa7bc211bbc48d2b3fb555ef34dc9ec96a4dea`; final blob `33763eb5435aa6e357a2ff3489a53e23b9487b00`
- Oracle: `38f4edde6519a75a671cbca22249364318ebefd5ccf46a878c0dbb02cbaa7adb` → `07a485d955b82d40d73cb633b228753d99d454d90bf151afc871790fab6e07f5`; final blob `a1b4852b92efb3f0a6ee3e233bb3758833375730`
- Final commit/tree: `f5052b75d00954655d953dc4e38f3b7fed19c7d5` / `fe6cb686cee2c39b4c5450f296f7d352afbff04f`

Six-file protected map: only popup changed; P1, tour, elements/assets, base three-products, and mounted-readiness hashes were unchanged.

Ledger paragraph for `deletion-ledger.app.md`:

> `P2-popup-traffic` — Exact read-only Runtime inspect POST classification added for the mounted canonical-head poll, preserving strict sole-film-commit equality, 200-status inspection checks, old-route/unknown-route negatives, and all canonical, identity, receipt, history, reload, undo, raw-field, wait, and timeout assertions. Independent old-RED/new-GREEN predicate review PASS on `f5052b75d0`; no browser/full-suite credit claimed. The popup spec changed `d68b773a…34562` → `ab66f693…a4dea`; six protected-file map shows only the popup delta.

## PASS

Reviewed `330f7756` against parent `2341a1de` and integrated `fd2f843a`.

- Image helper now offsets by production default preview `5s / 2`, yielding requested start `5` on `parent`.
- Real `useDragCoordinator`/planner regression covers old RED, new GREEN, zoom/scroll, video `20s` compatibility, lane rejection, missing rows, and ambiguous rows.
- Production chain traced through `useExternalDrop` → coordinator/planner → A2 semantic save.
- No product/test edits made by reviewer.
- Protected six hashes unchanged exactly.
- C0 contract request/reply shapes reviewed; no contract impact.

Tests/checks:

- Dedicated Vitest: `6/6 PASS`
- Planner/drop neighbors: `42/42 PASS`
- `tsc -p tsconfig.node.json --noEmit`: PASS
- `tsc -p tsconfig.app.json --noEmit`: PASS
- Scoped ESLint: PASS
- `git diff --check`: PASS
- Worktree clean

Hashes:

- `app.ts` before: `e10998e0eabb69926ab8fc276307d504f2ddcf5d4b76436968b935752cd10e21`
- `app.ts` after: `ae59815ee95f493cfc027fc61e69d2288e2a302e379fda8a26fdf308884451cc`
- Dedicated test: `f099e043032c0169ff006fbfb5adcecbced9912b3049666daf708787196f29e4`

Existing ledger evidence remains: Actual12239 had no commit POST; import returned 201 and selection 200. The first capture guard was not observed and is not claimed.

Commit message and `DONE` marker created.


## PASS

Reviewed commit `62fe238153ada3fd9882a5bea1fa4b3a66811ad0` against parent `50cfedd8890ba4ac0863c6e6bd8d92605f64a42e`.

- Real seeded `plate`/`V2` clips verified; corrected helper resolves V2 start `4.5s`.
- Old arithmetic helper: RED, 4 failures / 49 passed.
- New helper: GREEN, 53/53 tests.
- Zoom, scroll, viewport bounds, and wrong/missing/ambiguous-row rejection covered.
- Original production test body, selectors, payload/request/ownership/closure/reload/Undo/waits remain unchanged except the intended helper/import.
- No product, API, Runtime, or source changes made by reviewer.

Commands:

```text
Node20 Vitest with private config/cache: 53/53 PASS
tsc -p tsconfig.app.json --noEmit: PASS
tsc -p tsconfig.node.json --noEmit: PASS
scoped ESLint --max-warnings=0: PASS
git diff --check: PASS
```

Changed blobs:

```text
three-products.p2-elements-assets.spec.ts
413d314d5788021bd54ae29e03813bfac91e279d5e038d6108cbb3ae18fa4133
→ 2f682662c7761dae13bbc7686c790a65b790849292160a6af30282bf3ed15105

drop-file-geometry.test.ts
f099e043032c0169ff006fbfb5adcecbced9912b3049666daf708787196f29e4
→ 303ba3255f2a101a23673bf3daaa0cd7c8c71504d0b6f470a90e4bc415ffb2b7
```

The other five protected specs are byte-identical. No browser/full/service run was performed; historical actual `8259` attribution remains unclosed.

Commit message and `DONE` marker written.


## PASS

Reviewed exact author commit `0ff988aac6f0e4376c2be3ca53e8cd3979bc2302` against base `50cfedd8890ba4ac0863c6e6bd8d92605f64a42e`.

- Only the two authorized files changed.
- `reads: []` is truthful for native inverse commands: authenticated publication guards remain Runtime-derived; free-transform conservative handling is unchanged.
- Traced mounted Undo/Redo → shared handoff → persisted outbox → `DataProvider.commitTimeline` public client.
- Seven old producer branches were RED and new producer GREEN: accepted, merged, lost ACK, later write, ABA write, history unavailable, and invalid. Legacy-history refusal remains no-send.
- Exact unchanged P2 full-envelope oracle retained, including 11 malformed mutations.

Evidence:

- Vitest: **247/247 passed**
- P2 parent oracle: **13/13 passed**
- App/node TypeScript checks: **passed**
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- Six protected original specs: byte-identical to parent
- No browser, full suite, build, install, or live service run.

Reviewed blobs:

- `timelineLocalSaveHandoff.ts`: `4bce50f28c332c6e28aa4aed635ce80e32e3de52`
- `useTimelineSave.test.tsx`: `5ec79a429784e2492882965f3ca360c8d54869b3`

Merge request submitted and completed:

- Receipt: `5f4ce933ec`
- Integrated `tl/integration` contains both exact blobs.

No blockers. Browser qualification of the pinned parent/single journeys remains the next orchestrator step. `DONE` and `commit-msg` were created.


# PASS — P2 protected selector review and submission

- Reviewed author commit `8200c8bffa` against parent `0bc795f354`; no reviewer source changes.
- Verified actual production projection emits occurrence-qualified DOM IDs while canonical fields retain raw IDs.
- Independent controls passed: old selector RED; exact selector GREEN; wrong occurrence, sibling, and same-asset selectors refused.
- Author neighbor suite: 3 files, 62 tests passed.
- Independent Vitest neighbors: 3 files, 62 passed.
- Popup oracle: 3/3 passed.
- Node20 typechecks: `tsconfig.node.json`, `tsconfig.app.json`, `tsconfig.json` all passed.
- ESLint (`--max-warnings=0`) and `git diff --check` passed.
- Protected source hashes and selector/wait predicates were unchanged except the intended popup selector diff.

Merged normally:

- App integrated HEAD: `c9d71b651dc62be564a1ffdd3974edb455b57854`
- Tree: `12724e8199b0b6efc775fbea1f23252633843189`
- Immutable pins preserved:
  - Agent `0d142f79518ba4ec20eb195657ccc7eb6e903fc3`
  - Runtime `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`
  - Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`

D66 submission:

- Preflight: `app-pin-c9d71b65-p2-selector-add-0042-preflight-1025004929-28266` — PASS
- Body: `app-pin-c9d71b65-p2-selector-add-0042-1025005011-6954` — QUEUED
- Host: `vm`; target: `app-pin-c9d71b65`
- Free space before body: `6,632,067,072` bytes
- Plan: [p2-popup-add-submit-plan.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-ADD-selector-review-submit-0042/submission/p2-popup-add/p2-popup-add-submit-plan.json)

The initial CLI attempt correctly hit D66’s mutable-home guard; I resumed using supported recipe/preflight/registration helpers with the existing immutable pin metadata. No duplicate body was created. Full/body result remains pending; manager should monitor the same body ID.

Created the required commit message and `DONE` marker.


## PASS

Reviewed author commit `b11859b45970330bbe217b3355e9470ab8d09ecd`:

- Tree: `f3e8a51c3214b29d89554c153b80f319b1d4989e`
- Protected blobs:
  - Spec: `f53c9924d8a95743b6b2fe4576a779d60a7e7278`
  - Oracle: `898352551da0d6f605b88447288997310eca6a9b`
  - Oracle tests: `0074b04da471df27eba78b01cadd531915164fec`

The raw helper derives size/digest/MIME from genuine bytes and enforces the closed four-field Runtime ABI. The normalized helper requires exact original `media_id`, `content_sha256`, and `type`, while rejecting raw fields. Both parent and child placement sites use the same helpers; V2/4.5 geometry, semantic commands, closure, registry, history, reload, Undo, and waits remain unchanged.

Mutation controls cover old `content_sha256` raw claims, wrong object/MIME/size/filename, extra/missing raw fields, wrong normalized ID/digest/type, missing normalized digest, and opaque media ID versus digest derivation.

Tests:

- Node 20 oracle + existing controls: **25 passed**
- Vitest semantic/geometry oracle: **7 passed**
- `tsc --noEmit -p tsconfig.json`: passed
- `tsc --noEmit -p tsconfig.app.json`: passed
- `tsc --noEmit -p tsconfig.node.json`: passed
- Scoped ESLint with `--max-warnings=0`: passed
- `git diff --check`: passed

Five other protected specs were byte-identical to base.

Merge requested and completed normally:

- Receipt: `queue/done/merge-app-P2-assets-import-ABI-0038`
- Refused receipt: absent
- Integrated head: `913686448cafbb63dfba5d8053cb725e1140bb07`
- All three integrated blobs exactly match the author blobs.

No browser, service, full suite, or new live acceptance run was performed. Review worktree is clean; `DONE` and commit message were written.


# PASS — A3/P2 core source review

Reviewed `90058e4ff7` against base `913686448c`.

Source trace confirms:

- Popup mounts shared controls through `ShotTimelinePreview`.
- Runtime supplies a stable per-editor `Symbol` owner.
- Controls now use `useTimelineMultiSelect(runtime.agentSelectionOwner)` for display, capture, and async stale-selection guards.
- Projection produces occurrence-qualified IDs: `${occurrenceId}:${rawClipId}`.

Evidence:

- Mounted controls: **11/11 passed**
- Neighbor Vitest suite: **62/62 passed**
- Popup selector oracle: **PASS** — old selector RED; exact target/reference GREEN; wrong occurrence, sibling, and same-byte identities remain distinct/refused.
- `tsconfig.node.json`, `tsconfig.app.json`, `tsconfig.json`: PASS
- Scoped ESLint `--max-warnings=0`: PASS
- `git diff --check`: PASS

Reviewed blobs:

- Product: `9afbf18c4b2ecd8c357c0ee0caa416575c2c639f`
- Test: `444c9249eca75c845a9ad3eb6fd6be452502e84e`

All six protected SHA-256 hashes and popup predicates/waits are unchanged. No product/test files were authored by this reviewer.

Normal merge completed:

- Receipt: `18de74bd43bab71d11188054bd3035016b37ceaa`
- Merged into `tl/integration`
- Merged blobs match exactly.

Existing ledger: prior selector review/merge remains preserved. Historical ADD body `app-pin-c9d71b65...6954` correctly failed at the selected-label predicate; this review claims no browser, history, or Undo rerun.

No next ADD was reserved: placement body `...0062...16952` is terminal `fail`, but other App bodies remain running (`...6629`, `...4151`, `...11089`). `DONE` and commit message were created.


## Diff A — registry0064: FAIL

- Exact author: `4b633d09a796f4c14a2a388c28c46dfc52b055c5`
- Tree: `e248c6fee6c5f6a2008848737a5474e8bb7f7beb`
- Protected blobs matched:
  - Spec `b7ad889b5e492062e70c5fbad6b04cd76758488a`
  - Helper `ac6ecb7f3dc6256d6a4a2099f0aadf889a6e1dc1`
  - Test `f5f9da29dda417a5eeadd2f665dc1c7221871b89`

Finding: lines 518–524 of the spec derive `generationId`/`variantId` from `/media-selection`, then use them as canonical expectations. The authoritative `/media-imports` producer’s generation/variant pair is never cross-checked. A producer swapping those IDs would pass. This violates the requirement for independently source-derived values.

Preserved predicates statically: raw four-field ABI, object/digest/type checks, top-level registry, config absence, old-asset preservation, one-new-asset closure, manifest identity, history/reload/Undo.

Evidence:

- Node20 controls: 25/25
- Vitest semantic/geometry: 18/18
- `tsc --noEmit`: root, app, node passed
- Scoped ESLint: passed
- `git diff --check`: passed
- No browser/service/full-suite run; historical 32587 remains NO-GO

No merge requested for Diff A.

## Diff B — SWAP-11089: PASS

- Exact author: `adf067549915325d5d5c862d59c7e994d8dcd18f`
- Tree: `3091238a3f2afff1002915c9f8f86d4368e49342`
- Blobs:
  - Popup spec `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6`
  - Oracle test `d77ecc3c116453e3b0c1106580f7c5dd905114ea`
  - Unchanged producer `53550b81f0c10322ca360f7205878d602549ae92`

Evidence:

- Popup oracle: 4/4
- A3 producer controls: 37/37
- Playwright list: exactly original ADD and SWAP tests
- Root/app/node TypeScript no-emit: passed
- Scoped ESLint: passed
- Diff and reverse-apply checks: passed

Claims are independently derived from uploaded bytes and pre-save registry, including new/reused aliases and exact occurrence-scoped `created` arrays.

Merge completed: `tl/integration` at `3a2d6067b4`.

No browser/service/full-suite run; original 11089 browser result remains NO-GO.


## Verdicts

- Protected review: **PASS**.
- Normal merge: **PASS** — App commit `37384adf264bf8b44c0ede7e2c39177d06c94dd6`, tree `3f1b5812a983ca240b937ab493e9ded5b1093fb3`.
- Asset submission: **QUEUED/RUNNING**; manager must wait for terminal status.

Reviewed the complete three-file delta from base `4b633d09...` to candidate `41800de9...`. Exact reviewed blobs matched in normal App:

- Spec `54ee61cb...`
- Helper `b955a3b8...`
- Test `da75f00a...`

The prior 0115 failure is corrected: generation/variant identity now comes from the authoritative import producer, while object/digest/MIME derive independently from source bytes.

Source citations:

- Runtime producer emits `generation_id`, `variant_id`, `asset_id`, and raw ABI entry: `runtime_protocol/service.py:5151-5166`.
- Runtime selection returns the closed five-field identity and validates canonical binding: `runtime_protocol/timeline_commit_port.py:827-856`, `922-1021`.
- Production App caller cross-checks import and selection identities: `src/integrations/runtime/dataProvider.ts:1739-1775`.
- App oracle derives producer identity and asserts the exact closed shape: `p2-media-import-oracle.ts:72-105`.
- Parent and child paths preserve raw ABI, normalized identity, registry/config invariants, manifest, reload, history, and guarded Undo: `three-products.p2-elements-assets.spec.ts:510-578`, `589-662`.

## Test evidence

- Node20 controls: **26/26 passed**.
- Semantic/geometry Vitest controls: **18/18 passed**.
- Root, app, and node TypeScript checks with `--noEmit --incremental false`: all passed.
- Scoped ESLint with `--max-warnings=0`: passed.
- `git diff --check`: passed.
- Exact three-file delta and protected blob map: passed.

## Asset submission

Authentic detached checkout receipts verified for:

- App: `/home/user/work/wt/app-pin-37384adf`
- Agent: `/home/user/work/wt/agt-pin-0d142f79`
- Runtime: `/home/user/work/wt/rt-pin-a3cd1a32`
- Composition: `/home/user/work/wt/vw-pin-635f4de0`

Source preflight passed:

`app-pin-37384adf-p2-registry-asset-0130-preflight-1025013528-1359`

Normal body request:

`app-pin-37384adf-p2-registry-asset-0130-1025013558-15897`

Target host: `app-pin-37384adf`  
Persistent plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-registry-return-review-submit-0130/submission/p2-asset/p2-register-asset-submit-plan.json`  
Receipt/result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-37384adf-p2-registry-asset-0130-1025013558-15897`  
Current status: `running`.

No optional reviews were run. No browser/full-suite run was performed. Worker worktree remains clean; `DONE` and the commit message were created.


# Review report

## Native Undo reply

**Verdict: PASS**

- Source: `tl/app-P2-native-Undo-reply-0127`
- Commit/tree: `6107a8cddb21ada1c454be538eb72b2dad38111b` / `6c101596dd6ebcc247266eecefca70d40e3cdf0b`
- Exact checkout: `/home/user/work/wt/app-pin-6107a8cd`
- Reviewed blobs:
  - `three-products.p2-tour.spec.ts`: `62d799a92fca8b98399b6ca5bbd3a06127cd9d86`
  - `p2-parent-oracle.test.mjs`: `c24f9b3dde68e8328cf0ce5571b450bca17099f3`

Verified source-derived labels and steps, exact authoritative patch/dependency metadata, strict wrong/missing/extra metadata failures, native/modern branches, Undo/Redo predicates, request/reply history, and omission-only fallback behavior.

Commands passed:

- Parent oracle: 16 tests
- Transition oracle: 3 tests
- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`
- Scoped ESLint
- `git diff --check`
- Protected-file hashes and exact two-file delta

Normal merge completed:

`4b98436552bf30f5fb28bbb958b1817430b12e34`

The merged blobs exactly match the reviewed source blobs.

## Managed placement

**Verdict: FAIL**

- Source: `tl/app-A3-placement-coordinator-apply-0127`
- Commit/tree: `a90d4251cac526dd2723e037e5c91d4b547dc56a` / `8007f39e5de281f4b47a5b93cf7650b394081e9b`
- Exact checkout: `/home/user/work/wt/app-pin-a90d4251`
- Reviewed blobs:
  - `drop-position.ts`: `48ce58e641b00ca02c26aae4d9533a7d97a633ef`
  - `external-drop-utils.ts`: `a4af7b39ea051ca697b5938191868b390af2b08f`
  - `drop-position.test.ts`: `c8e8dd8c73995faab2db29388ff816bac9a1bc24`
  - `mountedFileDrop.test.tsx`: `a2f8bffc50ea0f2780d314ff0dc6b9274c04444b`

The actual mounted coordinator and asset planner paths were verified. Pointer geometry retains V2 at `(368,54)` and `32px/s`; generic collision remains V3 at `4.5s`; managed image save resolves through `occurrence.add-media` to V2 at `9s`.

The finite blocking finding is hover-preview inconsistency: the real hover indicator uses generic resolved `trackId/time` (V3 at 4.5s), while the committed managed-image path uses `pointerTrackId` and planner settlement (V2 at 9s). This is a concrete preview/commit mismatch, so placement merge was not requested.

Commands passed:

- 99 focused Vitest tests, including the final 25
- All three App typechecks
- Scoped ESLint
- `git diff --check`
- Protected-six exact hashes
- Old-source comparison against the real mounted path

No reviewer source fixes were authored.

## Submission ledger

Placement failed, so no placement merge or P2 body submission was made. There is no body ID, host, or plan to report. The existing native merge remains the only external state change.

Required `DONE` marker and conventional commit message were created.


### A3/P2 managed hover and commit review0209

# A3/P2 Review Report — PASS

Reviewed exact source `f2f5e667...`, including predecessor `a90d4251...`, against clean base `24865fa...`.

Applied only the reviewed six-file delta. Reviewed/applied diff SHA-256:

`59b2a748f081bce266b078723789a9a8aba8c09a39c7afd52b93e43bb5ad1250`

Verified blobs:

- `drop-position.ts`: `b1debc1f...`
- `drop-position.test.ts`: `b504dbdc...`
- `external-drop-utils.ts`: `bd74a756...`
- `useDragCoordinator.ts`: `c5985512...`
- `useExternalDrop.ts`: `33c59dd...`
- `mountedFileDrop.test.tsx`: `81c09f03...`

Evidence:

- Prior controls before product delta: `7 failed, 92 passed` (faithful RED).
- Final focused suite: `7 files, 99 tests passed`.
- Actual coordinator union: `4 files, 37 tests passed`.
- Root/App/Node TypeScript checks: all exit `0`.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected six E2E files unchanged.

Predicate coverage confirms retained pointer `(368,54)` resolves:

- Generic: `V3 @ 4.5s`
- Managed preview and semantic request: `V2 @ 9s`
- Parent: `V1 @ 5s`
- Semantic child command: `occurrence.add-media`
- Stale occurrence/row/media/registry guards remain enforced.
- Video/audio, generic, new-row, and unsupported-provider paths remain unmanaged.

No semantic fixes or protected-file changes were made. No browser/full-suite/service run was performed.

Normal merge receipt is pending harness finalization; no body or external ledger entry was created.
test(app): independently review P2 D96 placement scope

PASS f0c47759b9 against clean base 043631dbab: exact three-file delta,
56 insertions and 8 deletions. The final fixture has 18 direct seed calls:
17 omitted/default-12 calls and one explicit-14 call in the automatic child
placement TestType. The same elements-assets spec keeps element and
registerAsset on default 12; popup, D66, proxy, parent-delete, parent split,
parent trim, mounted trim, shot name, live edit, readiness, tour, main
three-products, track label, and both runtimeRestore calls remain default 12
(runtimeRestore's referenceAt=3 is unrelated). The placement callback body,
title, assertions, request/reply/canonical/history/reload/nativeUndo logic,
and waits are unchanged except for the fixture receiver.

Safe review ledger: no browser, Runtime service, full suite, build, install,
generated file, pin, product, or protected-file mutation was performed.
Node20 placement/receipt controls passed 3/3; D66 Node22 controls passed
24/24; embedded Python AST/compile, 21 native seed assertions, locked App/Node
typechecks, scoped ESLint with zero warnings, diff checks, protected-body
comparison, and all three final blob hashes passed. Node24 was unavailable in
the environment; Node22 was the available D66 control runtime.
# PASS — P2/A3 canonical placement rereview

Applied exact `ddb764adcf` blobs to clean `3199118dce`, preserving D97 adoption files.

- Spec SHA-256: `c75baf23fa743c19c9f4bfa5822aa69c8776188436f82a9c27bbf82431c21845`
- Support SHA-256: `4e1bedd0d4bc721c41f269d5eaba785e0e66bb4d3b81cc8dc29ef72bcabd53f0`
- Only the two assigned files changed.
- `DONE` and commit message created.

Evidence:

- Node controls: **134/134 passed** (`131` receipt, `1` placement receipt, `2` seed-window).
- Saved `a4df` probe: **5/5 invalid mutations accepted**.
- Final `ddb` probe: **0/5 accepted**; all rejected.
- Extra/missing records, wrong owner, fabricated payload, opaque/sibling/prior-row mutations: rejected.
- Root/App/Node TypeScript checks under `.app-tsc.lock`: passed.
- Scoped ESLint with `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected specs, product files, pins, generated files, and vendor kit hashes unchanged.

The projection now derives expected parent/shot/child/manifest/digest identities from original canonical data, intended row/media, and the Agent provider’s deterministic materialization rules. Existing request, history, reload, legacy-route, and native inverse/undo predicates remain intact. No browser, service, build, install, or full suite was run.

Recommended next step: harness commit and normal merge; defer browser/full-suite qualification to the central test service.

> D82/D83/D105a independent protected review PASS: current canonical child → unchanged upstream scoped action → exact occurrence-scoped reload/inverse assertion. Elements spec `36b1e2c9da6a27d74a99f8660e40bb5536c98a38` / SHA-256 `c75baf23fa743c19c9f4bfa5822aa69c8776188436f82a9c27bbf82431c21845` → `00a6fc147d9cd48086aa6726a3c96ae74ab8b53c` / SHA-256 `9b8791e6e3b71155daab01440466987de406b23e2b6269dcc67872cc75c807c7`; receipt control `e06f2d7a0803228e41f582f5bb6fbd9b83200986` / SHA-256 `4e1bedd0d4bc721c41f269d5eaba785e0e66bb4d3b81cc8dc29ef72bcabd53f0` → `719d6a6b9f2a153640c38c02ffadbf914ce6e652` / SHA-256 `8247e9a60d4c46c8ada16dbbf330fd93d8f01d7c59421a11e4e5d7347b7c2f8f`. Original request/reply, closure, media ABI, sibling opaque state, history/receipt, native Undo, waits, budgets, fixture/default, and zero-legacy predicates preserved. Independent controls reject wrong occurrence, sibling physical owner, raw fallback, duplicate, and byte-identical sibling. Old raw inverse passes vacuously with projected residue; fixed inverse is RED until residue is absent, then GREEN. Product/protected-neighbor evidence is byteexact. Candidate owns no Runtime pin changes; the prior pin FAIL was a two-dot comparison artifact. Three-way merge retains normal’s `1daca2a33f6d7b10053e07c539a54843e3984e19` pins. No browser/full-suite credit.

> P2-D113 — Protected placement original closes the reloaded embedded Dialog with the existing real `Close` control after both occurrence-scoped reload-row assertions and asserts the dialog count is zero before parent Undo; this corrects the authored UI sequence identified by Sol0819 while preserving every media/request/reply/canonical/history/reload/Undo predicate, locator, wait, setup, authored input, and product source. D69 comparison shows current `dialog.tsx` and `AstridTimelineEditor.tsx` byte-identical to frozen upstream `3881e9440`, including `modal: true`, so no product regression is implicated. Protected target SHA-256 `9b8791e6e3b71155daab01440466987de406b23e2b6269dcc67872cc75c807c7` → `777966e38459f13dec60a180253f3ed88e83995eee3fdbf81570a86946e78e7e`; the other five protected specs are unchanged. Author-reviewed D69 source hashes and the complete source/predicate map match; focused Node controls (139 passed), App/Node TypeScript, scoped ESLint, diffcheck, and static predicate map PASS; no browser/service/full-suite credit claimed.

D115/P2 independent protected review PASS: e74460003d09262cd30f46bccd3009fb4a321c9d corrects only the App native-asset Undo expectation from a stale whole-parent scope to the C0/D101 exact field union produced by Agent `native_asset_reads` and independently required by Runtime: present `parent.registry` plus absent `parent.config.registry`, with exact paths, refs, states, and values derived from the independent before document. Saved 15712 evidence bounds the original RED to that dependency field while both real commit POSTs, including accepted Undo, were HTTP 200; current Node 20 receipt/neighbour controls, semantic graph/bundle controls, type checks, lint, protected hashes, and D113 byte preservation pass. No product change or isolated successor is authorized; retain the existing ledger entry and take the next proof as the planned full P2 after qualified Runtime release/adoption.

D119 approved parent-readiness correction. Decision: require the `runtime-not-connected` panel to be hidden before any parent gesture begins. The one authorized source addition is `await expect(page.getByTestId('runtime-not-connected')).toBeHidden();` in `openCommandTimeline`, after the existing connected, project, and visible-track checks. Scope is limited to `tests/e2e/local/three-products.p2-tour.spec.ts`; the Playwright logical-hidden predicate rejects the retained-before-down state and is not an opacity or timeout claim. Evidence: candidate commit `f5f26c18daa9e715e0004777a573732c7954ad72` on base `96d4754b4eef0591a208d6b51b60c30fc44b6915`, source blob before `62d799a92fca8b98399b6ca5bbd3a06127cd9d86`, after `63dd04ef1055dbb380642f27f24d47e1fd104625`, exact one-line diff, reverse deletion restores the base bytes, and three audited callers at lines 747, 779, and 799; all other files remain unchanged. Frozen upstream commit `3881e9440688f774878e18806da2dc5c993a9b00` does not contain this spec. D69 upstream gate evidence is qualified by identical provider blob `d7e57cab13b1a37abafa0233f194252667f3913e` / SHA-256 `cf07a243f882591446965e161e20d611bb422a4f0767d3e20955c3d4dc7260f0` and panel blob `2008a4bb89e0bd624cefc90bb5c21a9817520e58` / SHA-256 `7285e0ad6dc9700dfb48483eef0070c15e5ff16723520e2ea718e1dcb4ebc5fd` in both frozen upstream and candidate: the connected app remains inert while the overlay exists, and the panel calls `exit.left` only after settlement and leave timing. The retained nine-frame witness showed connected/visible checks while inert at mouse-down, inert clearing by move completion, unchanged clip/selection, and zero commit POSTs; exact callback/capture, save scheduling, outbox, and Runtime cause remain UNKNOWN. Remaining browser proof is the integrated FULLP2 journey on the merged product; this source review makes no browser GO claim.

### D124 / D126 final protected App review

Source-only PASS for candidate `9d75477be4ab209fed52087f06bfcd20487ce1a9` (tree `7feb5b12a1ad9629f096700c40c393d5b3998217`). Owned blobs: fake-runtime `62a0e80dcd4b70523cbf4490e20cb7fe17518558`; phase-bootstrap `6f21c0c53517f24da5551bee09382f2f37d5f392`. D126 preserves the exact old three predicates: response status 500, JSON code `fake_internal`, and subsequent health status 200, with the throw-purpose title and POST call. D124 independently rejects the prior six predicates plus same-shape private-marker values while accepting the retained reviewed positive capture. Limits are scoped to the committed helper: 8 requests, 128 rolling events, 64 KiB output, 32 phase count, and 20 ms sampling. Normal genuine activation passed. Exact reviewed-helper fresh activation is unqualified because Runtime exited before endpoint readiness; retained parent control reached it and passed. No browser credit and no actual activation/capture GO is claimed.


D141e / A2 D141 REG: approved interface-support-only addition in upstream src/tools/video-editor/lib/shot-group-pack-commands.test.ts adds loadTimelineCommandBasisWithDisplay to the existing RuntimeDataProvider mock. Original blob 4df8a97cac77b3531cec437e5ae1dc98bebddeff -> candidate a073bb4b88ddd9a9216f3bded0e969d41331d33e. Removing only that method restores the original file byte-for-byte and AST-equivalently: every original title, input, assertion, fixture, loader counter, commit-side subtraction, and loads=2 predicate is exact. The mock uses the existing basis reader plus fixture display/version/registry state and rejects pair mismatch; no fabricated version or hidden read subtraction. Production duplicate uses the authenticated combined-reader seam while full closure validation and the fresh revision/publication check remain before owner/intent creation. Independent protected review PASS; targeted shot-group 6/6 and Workspace guards 16/16 PASS. No full/browser/ZIP qualification claim.
| D141d | App P2 automatic child placement | P2 placement expectation updated to the D124 materialization contract. | tests/e2e/local/three-products.p2-elements-assets.spec.ts |

### 2026-10-26T10:14Z — hub-repack (D141o, owner-approved in the app session)

Lossless: 11 batches; loose objects 31180 -> 0 (packed and verified before removal by git prune-packed); free 4641972224 -> 6095323136 B. Repo /home/user/timeline-hub.
