# App M2 producer retention central preflight — 0805

## Result

**PASS — one central preflight only.** The approved 0753 retention artifacts passed the
0801 conditional central preflight. No producer actual case was run or authorized;
the prior central23671 result remains **FAIL/UNKNOWN**.

The service snapshot used App source tree `c1ac3383624322ae8d67b10dee36965670d91cd7`.
The protected keeper was checked separately at:

- source target: `/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717`
- keeper HEAD: `6b0267c62aa8773132f1496d5014279e6c1edf61`
- keeper tree: `c1ac3383624322ae8d67b10dee36965670d91cd7`
- keeper worktree: clean; `KEEP` present

## Registration

Exactly one App-owned integration suite was added to
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`.
The literal stored registration is:

```text
app ap2-m2-producer-retention-central-preflight-0805-integration test "$(git -C "$PWD" show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 rev-parse HEAD)" = 6b0267c62aa8773132f1496d5014279e6c1edf61 && test "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && test -z "$(git -C /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 status --porcelain=v1 --untracked-files=all)" && test -f /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-helper-expect-import-0717/KEEP && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-retain-failure-artifacts-0753.sh | cut -d" " -f1)" = dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-public13-runner-0717-owned.sh | cut -d" " -f1)" = dc1159bd071b81c77bdab9f952d473c5e9b7e088f22693ca8c570a194daa51e7 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-runner-0717-owned.sh | cut -d" " -f1)" = 664ab0c500f5404e637a2524abaaf75937ee4335cc8fc987df91c37f79c11bd8 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-physical-keeper-gate-0717-owned.sh | cut -d" " -f1)" = 88cb8695c850fc2b3da52bfb2151191901e8f19a14c3f1cbace6f4d1a0166a8b && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-only-gate-0717-owned.sh | cut -d" " -f1)" = 3db5151a442811def19711e3a8e0cc63d0e91047e8f29d1480977c45e6f877d2 && test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-custody-gate-0717-owned.sh | cut -d" " -f1)" = e92ac3920d0f2e197c482444183518629f72e1f83b728fecb68e5553c45a48d0 && sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

The command binds all six final 0753 artifact hashes and invokes only the approved
custody gate with `preflight`; it does not invoke `run` or any actual producer mode.
The `$PWD` source-tree check is separate from the protected keeper HEAD/tree/clean/KEEP
checks. The registration uses literal shell quoting; it contains no backslash-quoted
`$PWD` or stray trailing quote.

## Validation

- Generated command: `sh -n` PASS.
- Stored registration extracted from `suites.conf`: `sh -n` PASS.
- argv-only dispatch stub: PASS; received exactly `preflight`.
- No local IPC was run.

## Central execution

Submitted exactly once with `--no-cache`:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-retention-central-preflight-0805 ap2-m2-producer-retention-central-preflight-0805-integration --no-cache
```

Result ID:
`ap2-m2-producer-retention-central-preflight-0805-ap2-m2-producer-retention-central-preflight-0805-integration-1021080643-29222`

Wait command: `wait-test <result-id> 1`; result: **PASS exit=0 in 6s**.
The service reported App tree `c1ac3383624322ae8d67b10dee36965670d91cd7`.
The preflight log reported:

```text
public13 preflight PASS checks=11 source=agent:8130a401bf44a518d5a40ae274d398b8c560be55 runtime:2c4ac180c2220bdad966bc01e95ad230e99ce26a graph=public13 isolation=private
module-format probe PASS: DirectHarness loaded as ESM; no daemon invoked
```

No browser, producer actual, daemon, socket, build, install, or run-mode execution occurred.
The central test runner's `counts:` field is empty because this is a shell preflight,
not a test-file suite; the gate itself executed and reported 11 checks, so this was not
a zero-test/no-body pass.

## Next step

Retention artifacts are ready for the manager's later single diagnostic run after the
parent browser lock is free. This preflight does not approve that diagnostic run.

