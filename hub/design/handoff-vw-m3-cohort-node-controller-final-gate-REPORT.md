# Fourcase Node-controller final-gate review

Verdict: **APPROVE as a held, test-only qualification candidate. NEVER MERGE WHOLESALE.**

## Candidate identity

- App candidate commit: `e26079c440d09d7712588581e369204b3e035db9`
- App candidate commit tree: `e523fc0dc76eeff03a68f3cdb59e78a8b6b55798`
- Parent candidate: `cc9c77b1f235d831200e629fe7ad253c084faf4f`
- App source/tree tuple: `30b8df2895536c471e270faf83ce710acd847065` / `0bf9c9f7fb849cb0938bf29fc72eca069014f623`
- Agent13 remains held: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` / `75354d38c898729bac09619679f5421faba319ed`
- Runtime13 remains held: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition13 source/artifact: `af98594dce80c0350a1fc21dfc44839b2279edf1` / `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; prior evidence records 77/77 extracted members and peer/lock integrity.
- Delta is exactly two existing App paths: `tab-audio.controller.mjs` and `tab-audio.controller.test.mjs`.

## Review findings

- Existing controller/launcher execution is rebound to the retained own Node20.19.4 path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`.
- The executable reports `v20.19.4` and SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Positive and negative Node identity tests, existing short-temp cleanup coverage, exact source tuple checks, Chrome155 full executable/tree pins, source before/after checks, fresh-grant/marker checks, free-disk floor, private-graph/flock checks, and fail-closed readiness guards remain present. The diff does not touch the public13 package/lock/peer or the existing five-case source.
- Discovery uses the existing five-case native-codec profile and worker-owned temporary stdout/stderr files, removing the directory in `finally`; no new counter, API, environment scheme, or duplicate framework was introduced.
- The prior 322-test/5-case parent result is accepted as existing evidence and was not rerun unnecessarily.

## Evidence run

- `sha256sum <retained-node>`: passed, exact `43d6cf…99490`.
- `<retained-node> --version`: passed, `v20.19.4`.
- Controller unit test file: passed, exit 0.
- Controller syntax check: passed, exit 0.
- Controller-owned discovery: passed, `discovered exactly five native-codec-chrome155 parity cases`, exit 0.
- Literal Playwright discovery: already recorded in the parent handoff as `Total: 5 tests in 1 file`; the controller discovery independently passed the same five-case assertion.
- `git diff --check e26079c^ e26079c`: passed, exit 0.
- `--ready <candidate> /home/user/work/agent /home/user/work/runtime`: correctly refused, exit 1 at `App13 consumer adoption is pending; --ready remains refused`, before graph/capture/grant checks.

No browser, render, capture, live socket, install, network, full suite, central actual qualification, normal Agent13 pin, normal Runtime provisioning, native-host environment qualification, or physical-mix claim was run or claimed. The candidate remains held until the actual source/environment prerequisites are qualified.

