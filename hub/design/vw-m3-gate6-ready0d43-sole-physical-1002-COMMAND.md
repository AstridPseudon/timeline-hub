# Commands and evidence: vw-m3-gate6-ready0d43-sole-physical-1002

## Static checks

    (cd /tmp && bash -n "$PACK/run.sh" "$PACK/preflight.sh")
    (cd /tmp && node-v20.19.4 --check prepare.mjs issue.mjs dist-availability.mjs)
    (cd "$PACK" && sha256sum -c SHA256SUMS)
    PYTHONDONTWRITEBYTECODE=1 python3 -B .../prepare-validation-diagnostic.py
    PYTHONDONTWRITEBYTECODE=1 python3 -B short-player-temp-controls.py --self-test

All passed. The packet SHA-256 entries were checked before central execution.

Registered packet commands (the central service invoked these exact bare
commands):

    bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-ready0d43-sole-physical-1002/packet/run.sh --preflight
    bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-ready0d43-sole-physical-1002/packet/run.sh

## Central preflight

    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-gate6-ready0d43-sole-physical-1002 e2e-viewing-gate6-ready0d43-sole-physical-1002-preflight)
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 100

ID: vw-m3-gate6-ready0d43-sole-physical-1002-e2e-viewing-gate6-ready0d43-sole-physical-1002-preflight-1021100413-23857
Result: PASS, exit 0.
Verified: exact source/graphs/dist, GET 200, five discovered/listed cases, clean child environment, negative propagation, central Python/helper validation. No Runtime/helper/browser started in preflight.

## Central physical

    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-gate6-ready0d43-sole-physical-1002 e2e-viewing-gate6-ready0d43-sole-physical-1002-physical)
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R" 100
    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-stop-test <physical-result-id> 'first physical case failed; stop remainder per authorized one-shot contract'

ID: vw-m3-gate6-ready0d43-sole-physical-1002-e2e-viewing-gate6-ready0d43-sole-physical-1002-physical-1021100528-15923
Result: cancelled after explicit stop, final exit 130. No retry or alternate request.

## Raw paths and hashes

Namespace: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-ready0d43-sole-physical-1002/packet/gate6-20261021T1002

First-case directory: namespace/playwright-output/player-export-normal-profi-d4d71-without-a-parity-comparison-native-codec-chrome155

error-context.md: dbb49fd6fdcbcb579aff1b664381e182da531d87585cf8188b2e62e03d6173b5
viewing-parity/page-diagnostics.json: 91e99ec5d0e453832da3bc8323dff9b9781b289cc338ace4c8448e1b97848ecb
trace.zip: 60e7302defa6fe012af2ef76efbb2b0fe98af8c43aa80ff62d731a7517ab07dc
central/invocation log: b1249bf75db3aa47a9392139b9aeebd596e6c84d64e3b8868fe41714ad01fa8b
source-tuple.json: e5fdb984701b9becd1c1192793075a56a4f3c6fe7aec0e82bcd5b4eeed41df85
grant: 9195360c316eda34f69065cad2b189634d25c441290551ceed232d4a0466c14f
marker: f453036618027b94b92ff15206dd8ddd9beaf12f97a3c9df3f74ebeffb9025fb

Storage was above threshold 11320247244 and floor 10737418240 at each guarded point.
