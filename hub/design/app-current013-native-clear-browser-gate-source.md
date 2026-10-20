# current013 native transition None browser gate — source prepared, actual run pending

Source task complete. No actual browser acceptance, writer retirement or paired qualification is claimed. Read PLAN first and the 07:00 owner ruling in `managers/app/INBOX.md`: None silently failing to publish is a pre-existing legacy defect; positive removal assertions must stay intact. No decision was changed or disputed.

Worktree: `/home/user/work/wt/app-m2-current013-native-clear-browser-gate-source`; base `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`, tree `f33b5268678efe390a5732022d81b53f35ccf509`. This task deliberately adds test source to that base; it does not compose or activate product code. Harness will assign the resulting commit. Native None source authority remains independently approved `80c65d5a5e1a52abe18f1ef7ead500c7407328f9`. Required guard wrapper source is approved `cee35da4b1ed653db50dd9d5c26693fab00f04ad`.

## Exactly two additive browser cases

Both live at the end of `tests/e2e/local/three-products.spec.ts`, selected by **`--grep 'M2 native None'`**. The complete original file is an unchanged prefix: all seven existing case bodies, expectations, hooks and helpers retain their bytes. No failure markers, skips, assertion weakening or M1 rewrites were added.

1. **`M2 native None single: ordinary default crossfade clears raw mirrors, reloads, retries exactly after restart and undoes through Runtime`**. The original ordinary/default `{type:'crossfade', duration:0.5}` is explicitly checked before using the installed inspector's None control. The request must be official `clip.set` v1, exactly `values:{}, clear:['transition']`, with the original publication/revision and raw transition expectation. Both raw clip mirrors must lack the own transition key; null/sentinel substitution fails. Runtime history must record the original command and a tagged ABSENT write, and immutable parent/shot/internal reads must match the receipt's canonical closure. Lose the real accepted response, restart the same Runtime, reload the browser, verify the persisted exact request, explicitly recover it, and require identical body/key/status/receipt/result with no duplicate revision/history entry. Use the App Undo button and assert an actual `timeline.inverse` request, Runtime `undo_of`, exact raw restoration and another reload. Zero observed legacy composition-revision POSTs and the existing credential sniff are required.
2. **`M2 native None bulk: one original-basis atomic clear preserves unknown revision and opaque data; real conflict retains the whole draft`**. Shift-select two actual clips and assert the mounted inspector says `2 clips selected`. One durable intent/request must contain exactly two guarded clears on the original common base. The second fixture transition carries an unknown revision, explicit nulls, nested ordering and literal `__proto__`/`constructor`/`prototype` keys. Accepted raw parent comparisons remove only the two transition leaves, preserving all other parent/opaque/occurrence content; immutable closure/history and ABSENT records are required. Lose the ACK and require exact retry with only one publication, reload both cleared controls, then undo the whole batch and reload the exact original raw parent, including unknown revision and literal own keys. Capture a second bulk clear and hold delivery; the real Agent captures and commits one guarded transition clear against the same original base. Release the unchanged App request: it must return a real non-stale-head 409 conflict, retain both original commands/basis/request identity as one intent, and create no partial revision. Reload/recover the rejected owner; both local controls must still show None while accepted Runtime content holds only the Agent's clear. Recovery must not retransmit. Zero legacy traffic remains required.

The fixture is the existing normal direct Runtime + three-products seed, followed by the existing `enableTimelineAuthoring` profile startup, not a mock backend. A worker fixture override selects an optional seed variant, leaving ordinary seeding unchanged for the original cohort. Existing Python retained-revision capture gains only a `clear-transition` branch using the official `capture_clip_set`; no new endpoint/wire operation, launcher service, journal or fixture framework exists. Renderer/render tasks are never requested by these cases.

Five source paths only, +399/-2 lines (net +397):

- `tests/e2e/local/three-products.spec.ts`: +250 additive test/helper lines.
- `tests/e2e/local/support/harness.ts`: optional seed variant (+11/-1).
- `tests/e2e/local/support/astrid.ts`: official Agent clear capture branch (+5/-1).
- `scripts/testing/current013-native-none.mjs`: 37-line grep launcher.
- `tests/e2e/local/support/current013-native-none.test.mjs`: 96 lines of pure launcher controls.

The small launcher is needed because the reviewed current013 wrapper launches the entire existing cohort. It imports that wrapper's exact `readCurrent013Inputs` and `checkCurrent013Sources` instead of duplicating any lock/cleanliness/archive/vendor guard. It checks before/after the child, preserves nonzero/null/throw failures, passes validated source identities/venv executable paths and delegates only the named grep. **The wrapper file is intentionally absent from this worker's base: compose the approved wrapper and native None product source before invoking this new launcher.** The pure tests substitute guard/child modules and prove launcher control flow only; their synthetic identities are not a paired acceptance result.

## Validation actually run

All from the assigned App worktree. `O` below is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`; `W=$O/workers/app-m2-current013-native-clear-browser-gate-source`.

```sh
node --experimental-vm-modules --test --experimental-test-isolation=none tests/e2e/local/support/current013-native-none.test.mjs
```

Exit 0: **6 passed, 0 failed/skipped**. Explicit enablement, guard refusal before delegation, exact grep/validated tuple forwarding, child exit 7/null, changed postflight fingerprint, postflight after launch exception. An initial default-isolation run exited 0 with a file-level 1/1 summary; the isolation-none run above is the six-case evidence.

```sh
PWTEST_CACHE_DIR="$W/notes/playwright-cache" node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list --grep 'M2 native None'
```

Exit 0: **exactly 2 cases collected**, no global setup or fixture/browser/build/socket execution. Earlier unfiltered collection also found **9 total = original 7 + new 2**. Initial collections used `PLAYWRIGHT_TEST_CACHE_DIR`, which this installed Playwright does not recognize; those used its default `/tmp/playwright-transform-cache-<uid>` location. Final collection uses the verified supported `PWTEST_CACHE_DIR`. No shared node_modules/.vite cache, dependency, venv or runtime file was modified; no shared default /tmp cache was deleted.

```sh
node node_modules/eslint/bin/eslint.js scripts/testing/current013-native-none.mjs tests/e2e/local/support/current013-native-none.test.mjs tests/e2e/local/three-products.spec.ts tests/e2e/local/support/astrid.ts tests/e2e/local/support/harness.ts --max-warnings 0
node --check scripts/testing/current013-native-none.mjs
node --check tests/e2e/local/support/current013-native-none.test.mjs
python "$W/notes/source-audit.py"
git diff --check
```

All exit 0, zero lint warnings. Audit: unchanged original seven cases by byte prefix; exactly two additive cases; unchanged configs/global setup/package/normal Runtime pin; exactly the five-path source scope; unchanged Git index. No product/root/pin/generated client changes. No full suite, central request, actual browser run, build, renderer, localhost/socket, tsc or install was run or requested. No build/temp output remains in the worktree. Shared dependencies were used read-only; there is no claim of a recursive before/after dependency metadata audit.

## Required final source inputs and future central invocation

Actual qualification is still pending **matching Agent905 integration + a frozen composed App None root including the reviewed wrapper and these tests**. Observed Agent candidate is `905a4f0f1dcadf92a226b1da0baba50b8a37178d`; checked integration `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` did not contain it (`git merge-base --is-ancestor ...` exited 1). Do not use either observation as a final run pin. The final App commit/TREE, actual merged matching Agent SHA and retained checkout paths must be supplied by the manager; none is invented here.

The existing guards require:

- exact final App **TREE**, with tracked/staged/untracked source clean at start/end (snapshot commit may differ);
- full actual matching Agent SHA + retained absolute checkout + exact executable venv path;
- Runtime **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`**, retained Runtime checkout and producer checkout at that HEAD, both clean;
- contract **0.2.13**, schema **`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`**, component manifest **`sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`**, artifact manifest **`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`**, 75 entries and successful producer-backed normal App/Agent vendor checks;
- both immutable Composition **0.0.12** archives, 77 members, SHA-256 **`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`**;
- normal hosted freshness/build authority, no `ASTRID_APP_DIRECT_DIST` override; private tool/config caches and output paths, with shared dependencies read-only. `PWTEST_CACHE_DIR` controls Playwright, `npm_config_cache` controls npm; neither claims to relocate Vite's config bundle/cache. The manager must resolve the existing Vite private-cache prerequisite before an actual build, as already required by wrapper review. This worker did not change the normal build helper or invent an unsupported Vite cache environment variable.

After verifying those prerequisites, the manager registers **one new named suite** with a **complete literal command**. The following is a non-executable substitution recipe: every `__...__` token must be replaced in `tests/suites.conf`, including the suite name, before requesting it. Use the central App snapshot cwd; do not hardcode this worker checkout as the App cwd. Do not edit/reuse the old incomplete `e2e-current013-integration` placeholder or central bins.

```text
app e2e-current013-native-none-a__FINAL_AGENT_FULL_SHA__-t__FINAL_APP_TREE__ flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_TREE=__FINAL_APP_TREE__ TIMELINE_CURRENT013_AGENT_SHA=__FINAL_AGENT_FULL_SHA__ TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=__RETAINED_PRODUCER_ABSOLUTE_PATH__ ASTRID_CHECKOUT=__RETAINED_FINAL_AGENT_ABSOLUTE_PATH__ ASTRID_RUNTIME_CHECKOUT=__RETAINED_RUNTIME013_ABSOLUTE_PATH__ ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python npm_config_cache=__PRIVATE_NPM_CACHE_ABSOLUTE_PATH__ PWTEST_CACHE_DIR=__PRIVATE_PLAYWRIGHT_CACHE_ABSOLUTE_PATH__ PLAYWRIGHT_OUTPUT_DIR=__PRIVATE_BROWSER_OUTPUT_ABSOLUTE_PATH__ TMPDIR=__PRIVATE_TMP_ABSOLUTE_PATH__ PYTHONDONTWRITEBYTECODE=1 node scripts/testing/current013-native-none.mjs
```

This exact complete command/name establishes the service cache identity. Requester exports are not forwarded by `request-test` and are not a substitute for literal registration. Only after registration and authorization:

```sh
R=$("$O/bin/request-test" app-m2-current013-native-clear-browser-gate-source __NEW_EXACT_SUITE_NAME__) && "$O/bin/wait-test" "$R"
```

If wait exits 124, wait on that same result; do not resubmit. This source task has no authorized actual run and made no such request. A future pass must include the exact pair's acceptance/reload/inverse/retry/conflict/zero-legacy assertions above before claiming D01 native None closure or removing a legacy writer. These two cases are representative single/bulk None coverage, not a claim of all scalar, Remove-button, mobile, frame/audio or all-writer qualification.

No local source-task blocker. Next: review/compose the five-path test delta onto the safe013/nativeNone root, freeze actual matching Agent and producer paths, verify the private-cache setup, then register/run only the new named central lane. Typechecking and actual browser/runtime behavior remain unverified. No KEEP request; recycle after harness capture.
