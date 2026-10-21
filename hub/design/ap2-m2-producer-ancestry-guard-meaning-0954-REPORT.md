# AP2 M2 producer source-ancestry guard meaning — 0954

## Verdict

The 0945 preflight failure is a real source-ancestry failure. There is no
valid data-binding-only correction that both keeps the exact source pin
`09171792bd626f5eabd421d1f1c2b497a4fc9786` and preserves the frozen baseline
`17d2518c341c47a2d8634047b400399886da3a2a` under the executed guard.

The required next step is a current-source rebase/squash, subject to
orchestrator authorization. No retry or control run was made here.

## Exact meaning of the constants

The executed owned wrapper is
`producer-runner-0717-owned.sh`, lines 85–89 and 146–159, from the 0945
artifact directory. Its executed checks are:

```sh
parent(APP_SOURCE_SHA) = APP_SOURCE_PARENT_SHA
parent(APP_SOURCE_PARENT_SHA) = APP_SHA
```

The same `APP_SHA` is independently used by `check_app_baseline` to verify
the frozen baseline commit and `APP_TREE`; it is not compared to the
checkout's current HEAD. `check_approved_delta` then binds `APP_SOURCE_SHA`
to the actual checkout ancestry and permits only the wrapper path after that
source.

| Constant | Bound identity | Exact role | Evidence |
|---|---|---|---|
| `APP_SOURCE_SHA` | `09171792bd626f5eabd421d1f1c2b497a4fc9786` | Exact source binding for the normal App profile/checkout; its tree is `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`. | `verify_app_ref` plus `check_source_ancestry`; the profile config selects the normal direct Runtime-door harness and the one producer spec, but does not select a different source. |
| `APP_SOURCE_PARENT_SHA` | Bound stale value `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` | Immediate-parent equality operand for `APP_SOURCE_SHA`. | The third equality in `check_source_ancestry`; actual `parent(09171792)=4d6ff2176c6a19fc8b5831662beb8e6d7d0e5de6`. |
| `APP_SHA` | `17d2518c341c47a2d8634047b400399886da3a2a` | Frozen unchanged-product baseline anchor, with tree `d63fe4f1e1f32a01acfc9d11cda6c29066fce162`; also the second-parent operand in the two-link ancestry check. It is not current HEAD. | `check_app_baseline`; `parent(b8cc)=17d2518`; baseline-to-source diff contains only the wrapper, producer spec, and producer helper. |

The normal profile setup does not turn `APP_SHA` into a profile/source
selector. The config at
`/home/user/work/wt/app-pin-09171792/playwright.producer-ownership-current-pin.config.ts:4-13`
just composes the direct Runtime-door config and selects the producer spec.
The wrapper's short alias is only for runner temp/cache/profile paths; its
source guards continue to inspect the original App checkout
(`producer-runner-0717-owned.sh:255-262`).

## Git and blob evidence

Read-only Git inspection of `/home/user/work/wt/app-pin-09171792` gives:

```text
09171792  tree 31b0f77c  parent 4d6ff217
4d6ff217  tree 16d17331  parent 3c2dac2a
3c2dac2a  tree b1c3485c  parent 6b0267c6
6b0267c6  tree c1ac3383  parent b8cc7e1c
b8cc7e1c  tree fd16d32f  parent 17d2518c
17d2518c  tree d63fe4f1  parent 7fafee1f
```

The intervening commits are not value lookalikes: `b8cc7e1c` changes the
wrapper, `6b0267c6` changes the producer helper, `3c2dac2a` and `4d6ff217`
change the producer spec, and `09171792` changes the producer spec/helper.
The exact baseline-to-source name-status diff is therefore:

```text
M  scripts/testing/run-producer-public13-list.sh
M  tests/e2e/local/producer-ownership-current-pin.spec.ts
M  tests/e2e/local/support/producer-ownership-current-pin.ts
```

The final source blobs match the 0945 manifest/readback:

```text
spec   6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6
helper df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949
config 5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
```

## All positive-chain 40-hex identity checks

The 0945 eight-artifact readback reports all repeated positive identity
guards as matching:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Final App `09171792bd626f5eabd421d1f1c2b497a4fc9786`, tree
  `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89` in all physical/startup/
  custody gates.
- Body `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree
  `d908845dbc8e5ebf96698d08621557e904f20c52`.
- Frozen baseline object `APP_SHA=17d2518c...`, `APP_TREE=d63fe4f...`.
- Source object/tree `APP_SOURCE_SHA=09171792...`,
  `APP_SOURCE_TREE=31b0f77c...`.

The complete mismatch set is one failed ancestry edge, plus one deterministic
follow-on failure if it is repaired in isolation:

1. **Actual mismatch:** bound `APP_SOURCE_PARENT_SHA` is
   `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`, but the exact immediate parent
   of source `09171792...` is
   `4d6ff2176c6a19fc8b5831662beb8e6d7d0e5de6`.
2. **Follow-on mismatch for the tempting one-constant repair:** changing only
   `APP_SOURCE_PARENT_SHA` to `4d6ff217...` makes the next executed equality
   require `parent(4d6ff217)=APP_SHA`; actual `parent(4d6ff217)=3c2dac2a...`,
   while the legitimate baseline anchor remains `APP_SHA=17d2518...`.
   Replacing `APP_SHA` with `3c2dac2a...` would no longer preserve the frozen
   baseline and would also conflict with its paired `APP_TREE=d63fe4f...`.

The old-before negative graph remains intentionally stale/refusing and was
not treated as a positive-chain mismatch.

## Required correction boundary

No allowed literal replacement exists for the current source pin. Do not
replace `APP_SHA` with current HEAD, do not weaken the guard to ancestry
containment, and do not treat the normal profile as a source authority.

To preserve the original source authority while retaining the unchanged
product baseline, the current source must be rebased/squashed into a new
source commit `S'` with these exact properties:

```text
tree(S')       = 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
parent(S')     = b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
parent(b8cc7e1c)= 17d2518c341c47a2d8634047b400399886da3a2a
HEAD           = S'
APP_SHA        = 17d2518c341c47a2d8634047b400399886da3a2a
APP_TREE       = d63fe4f1e1f32a01acfc9d11cda6c29066fce162
APP_SOURCE_PARENT_SHA = b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
APP_SOURCE_TREE = 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
```

That rebase preserves the final source tree and approved spec/helper/config
bytes while making the strict two-link guard true. It necessarily changes
the source commit identity from `09171792...` to `S'`; therefore it requires
an explicit orchestrator decision before any pin/artifact regeneration.

## Commands and results

Read-only commands run:

```text
git show -s --format='%H %T %P' <each App identity above>       PASS
git diff-tree --name-status 17d2518c..09171792                  PASS
git show <final source file> | sha256sum                         PASS
readback of 0945/bound-hash-readback.json                       PASS
```

The only prior execution evidence is 0945's single `sh registration.sh`
preflight: it failed at `source-ancestry`, controls `0/5`. No tests, browser,
build, daemon, socket, install, service, actual, or full run was performed by
this worker.

