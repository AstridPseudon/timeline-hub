<!-- app | 2026-10-24T02:58:35Z | dispatcher heartbeat 4s | live 5 (sol 1, luna 4, other 0) | busy30 22 | status age 0m -->
# app board, 2026-10-24T02:57Z

| ID | task (short) | model | needs | status | worker | proof | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3 | Upstream editor baseline | Luna | Upstream main | merged | app-U3-final-joined-review-r3 | Baseline reviewed and integrated. Freeze update is separate. | 22bfe5349 |
| U4p | Official client and schema | Luna | U1 and U3 | merged | app-U4p-envelope-review-r2 | Frozen client 34e and schema d106 remain unchanged. | c2a1fab50 |
| A2 | Production save funnel | Sol; Luna review | C0 and U3 | merged | app-A2-final-composed-review-r7 | Original P1 chain passed on pinned f8. Latest bootstrap fix is listed below. | 9eda8e907 |
| A3 | Popup, placement and asset saves | Sol; Luna review | A2 | merged | App and Proof workers | Source qualifications passed. P2 live gesture proof remains pending. | See linked proofs |
| P1 | Original mixed chain | App runner; Proof review | Resolved | merged | Test 18792; Proof 0036 and 0040 | GO at 00:43. Both cases passed; exit 0, 141 seconds. Fixed App f8 / Agent 787 / Runtime 2a9. | f8b15af0a6 |
| A4 | Executor and capture retirement | Luna; Sol author | P1 GO and D37 | doing | Recovery review 0222; basis fix 0224 | Exports and lifecycle merged. Remaining recovery guards and final reachable-path cuts continue. | 5ad7907e86 |
| A2-staged-caller | Move staged generation onto current save | Sol; Luna review | Review 0133 PASS | merged | app-A2-staged-caller-sol-0122 | Independent 279 tests, three types and lint passed. Integrated joined proof 0150 passed 448 tests, three types and lint. | 9969949827 / e9bce18bea |
| A4-state | Retire state transaction runner API | Luna | Review 0142 PASS | merged | app-A4-state-runner-retirement-0135 | Independent 175 tests, three types and lint passed. Integrated source follow-up will include current media-wrapper cut. | ce7a48e137 / 1f4b30a51b |
| A4-history | Retire history runner execution | Luna | Review 0131 PASS | merged | app-A4-history-retirement-0125 | Independent 95 tests, three types and lint passed. Mounted guarded Runtime undo retained; joined proof 0150 passed 448 tests, three types and lint. | b2a546f535 / 0a0f95efc7 |
| A4-session-tests | Move five protocol tests to current save | Luna | Review 0123 and proof 0129 PASS | merged | Proof app-A4-preview-session-integrated-0129 | Five cases retained. Joined preview/session proof passed 136 tests, three types and lint on 8bd7. | 039fc35ed7 / 8bd7d59e19 |
| A4-dormant-scope | Record dormant raw and track subsets | Luna | D37 applied | merged | app-A4-D37-wording-0222 | Both exact worker records copied into existing App and combined ledgers. Implementations and tests unchanged. | Documentation only |
| A4-reviewed-stack | Ports and mounted witnesses | Luna | Review 0105 and integrated 0115 PASS | merged | app-A4-mounted-fixture-return-0059 | Independent and integrated 111 plus 33 tests passed on exact93d487. Types/lint passed; mocked authority limit retained. | 93d48799a2 |
| A2-bootstrap-fix | Restart cancelled bootstrap | Sol; Luna review | Resolved | merged | app-A2-basis-cancel-repro-sol-0029 | [326 tests, three typechecks and lint passed.](/home/user/timeline-hub/hub/design/app-A2-bootstrap-integrated-0046.md) | 804134d747 |
| readiness-after-bootstrap | Bind qualified Runtime history fix | Sol; Luna review | Exact backend custody | doing | App caller Sol 0250; Runtime review 0245 | Runtime 37eb independently passed 145 with Agent 4151. Old 079 transcript failure retained. Actual child 0256 passed; matching Remotion registration 0258 queued; caller controls active. | Runtime proof pin 37eb6c7bdb |
| P-door-port-alloc | Allocate door port per run | Luna; D21 | Resolved | merged | app-P2-P3-door-allocation-0039 | [Node 20 allocation, shared stage value and failure checks passed.](/home/user/timeline-hub/hub/design/app-P2-P3-door-allocation-0039.md) | Harness rows only |
| readiness-upstream-check | Check f38e candidate | Sol; Luna review | Review 0057 PASS | merged | App Sol 0046; Luna 0057 | No census or attempt-root signature supports attribution. Exact patch is unavailable locally; historical cause remains unknown. | Report only |
| P2 | Eight original gesture cases | App service; Proof verdict | D41 source and actual backend custody | doing | app-readiness-D41-caller-sol-0250 | Prior 10973: exit 2, 189 seconds; all eight NOT RUN. Prepare one changed run with compatible Runtime 37eb; no new request yet. | App 804134d747 |
| P3 | Original Gate-5 journey | App service; Proof verdict | D41 source and actual backend custody | doing | app-readiness-D41-caller-sol-0250 | Prior 14249: exit 2, 194 seconds; Gate-5 NOT RUN. Prepare one changed run alongside P2 with Runtime 37eb; no new request yet. | App 804134d747 |
| A2-parent-media-closure | Preserve untouched child closure | Sol; Luna review | Resolved | merged | app-A2-parent-media-integrated-0035 | [299 tests, types, lint and external producer passed.](/home/user/timeline-hub/hub/design/app-A2-parent-media-integrated-0035.md) | 1b0428db7d |
| A2-image-created | Declare genuine image creations | Sol; Luna review | Review 0133 PASS | merged | app-A2-image-created-sol-0126 | Independent 261 tests and producer 28, three types and lint passed. Clip and new authored registry alias claims match provider. Joined proof 0150 passed 448 tests, three types and lint. | b3a84dea71 / 1c5cc47bf6 |
| A4-image-live | New authenticated image witness | App producer; Agent fixture | Agent boundary classification | doing | Agent witness 0154 | Request reached Runtime before deadline and has an accepted response. A later command-equality assertion failed; reopen and inverse remain unproven. | Fixed 1c5cc47bf6 |
| A2-video-caller | Normalized video duplication | Sol; Luna review | Resolved | merged | app-A2-video-integrated-2350 | 217 integrated tests and three typechecks passed. Agent provider is merged; no old raw-positive parity claim. | a714a4cc11 |
| U3b-draft | Final upstream composition | Sol; Luna review | P2/P3 and final freeze | gated:freeze | app-U3b-current-join-2053 | Reviewed branch stays isolated. Refresh live upstream refs at freeze; do not merge during pinned proof. | Branch only |
| F-App-full | Full suite before retirement | Test service; Luna review | Resolved for historical head | merged | app-F-D19-current-full-1230 | 18,819 tests passed on exact 12ef. A final qualification follows actual retirement and freeze. | 12ef320545 |

| A4-lifecycle-tests | Move close and recovery protocol cases | Luna | Cumulative review 0208 PASS | merged | app-A4-exports-lifecycle-current-0213 | 105 tests, three typechecks and lint passed on current packet. Actual exclusive-lock witness retained. | b7261d56fd / 5ad7907e86 |
| A4-unused-goldens | Delete two unused parity scripts | Luna | Review 0150 PASS | merged | app-A4-unused-goldens-0140 | Independent zero-consumer census, fixture integrity and three types passed. Source merged; next joined check covers integrated types. | ae91c2ee0f / 4b7786fb88 |
| A2-A4-joined-proof | Qualify staged, image and history join | Luna | Three reviewed merges | merged | app-A2-A4-current-integrated-0150 | Exact 1c5cc47bf6 passed 448 tests across 16 files, three types and lint. No Runtime or browser acceptance claimed. | 1c5cc47bf6 |

| A4-media-wrappers | Retire unused media executor wrappers | Luna | Reviewed packet PASS | merged | app-A4-media-wrappers-current-packet-0205 | Four exact reviewed blobs; 108 tests, three typechecks and governance passed. | 7987a0b0dc / 9e5d1bb791 |

| A4-owner-recovery-tests | Move explicit owner recovery cases | Luna | Independent review and current packet PASS | merged | app-A4-owner-current-packet-0226 | Independent review and current packet each passed 105 tests, three typechecks and lint. Genuine outbox lock behavior retained. | 69d10d65ff / 78d05b8a36 |

| A4-public-executor | Remove executor value exports | Luna | Review 0208 PASS | merged | app-A4-exports-lifecycle-current-0213 | 108 tests, three typechecks and governance passed. Exact reviewed exports copied; test-only runner remains. | b7261d56fd / 5ad7907e86 |
| readiness-client-confirmation | Compare history cardinality and wait | Sol; Luna review | Existing 0121 and 0128 PASS | merged | App Sol 0121; Luna 0128 | Both histories have two entries; full child closure and seed command count differ. Browser request count unknown. Reply 0200 published. | Report only |



Safety: Historical cleanup, graph and publication denials stand. Managers write boards, briefs and shared reports; workers own product changes.
Delivery legacy subset: Keep transcriptAssociateCapture.ts and its unchanged 397-line, 40-assertion test, plus required helpers, under D31.
Evidence: [P1 result](/home/user/timeline-hub/hub/design/app-P1-18792-result-handoff-0029.md), [image review](/home/user/timeline-hub/hub/design/app-A2-image-created-review-0133.md), [A4 cut map](/home/user/timeline-hub/hub/design/app-A4-current-cut-census-0042.md).

| A2-recovery-basis | Preserve seven dependent recovery guards | Sol; Luna review | Independent 0240 and current proof PASS | merged | app-A2-recovery-basis-current-0250 | Exact reviewed current packet passed 106 tests, three types and lint; merged at dbde9cc37d. | 499a791db7 / dbde9cc37d |
| A4-remaining-protocol | Map remaining legacy protocol cases | Luna | Read-only map complete | merged | app-A4-remaining-protocol-map-0226 | Remaining cases mapped into bounded current-save packets. Six chain and six label declarations are now assigned. | Report only |
| A4-protocol-chain | Move faithful local chain declarations | Luna | First return completed | review | app-A4-chain-return-review-0257 | Author 138 tests, three types and lint passed. Manifest-corruption original kept unchanged where mapping is missing. | Return branch only |
| A4-track-label | Move faithful label protocol declarations | Luna | First return completed | review | app-A4-label-return-review-0257 | Author 215 tests, three types and lint passed. Presence/remove and remote oracle originals retained. | Return branch only |
| A4-replay-protocol | Move one faithful replay declaration | Luna | Independent 0249 PASS | doing | app-A4-replay-current-packet-0257 | Review passed 124 tests, three types and lint. Current own-only packet queued; five unmappable originals retained unchanged. | 6585ad99e3 donor |
| A4-label-refusals | Move three equivalent label refusals | Luna | Independent 0252 PASS | doing | app-A4-label-refusal-current-0257 | Independent 124 tests, three types and lint passed. Three original ownership, basis and mixed-preview cases kept unchanged. Current packet queued. | 594ce7ba8a donor |
| readiness-backend-bench | Exact compatible backend child custody | Dispatcher; App caller | Actual keyed child receipt | doing | child app-ready-079-37eb-0256 | Exact 37eb checkout verified. Normal child 0256 passed with exact installed backend. Remotion reuse registration 0258 queued for matching Runtime identity. | Runtime 37eb6c7bdb |

Blockers: U3b awaits P2/P3 and the final freeze.
Blockers: App caller 0250 awaits actual keyed child receipt for qualified Runtime 37eb and Agent 079. Then submit the one changed P2/P3 pair; Proof owns verdict.

Next ready: Bind D41 actual backend custody first, consume current recovery merge, and qualify the reviewed protocol packets without weakening retained originals.
Integration: dbde9cc37d. Current recovery packet passed 106 tests, three types and lint before its exact merge. Exports and lifecycle joined proof passed 108 plus 105 tests, three types, lint and governance. Historical joined proof 0150 remains bound to 1c5cc47bf6.
Disk: About 11 GB free. Recycle refused two dirty old U3 trees; both retained. Finished protocol tree was already recycled. Sweep completed with zero eligible directories; prior compact refusal stands. No cleanup refusal retried.
