# App M2 producer evidence retention custody review — 0801

## Decision

**APPROVE — retention delta only, conditional on the exact central preflight
below.** The bytes preserve the original execution path and custody guards.
This is not approval of a new actual producer run. The prior central23671
result remains **FAIL/UNKNOWN** and is not replayed or reclassified.

The reviewed source/service identity is:

```text
keeper=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
keeper_HEAD=6b0267c62aa8773132f1496d5014279e6c1edf61
keeper_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
service_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
service_HEAD=6b0267c62aa8773132f1496d5014279e6c1edf61
```

No App product/spec/helper/pin/assertion/selector/timeout file changed in this
review worktree; `git status --short` is clean.

## Exact owned retention bytes

```text
producer-retain-failure-artifacts-0753.sh  dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
producer-public13-runner-0717-owned.sh     dc1159bd071b81c77bdab9f952d473c5e9b7e088f22693ca8c570a194daa51e7
producer-runner-0717-owned.sh              664ab0c500f5404e637a2524abaaf75937ee4335cc8fc987df91c37f79c11bd8
producer-physical-keeper-gate-0717-owned.sh 88cb8695c850fc2b3da52bfb2151191901e8f19a14c3f1cbace6f4d1a0166a8b
producer-startup-only-gate-0717-owned.sh   3db5151a442811def19711e3a8e0cc63d0e91047e8f29d1480977c45e6f877d2
producer-startup-custody-gate-0717-owned.sh e92ac3920d0f2e197c482444183518629f72e1f83b728fecb68e5553c45a48d0
```

The transitive guards match exactly: public13 runner -> retention helper
`dab4e8…`; wrapper -> public13 runner `dc1159…`; physical/startup/custody
gates -> wrapper `664ab0…`; custody gate -> physical gate `88cb86…` and
startup gate `3db515…`. The custody gate keeps service `TREE` separate from
keeper `HEAD` and `TREE`, and retains the Agent/Runtime pins, graph, package,
source ancestry, original wrapper, spec, helper, config, argv, list/zero-test,
child-RC, cleanup, and refusal checks.

Compared with the approved 0728 chain, the minimal delta is the new retention
helper, the public13 EXIT-trap/helper binding, the owned wrapper's public13
path and durable-root allocation, and the transitive path/hash rebinding.
There is no product or test-behavior change.

## Retention and custody findings

The original central path is retained before cleanup:

1. The unchanged producer config sets Playwright `outputDir` from
   `PLAYWRIGHT_OUTPUT_DIR`; the owned public13 runner sets that to
   `$RUN_ROOT/browser-output`.
2. The owned wrapper invokes the real Playwright child with
   `>"$LIST_LOG" 2>&1`, then validates the unchanged one-test result and
   returns the child status. This is the real child log, not a fabricated
   summary.
3. The public13 EXIT trap calls retention while `$RUN_ROOT` still exists and
   before graph attachment cleanup and `find "$RUN_ROOT" -depth -delete`.
4. Retention copies only the complete recursive `browser-output` tree and the
   exact `LIST_LOG`; it requires `error-context.md` and `trace.zip` somewhere
   in the copied tree, records source/command identity and child RC, and
   writes `SHA256SUMS` over the durable bytes.

The helper rejects non-absolute paths, non-real run roots, symlinked browser
output, missing child logs, non-ordinary mode, non-failure status, and a
pre-existing durable destination. It does not copy or print environment,
credential, profile, npm cache, Playwright cache, Vite cache, or browser
profile files. The only copied paths are `browser-output/` and `child.log`.
Copy failure forces a nonzero outer result; it cannot turn a failed child into
pass. Success does not create failure evidence and still removes the run root.

This static path proof is consistent with central23671's previously observed
`.../browser-output/.../error-context.md` and `trace.zip` locations. No new
actual was run, so complete real DOM bytes are conditionally accepted pending
the exact central preflight and a later separately authorized diagnostic
execution. No independent review of retained runtime artifacts is required
after that execution; diagnosis may consume the verified manifest directly.

## Controls run by this review

All commands ran from the review worktree and created no lasting worktree
output:

```text
for f <0753-artifacts>/*.sh; do sh -n "$f"; done
PASS (8 scripts)

<0753-artifacts>/producer-retention-controls-0753.sh \
  <0753-artifacts>/producer-retain-failure-artifacts-0753.sh \
  /home/user/work/wt/ap2-m2-producer-evidence-retention-custody-review-0801
producer retention controls PASS count=3 sockets=0

PATH=<private fake npm>:$PATH \
  sh <0753-artifacts>/producer-public13-runner-0717-owned.sh \
  /home/user/work/wt/ap2-m2-producer-evidence-retention-custody-review-0801 ordinary
PASS outer_status=1; error-context.md, trace.zip, child.log, identity.txt,
SHA256SUMS survived; .public13-effective-ordinary was removed.

(cd /home/user/work/wt/ap2-m2-producer-evidence-retention-custody-review-0801 && \
  sh <0753-artifacts>/producer-physical-keeper-gate-0717-owned.sh preflight)
public13 preflight PASS checks=11
```

The three planted controls cover failed-child retention/RC, successful cleanup,
and pre-existing-destination copy refusal. The fake runner is launch-only and
uses no browser, daemon, build, socket, actual producer, install, or central
test service.

## Existing evidence reused

- 0717: exact one-line Playwright `expect` import; original spec, config,
  assertions, selector, timeout, and source contract unchanged.
- 0728/0735: approved source/service custody, original-wrapper reverse proof,
  physical-root and cleanup guards, direct/door identity, graph and
  Agent/Runtime/Composition pins, list/zero/multiple-test and child-RC
  controls. The old wrapper hash remains
  `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`.
- 0741/0748: central23671 exact single-case **FAIL**, expected 2 transcript
  chips and received 0; failure before producer mutations; retained status is
  **FAIL/UNKNOWN**. Its temporary DOM/error-context/trace output was lost by
  the old cleanup path; no cause is invented here.
- 0753: retention implementation, three controls, fake runner, source-only
  preflight, and final owned hashes. The inherited full custody preflight hit
  tsx IPC `listen EPERM`; this review did not retry it locally or change
  source/options to evade it.

## Final literal central preflight-only registration proposal

Do not register the stale 0721/0735 actual recipe and do not submit an actual.
If central confirmation is required, register exactly one unique preflight-only
entry using the exact final bytes:

```text
app ap2-m2-producer-evidence-retention-custody-review-0801-preflight-e92ac392-integration test "$(git -C \"$PWD\" show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 rev-parse HEAD)" = 6b0267c62aa8773132f1496d5014279e6c1edf61 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test -z "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 status --porcelain=v1 --untracked-files=all)" && test -f /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-helper-expect-import-0717/KEEP && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-retain-failure-artifacts-0753.sh | cut -d' ' -f1)" = dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-public13-runner-0717-owned.sh | cut -d' ' -f1)" = dc1159bd071b81c77bdab9f952d473c5e9b7e088f22693ca8c570a194daa51e7 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-runner-0717-owned.sh | cut -d' ' -f1)" = 664ab0c500f5404e637a2524abaaf75937ee4335cc8fc987df91c37f79c11bd8 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-physical-keeper-gate-0717-owned.sh | cut -d' ' -f1)" = 88cb8695c850fc2b3da52bfb2151191901e8f19a14c3f1cbace6f4d1a0166a8b && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-only-gate-0717-owned.sh | cut -d' ' -f1)" = 3db5151a442811def19711e3a8e0cc63d0e91047e8f29d1480977c45e6f877d2 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-custody-gate-0717-owned.sh | cut -d' ' -f1)" = e92ac3920d0f2e197c482444183518629f72e1f83b728fecb68e5553c45a48d0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-custody-gate-0717-owned.sh preflight"
```

The proposal is preflight-only: no `run`, no browser, no daemon, no build, no
socket, and no actual case. Existing runner approval remains conditional on
that exact central preflight; no unverified actual is claimed.

## Blockers and next steps

The inherited tsx IPC `listen EPERM` prevents local full-custody preflight
verification. It is an environment limitation, not a source failure; it was
not retried. The orchestrator may run the exact central preflight proposal,
then separately authorize one evidence-producing diagnostic execution if
desired. No code edit is required by this review.
