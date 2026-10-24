<!-- app | 2026-10-24T02:22:43Z | dispatcher heartbeat 77s | live 2 (sol 1, luna 1, other 0) | busy30 19 | status age 6m -->
# app board, 2026-10-24T02:06Z

| ID | task (short) | model | needs | status | worker | proof | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3 | Upstream editor baseline | Luna | Upstream main | merged | app-U3-final-joined-review-r3 | Baseline reviewed and integrated. Freeze update is separate. | 22bfe5349 |
| U4p | Official client and schema | Luna | U1 and U3 | merged | app-U4p-envelope-review-r2 | Frozen client 34e and schema d106 remain unchanged. | c2a1fab50 |
| A2 | Production save funnel | Sol; Luna review | C0 and U3 | merged | app-A2-final-composed-review-r7 | Original P1 chain passed on pinned f8. Latest bootstrap fix is listed below. | 9eda8e907 |
| A3 | Popup, placement and asset saves | Sol; Luna review | A2 | merged | App and Proof workers | Source qualifications passed. P2 live gesture proof remains pending. | See linked proofs |
| P1 | Original mixed chain | App runner; Proof review | Resolved | merged | Test 18792; Proof 0036 and 0040 | GO at 00:43. Both cases passed; exit 0, 141 seconds. Fixed App f8 / Agent 787 / Runtime 2a9. | f8b15af0a6 |
| A4 | Executor and capture retirement | Luna; Sol author | P1 GO | doing | State review 0142; lifecycle 0139; goldens review 0150 | Preview, session, history and staged changes are merged. State and lifecycle cuts continue; joined proof 0150 passed 448 tests, three types and lint. | See cut rows |
| A2-staged-caller | Move staged generation onto current save | Sol; Luna review | Review 0133 PASS | merged | app-A2-staged-caller-sol-0122 | Independent 279 tests, three types and lint passed. Integrated joined proof 0150 passed 448 tests, three types and lint. | 9969949827 / e9bce18bea |
| A4-state | Retire state transaction runner API | Luna | Review 0142 PASS | merged | app-A4-state-runner-retirement-0135 | Independent 175 tests, three types and lint passed. Integrated source follow-up will include current media-wrapper cut. | ce7a48e137 / 1f4b30a51b |
| A4-history | Retire history runner execution | Luna | Review 0131 PASS | merged | app-A4-history-retirement-0125 | Independent 95 tests, three types and lint passed. Mounted guarded Runtime undo retained; joined proof 0150 passed 448 tests, three types and lint. | b2a546f535 / 0a0f95efc7 |
| A4-session-tests | Move five protocol tests to current save | Luna | Review 0123 and proof 0129 PASS | merged | Proof app-A4-preview-session-integrated-0129 | Five cases retained. Joined preview/session proof passed 136 tests, three types and lint on 8bd7. | 039fc35ed7 / 8bd7d59e19 |
| A4-dormant-scope | Record dormant raw and track subsets | Luna | D37 decision received | doing | app-A4-D37-delivery-record-0216 | D37 says keep both implementations and tests unchanged. Draft two records for the existing App deletion ledger; no provider migration. | No product change |
| A4-reviewed-stack | Ports and mounted witnesses | Luna | Review 0105 and integrated 0115 PASS | merged | app-A4-mounted-fixture-return-0059 | Independent and integrated 111 plus 33 tests passed on exact93d487. Types/lint passed; mocked authority limit retained. | 93d48799a2 |
| A2-bootstrap-fix | Restart cancelled bootstrap | Sol; Luna review | Resolved | merged | app-A2-basis-cancel-repro-sol-0029 | [326 tests, three typechecks and lint passed.](/home/user/timeline-hub/hub/design/app-A2-bootstrap-integrated-0046.md) | 804134d747 |
| readiness-after-bootstrap | Verified basis read does not finish | Sol; Luna review | Runtime uninstrumented cost | blocked:runtime | rt-R-readiness-auth-cost-sol-0155 | All 18 probe requests completed. Native history took about six seconds with wrappers. Historical hang cause remains unknown; no P2/P3 rerun. | Fixed 804134d747 |
| P-door-port-alloc | Allocate door port per run | Luna; D21 | Resolved | merged | app-P2-P3-door-allocation-0039 | [Node 20 allocation, shared stage value and failure checks passed.](/home/user/timeline-hub/hub/design/app-P2-P3-door-allocation-0039.md) | Harness rows only |
| readiness-upstream-check | Check f38e candidate | Sol; Luna review | Review 0057 PASS | merged | App Sol 0046; Luna 0057 | No census or attempt-root signature supports attribution. Exact patch is unavailable locally; historical cause remains unknown. | Report only |
| P2 | Eight original gesture cases | App service; Proof verdict | Shared readiness cause | blocked:runtime | Test 10973; Proof review 0126 PASS | Exit 2 after 189 seconds. Native and history passed; outbox basis read failed. All eight original gestures NOT RUN. No rerun. | Fixed 804134d747 |
| P3 | Original Gate-5 journey | App service; Proof verdict | Shared readiness cause | blocked:runtime | Test 14249; Proof review 0126 PASS | Exit 2 after 194 seconds. Native and history passed; outbox basis read failed. Original Gate-5 NOT RUN. No rerun. | Fixed 804134d747 |
| A2-parent-media-closure | Preserve untouched child closure | Sol; Luna review | Resolved | merged | app-A2-parent-media-integrated-0035 | [299 tests, types, lint and external producer passed.](/home/user/timeline-hub/hub/design/app-A2-parent-media-integrated-0035.md) | 1b0428db7d |
| A2-image-created | Declare genuine image creations | Sol; Luna review | Review 0133 PASS | merged | app-A2-image-created-sol-0126 | Independent 261 tests and producer 28, three types and lint passed. Clip and new authored registry alias claims match provider. Joined proof 0150 passed 448 tests, three types and lint. | b3a84dea71 / 1c5cc47bf6 |
| A4-image-live | New authenticated image witness | App producer; Agent fixture | Output published | doing | App producer 0206; Agent fixture 0154 | Exact 1492-byte output af1a9a84 published at 02:08 from new input c0a3b657. Agent owns same-fixture Runtime acceptance. | Fixed 1c5cc47bf6 |
| A2-video-caller | Normalized video duplication | Sol; Luna review | Resolved | merged | app-A2-video-integrated-2350 | 217 integrated tests and three typechecks passed. Agent provider is merged; no old raw-positive parity claim. | a714a4cc11 |
| U3b-draft | Final upstream composition | Sol; Luna review | P2/P3 and final freeze | gated:freeze | app-U3b-current-join-2053 | Reviewed branch stays isolated. Refresh live upstream refs at freeze; do not merge during pinned proof. | Branch only |
| F-App-full | Full suite before retirement | Test service; Luna review | Resolved for historical head | merged | app-F-D19-current-full-1230 | 18,819 tests passed on exact 12ef. A final qualification follows actual retirement and freeze. | 12ef320545 |

| A4-lifecycle-tests | Move close and recovery protocol cases | Luna | Review 0154 FAIL | doing | app-A4-lifecycle-return-0202 | First return replaces a no-op lock witness with a genuine held exclusive claim. Other mappings, 105 tests, types and lint pass. | 59654edbb8 held |
| A4-unused-goldens | Delete two unused parity scripts | Luna | Review 0150 PASS | merged | app-A4-unused-goldens-0140 | Independent zero-consumer census, fixture integrity and three types passed. Source merged; next joined check covers integrated types. | ae91c2ee0f / 4b7786fb88 |
| A2-A4-joined-proof | Qualify staged, image and history join | Luna | Three reviewed merges | merged | app-A2-A4-current-integrated-0150 | Exact 1c5cc47bf6 passed 448 tests across 16 files, three types and lint. No Runtime or browser acceptance claimed. | 1c5cc47bf6 |

| A4-media-wrappers | Retire unused media executor wrappers | Luna | Cumulative review and exact packet PASS | merging | app-A4-media-wrappers-current-packet-0205 | Exact four reviewed blobs, 108 tests, three types and governance passed on current base. One own commit queued. | 7987a0b0dc |

| A4-owner-recovery-tests | Move explicit owner recovery cases | Luna | Review 0202 HOLD | doing | app-A4-owner-recovery-return-0210 | First return moves lock assertions from a preemptive owner set to actual outbox exclusive-lock acquisition. Other mapping and 105 tests pass. | 8f92a51e3a held |

| A4-public-executor | Remove executor value exports | Luna | Author 0203 PASS | review | app-A4-public-executor-review-0208 | 108 tests, three types and governance passed. Only executor value exports and matching inventory removed; test-only runner remains. | Branch only |
| readiness-client-confirmation | Compare history cardinality and wait | Sol; Luna review | Existing 0121 and 0128 PASS | merged | App Sol 0121; Luna 0128 | Both histories have two entries; full child closure and seed command count differ. Browser request count unknown. Reply 0200 published. | Report only |

Blockers: U3b awaits P2/P3 and the final freeze.

Blockers: Runtime Sol 0155 owns uninstrumented history cost and guard-preserving source assessment. Historical hang remains unknown; P2/P3 stay held.

Next ready: Consume lifecycle and executor reviews, owner-recovery return and wrapper merge. Agent has the exact image output. Runtime cost source is in review; P2/P3 remain held.
Integration: 9e5d1bb791; reviewed media-wrapper packet is also merged. Joined proof 0150 stays bound to exact 1c5cc47bf6. History, staged caller and image created claims are merged. Changed readiness experiments remain fixed at 804134d747.
Disk: Available 11.79 GB. Eight finished worker trees were already recycled, so recycling freed 0 GB. Sweep removed three old temporary directories and freed about 139 MiB. Protected and refused paths stayed untouched.
Safety: Historical cleanup, graph and publication denials stand. Managers write boards, briefs and shared reports; workers own product changes.
Delivery legacy subset: Keep transcriptAssociateCapture.ts and its unchanged 397-line, 40-assertion test, plus required helpers, under D31.
Evidence: [P1 result](/home/user/timeline-hub/hub/design/app-P1-18792-result-handoff-0029.md), [image review](/home/user/timeline-hub/hub/design/app-A2-image-created-review-0133.md), [A4 cut map](/home/user/timeline-hub/hub/design/app-A4-current-cut-census-0042.md).
