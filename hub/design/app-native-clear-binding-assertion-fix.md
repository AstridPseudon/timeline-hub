# Native parent clear binding assertion — fixed source, acceptance pending

Read PLAN.md and app-native-clear-browser-source-review.md. No settled decision changed or disputed. D01 native None acceptance and writer retirement remain open.

Assigned worktree: `/home/user/work/wt/app-m2-native-clear-binding-assertion-fix`. Starting App commit `546fd8464e6ccc1ddf46be2c56c2ca3471df112a`, tree `bc6e87c1b4588c4b400de7dcadf24c8259ce630c`. The harness will commit the corrected source; no new commit/tree identity is claimed here.

## Old/new assertion pair and scope

At `tests/e2e/local/three-products.spec.ts:1340`:

```ts
// Old: rejects the approved parent capture and accepts invented parent ownership.
expect(command.bindings).toMatchObject({ 'scalar.owner': 'parent', 'scalar.target': command.select });
// New: matches the exact parent golden and forbids any owner key, including undefined.
expect(command.bindings).toStrictEqual({ 'scalar.target': command.select });
```

This is the only changed line in the existing spec. Parent selection remains exactly `parent/clip:<id>`; the original base revision/publication, operation/version, tagged raw transition expectation, nonempty reads and closed clear arguments remain intact. Every reload, undo, retry, conflict, zero-legacy and opaque-data assertion is byte-identical. The entire original seven-case spec remains a byte-identical prefix of `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`. No old helper inputs, product code, capture bindings, configs, pins or dependencies changed.

Added a 35-line pure contract test and a 34-line frozen fixture extract under `tests/e2e/local/support/`. The test reads/transpiles only the actual `expectTransitionClear` function and exercises the installed Playwright matcher without registering the spec or executing fixtures. The complete parent command (including reads) and original clip are copied without semantic changes from the official App S2 fixture at `80c65d5a5e1a52abe18f1ef7ead500c7407328f9`; the audit verifies exact JSON equality with Agent `905a4f0f1dcadf92a226b1da0baba50b8a37178d`'s corresponding fixture. Full fixture paths are retained in the extract. Occurrence-only owner binding remains the native policy.

The positive test accepts the real golden. The negative test rejects invented `scalar.owner: 'parent'`, an own owner key with undefined value, a mismatched target and empty bindings. Strict equality was chosen to enforce exact target-only shape and owner absence.

## Exact validation

All commands ran from the assigned worktree. `W` below denotes `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-native-clear-binding-assertion-fix`.

```sh
node --experimental-vm-modules --test --experimental-test-isolation=none tests/e2e/local/support/current013-native-none.test.mjs
```

Exit 0: **6 launcher tests passed**, zero failures/skips/todo. Launcher/guard control flow only; no real wrapper invocation.

```sh
node --test --experimental-test-isolation=none tests/e2e/local/support/native-transition-clear.contract.test.mjs
```

Final exit 0: **2 contract tests passed**, zero failures/skips/todo. Before the binding fix, this command exited 1 with both tests failing: the old helper rejected the official golden and accepted the invented owner. An intermediate loader used a separate VM context, causing strict equality to reject different object prototypes; using `compileFunction` in the matcher context fixed that test-loader issue. Final checks exercise the unchanged golden and actual corrected helper.

```sh
PWTEST_CACHE_DIR="$W/playwright-cache" node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list --grep 'M2 native None'
```

Exit 0: **exactly 2 cases discovered**, single at line 1382 and bulk at line 1458. Collection only; no global setup/browser/build/socket execution.

```sh
node node_modules/eslint/bin/eslint.js scripts/testing/current013-native-none.mjs tests/e2e/local/support/current013-native-none.test.mjs tests/e2e/local/support/native-transition-clear.contract.test.mjs tests/e2e/local/three-products.spec.ts tests/e2e/local/support/astrid.ts tests/e2e/local/support/harness.ts --max-warnings 0
node --check scripts/testing/current013-native-none.mjs
node --check tests/e2e/local/support/current013-native-none.test.mjs
node --check tests/e2e/local/support/native-transition-clear.contract.test.mjs
python "$W/verify-source.py"
git diff --check
```

All exit 0; lint has zero warnings. The retained audit verifies the single-line spec delta, original seven cases/helpers, all other new assertions, unchanged support/launcher inputs, configs/pins/old positive None tests, and the fixture extract against both frozen sources. It also confirms the wrapper and native product port remain absent from this starting tree.

No actual browser, socket, build, full suite, central test request, tsc, install, renderer or native acceptance was run. Shared node_modules/caches/venvs/runtimes were used read-only; Playwright collection used the worker-private cache, removed afterward. No private Composition package was needed for the pure matcher/launcher/collection checks. Normal source Composition 0.0.12 pins remain unchanged; runtime package/archive qualification was not performed. No build/temp output remains in the worktree.

## Composition still required

Compose this repaired test delta with the approved native None product source `80c65d5a5e1a52abe18f1ef7ead500c7407328f9` and current013 guard wrapper `cee35da4b1ed653db50dd9d5c26693fab00f04ad` onto the safe current013 root. Retain normal generated-client/lock and Composition 0.0.12 authority. Supply the clean, actually matching Agent integration including the native capture associated with `905a4f0f1dcadf92a226b1da0baba50b8a37178d`; that source observation is not a final merged pin. Freeze Runtime/producer at `2c4ac180c2220bdad966bc01e95ad230e99ce26a` and freeze the resulting App TREE.

Before the future central browser run, establish the private cache/build arrangement without modifying shared dependencies, retain normal hosted freshness/build authority, and register a new exact named suite invoking `node scripts/testing/current013-native-none.mjs` with literal real tuple/private-path inputs. The real wrapper must pass its existing source/lock/vendor/archive guards at both boundaries. Do not substitute missing-port success, fake acceptance, skips or an old other-tree suite. The actual two browser journeys must then prove the retained positive clear/reload/retry/inverse/conflict assertions. This repair and its matcher tests are **not native acceptance proof**.

No blocker for this bounded source task. No KEEP request.
