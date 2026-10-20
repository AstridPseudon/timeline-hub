# Exact current013 paired editing gate executor

**BLOCKED / NOT QUALIFIED.** Prepared one exact named central suite and the snapshot-only public12 dependency helper. No central request was submitted, so there are **no Test IDs** and no actual browser, Runtime/Agent acceptance, or restore result. The independent exact-root review returned **HOLD**; composed source typecheck is **PASS**. Required cold-label test files and the documented Chrome155 executable are absent from the supplied inputs. No pins, product code, test bodies, assertions, helpers, or settled decisions were changed.

## Exact sources: start and end

| Source | Retained path | HEAD | TREE |
| --- | --- | --- | --- |
| App | `/home/user/work/wt/app-m3-current013-paired-gate-executor` | `927545cf52fdfbb273afbe7f190e00e11e5e2d70` | `96605f2a46c49fcf96cd12ca3679014f00ae28de` |
| Agent | `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime and producer | `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

All three checkouts are clean and unchanged at both boundaries. `notes/git-start.txt` and `git-end.txt` compare equal. Existing wrapper source/lock/metadata/archive/manifest fingerprints in `notes/source-start.json` and `source-end.json` compare byte-equal (these files include the successful vendor-check output before the JSON). No moving integration or retired source lease is consumed.

Both normal consumer locks pass the existing producer-backed vendor checks against the exact retained Runtime keeper. Tuple: contract/client `0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, producer artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`, 75 Runtime manifest artifacts. Public12 archive `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 files, is identical in both consumers.

Relevant App SHA-256 fingerprints, identical at start/end:

```text
82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901  scripts/testing/current013-integration.mjs
d0196c5ae92f8164996229d0b17c21ad2b199eaef222b7b148e2549461fd93e8  scripts/testing/current013-integration.test.mjs
2e66a73e190dca42fd41bd41c826076ccfbc7a3ff251a3dc12717108b7c7e330  tests/e2e/local/three-products.spec.ts
5e21bb734436b03fee239ac5f280a78c34e276c8d79aba530a29636a51105a9e  playwright.three-products.config.ts
336feba076afddc4ca90cf4aaeafe81bfe6848ac498721dbe40561d29db14114  config/testing/vitest.runtime-restore.integration.config.ts
4aa91d88f580651c38d341707553a3295777998fc6464d0c642edb886636179f  tests/integration/runtimeRestore.test.ts
0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3  vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
```

Read PLAN.md, wrapper final review/fix/preparation reports, MAIN17 Root013 source report, Agent keeper and Runtime keeper reports, and existing central/vendor/build/config support. The final repaired wrapper approval applies to wrapper source only. The separate exact-root review is the mandatory execution gate and has not approved this source.

## Prepared central command

App source and original worktree `node_modules` are unchanged. Changes are only this worker's ORCH notes/report plus **one appended, new** `tests/suites.conf` line; no pre-existing registration or central bin was changed.

```text
app e2e-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-t96605f2a46c49fcf96cd12ca3679014f00ae28de flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_TREE=96605f2a46c49fcf96cd12ca3679014f00ae28de TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/google/chrome/chrome PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TIMELINE_CURRENT013_CACHE_ID=app927545cf52fdfbb273afbe7f190e00e11e5e2d70-tree96605f2a46c49fcf96cd12ca3679014f00ae28de-agent75354d38c898729bac09619679f5421faba319ed-runtime7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runner85e1c54065367bddeb9b70a6b094de778ff9d6db8cc45b098248bfda9776650b-helperddffbeca3b69e0f21fa239e29f4e3e47129e6cac06d542e61e1cf0097829d25c bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-paired-gate-executor/notes/run-lane.sh
```

The complete command contains literal final SHAs, retained checkout/producer/venv paths, full App TREE and explicit cache identity including both helper hashes. The `e2e` name activates the existing external-ref cache-key handling. Lane arguments supplied with the service's existing `--files` option separate M1, cold-label and restore cache keys while preserving the same immutable App TREE. Requester exports are not used as bindings.

- `notes/central-private12-snapshot.py` is adapted from the existing standard8 snapshot helper. Before mutation it requires this worker's own `.test-*` cwd, exact source tree and cleanliness, root public12 dependency, immutable archive hash, exactly 77 unique safe regular archive members, byte-identical installed 77-file package, and React/ReactDOM `18.3.1`, Remotion/Player `4.0.509`. It verifies `node_modules` is an ignored symlink and changes only that snapshot's link to read-only `/tmp/app-coherent-deps12/node_modules`. `--verify-only` performs the checks without relinking; mutation mode refuses this original worktree.
- `notes/run-lane.sh` uses the existing current013 wrapper for all **seven** unchanged three-products cases. The cold-label lane selects the existing `playwright.track-label.config.ts` with `--grep 'M2 cold-open'`; it intentionally refuses missing files. Restore uses the unchanged runtime-restore integration config, an external snapshot-bound config setting a private Vite cacheDir, and the existing config-runner shim with `--configLoader=runner --no-cache --maxWorkers=1`.
- Lane execution runs through the normal service and existing browser flock. npm, Playwright transformation/output, TMPDIR, and restore Vite caches are private under this worker's `notes/runs/<snapshot>/`. No stale dist or `ASTRID_APP_DIRECT_DIST` is supplied: the original default hosted-build helper remains authoritative. Vite5's normal build config temporary module is adjacent to the snapshot config; no shared dependency config/cache write is introduced. No local socket/browser/build was launched to validate the prepared browser command.
- Existing venv executable paths remain `/home/user/work/venv-agent/bin/python` and `/home/user/work/venv-runtime/bin/python`, without realpath dereferencing.
- Each central lane records the existing full source fingerprints before and after, even on failure, and preserves failure status. The wrapper itself repeats its own checks around the seven-case child.

The helper and runner SHA-256 values bound into the command are:

```text
ddffbeca3b69e0f21fa239e29f4e3e47129e6cac06d542e61e1cf0097829d25c  central-private12-snapshot.py
85e1c54065367bddeb9b70a6b094de778ff9d6db8cc45b098248bfda9776650b  run-lane.sh
```

The helper's actual snapshot relink, browser/build operation, cache isolation during a central run, and restore external-config loading are **UNRUN**. Prepared code is not a qualification result.

## Commands actually run

From the exact assigned App worktree; `O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`, `W=$O/workers/app-m3-current013-paired-gate-executor`.

```sh
env TIMELINE_CURRENT013_APP_TREE=96605f2a46c49fcf96cd12ca3679014f00ae28de \
 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
 TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
 ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
 ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
 PYTHONDONTWRITEBYTECODE=1 node --input-type=module -e \
 'import {checkCurrent013Sources,readCurrent013Inputs} from "./scripts/testing/current013-integration.mjs"; console.log(JSON.stringify(checkCurrent013Sources(readCurrent013Inputs()),null,2));'
node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs
python3 -B "$W/notes/central-private12-snapshot.py" --verify-only
python3 -B "$W/notes/central-private12-snapshot.py"
bash -n "$W/notes/run-lane.sh"
```

Results: source preflight ran at start and end, exit 0 with both producer-backed lock checks passing; fingerprints compare equal. Wrapper control tests exit 0: **15 passed / 0 failed / 0 skipped** (`notes/wrapper-tests.log`). These mock child execution and do not prove any journey. Dependency verification exits 0: all 77 files and four peers match. Deliberate mutation-mode control exits 1 at the own-central-snapshot path assertion, before any write, proving the original link is protected. Shell syntax exits 0.

Other read-only checks: `git rev-parse HEAD HEAD^{tree}`, `git status --porcelain=v1`, `git ls-tree -r HEAD tests/e2e/local playwright.track-label.config.ts`, and SHA-256 checks above. Shared `.vite`/`.vite-temp` state was read at both boundaries for `/tmp/app-coherent-deps12/node_modules` and `/home/user/work/app/node_modules`; all file hashes/metadata compare equal in `notes/shared-cache-{start,end}.json`. This checks those cache subtrees, not a full dependency-tree census. No install/shared write was performed.

## Blocking evidence and unrun work

1. **Independent root review is HOLD.** `design/app-main17-root013-final-review.md` reports a P1: a dirty focused track row unmounts, its finish is synchronously refused, and remount loses the typed name and original capture. The independent reviewer reproduced this on desktop, phone and tablet (3 private diagnostic assertions fail; its existing targeted main suites passed 156 and package checks passed 9). This worker did not rerun or weaken those tests and did not make a source fix. The explicit required APPROVE is absent, so **no central lane may be launched**. **Composed typecheck PASS is confirmed** by `design/app-main17-root013-composed-typecheck.md`: exact App commit/tree, one actual `npm exec tsc -- --noEmit -p tsconfig.app.json`, exit 0, zero diagnostics. This worker did not rerun tsc.
2. **Cold-label source is absent on exact tree 96605f2.** Both `playwright.track-label.config.ts` and `tests/e2e/local/track-label-command.spec.ts` are absent from disk and `git ls-tree`. They exist on retained older source `080a5743a4e38847e0cc84dd07ccada67adb27f1` / tree `e23943807f9bf5c30a568dc7441357130747f68c`, inspected read-only. That tree was not substituted. An external overlay would change the asserted test-source inputs and needs an explicit orchestrator decision; no overlay was applied. The prepared cold-label lane cannot run successfully on the specified source as supplied.
3. **Documented Chrome155 is unavailable.** The retained Chrome155 environment report names `/opt/google/chrome/chrome`, version `155.0.8059.84`, hash `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`. `ls -l` and `sha256sum` on that exact path fail because it does not exist. A read-only search under `/home/user/work`, `/tmp`, `/usr/bin`, `/opt` found only `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (the old documented141 executable). No browser was launched, no download/install attempted, and no browser fallback chosen. The prepared browser lane requires the prescribed155 executable/hash before launch.

**Test IDs: NONE.** M1 seven-case suite/new Gate5, pinned cold-label, and restore integration are all UNRUN; no central request or retry. No full suite was requested. Renderer-independent actual acceptance, restart/exact retry/reload/undo, frame/render/audio parity, owner-film and macOS behavior remain unverified. Frame/render/audio lanes were never authorized by this task and were not invoked.

## Recommended next steps

Resolve the exact-root HOLD in a bounded follow-up source worker and obtain fresh independent approval; do not weaken the failed assertions. Have the orchestrator resolve the missing cold-label source and existing Chrome155 path before requesting a browser lane. If source changes, rebind the newly reviewed App TREE and command/cache identity rather than claiming this tree was qualified.

Only after the review is APPROVE, typecheck is PASS, all inputs exist and the exact pins still match, the intended sequential service commands are the following (prepared, **not executed**):

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
S=e2e-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-t96605f2a46c49fcf96cd12ca3679014f00ae28de
R=$("$O/bin/request-test" app-m3-current013-paired-gate-executor "$S" --files m1) && "$O/bin/wait-test" "$R"
R=$("$O/bin/request-test" app-m3-current013-paired-gate-executor "$S" --files cold-label) && "$O/bin/wait-test" "$R"
R=$("$O/bin/request-test" app-m3-current013-paired-gate-executor "$S" --files restore) && "$O/bin/wait-test" "$R"
```

Run each only after assessing the preceding result; wait again on the same result if exit124, never resubmit. Actual failures require concrete triage/report and a follow-up worker, with no broad automatic retry. The manager retains its one post-merge full suite; none belongs to this worker. No running gate needs this worker's worktree kept.

Final status recorded 2026-10-20T12:41Z: BLOCKED marker written, no DONE or KEEP because the requested actual qualification has not completed and no gate is running. Commit message supplied. The one added suite remains prepared but unrequested.
