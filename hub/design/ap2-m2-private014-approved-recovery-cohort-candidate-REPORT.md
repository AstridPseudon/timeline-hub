# Private normal014 recovery candidate report

## Result

Prepared one clean current App candidate and submitted exactly one fresh Gate 5
request after the central Chromium smoke passed. The Gate 5 journey ran with
the exact private 0.2.14 tuple and failed at the existing durable command-owner
readiness assertion: `ready: false` after the 90-second wait. This is not a
Chromium SIGTRAP and is not an adoption, activation, pin, release, or source
qualification pass.

Central Gate 5:

- Test ID: `ap2-m2-private014-approved-recovery-cohort-candidate-normal014-integration-e2e-gate5-1020191947-16711`
- Result: **FAIL**, exit 1, 290 seconds, `1 failed`
- Failure: `tests/e2e/local/three-products.spec.ts:1017`, “the mounted editor
  must claim a new durable command owner before the gesture”; expected
  `ready: true`, received `ready: false`; predicate timed out at 90 seconds.
- Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-private014-approved-recovery-cohort-candidate-normal014-integration-e2e-gate5-1020191947-16711/log.txt`

The previously qualified parent-media control was not rerun:
`app-normal014-integration-parent-media-accepted-1020173445-31361`, 1 test
passed under `--runxfail`.

## Candidate and exact source fingerprint

- App snapshot: commit `8cfcee9c0`, tree
  `d44bc9c76eee46f34de77e1ef1ee87e7fe347518`; clean before and after the run.
- Approved recovery source was already present. App recovery commit `9b14bf9f7`
  is an ancestor of the candidate; the current blobs match approved `741c78539`:
  - `useTimelineSave.ts`:
    `875073964dfe7db945fbbc66e6944ba79f8772ec`
  - `useTimelineSave.recovery.test.tsx`:
    `a8fc03b984f081055c9162e960bdbcb36e1c8e2c`
- Agent: commit `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree
  `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime: commit `202074110717146fc7f08af2306a8dd7f695b0b1`, tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Immutable producer: commit `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- Runtime manifest: 75 entries,
  `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Shared schema:
  `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime wire digest:
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Locked public13 graph archive:
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Composition artifact:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The central overlay changed only its disposable Runtime selector and generated
lock/client material through the existing vendor-lock recipe. No checked-in App
pin, package, generated file, shared source, or release state changed.

## Evidence

- `sh -n .../normal014-source-common.sh .../normal014-parent-media-central.sh .../normal014-app-central.sh` — PASS.
- Independent exact source guard — PASS: Agent/Runtime/producer refs and trees,
  ancestry, all 75 artifact bytes, manifest, and Agent/Runtime schema equality.
- Recovery blob comparison against approved `741c78539` — PASS.
- Local normal014 App preflight — reached source/artifact/schema guards, then
  stopped because this sandbox cannot reach the package index while the runner
  creates its throwaway venv (`jsonschema>=4.18` unavailable). No shared venv,
  node_modules, cache, or repository file was written.
- Central Chromium smoke from the active repair run
  `ap2-m2-chromium-launch-private-environment-fix-e2e-m2-ordinary-integration-1020191750-14430` — PASS for real page launch, DOM assertion, and clean close using short private TMPDIR/XDG paths. Its overall ordinary run failed later on an unrelated Runtime-venv/source-tuple setup error.
- The single authorized Gate 5 run — source guards, private graph/bin setup,
  vendor-lock checks, hosted build, and Chromium journey started successfully;
  the failure was owner readiness as stated above.

## Held by environment vs owner activation

Environment blockers were confined to this worker’s offline local venv
preflight; central execution supplied the required environment and disproved
the prior Chromium SIGTRAP for this run. The remaining blocker is owner-side
durable command-session readiness: the mounted editor never exposed a ready
owner, so the journey did not qualify recovery/outbox behavior. No claim is made
for activation, adoption, release, pin movement, or full-suite status.

## Next step

App owner should diagnose the `ready: false` command-owner path and authorize a
future fresh Gate 5 only after that fix is reviewed. Do not rerun the parent
control or submit another current cohort job from this candidate.
