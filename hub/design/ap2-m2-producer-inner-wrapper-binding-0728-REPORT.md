# App M2 producer inner-wrapper binding — 0728

## Result

Prepared an owned 0717 wrapper/gate packet. The App source tree and the
original wrapper remain immutable. The owned wrapper changes only the explicit
source/helper custody literals:

```text
APP_SHA=17d2518c341c47a2d8634047b400399886da3a2a
APP_TREE=d63fe4f1e1f32a01acfc9d11cda6c29066fce162
APP_SOURCE_SHA=6b0267c62aa8773132f1496d5014279e6c1edf61
APP_SOURCE_TREE=c1ac3383624322ae8d67b10dee36965670d91cd7
APP_SOURCE_PARENT_SHA=b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
HELPER_SHA=d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b
```

The exact 0717 closure is therefore `17d251… -> b8cc… -> 6b026…`, with
the keeper HEAD/tree separately pinned to `6b026…`/`c1ac…`. The original
wrapper remains `329cfca…`; the owned rebound wrapper is `48c89f…`.

Owned artifacts are in:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts/
```

## Final hashes

```text
producer-runner-0717-owned.sh                 48c89f338891b732234fd8ddae1c10585fb6aafbf222b216b14b8cd3c1f210ce
producer-physical-keeper-gate-0717-owned.sh  05e1ce136aeff7c90184672f9dfd2848198457776669698704610e53b046ea25
producer-startup-only-gate-0717-owned.sh     cc54a90867d6681fb88ca964ff691c8670d151792edc65d8b99c0064e91fc9b2
producer-startup-custody-gate-0717-owned.sh  64e7befb995b38fbf387b9ac2c0fb698dda59b514dfec54adb3be12c10f3ace4
producer-startup-only-probe-0717-owned.mts   a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
producer-startup-module-format-probe-0717-owned.mts d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
producer-health-realm-offline-review-owned.mjs 5169e8628ef77cd9a20b51b41ab842b319f84249fef9ed1fcf18527169caad4a
producer-launch-only-playwright-stub-0717.sh aeaffe7a8aea1327fc2391f2fc137ec456b7136ca2698777c5f157ca59b85ce7
producer-launch-only-npm-stub-0717.sh       b4fd677ed9069eb75b040b951515c89d7de3ff79d85873f4b198ff8ede1f22e
```

The three copied shell gates differ from their predecessors only by owned
artifact paths/hashes, original-wrapper-versus-owned-wrapper checks, and the
0717 source/helper closure. The owned wrapper differs from the immutable
original in exactly six literal lines: the three source-closure pairs and the
helper hash. No App product file, generated file, pin, assertion, spec,
config, or original artifact was edited.

## Reverse proof

The current helper with only `expect, ` removed from its Playwright import
reproduces the original helper hash exactly:

```text
50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
```

The frozen spec, config, and original wrapper remain respectively:

```text
d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
```

## Evidence

- `for f artifacts/*.sh; do sh -n "$f"; done` — PASS.
- Owned offline source/result review — PASS, including direct/door identity,
  physical path and teardown guards, service-tree/keeper-HEAD separation,
  exact 0717 closure, and original/owned wrapper separation.
- `sh producer-physical-keeper-gate-0717-owned.sh preflight` — PASS. The real
  public13 resolver ran and reported `public13 preflight PASS checks=10`; no
  build, browser, producer body, or actual ran.
- Launch-only forwarder matrix through the owned wrapper — PASS: valid list and
  run reached the stub; zero tests refused with RC 1; multiple tests refused
  with RC 1; a reported `1 failed` child propagated RC 7; a `1 passed` child
  with RC 7 was refused; unknown mode refused with RC 2. Temporary app/realm,
  logs, and symlinks were removed after success and failure cases.
- Wrong helper/source, wrong service tree, extra source hunk, unknown mode, and
  wrong argv — PASS, all refused before launch.
- Reverse helper/spec/config/original-wrapper hash proof — PASS.
- Keeper cleanup — PASS: `node_modules` restored to
  `/home/user/work/app/node_modules`, `.public13-effective-ordinary` absent,
  keeper clean, and worker worktree clean.

The custody `preflight` wrapper was also attempted with a private physical
`TMPDIR`. Its public13 portion passed, but the copied TSX format probe failed
at Node IPC setup with sandbox `EPERM` creating a Unix pipe. This is an
environment boundary, not a source assertion result; no startup probe was
claimed. A launch-only outer run reached the real resolver/build handoff but
waited on the shared browser lock, so it was interrupted before any browser or
actual and its residue was manually cleaned and rechecked.

No daemon, browser, build, startup probe, producer actual, central test
service, full suite, install, or shared dependency write was performed.

## Immutable later-review recipe

The exact service target is:

```text
serviceTARGET0717=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
```

Named recipe:
`ap2-m2-producer-inner-wrapper-binding-0728-0717-owned-custody`.

After independent review, run from the immutable target with the artifact
directory above; do not substitute the 0538 source or the original wrapper:

```sh
SERVICE_TARGET_0717=/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
ARTIFACT_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-inner-wrapper-binding-0728/artifacts
(cd "$SERVICE_TARGET_0717" && sh "$ARTIFACT_ROOT/producer-startup-custody-gate-0717-owned.sh" preflight)
# Only after the preflight and independent review authorize it:
(cd "$SERVICE_TARGET_0717" && sh "$ARTIFACT_ROOT/producer-startup-custody-gate-0717-owned.sh" run)
```

This packet was not registered as or executed through a central actual suite.
