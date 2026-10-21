# App2 M2 selected seed — reviewed main execution packet

Status: READY FOR REVIEW; do not submit the actual until this packet is approved.

## Exact source and custody

- Repository: App; branch `tl/integration`.
- Main source: commit `0cc2583aaf07e89190b9344b5ac82849d6279586`, tree
  `320e74a93676c781e83885b86ec237b4a1465d80`.
- HOME ancestor: commit `32b74fdea165816226b6f0727a16817a6a1a79c3`, tree
  `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`.
- Immutable original remains available and is not relabelled: App commit
  `a50ca4a0172cce9c73ce3c040290bf9479098b0f`, tree
  `92391f9a57dd38ce327b0a63990725053ea34601`, selected spec SHA-256
  `10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`.
  Keeper: `/home/user/work/wt/app-pin-a50ca4a0`.
- Current-source keeper for this packet: `/home/user/work/app`; it must remain
  clean at the current commit/tree. The original keeper above must remain
  separately clean and leased.

Current committed source hashes:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts
  2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0
tests/e2e/local/support/harness.ts
  bdd9b30b025c87097a99e5e67117ee01612f50b4f5a7c11f8f8dbe1ddb13f64a
config/vite/vite.config.ts
  5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
scripts/runtime-discovery-proxy.mjs
  93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0
```

The current spec is the existing `42b0c6c84`/`32b74fdea` retained variant.
Its only delta from the immutable `10250fa4…` selected proof is the already
approved readiness/context retention: `expectConnected` replaces the
same-origin mount helper and the current helper owns the timeline opening
context. The P1/P2, edit, refusal, dirty-draft, lost-ack, exact retry body and
idempotency key, reload, inverse/undo, zero-legacy assertion, title, 90-second
ceiling, and 240-second worker budget remain the current selected contract.
No spec or harness edit is part of this packet.

HOME's integrated `e5afdaed02a7bf57fdd3768bb6cbe356e9c776f7` order fix is
present in `harness.ts`: the exact selected raw publication retains the seed
head, V1/FX clips, selected media registry, and `draft-1` element reference;
the publication's returned `new_head` is passed to P1 as `--expected-head`;
Runtime is restarted before the selected credential is provisioned. The
case-local context remains the harness realm, actor
`astrid-selected-param`, discovery endpoint, credential FILE, and normal
same-origin discovery proxy/origin path.

## Owned runner

The approved `96629aa9dbb00c6bb7ad23591a98229e56e6a6c0184a2ac254e2b825174707c9`
runner is retained unchanged at its original worker artifact path. The owned
current-main copy is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-seed-current-main-packet-1110/artifacts/run-owned-selected-final95-current-main.sh
SHA-256: dcd4bf11e178cabd63a0a450e206b7450abb098a27110a2eca6ecd085794cefc
```

Its only delta from runner `96629aa9…` is data/contract rebinding to the
committed current App source: source commit/tree, selected-spec hash, harness
hash, and the readiness literals/count for the approved current spec variant.
The final95 Agent/Runtime tuple, Composition graph, old-driver/helper hashes,
argv, role scope, private-copy controls, cleanup, and retention function are
unchanged. The shared helper is read-only; its current SHA is
`96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109`.

Transitive identity guards retained by the runner:

```text
Agent                  6efc81500a0e0688c2bb41e736503f0fc3e04abb
Agent tree             2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime/producer       95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
Runtime/producer tree  d3a290b407fa61e6ab2d476f50c068073f70df00
Runtime manifest       a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d (76)
Edit-command schema    6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Runtime wire           sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
App runtime lock       770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
App generated metadata 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
App generated client   c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
App generated types    f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
App timeline schema    f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
Composition graph      895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Composition archive    9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 (77 members)
Old selected driver    a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
Source helper          96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109
Parent helper          1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
```

Toolchain and resolution are closed to Node `v22.22.0`, Vite `5.4.21`,
Vitest `4.1.5`, Playwright `1.60.0`, the absolute App venv
`/home/user/work/venv-app2-native/bin/python`, and browser binaries under
`/opt/pw-browsers`. Shared `node_modules`, Runtime, Agent, graph, and keeper
paths are read-only.

## Complete preflight

Run these checks on the exact clean `tl/integration` source before any actual:

```sh
git -C "$PWD" rev-parse --abbrev-ref HEAD
test "$(git -C "$PWD" rev-parse HEAD)" = 0cc2583aaf07e89190b9344b5ac82849d6279586
test "$(git -C "$PWD" rev-parse 'HEAD^{tree}')" = 320e74a93676c781e83885b86ec237b4a1465d80
test -z "$(git -C "$PWD" status --porcelain=v1 --untracked-files=all)"
test "$(git -C /home/user/work/app rev-parse HEAD)" = 0cc2583aaf07e89190b9344b5ac82849d6279586
test "$(git -C /home/user/work/app rev-parse 'HEAD^{tree}')" = 320e74a93676c781e83885b86ec237b4a1465d80
test -z "$(git -C /home/user/work/app status --porcelain=v1 --untracked-files=all)"
test "$(git -C /home/user/work/wt/app-pin-a50ca4a0 rev-parse HEAD)" = a50ca4a0172cce9c73ce3c040290bf9479098b0f
test "$(git -C /home/user/work/wt/app-pin-a50ca4a0 rev-parse 'HEAD^{tree}')" = 92391f9a57dd38ce327b0a63990725053ea34601
test -z "$(git -C /home/user/work/wt/app-pin-a50ca4a0 status --porcelain=v1 --untracked-files=all)"
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-seed-current-main-packet-1110/artifacts/run-owned-selected-final95-current-main.sh
node --check "$PWD/scripts/runtime-discovery-proxy.mjs"
flock -n /home/user/work/.app-m1-browser.lock -c ':'
test "$(realpath /home/user/work/app/node_modules)" = /home/user/work/app/node_modules
test "$(realpath /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/node_modules)" = /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/node_modules
test "$(node --version)" = v22.22.0
test -x /home/user/work/venv-app2-native/bin/python
test "${#PWD}" -lt 100
test "${#TMPDIR}" -lt 100
```

Then run the owned runner's offline preflight, which reports all failures
together and performs exactly one Playwright `--list` collection (one test in
one file), without starting Vite, Runtime, a browser, a daemon, a socket, a
build, or the selected case:

```sh
env -i HOME=/root LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers NORMAL014_USE_BASE_PYTHON=1 \
  SELECTED_FINAL95_MODE=preflight \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-seed-current-main-packet-1110/artifacts/run-owned-selected-final95-current-main.sh \
  "$PWD"
```

The runner's 11 aggregate checks cover source/ancestry/cleanliness, keeper and
lock identity, Agent/Runtime/producer bytes, 76-artifact manifest and schema,
Composition13 graph, Node/Vite/Vitest/Playwright resolution, helper/driver
syntax and origin/credential scope, selected title/budgets/reload contract,
disk/lock/private-copy controls, planted refusal probes, and wrong artifact
version refusal. A zero-test or missing-list result is a failure.

## Exact guarded actual command — do not submit yet

Only after review of the preflight result, use the same clean main source and
the existing current-source keeper. The durable root is intentionally unique;
if the child fails, preserve it and do not delete or retry it:

```sh
env -i HOME=/root LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers NORMAL014_USE_BASE_PYTHON=1 \
  SELECTED_FINAL95_MODE=run APP_KEEPER_ROOT=/home/user/work/app \
  SELECTED_FINAL95_DURABLE_ROOT="/tmp/ap2-m2-selected-seed-current-main-packet-1110-retained-$$" \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-seed-current-main-packet-1110/artifacts/run-owned-selected-final95-current-main.sh \
  "$PWD"
```

The runner retains the original command recipe: hosted build, then the
existing browser-locked `npm run test:e2e:three-products -- --grep "$TEST_TITLE"`.
It uses one private `mktemp` root, private source clones, one private App
overlay, private Vite/npm/Playwright caches, and `TMPDIR` under that short
root. No new install, graph, fallback, timeout, selector, navigation, or
credential authority is introduced.

Failure retention copies `child.log` and independently present
`browser-output/{dom.html,error-context.md,trace.zip}`. DOM is optional. Every
bounded copy checks source existence, byte limit, size read, and `cp` status;
durable-root creation, mode, each copy, identity write, manifest generation,
and nonempty `SHA256SUMS` all return explicitly on failure. The child exit
status is preserved when retention succeeds; the run root is cleaned; the
durable failure root remains. `BODY`/partial trace/context is evidence of the
launch/output phase only, not P1/P2 or browser-behavior success.

Changed live callers: **NONE** (runner/design and source/test identity only).
No actual, browser, socket, daemon, build, install, central service request,
or full suite was run for this packet.
