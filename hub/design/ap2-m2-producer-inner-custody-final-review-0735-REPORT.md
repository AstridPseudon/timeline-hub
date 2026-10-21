# App M2 producer inner-wrapper custody final review — 0735

## Decision

**APPROVE — custody delta only.** No App product/helper/spec/pin/assertion
files were edited, and no actual producer case was authorized or run.

The reviewed immutable source target is:

```text
serviceTARGET0717=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
HEAD=6b0267c62aa8773132f1496d5014279e6c1edf61
TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
PARENT=b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
```

The owned wrapper is `48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce`.
The owned final custody gate is
`64e7befb995b38fbf387b9ac2c0fb698dda59b514dfec54adb3be12c10f3ace4`.
The immutable keeper wrapper remains `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`.

## Independent findings

- The committed source delta from `b8cc7e1c` changes exactly one file and one
  import: `import type { Page }` becomes `import { expect, type Page }`.
  Reversing only `expect, ` restores helper hash
  `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`.
- The six declared wrapper literals are the only wrapper changes. Reversing
  `APP_SHA`, `APP_TREE`, `APP_SOURCE_SHA`, `APP_SOURCE_TREE`,
  `APP_SOURCE_PARENT_SHA`, and `HELPER_SHA` restores the original wrapper byte
  hash `329cfca7…` exactly.
- Reversing the physical, startup-only, and startup-custody copied gate
  bindings restores each 0721 predecessor byte-for-byte. The final gate binds
  the owned wrapper and checks its hash before dispatch.
- The source gate requires the exact 0717 ancestry and allows no post-source
  hunk except the named runner path. The original selector/config/spec and all
  original assertions remain covered by the unchanged spec hash
  `d91d0c1c…`; helper/config hashes are `d86721bd…` and `5b880cef…`.
- The service `TREE` and keeper `HEAD` are checked separately and must both be
  `c1ac3383…` / `6b0267c6…`. The external `KEEP` marker is present, the source
  checkout is clean, source `node_modules` remains the read-only shared link,
  and the locked graph `node_modules` is physical.
- Physical TMPDIR, private scratch/cache/output roots, early cleanup traps,
  planted realm-root symlink refusal, direct/door identity mapping, zero and
  multiple test refusal, child-RC propagation, unknown-mode refusal, and
  wrong-source/helper/tree/argv refusal are all covered by the reviewed packet.
  No guard bypass or validation stub was used for this review.

## Checks run

Exact commands run independently:

```text
node <owned>/producer-health-realm-offline-review-owned.mjs \
  /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717 \
  <owned-artifact-dir> \
  <git-show 2c4ac180:contract/schemas/health.json> \
  <git-show 2c4ac180:runtime_protocol/service.py> \
  <git-show 2c4ac180:runtime_protocol/server.py>
```

Result: **PASS, 25 offline checks**, including health/realm separation,
direct/door contracts, identity mismatch refusals, physical-root guards,
cleanup ordering, exact source closure, and original/owned wrapper separation.

```text
for f <owned-artifact-dir>/*.sh; do sh -n "$f"; done
```

Result: **PASS**.

The independent committed-binding check also passed for the exact Agent
`8130a401…/236c3e57…`, Runtime `2c4ac180…/7ab412cc…`, App baseline/body,
0717 source, spec/config, locked graph archive, Composition package/evaluator,
and the 10 GiB disk floor. The source target remained clean.

Reused evidence, permitted because the relevant final artifact hashes match:

- prior 0703 startup-only test `…startup-1021070652-30920`: **PASS**; its
  unchanged startup probes and Runtime/source/blob inputs are still exact;
- prior 0728 physical preflight: **PASS**;
- prior 0728 launch-only nested matrix through the final owned wrapper:
  **PASS** for valid list/run reachability, zero/multiple refusal, child-RC
  propagation, unknown mode, wrong bindings, extra source hunk, and cleanup.

Not run: producer actual, browser, daemon/startup, build, socket/live service,
full suite, install, or central test submission. The selected `8082` run was
checked before disposition and is now `DONE` with exit 0, so it is not active.

## Immutable central integration recipe (not submitted)

The existing `suites.conf` entry is the stale 0721 recipe and must not be
used. Register a new entry generated from the final hashes below, then submit
only after the orchestrator explicitly authorizes the actual:

```text
app ap2-m2-producer-inner-custody-final-review-0735-actual-64e7befb48c89f33-integration \
  test "$(git -C "$PWD" rev-parse HEAD)" = 6b0267c62aa8773132f1496d5014279e6c1edf61 && \
  test "$(git -C "$PWD" show -s --format=%T HEAD)" = c1ac3383624322ae8d67b10dee36965670d91cd7 && \
  test -z "$(git -C "$PWD" status --porcelain=v1 --untracked-files=all)" && \
  test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-startup-custody-gate-0717-owned.sh | cut -d' ' -f1)" = 64e7befb995b38fbf387b9ac2c0fb698dda59b514dfec54adb3be12c10f3ace4 && \
  test "$(sha256sum -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-runner-0717-owned.sh | cut -d' ' -f1)" = 48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce4 && \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/producer-startup-custody-gate-0717-owned.sh run
```

Invocation, when authorized:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-producer-helper-expect-import-0717 \
  ap2-m2-producer-inner-custody-final-review-0735-actual-64e7befb48c89f33-integration \
  --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This is the exact 0717 service target, never 0538. The owned wrapper retains
the original selector `tests/e2e/local/producer-ownership-current-pin.spec.ts`
and original assertions; the owned copy changes custody literals only.

## Remaining prerequisites and protection

1. Register the exact final-hash-bound suite above; do not reuse the stale
   0721 entry, substitute the 0538 source, or substitute the original wrapper.
2. Keep source target `6b0267c6/tree c1ac3383`, its external `KEEP` marker,
   keeper HEAD/tree, original wrapper, graph, Agent/Runtime pins, and all owned
   artifacts immutable until the central run completes.
3. Preserve shared `node_modules` and graph installs as read-only; keep all
   run scratch, TMPDIR, caches, browser output, and cleanup private to the
   central captured run.
4. Obtain explicit authorization for the one central actual after confirming
   no competing selected run is active. This review makes no actual claim.
5. After that run, report its real result and cleanup state separately; no
   source fix belongs in this review.

