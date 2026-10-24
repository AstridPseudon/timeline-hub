<!-- app | 2026-10-24T01:13:30Z | dispatcher heartbeat 7s | live 5 (sol 2, luna 3, other 0) | busy30 19 | status age 1m -->
# app board, 2026-10-24T01:14Z

| ID | task (short) | model | needs | status | worker | proof | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3 | Upstream editor baseline | Luna | Upstream main | merged | app-U3-final-joined-review-r3 | Baseline reviewed and integrated. Freeze update is separate. | 22bfe5349 |
| U4p | Official client and schema | Luna | U1 and U3 | merged | app-U4p-envelope-review-r2 | Frozen client 34e and schema d106 remain unchanged. | c2a1fab50 |
| A2 | Production save funnel | Sol; Luna review | C0 and U3 | merged | app-A2-final-composed-review-r7 | Original P1 chain passed on pinned f8. Latest bootstrap fix is listed below. | 9eda8e907 |
| A3 | Popup, placement and asset saves | Sol; Luna review | A2 | merged | App and Proof workers | Source qualifications passed. P2 live gesture proof remains pending. | See linked proofs |
| P1 | Original mixed chain | App runner; Proof review | Resolved | merged | Test 18792; Proof 0036 and 0040 | GO at 00:43. Both cases passed; exit 0, 141 seconds. Fixed App f8 / Agent 787 / Runtime 2a9. | f8b15af0a6 |
| A4 | Executor and capture retirement | Sol; Luna review | P1 GO: resolved | doing | Sol 0112; Luna 0110 | Scalar cut is in review. Live preview dependency is being removed. Remaining capture and golden assertions stay. | 84330da5fd branch |
| A4-reviewed-stack | Ports and mounted witnesses | Luna | Review 0105 PASS | merging | app-A4-mounted-fixture-return-0059 | Independent 111 plus 33 tests, three types and lint passed. Integrated proof 0115 is active. | 93d48799a2 |
| A2-bootstrap-fix | Restart cancelled bootstrap | Sol; Luna review | Resolved | merged | app-A2-basis-cancel-repro-sol-0029 | [326 tests, three typechecks and lint passed.](/home/user/timeline-hub/hub/design/app-A2-bootstrap-integrated-0046.md) | 804134d747 |
| readiness-after-bootstrap | Verified basis read does not finish | Sol; Luna review | Retained changed pair | doing | Sol 0113; review 0105 | P2 restarted its read; both runs stop at the outbox wait. History requests have no captured response. Server cause unknown; no further run. | Fixed 804134d747 |
| P-door-port-alloc | Allocate door port per run | Luna; D21 | Resolved | merged | app-P2-P3-door-allocation-0039 | [Node 20 allocation, shared stage value and failure checks passed.](/home/user/timeline-hub/hub/design/app-P2-P3-door-allocation-0039.md) | Harness rows only |
| readiness-upstream-check | Check f38e candidate | Sol; Luna review | Review 0057 PASS | merged | App Sol 0046; Luna 0057 | No census or attempt-root signature supports attribution. Exact patch is unavailable locally; historical cause remains unknown. | Report only |
| P2 | Eight original gesture cases | App service; Proof verdict | Qualified fixed caller | doing | Test 10973; cause Sol 0105 | Exit 2 after 189 seconds. Native and history passed; bootstrap outbox wait failed. All eight original cases NOT RUN. Review 0105 active. | Fixed 804134d747 |
| P3 | Original Gate-5 journey | App service; Proof verdict | Qualified fixed caller | doing | Test 14249; cause Sol 0105 | Exit 2 after 194 seconds. Native and history passed; bootstrap outbox wait failed. Original Gate-5 NOT RUN. Review 0105 active. | Fixed 804134d747 |
| A2-parent-media-closure | Preserve untouched child closure | Sol; Luna review | Resolved | merged | app-A2-parent-media-integrated-0035 | [299 tests, types, lint and external producer passed.](/home/user/timeline-hub/hub/design/app-A2-parent-media-integrated-0035.md) | 1b0428db7d |
| A4-image-live | New authenticated image witness | App producer; Agent fixture | Agent same-fixture acceptance | doing | app-A4-image-current-producer-0059 | Output published before deadline: 1,371 bytes, hash b9f9b3c5. Exact new selection and raw opaque location preserved; App made no Runtime call. | 22efcda3da |
| A2-video-caller | Normalized video duplication | Sol; Luna review | Resolved | merged | app-A2-video-integrated-2350 | 217 integrated tests and three typechecks passed. Agent provider is merged; no old raw-positive parity claim. | a714a4cc11 |
| U3b-draft | Final upstream composition | Sol; Luna review | P2/P3 and final freeze | gated:freeze | app-U3b-current-join-2053 | Reviewed branch stays isolated. Refresh live upstream refs at freeze; do not merge during pinned proof. | Branch only |
| F-App-full | Full suite before retirement | Test service; Luna review | Resolved for historical head | merged | app-F-D19-current-full-1230 | 18,819 tests passed on exact 12ef. A final qualification follows actual retirement and freeze. | 12ef320545 |

Blockers: U3b awaits P2/P3 and the final freeze.
Blockers: App owns the unfinished verified history read. Sol 0113 diagnoses source; review 0105 checks retained evidence. No further P2/P3 run.
Next ready: Consume readiness review and source diagnosis, scalar cut review and preview cut. Qualify the merged fixture on integration. Await Agent image result.
Integration: 93d48799a2. Changed readiness experiments used fixed 804134d747. No source-head chase or repeat is authorised.
Disk: Four clean finished worktrees recycled; exact byte delta was not recorded. Last available space: 12.06 GB. No protected or previously refused paths were touched.
Safety: Historical cleanup, graph and publication denials stand. Managers write only boards, briefs and shared reports; workers own product changes.
Delivery legacy subset: Keep transcriptAssociateCapture.ts and its unchanged 397-line, 40-assertion test, plus required helpers, under D31.
Evidence: [P1 result](/home/user/timeline-hub/hub/design/app-P1-18792-result-handoff-0029.md), [bootstrap review](/home/user/timeline-hub/hub/design/app-A2-basis-cancel-review-0041.md), [A4 cut map](/home/user/timeline-hub/hub/design/app-A4-current-cut-census-0042.md).
