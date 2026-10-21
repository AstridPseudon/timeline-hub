# App M2 producer durable failure evidence — 0753

## Result

Repaired only the owned producer runner’s failure-artifact retention. No App
product source, producer test/spec, selector, timeout, pin, helper, or shared
reviewed artifact was changed. Changed live callers: **NONE**. The historical
23671 cause remains **UNKNOWN**; this work does not infer one.

The original reviewed source remains the exact keeper:

```text
keeper=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
keeper_HEAD=6b0267c62aa8773132f1496d5014279e6c1edf61
keeper_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
original_committed_wrapper_sha256=329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
old_owned_wrapper_sha256=48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce
old_public13_runner_sha256=be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75
```

## Owned artifacts

All paths below are in this worker’s durable folder and are SHA256-bound by
the copied custody chain where applicable.

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-runner-0717-owned.sh
  664ab0c500f5404e637a2524abaaf75937ee4335cc8fc987df91c37f79c11bd8
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-public13-runner-0717-owned.sh
  dc1159bd071b81c77bdab9f952d473c5e9b7e088f22693ca8c570a194daa51e7
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-retain-failure-artifacts-0753.sh
  dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-retention-controls-0753.sh
  ed96d5d11e60bd66c91f7af50db2e20534c08bcbf39f83960669d46e9e7bfe9b
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-fake-npm-failure-0753.sh
  c575522761ff4c95fe08bf3ba69c491652ba3081dfddfadfdd34714da3580205
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-physical-keeper-gate-0717-owned.sh
  88cb8695c850fc2b3da52bfb2151191901e8f19a14c3f1cbace6f4d1a0166a8b
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-only-gate-0717-owned.sh
  3db5151a442811def19711e3a8e0cc63d0e91047e8f29d1480977c45e6f877d2
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-durable-failure-evidence-0753/artifacts/producer-startup-custody-gate-0717-owned.sh
  e92ac3920d0f2e197c482444183518629f72e1f83b728fecb68e5553c45a48d0
```

The copied unchanged probes remain bound at `a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f` and `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3`.

## Minimal delta and guarantees

- The owned wrapper’s original source/tree/pin/graph/argv/list-one/child-exit/
  zero-test/refusal guards and original selector/assertions/options remain
  intact. Its only functional additions are a durable run destination, an
  initially empty exact child-log path, and binding to the owned runner copy.
- The owned public13 runner is a byte copy of the reviewed public runner plus
  retention-helper hash validation and an `EXIT`-trap call before normal
  attachment/dist/run-root cleanup. A nonzero child status is preserved when
  copying succeeds; a copy failure forces a nonzero outer result and cannot
  become pass. Success still performs normal cleanup without creating failure
  evidence.
- The helper copies only the complete `browser-output` tree and exact child
  log. It refuses symlinked browser output, does not copy environment,
  profile, cache, or credential files, records child exit/source/command
  identity, and writes a SHA256 manifest. It explicitly requires a full
  `error-context.md` and `trace.zip` somewhere in the copied tree.
- The copied physical/startup custody gates retain original committed-wrapper,
  source HEAD/tree, pins, graph, argv, zero/multiple-test, cleanup, and
  refusal guards. Only owned transitive paths and hashes were rebound.

## Controls and evidence

Commands and results:

```text
for f <owned-artifacts>/*.sh; do sh -n "$f"; done
PASS

<owned-artifacts>/producer-retention-controls-0753.sh \
  <owned-artifacts>/producer-retain-failure-artifacts-0753.sh \
  /home/user/work/wt/ap2-m2-producer-durable-failure-evidence-0753
producer retention controls PASS count=3 sockets=0
```

The three launch-only planted controls are: fake child creates representative
error-context/trace and returns 1 (durable bytes survive; outer status 1),
success cleanup (root removed; status 0), and pre-existing destination forcing
artifact-copy refusal (root removed; outer status 1, never pass).

End-to-end owned-runner planted control:

```text
PRODUCER_PUBLIC13_DURABLE_ROOT=<worker>/evidence/runner-control-...
PRODUCER_PUBLIC13_LIST_LOG=<private-temp>/child.log
PATH=<private-fake-npm>:$PATH
sh <owned-artifacts>/producer-public13-runner-0717-owned.sh \
  /home/user/work/wt/ap2-m2-producer-durable-failure-evidence-0753 ordinary
outer_status=1
```

It passed with the fake child only: `error-context.md`, `trace.zip`, exact
`child.log`, identity metadata, and `SHA256SUMS` survived; the private
`.public13-effective-ordinary` root was removed. No browser, daemon, real
build, live socket, or producer body ran.

Source-only custody preflight:

```text
sh <owned-artifacts>/producer-physical-keeper-gate-0717-owned.sh preflight
public13 preflight PASS checks=11 ...
```

The full copied custody `preflight` was attempted once. Its source preflight
passed, then the inherited format probe attempted tsx IPC and the sandbox
returned `listen EPERM` for `/tmp/w-0404934117/tsx-0/341.pipe`. It was not
rerun. No actual producer case or central test-service submission was made.

## Remaining prerequisites for one evidence-producing diagnostic execution

1. Independent process-custody review must approve the final owned hashes
   above and verify the original keeper remains clean at HEAD/tree
   `6b0267c62aa8773132f1496d5014279e6c1edf61` /
   `c1ac3383624322ae8d67b10dee36965670d91cd7`.
2. Keep the original spec/helper/config hashes, Agent/Runtime pins, locked
   graph, Composition package, shared installs, 10 GiB floor, and browser lock
   valid. Do not register or execute this run from this worker.
3. Register one new central suite recipe that binds the captured source tree
   and invokes the final owned custody gate’s `run` mode. The registered
   command must point to this worker’s
   `producer-startup-custody-gate-0717-owned.sh`, not the stale 0721/0735
   artifact path, and must bind the final hashes above.
4. Obtain explicit authorization, confirm no competing selected run is active,
   submit exactly once, and preserve the resulting durable
   `evidence/failure-*` directory before reporting the actual result. The
   retained artifact must then receive an independent custody review before
   any diagnosis or product change.
