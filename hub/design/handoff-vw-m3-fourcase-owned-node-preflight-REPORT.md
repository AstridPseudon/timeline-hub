# Fourcase owned-Node preflight

Status: TEST-ONLY future-qualification candidate. **NEVER MERGE WHOLESALE.**

## Result

Rebound the existing fourcase controller and child launchers to the retained admitted own Node20.19.4 executable:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
v20.19.4
sha256 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
```

The controller retains the full Node version/hash check, whole private-graph check, all-77 Composition pin, Chrome155 executable/tree pin, source pre/postflight checks, and the pending-App fail-closed `--ready` guard. Discovery writes only to a short owned `/tmp` directory and removes it after reading the child result; no shared dependency, cache, symlink, install, or product path was changed.

## Candidate identity

- Source branchbase: `tl/vw-m3-reviewed-fourcase-cohort-compose`.
- Parent candidate SHA: `cc9c77b1f235d831200e629fe7ad253c084faf4f`.
- Final working-tree SHA-1 tree after this worker delta: `23d7f8b138fb3d65f1010609833f24075e5b789e`.
- Final harness commit SHA: pending harness commit on worker exit; the exact final tree above is independent of that commit metadata.
- App candidate source/tree: `30b8df2895536c471e270faf83ce710acd847065` / `0bf9c9f7fb849cb0938bf29fc72eca069014f623`.
- Agent13 source/tree remains held: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` / `75354d38c898729bac09619679f5421faba319ed`.
- Runtime13 source/tree remains held: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Composition13 source/artifact: `af98594dce80c0350a1fc21dfc44839b2279edf1` / `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` (77 files as previously frozen).

## Evidence

- Retained Node digest/version probe: passed.
- Changed controller unit plus Node positive/negative identity tests: passed, exit 0.
- Controller-owned `--discover`: passed, exact `discovered exactly five native-codec-chrome155 parity cases`.
- Literal native-codec Playwright `--list`: passed, `Total: 5 tests in 1 file`.
- Controller syntax check: passed.
- `git diff --check`: passed.
- `--ready <app> /home/user/work/agent /home/user/work/runtime`: refused, exit 1 with `App13 consumer adoption is pending; --ready remains refused`, before graph/capture/grant checks.

No 322-test rerun, browser, render, capture, grant, full suite, install, network, live socket, or actual qualification was run.

## Decisions and limits

- The existing native-codec Chrome155 profile was preserved; no new profile/API/env scheme was introduced.
- The old missing `/tmp/vw-m3-agent-gate-node20.19.4/bin/node` was not substituted, linked, or recreated.
- The candidate remains App-public13/test-only and does not adopt Agent13, Runtime13, normal Render registration, or host setup.

See the delta manifest and source tuple files beside this report. The composed candidate remains a test candidate and must not be merged as a forest.
