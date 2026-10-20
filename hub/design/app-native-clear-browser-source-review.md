# Native transition None browser source review — HOLD

Reviewed App `546fd8464e6ccc1ddf46be2c56c2ca3471df112a`, tree `bc6e87c1b4588c4b400de7dcadf24c8259ce630c`, against its base `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`. Read `PLAN.md`, the 07:00Z None publication ruling in `managers/app/INBOX.md`, and `design/app-current013-native-clear-browser-gate-source.md`. No settled decision is disputed. D01-app-transition-none-serialization remains OPEN: discovery and launcher controls cannot establish publication, reload, inverse, retry or writer retirement.

## Blocking source finding

**P1: the new shared assertion requires a binding that the approved parent capture does not emit.** `tests/e2e/local/three-products.spec.ts:1340` requires:

```ts
expect(command.bindings).toMatchObject({ 'scalar.owner': 'parent', 'scalar.target': command.select });
```

Every new gesture targets `parent/clip:…`. In approved native source `80c65d5a5e1a52abe18f1ef7ead500c7407328f9`, `clipScalarCapture.ts`'s `target()` binds `scalar.owner` only inside `if (owner !== 'parent')`; it always binds `scalar.target`. The same commit's retained `recipe_m2_app_clip_scalar_fields.json` parent-transition-clear command has exactly `{"scalar.target":"parent/clip:f2-transition-clip"}`. Agent candidate `905a4f0f1dcadf92a226b1da0baba50b8a37178d` agrees: `_clip_scalar_commands.py` uses `_scalar_commands._target`, which also records an owner binding only for an occurrence.

A pure probe using the installed Playwright matcher and that retained golden reproduces the assertion rejection; requiring only the parent command's `scalar.target` passes. Both browser cases call this helper immediately after their first accepted clear, so composing the approved native code still leaves both cases failing before their reload/retry/inverse/conflict assertions.

Recommended repair: change this **new** helper to match the official parent capture shape, retaining the exact `parent/clip:` selector, target binding, original revision/publication pair, tagged raw transition expectation, reads, operation/version and exact clear arguments. Do not change product capture to invent a parent binding, weaken positive-removal assertions, or add failure markers. No product or test edits were made by this review.

## Source requirements checked

- Real gestures: the single case clicks the installed Effects/None control on the ordinary `{type:'crossfade',duration:0.5}` clip. Bulk shift-clicks two real clips, requires `2 clips selected`, and chooses None once. No in-page command injection or outbox mutation is introduced.
- Real authority: existing `DirectHarness`, main seeding APIs, `enableTimelineAuthoring` and normal Runtime door remain in use. Existing `faultFirstCommit` calls `route.fetch` against Runtime and only withholds/loses the returned ACK; it does not synthesize acceptance. Agent conflict capture reads the retained original closure and calls official `capture_clip_set(clear=['transition'])` using its own client credential. There is no new service framework or fixture backend bypass.
- Raw ABSENT: `expectRawTransitionsCleared` compares the entire raw parent to a clone with only the selected transition leaves deleted, then requires `Object.hasOwn(clip,'transition') === false` in both parent and config mirrors. It is not an undefined projection check. History must contain the original commands and present-to-absent writes; immutable parent/shot/internal reads must match accepted closure and receipt.
- Single: real acceptance is checked before ACK loss; Runtime restarts; reload preserves the exact pending method/path/body/key; explicit recovery must return an identical complete observed request/status/receipt/result, unchanged history and revision count. UI Undo must send `timeline.inverse` naming the accepted publication, restore the raw parent exactly, record `undo_of`, and survive another reload.
- Bulk: two commands must share the original base and one durable intent. Raw full-parent comparisons cover occurrence and unrelated opaque data. The seed includes an unknown transition revision, nulls, ordered nested arrays and literal `__proto__`, `constructor` and `prototype` data; raw inverse restoration and own-key checks preserve these. Accepted retry is exact, creates one history entry and reloads both controls as None. The second attempt is held before delivery, the real Agent changes one guarded leaf, and the unchanged App body/key must receive a non-stale-head 409 conflict. Both commands, intent ID/payload/basis and pending request survive as one rejected draft; accepted history/revisions remain unchanged. Reload/recovery retains the draft and does not retransmit; both local controls remain None while Runtime holds only the Agent clear.
- Both cases assert zero observed browser legacy composition-revision POSTs and retain credential sniffing. Fixture publication before authoring remains the existing seed operation, outside browser gesture traffic. This does not prove every App writer is retired.
- The original seven cases, hooks and helpers **inside the spec** are a byte-identical prefix of base `171a259ac`. `support/app.ts`, global setup, both Playwright configs, package file, Runtime pin and old `TransitionPreservation.test.tsx` (including positive None assertions) are unchanged. Shared `harness.ts` and `astrid.ts` are not byte-identical: their narrow optional seed and official clear-capture additions are the documented five-path delta. Existing normal seed defaults and prior operation branches are retained. No added skips/fails/fixmes were found.

## Exact composition required before actual qualification

The reviewed branch contains root `171a259ac` plus the five-path test delta; it contains **neither** `scripts/testing/current013-integration.mjs` **nor** the native `clipScalarCapture.ts` port. The new launcher imports the absent wrapper at module load. Running this branch alone is not a qualification candidate; pure VM launcher tests replace that import and cannot establish its presence or real guards.

After repairing the binding assertion, compose the reviewed test delta with the approved native None product delta from `80c65d5a5e1a52abe18f1ef7ead500c7407328f9` and wrapper from `cee35da4b1ed653db50dd9d5c26693fab00f04ad` onto the safe current013 root, preserving its normal generated client/lock and Composition 0.0.12 pins. Freeze the **resulting App TREE**, not the source branch's tree or an old integration tree. Supply a retained, clean, actually matching Agent integration including the native capture work associated with `905a4f0…`; that candidate observation is not a final merged pin. Freeze Runtime and producer at `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.

The existing wrapper requires clean tracked/staged/untracked sources at both boundaries; exact App TREE and Agent/Runtime HEADs; absolute retained checkouts and executable venv entry points; normal producer-backed App/Agent vendor checks; contract 0.2.13, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`, artifact manifest `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`/75 entries; and matching Composition archives `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`/77 members. Launcher preflight/postflight reuse those guards and preserve child failure/exception handling. The native cases must fail without native ports; no missing-port success, fake accepted response or skip is acceptable. Such a missing-port browser run was not performed here.

For the future central run, register a **new exact named suite with all real input values literally in its command**, invoking `node scripts/testing/current013-native-none.mjs` from the service's App snapshot cwd. `request-test` records target/repo/suite/files/cache only; requester exports are not a means of delivering this tuple. Neither the old incomplete `e2e-current013-integration` placeholder nor an existing other-tree suite establishes this new lane's identity. The source handoff's substitution recipe is deliberately not an executable final registration.

Keep shared dependencies read-only. Literal private `PWTEST_CACHE_DIR`, npm cache, TMPDIR and output paths must be supplied. They do not solve Vite's config-bundle/cache location: resolve that prerequisite privately before the normal hosted freshness/build path runs, retain its build authority, and prohibit `ASTRID_APP_DIRECT_DIST`. This review did not validate a future build/cache arrangement or run the real wrapper's vendor checks.

## Validation performed

Working directory: `/home/user/work/wt/app-m2-native-clear-browser-source-review`. In these exact commands, `W` denotes `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-native-clear-browser-source-review`.

```sh
node --experimental-vm-modules --test --experimental-test-isolation=none tests/e2e/local/support/current013-native-none.test.mjs
```

Exit 0: **6 passed, 0 failed/skipped/todo**. Covers explicit enablement, preflight refusal, exact grep/validated input forwarding, nonzero/null child status, postflight movement and postflight after launch exception. These are synthetic launcher controls only.

```sh
PWTEST_CACHE_DIR="$W/notes/playwright-cache" node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list
PWTEST_CACHE_DIR="$W/notes/playwright-cache" node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts --list --grep 'M2 native None'
```

Both exit 0: **9 total tests** (the original 7 plus 2 additions); grep collects **exactly 2**, at spec lines **1382** and **1458**. Collection did not run global setup, worker fixtures, browser, Runtime or hosted build.

```sh
node node_modules/eslint/bin/eslint.js scripts/testing/current013-native-none.mjs tests/e2e/local/support/current013-native-none.test.mjs tests/e2e/local/three-products.spec.ts tests/e2e/local/support/astrid.ts tests/e2e/local/support/harness.ts --max-warnings 0
node --check scripts/testing/current013-native-none.mjs
node --check tests/e2e/local/support/current013-native-none.test.mjs
node "$W/notes/source-review.mjs"
git diff --check
git diff --check 171a259ac HEAD
```

All final commands exit 0; lint emits no warnings. The retained pure source probe verifies unchanged source scope/prefix and reproduces the binding mismatch using the real matcher against frozen JSON; its passing result means the incorrect assertion was rejected, not that either journey passed. Its first invocation failed with sandbox `spawnSync git EPERM`; using explicit ignored stdin and piped output resolved that audit-helper invocation. No product/test source was changed to resolve it.

No central request, socket/listener, browser execution, build, full suite, tsc, install, renderer or actual acceptance run was performed. Shared dependencies were used read-only; no recursive dependency metadata audit is claimed. The App worktree remains clean with no review-generated build/temp output. Review files and the private audit/cache live under this worker's shared orchestration paths only; the private Playwright transform cache was removed after collection.

## Handoff

Review complete; **HOLD source approval on the parent-binding assertion**. Manager should authorize its narrow correction, repeat discovery/pure checks, compose/freeze the exact source pair and private-cache arrangement, and only then register/run the new central browser lane. Keep D01 and writer retirement open until that actual run passes all positive assertions. No KEEP request; no review-workflow blocker requiring a BLOCKED marker.
