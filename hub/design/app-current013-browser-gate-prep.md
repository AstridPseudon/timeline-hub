# App current013 exact-pair browser gate preparation

Manager11:57: **HOLD supersedes READY-only below.** Independent review found missing App tracked/staged cleanliness checks and Python symlink normalization that loses venv identity. See app-current013-wrapper-independent-review.md. Fix-and-compose worker is active on approved normal013Root171a; no invocation before repair and review. Final exact inputs must be bound into a new named central suite command/cache identity after actual Agent publication; caller environment on request-test is not forwarded.

Status: READY-ONLY. This is a launcher/preflight for the existing M1
renderer-off three-products journey. It is not a qualification result and it
does not invoke a browser, build, render, Runtime socket, or four-case frame
parity lane.

## What landed in the App worktree

- `scripts/testing/current013-integration.mjs`: a small central wrapper.
- `scripts/testing/current013-integration.test.mjs`: pure input-guard tests.
- The central test-service allow-list has the named suite
  `app e2e-current013-integration`.

The wrapper delegates to the existing `npm run test:e2e:three-products`
configuration and `tests/e2e/local/three-products.spec.ts`; it does not change
any of the seven existing cases, the 21 existing helpers, or their assertions.
That suite includes the additive M2 after-ACK Gate 5 case already present in
the 0ea/current source. It does not invoke `viewing-parity` or any frame grant.

## Exact ready command

Run centrally, only after the manager supplies the actual final Agent SHA and
App tree and approves this M1 renderer-off lane:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_TREE="$FINAL_APP_TREE" \
  TIMELINE_CURRENT013_AGENT_SHA="$FINAL_AGENT_SHA" \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="${FINAL_RUNTIME_PRODUCER_CHECKOUT:?supply retained checkout at the published Runtime SHA}" \
  ASTRID_CHECKOUT="$FINAL_AGENT_CHECKOUT" \
  ASTRID_RUNTIME_CHECKOUT="$FINAL_RUNTIME_CHECKOUT" \
  ASTRID_PYTHON="$FINAL_AGENT_PYTHON" \
  ASTRID_RUNTIME_PYTHON="$FINAL_RUNTIME_PYTHON" \
  node scripts/testing/current013-integration.mjs
```

The existing named central suite is an incomplete placeholder and MUST NOT be requested as qualification:

```text
app e2e-current013-integration flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 node scripts/testing/current013-integration.mjs
```

`request-test` does not forward the requester's environment or cache variables.
When the final Agent is published, the manager will add ONE new exact named
suite command with literal retained checkout/producer/venv paths, the actual
full Agent SHA and final App TREE, and private cache/output paths. Its new
suite name and complete command must encode that exact pair/cache identity;
worker-local exports or dispatcher environment changes are insufficient.
Do not edit the existing suite line, `bin/test-run`, or other central bins
for this repair. See `app-current013-wrapper-fix-compose.md` for the recipe.
No exact final Agent SHA or central command is claimed here.

The wrapper refuses missing inputs, refuses the old/moving checkout defaults,
rejects `ASTRID_APP_DIRECT_DIST`, and passes the validated Agent/Runtime SHAs
to the existing three-products source guard as
`TIMELINE_BUNDLE_AGENT_HEAD` and `TIMELINE_BUNDLE_RUNTIME_HEAD`.

## Required source inputs and checks

Before the suite starts, and again after it ends, the wrapper requires and
checks:

- `TIMELINE_CURRENT013_APP_TREE`: exact 40-character App tree. App HEAD is
  intentionally not required to equal a pin; a central snapshot commit may
  differ while its tree matches this value.
- `ASTRID_CHECKOUT` and `TIMELINE_CURRENT013_AGENT_SHA`: the actual Agent
  checkout and exact matching HEAD.
- `ASTRID_RUNTIME_CHECKOUT` and
  `TIMELINE_CURRENT013_RUNTIME_SHA`: the actual Runtime checkout and the
  published Runtime SHA `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- `TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT`: the read-only producer
  checkout at that same Runtime SHA. The exact path is an input, not a moving
  repo default.
- `ASTRID_PYTHON` and `ASTRID_RUNTIME_PYTHON`: absolute executable files;
  retain the supplied venv entry points without realpath normalization.
- App tracked/staged and untracked source must be clean at both boundaries;
  normal ignored build/test output is allowed. App identity stays TREE based.

It compares both App and Agent normal Runtime locks to the published current
tuple: source `2c4ac180...`, contract `0.2.13`, schema
`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
component manifest
`sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
and artifact manifest version
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
with 75 entries. It runs the existing App `vendor-lock.mjs` and Agent
`vendor_lock.py` checks against the supplied producer checkout.

It also checks the immutable Composition 0.0.12 archive in both consumers:
77 regular `package/` members and archive SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

The start/end fingerprints include the source roots, exact consumer metadata,
Runtime manifest, lock bytes, and both Composition archive identities. Any
change fails closed. The existing three-products suite additionally records
and checks its Runtime/Agent source tuple at start/end.

The existing `tests/e2e/local/global-setup.ts` remains the build authority. The
wrapper deliberately forbids `ASTRID_APP_DIRECT_DIST`, so a stale caller-supplied
dist cannot bypass its normal freshness check.

## Still pending

- Agent’s final matching public12/current-tuple SHA is not supplied.
- Approved App normal013 root is `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`
  (tree `f33b5268678efe390a5732022d81b53f35ccf509`); the two wrapper
  paths are composed onto it by the repair worker. This is source preparation,
  not exact-pair browser evidence.
- No exact final Runtime producer checkout or final Agent checkout has been
  supplied for the future central invocation. Existing venv paths must be
  supplied literally by the manager as part of that exact command.
- Actual M1 renderer-off browser evidence, Gate 5 acceptance, and any later
  frame/audio parity grant remain unrun.

Frame parity remains a separate gate and requires its own fresh grant; this
wrapper never requests or implies that grant.

