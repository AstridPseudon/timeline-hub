# current013 wrapper repair composed on approved normal013 root

**SOURCE ONLY; repair complete, exact-pair qualification pending.** No settled PLAN decision changed. Actual matching Agent SHA remains unpublished/unsupplied for this task; no wait, guessed pair, browser acceptance, or parity claim.

## Exact source

- Worktree: `/home/user/work/wt/app-m3-current013-wrapper-fix-compose`.
- Base HEAD: approved normal013 root `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`.
- Base tree: `f33b5268678efe390a5732022d81b53f35ccf509`.
- Composed source TREE: **`2b304de3a92faa011b289cd99859c5e43c57e8fe`**.
- Exactly two added App paths: `scripts/testing/current013-integration.mjs` (240 lines) and `scripts/testing/current013-integration.test.mjs` (225 lines). No other App path, product code, package/lock, generated client, pin, normal runner, or original journey changed.
- Started with exactly the two additions from `git diff 0ea988bdd ba8ae7228b460b0188170276e6711725d45c352c`; then repaired those paths only. The old base's package/Runtime pins were not copied.

The TREE was calculated without writing an index or Git objects, using the existing HEAD tree entries and Git blob/tree SHA-1 encoding for the two additions. Reproduction script: `workers/app-m3-current013-wrapper-fix-compose/notes/source-tree.py` under ORCH. Harness should confirm the committed TREE equals the value above. App commit identity is intentionally unrestricted when the TREE matches, including central snapshot commits.

## Repairs and decisions

1. Add App to the existing `checkClean` calls, which run in preflight and postflight. The existing porcelain command covers tracked modifications, staged changes, and untracked source; ignored normal build/test output remains allowed.
2. Require absolute existing executable Python files with `accessSync(..., X_OK)` and preserve the supplied path. Do not realpath the venv entry point. Source directory normalization stays as before.
3. Export the existing normal launcher as `runCurrent013Integration` for direct unit controls. Its CLI still invokes exactly `npm run test:e2e:three-products`; no alternate runner, browser fixture, or shadow journey was introduced.
4. Correct prep prose from six to seven journeys and replace the absent hardcoded producer path with `${FINAL_RUNTIME_PRODUCER_CHECKOUT:?supply ...}`. Document the central service's actual environment/cache behavior and remove obsolete claims that this approved App root still carries the old normal pin.

No new policy decisions were needed. Test fixtures substitute only Git responses/vendor-child execution and exercise the real wrapper/file checks; they are launcher controls, not cross-product qualification. The original three input tests retain their expectations with private portable fixture paths.

## Exact checks and results

Run from the assigned worktree unless absolute paths are shown. `O` below denotes `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

```sh
node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs
```

Exit 0: **15 passed, 0 failed**. Controls cover all eight required inputs, abbreviated SHAs, wrong Runtime, relative/missing paths, dist override refusal, executable checks for both Python inputs, two real private symlinked venvs retaining their actual `sys.prefix`, same-TREE/different-commit snapshot acceptance, normal ignored output, dirty/staged/untracked App preflight refusal, postflight App mutation, child exit 7/null, postflight metadata failure when the child also fails, and changed fingerprint bytes with unchanged field values. Git/child results are controlled; no actual browser/build/vendor qualification runs.

```sh
node --experimental-vm-modules "$O/workers/app-m3-current013-wrapper-fix-compose/notes/review-probes.mjs"
```

Exit 0: **18 independent review checks completed**. This is a retained copy of the original independent probe with its App path redirected and the three defect-detection expectations corrected to repaired behavior (venv preservation, App-dirty refusal, required producer input). The original review file is untouched. No subprocess is launched by this probe.

```sh
node --check scripts/testing/current013-integration.mjs
node --check scripts/testing/current013-integration.test.mjs
git diff --exit-code 171a259acbeb3ced855ca8f72fed0943a2f5a5cb
git ls-files --others --exclude-standard
git diff --exit-code ba8ae7228b460b0188170276e6711725d45c352c -- tests/e2e playwright.three-products.config.ts playwright.direct.config.ts package.json scripts/vendor-lock.mjs
git diff --check
git check-ignore --no-index dist/current013-smoke
python3 "$O/workers/app-m3-current013-wrapper-fix-compose/notes/source-tree.py"
```

All exit 0. Tracked diff is empty; the untracked list is exactly the two additions above. Original journey/helper/config/package/vendor-check bytes match the reviewed wrapper source. `dist/current013-smoke` is ignored (no output file was created). Tree script prints `2b304de3a92faa011b289cd99859c5e43c57e8fe`.

```sh
/home/user/work/venv-agent/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
/home/user/work/venv-runtime/bin/python -I -B -c 'import sys; print(sys.executable, sys.prefix)'
env -u TIMELINE_CURRENT013_RUN node scripts/testing/current013-integration.mjs
```

Both prefix commands exit 0 and show their supplied executable paths with prefixes `/home/user/work/venv-agent` and `/home/user/work/venv-runtime`. The final command intentionally exits 1 at the explicit manager-input guard, before child launch.

Initial diagnostic runs: default `node --test scripts/testing/current013-integration.test.mjs` failed in Node's sandbox subprocess mode; a direct run then exposed `spawnSync python3 EPERM` despite status 0/output. The prefix test now uses asynchronous `execFile` (no EPERM), and the full targeted file passes with Node's supported isolation-none flag. No assertion was disabled or weakened. The additional fingerprint control was included in the final 15-test pass.

No full suite, central request, build, browser, localhost/socket, project tsc, dependency install, or dependency/cache mutation was performed. Shared dependencies were read only; fixtures were private and cleaned. No commit/merge/checkout/push or central bin/suite edit occurred.

## Next central command recipe — manager only, after final Agent publication

`request-test` records target/suite/files; it does **not** forward requester environment/cache variables. `test-run` caches by repo + App TREE + suite + files + complete command (+ integration refs for cross-product suites). A worker-local `env ... request-test ...` or a dispatcher environment change cannot bind the final pair or safely establish a new cache identity.

After reviewing this repair and obtaining the actual matching Agent SHA, the manager will add **ONE new exact named suite command**. Leave the existing `e2e-current013-integration` line and central bins unchanged. The new suite's literal full Agent SHA, full App TREE, retained absolute source/producer/venv paths, and private cache/output locations must appear in its command and cache identity. Retained Runtime and producer HEADs must both equal `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.

The following is an intentionally incomplete substitution recipe, **not an executable registered command**. Replace every `__...__` token with verified literal values before adding the single line to `tests/suites.conf`. Confirm the final App TREE after harness commit; use the TREE above only if no source changes intervene. The central service runs from its own App snapshot, so there is no hardcoded external App cwd.

```text
app e2e-current013-a__FINAL_AGENT_FULL_SHA__-t2b304de3a92faa011b289cd99859c5e43c57e8fe flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_TREE=2b304de3a92faa011b289cd99859c5e43c57e8fe TIMELINE_CURRENT013_AGENT_SHA=__FINAL_AGENT_FULL_SHA__ TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=__RETAINED_PRODUCER_ABSOLUTE_PATH__ ASTRID_CHECKOUT=__FINAL_AGENT_ABSOLUTE_PATH__ ASTRID_RUNTIME_CHECKOUT=__RETAINED_RUNTIME_ABSOLUTE_PATH__ ASTRID_PYTHON=__AGENT_VENV_EXECUTABLE_ABSOLUTE_PATH__ ASTRID_RUNTIME_PYTHON=__RUNTIME_VENV_EXECUTABLE_ABSOLUTE_PATH__ npm_config_cache=__PRIVATE_NPM_CACHE_ABSOLUTE_PATH__ PLAYWRIGHT_OUTPUT_DIR=__PRIVATE_BROWSER_OUTPUT_ABSOLUTE_PATH__ PYTHONDONTWRITEBYTECODE=1 node scripts/testing/current013-integration.mjs
```

The new name and literal command change the service cache key; do not reuse the old placeholder suite's cached result. `npm_config_cache` configures npm only: it does not assert that Vite honors an arbitrary cache env var. Before the central run, the manager must ensure the unchanged normal runner keeps all tool/config caches private and shared node_modules/venvs read only. Continue using the existing hosted freshness helper and original seven journeys, with no supplied `ASTRID_APP_DIRECT_DIST` and no alternate e2e suite.

Only after that new literal line is registered, request it through the existing service interface (no requester env prefix):

```sh
R=$("$O/bin/request-test" app-m3-current013-wrapper-fix-compose "__NEW_EXACT_SUITE_NAME__") && "$O/bin/wait-test" "$R"
```

Do not run this while Agent is pending. If the wait returns 124, wait on the same result again. Keep this worktree for manager-owned final typecheck/review/gate; no such typecheck or gate is claimed by this worker. No local implementation blocker remains; final-pair acceptance depends on actual Agent publication and central execution.
