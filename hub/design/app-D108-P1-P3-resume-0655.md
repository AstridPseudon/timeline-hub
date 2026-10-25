# D108 P1/P3 resume report

## Result

P1 and P3 both passed on the fixed current tuple. P1 reused the retained original ID and was not resubmitted. P3 ran once after an independent P1 GO review and a passing source preflight.

Tuple: App `f7201e02dc53ca7b1e70e38894284528fc78aa70` / `cdc1809f3ec82fa1f360092041eb2a8597fc62e5`; Agent `d6294843286c18e57af3c1874cf1996be42212d2` / `6aeae30f0892a424104a4348bca6fd74ba1315d6`; Runtime `c91626f5e905f9336b51aae0486a071d83f0bac7` / `16264479ae18fbb05ec5356ce5b5ab6f69dea9aa`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`.

## Evidence

- P1 preflight `app-pin-f7201e02-d108-p1-current-0648-preflight-1025064914-13611`: PASS, exit 0, 2s.
- P1 retained original `app-pin-f7201e02-d108-p1-current-0648-1025064944-15075`: PASS, exit 0, 177s; readiness 1/1 and original 2/2; failures/skips/errors 0/0/0.
- Independent read-only P1 review `app-D108-P1-independent-GO-review-0655-r2`: GO. It independently verified the immutable App service snapshot commit’s recorded tree and sole parent; temporary snapshot-directory recycling is disclosed.
- P3 preflight `app-pin-f7201e02-d108-p3-current-0655-preflight-1025065907-15346`: PASS, exit 0, 3s.
- P3 original `app-pin-f7201e02-d108-p3-current-0655-1025065937-31792`: PASS, exit 0, 217s; readiness 1/1 and original 1/1; failures/skips/errors 0/0/0; first failure none.
- P3 passed the exact recovery/transport, v2 request, merged-B, canonical/history, restart, and guarded-undo predicates, including 5 observed and 3 forwarded requests and no legacy traffic.

Source/spec, manifest, XML, tuple, checkout receipts, recipes, and redacted terminal packets are retained under `workers/app-D108-P1-P3-resume-0655/submission/{p1,p3}`. The preparation worktree is clean; no product/source/spec/harness/pin/manifest changes were made.

## Commands

- `bin/wait-test app-pin-f7201e02-d108-p1-current-0648-1025064944-15075` — PASS, exit 0.
- Existing D66 `p3 --submit` API from `/home/user/work/app` with `D66_OUTPUT_DIR` set before Node20 executable — preflight PASS, then one original request.
- `bin/wait-test app-pin-f7201e02-d108-p3-current-0655-1025065937-31792` — PASS, exit 0.

No blockers remain for this P1/P3 assignment. Recommended next step is orchestrator consumption of the two terminal handoffs; P2/full-tour work remains governed by the separate D110/D111 release decision.
