<!-- app | 2026-10-24T00:59:44Z | dispatcher heartbeat 7s | live 3 (sol 1, luna 2, other 0) | busy30 18 | status age 0m -->
# app board, 2026-10-24T00:59Z

| ID | task (short) | model | needs | status | worker | proof | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3 | Upstream editor baseline | Luna | Upstream main | merged | app-U3-final-joined-review-r3 | Baseline reviewed and integrated. Freeze update is separate. | 22bfe5349 |
| U4p | Official client and schema | Luna | U1 and U3 | merged | app-U4p-envelope-review-r2 | Frozen client 34e and schema d106 remain unchanged. | c2a1fab50 |
| A2 | Production save funnel | Sol; Luna review | C0 and U3 | merged | app-A2-final-composed-review-r7 | Original P1 chain passed on pinned f8. Latest bootstrap fix is listed below. | 9eda8e907 |
| A3 | Popup, placement and asset saves | Sol; Luna review | A2 | merged | App and Proof workers | Source qualifications passed. P2 live gesture proof remains pending. | See linked proofs |
| P1 | Original mixed chain | App runner; Proof review | Resolved | merged | Test 18792; Proof 0036 and 0040 | GO at 00:43. Both cases passed; exit 0, 141 seconds. Fixed App f8 / Agent 787 / Runtime 2a9. | f8b15af0a6 |
| A4 | Executor and capture retirement | Luna | P1 GO: resolved | doing | app-A4-retirement-sol-0102 | Luna 0051 produced only a type cut on the old base. Current ports are removed. Sol is authoring the remaining retirement; assertions stay. | 7135ac722a |
| A4-reviewed-stack | Ports and mounted witnesses | Luna | P1 GO: resolved | merged | app-A4-mounted-fixture-return-0059 | 6e04, da7f25, 001145 and cf05 each had independent PASS. Integrated checks found six old fixtures missing media selection. Return 0059 is fixing setup; guards stay. | 7135ac722a |
| A2-bootstrap-fix | Restart cancelled bootstrap | Sol; Luna review | Resolved | merged | app-A2-basis-cancel-repro-sol-0029 | [326 tests, three typechecks and lint passed.](/home/user/timeline-hub/hub/design/app-A2-bootstrap-integrated-0046.md) | 804134d747 |
| readiness-after-bootstrap | Shared P2/P3 readiness failure | Sol; Luna review | Fixed source and caller checks | doing | app-P2-P3-fixed-source-caller-sol-0053 | Cleanup left started=true after cancellation. Fixed and reviewed. Historical trigger remains unknown; one changed run is authorised. | 42db156ede |
| P-door-port-alloc | Allocate door port per run | Luna; D21 | Resolved | merged | app-P2-P3-door-allocation-0039 | [Node 20 allocation, shared stage value and failure checks passed.](/home/user/timeline-hub/hub/design/app-P2-P3-door-allocation-0039.md) | Harness rows only |
| readiness-upstream-check | Check f38e candidate | Sol; Luna review PASS | Retained 18800 and 458 evidence | review | App Sol 0046; Luna 0057 | No census or attempt-root signature found. No direct host dependency in basis/history path. Independent review agrees: evidence cannot attribute historical cause. | Report only |
| P2 | Eight original gesture cases | App service; Proof verdict | Qualified fixed caller | ready | Caller 0053 preparing fixed 804 | Prior 18800 stopped at readiness; all eight cases were not run. One changed run is authorised; no port-only retry. | Fixed 804134d747 |
| P3 | Original Gate-5 journey | App service; Proof verdict | Qualified fixed caller | ready | Caller 0053 preparing fixed 804 | Prior 458 stopped at readiness. Original body remains unchanged. One changed run is authorised. | Fixed 804134d747 |
| A2-parent-media-closure | Preserve untouched child closure | Sol; Luna review | Resolved | merged | app-A2-parent-media-integrated-0035 | [299 tests, types, lint and external producer passed.](/home/user/timeline-hub/hub/design/app-A2-parent-media-integrated-0035.md) | 1b0428db7d |
| A4-image-live | New authenticated image witness | App producer; Agent fixture | Live input received; deadline 01:08:46Z | doing | app-A4-image-current-producer-0059 | New input 09f4afbb is ready. The unchanged producer is dispatched on qualified 22ef; output goes to Agent for same-fixture acceptance. | 22efcda3da |
| A2-video-caller | Normalized video duplication | Sol; Luna review | Resolved | merged | app-A2-video-integrated-2350 | 217 integrated tests and three typechecks passed. Agent provider is merged; no old raw-positive parity claim. | a714a4cc11 |
| U3b-draft | Final upstream composition | Sol; Luna review | P2/P3 and final freeze | gated:freeze | app-U3b-current-join-2053 | Reviewed branch stays isolated. Refresh live upstream refs at freeze; do not merge during pinned proof. | Branch only |
| F-App-full | Full suite before retirement | Test service; Luna review | Resolved for historical head | merged | app-F-D19-current-full-1230 | 18,819 tests passed on exact 12ef. A final qualification follows actual retirement and freeze. | 12ef320545 |

Blockers: Proof awaits caller 0053 before the one authorised changed P2/P3 run on App’s service. Node 20 hook check 0103 is running.
Blockers: U3b awaits P2/P3 and the final freeze.
Next ready: Complete caller 0053, run once under Proof ownership, review executor cut 0051, and publish the live image producer output before 01:08:46Z.
Integration: 7135ac722a. The next readiness run stays fixed on 804134d747; no source-head chase.
Disk: About 11.8 GB free. Cleanup is paused above the floor under D34. No protected or previously refused paths were touched.
Safety: Historical cleanup, graph and publication denials stand. Managers write only boards, briefs and shared reports; workers own product changes.
Delivery legacy subset: Keep transcriptAssociateCapture.ts and its unchanged 397-line, 40-assertion test, plus required helpers, under D31.
Evidence: [P1 result](/home/user/timeline-hub/hub/design/app-P1-18792-result-handoff-0029.md), [bootstrap review](/home/user/timeline-hub/hub/design/app-A2-basis-cancel-review-0041.md), [A4 cut map](/home/user/timeline-hub/hub/design/app-A4-current-cut-census-0042.md).
