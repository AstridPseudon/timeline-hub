# App M2 producer exact custody rebind — 0721

## Result

Prepared an owned, dormant custody packet for the already-committed 0717 App
source. No App product file was edited in this worker, and no browser, build,
daemon, socket, startup, actual, full suite, install, or new pin was run.

The protected keeper is the exact 0717 source:

```text
App HEAD  6b0267c62aa8773132f1496d5014279e6c1edf61
App tree  c1ac3383624322ae8d67b10dee36965670d91cd7
helper    d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b
spec      d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
config    5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
wrapper   329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
```

`git diff b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7..6b0267c62aa8773132f1496d5014279e6c1edf61`
contains exactly one path: the helper. The helper change is the existing
single import of Playwright `expect`; assertions, spec, config, wrapper,
probe, harness, body, and source behavior remain unchanged.

## Owned artifacts and final hashes

Artifacts are under:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-import-exact-custody-rebind-0721/artifacts/
```

```text
producer-health-realm-offline-review.mjs       a681e0a4ff618a103195c4cd6704556f9f3d13f841cf687b99b6f810faee2561
producer-physical-keeper-gate-owned.sh         8c451c478f3cfd9a25da3c30b2726fa7df48cb2736b98f13d0c5be0de90e468d
producer-startup-only-gate-owned.sh            38228fa42c0a17ada7b1a2aa74946a85a85793567814ddf5cb974a9560641502
producer-startup-custody-gate-owned.sh         0a4baf1b2f3982daa84f6cbe3fe0a6f73850d4a094eafd37f0e3dd06be7c3d29
producer-startup-only-probe-owned.mts          a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
producer-startup-module-format-probe-owned.mts d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
```

The source gate binds keeper `/home/user/work/wt/ap2-m2-producer-helper-expect-import-0717`,
HEAD `6b0267c62aa8773132f1496d5014279e6c1edf61`, tree
`c1ac3383624322ae8d67b10dee36965670d91cd7`, and the 0717 `KEEP` marker.
The startup gate binds the same keeper and its owned source/probe paths. The
custody gate rebinds those paths, the source/startup gate hashes, and only the
helper hash to `d86721bd...`; all other hashes remain the passing 0703 values:

```text
Agent  8130a401bf44a518d5a40ae274d398b8c560be55 / 236c3e57e0265c52b81ba8085de3193026176bff
Runtime 2c4ac180c2220bdad966bc01e95ad230e99ce26a / 7ab412cc4bcbe517efcfa806e092336390312e18
body commit/tree 36dd91257fd13dcad0d58b48c790caa5063b4c8c / d908845dbc8e5ebf96698d08621557e904f20c52
graph archive 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
tsx bin/CLI 8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8
tsx loader 0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1
tsx package 6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2
```

## Minimality and reverse proof

The three copied shell gates differ from their 0703 owned predecessors only
by the declared binding changes:

- keeper path, HEAD, tree, and `KEEP` path;
- owned source/startup/probe/format-probe paths and transitive gate hashes;
- helper SHA in the custody gate.

The offline review, startup probes, and format probe are byte-identical. A
memory-only reverse substitution of every declared binding reproduced all
three original gate files byte-for-byte. The reverse proof also compared the
immutable probes/review with `cmp`-equivalent byte comparisons and passed.
No original artifact was edited.

The custody structure preserves the existing service-captured `SERVICE_TREE`
as a separate value from protected keeper `KEEPER_HEAD`/`KEEPER_TREE`, physical
TMPDIR and early cleanup, the planted Runtime-root symlink negative, physical
Runtime positive, direct/door identity checks, source/body/Agent/Runtime,
all75, graph9412, all77, and tsx pins, zero-test and child-exit handling, drift and
unknown-mode refusals, and the existing selector/path/argv controls.

## Checks

```text
for f in artifacts/*.sh; do sh -n "$f"; done
  PASS — all owned shell gates

node producer-health-realm-offline-review.mjs <current App> <owned artifacts>
  PASS — matching/wrong identity/version, direct/door mapping, and physical,
         symlink, teardown, and no-producer-body guards

memory-only reverse binding proof
  PASS — all three rebound gates restored their 0703 originals exactly

source/keeper/hash assertions
  PASS — 0717 HEAD/tree/helper/spec/config/wrapper; keeper clean; `KEEP`
         present; node_modules still points to /home/user/work/app/node_modules

git diff --check and worker worktree status
  PASS — no App worktree changes
```

The passing startup evidence reused is 0703 startup test
`...health-conversion-review-0703-startup-1021070652-30920`; it was not
replayed. No new startup or build was requested.

## Dormant suite and literal future recipe

Registered one unique, hash-bound dormant suite in
`scratchpad/orch/tests/suites.conf`:

```text
ap2-m2-producer-helper-expect-import-0717-actual-0a4baf1b2f39-integration
```

Its command verifies custody hash
`0a4baf1b2f3982daa84f6cbe3fe0a6f73850d4a094eafd37f0e3dd06be7c3d29` and
delegates to the owned custody gate in `run` mode. It was not executed.

After an independent delta/custody review, the future request must target the
0717 service source, never 0538:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-producer-helper-expect-import-0717 \
  ap2-m2-producer-helper-expect-import-0717-actual-0a4baf1b2f39-integration \
  --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The existing wrapper's `list` branch remains the one-test guard (`Total: 1
test in 1 file`); the `run` branch preserves the one-pass-or-one-fail and
child-status guard. Do not treat this dormant recipe as executed evidence.

## Important unverified boundary

The required unchanged wrapper still contains its pre-existing source/helper
pins (`APP_SOURCE_SHA=00bbc22d...` and `HELPER_SHA=50cbe534...`). This packet
does not alter or bypass those bytes. Therefore no claim is made that a future
actual will pass the unchanged wrapper's approved-delta/helper checks; the
independent delta/custody reviewer must resolve that boundary before any
actual. The 0717 source, keeper, and custody bindings themselves are exact.
