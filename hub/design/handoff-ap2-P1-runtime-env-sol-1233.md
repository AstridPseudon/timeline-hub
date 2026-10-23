# P1 Runtime environment repair — qualification blocked

Runtime executable/import repair: PASS. Build-free existing row guards and original selector discovery: PASS. Complete requested availability qualification: BLOCKED; **do not treat this as OPS_READY or chain credit**.

## Changes

- Retained own Runtime checkout `/home/user/work/wt/ap2-P1-runtime-env-sol-1233`, HEAD `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`. `/home/user/work/runtime` had the same HEAD/tree at start and recheck: exact integration delta is zero.
- Created ignored `.venv/` containing only symlinks `bin`, `lib`, `pyvenv.cfg` to the corresponding existing `/home/user/work/venv-app2-native` entries. No install, build, new venv creation, package modification, shared dependency write, or Git metadata write.
- A top-level `.venv` symlink proved untracked because the existing ignore is directory-only `.venv/`; replaced that newly created trial link with an ignored directory of links. No preexisting file was deleted. Existing ignore rules and tracked files are unchanged.
- Changed only the existing `app ap2-P1-chain-h6` row's `RT=` checkout path. Wrote `KEEP` retaining this exact Runtime environment. The requested persistent strict availability preflight is **not installed**, because it would fail on missing dist before the original service's normal build. No build relocation or guard exception was applied without authorization.

## Blocking evidence and decision

Read actual App `tests/e2e/local/support/harness.ts`, especially lines 71–82 and 505–595. `runtimePython()` ignores `ASTRID_RUNTIME_PYTHON`: it selects `<RUNTIME_CHECKOUT>/.venv/bin/python`. `runtimeEnv()` supplies `PYTHONPATH=<RT>:<AG>` and disables bytecode. `createRealm()` and initial `startRuntime()` use that actual interpreter; authoring later uses its explicit Python. The original service3016 failed exactly on the absent old checkout `.venv`, before either test body; its build took 64 seconds and its result remains FAIL (one failed, one did not run), with zero chain credit.

The actual exported `harnessUnavailableReason()` also requires a production `dist/index.html`. There is no retained dist in the App integration checkout or the inspected retained worktree/worker locations. `--list` does not execute App globalSetup, which is why prior discovery was insufficient. Under the exact original checkout/interpreter/private graph environment, actual availability now returns:

```
no production build at /tmp/w-14adae5506/app/dist (run npm run build, or use npm run test:e2e:direct)
```

A strict `assert.equal(reason, null)` was executed and failed (exit 1). No fake index, alternate dist override, monkeypatch, ignored reason, source modification, or guard waiver was used. The brief simultaneously requires that assertion to pass and prohibits building; no existing qualified artifact was found to satisfy it. An optional clarification was sent about permitting original globalSetup before the preflight; no answer had arrived when reporting. Preserved original build placement and reported the blocker.

## Exact checks and results

Scratch App source was extracted with read-only `git -C /home/user/work/app archive 12ef32054524a3cce449fdcb6d94788415b9571a` into `/tmp/w-14adae5506/app`; original row switched only this scratch checkout's node_modules link to the existing private graph. Source App remains exact `12ef32054524a3cce449fdcb6d94788415b9571a`, tree `4bf9a980d1d5ef38d485702006e52ee33f5dbc3d`.

1. `bash -n /tmp/w-14adae5506/row.after.sh` — PASS, exit 0.
2. `PATH="/tmp/w-14adae5506/bin:$PATH" GIT_OPTIONAL_LOCKS=0 GIT_DIR="$(git -C /home/user/work/app rev-parse --absolute-git-dir)" GIT_WORK_TREE=/tmp/w-14adae5506/app TMPDIR=/tmp/w-14adae5506 XDG_CACHE_HOME=/tmp/w-14adae5506/cache bash -c 'cd /tmp/w-14adae5506/app && timeout 25 bash -x /tmp/w-14adae5506/prelude-build-free.sh'` — PASS, exit 0 (`prelude-third.log`). Scratch Git wrapper only unsets the scratch GIT_DIR/WORK_TREE when the actual row uses `git -C` for Agent/Runtime; real Git performs every read. It does not synthesize HEAD. This runs all existing guards through original discovery, stopping before broad tsc/lint and body. All 15 original file guards, original ancestry/source-tree/clean tuple, private 819acf graph's 80 files/version/public exports, exact Agent/Runtime pins and native imports pass. This is the exact source-HEAD branch; no new synthetic snapshot or Git object was created. Existing 1216/1221 snapshot-parent qualification is preserved by identity, not independently rerun here.
3. From `/tmp/w-14adae5506/app`, with the environment below: `timeout 25 npm run test:e2e:three-products -- --list tests/e2e/local/three-products.p1-chain.spec.ts` — PASS, exit 0 (`list.log`), exactly the original accepted/merged/lost-ACK selector at line 732 and refused/rollback selector at line 859; `Total: 2 tests in 1 file`.
4. Same cwd/environment: `timeout 25 node --import tsx /tmp/w-14adae5506/availability.cjs` — runtime executable and exact imports PASS, final actual availability null assertion FAIL, exit 1 (`availability.final.log`). The probe calls the actual exported functions and actual `DirectHarness.prototype.runtimeEnv`, checks executable access, then imports using that returned Python and runtimeEnv from the scratch temp cwd.
5. In own Runtime worktree: `git check-ignore -v .venv` — PASS (`.gitignore:4:.venv/`). `git status --porcelain=v1 --untracked-files=all` — empty. `git diff --check` — PASS. No tracked Runtime changes.
6. `git -C /home/user/work/app diff ad96a4cac58771baf5fbe2b07f30cccce4340040 12ef32054524a3cce449fdcb6d94788415b9571a --name-only` — exactly the three reviewed P1/P3 test/support files. Original 1156 TypeScript/scoped lint evidence and 1221 review are reused only for the unchanged App identity; no broad repeat.

Environment for checks 3–4 (NODE_PATH unset):

```
NODE_OPTIONS=--max-old-space-size=6144
TMPDIR=/tmp/w-14adae5506
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-d1fa6c13
ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/ap2-P1-runtime-env-sol-1233
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python
TIMELINE_BUNDLE_AGENT_HEAD=d1fa6c1332011e4c6f6e075ca458c7dff6bf130c
TIMELINE_BUNDLE_RUNTIME_HEAD=3b926efab2eed122d374540baee297d4cdcec62a
PYTHONPATH=/tmp/w-14adae5506/app:/home/user/work/wt/ap2-P1-runtime-env-sol-1233:/home/user/work/wt/agt-pin-d1fa6c13
```

Actual returned Python: `/home/user/work/wt/ap2-P1-runtime-env-sol-1233/.venv/bin/python` (executable). Actual imported files:

```
runtime_protocol: /home/user/work/wt/ap2-P1-runtime-env-sol-1233/runtime_protocol/__init__.py
astrid: /home/user/work/wt/agt-pin-d1fa6c13/astrid/__init__.py
astrid.sdk: /home/user/work/wt/agt-pin-d1fa6c13/astrid/sdk/__init__.py
astrid_runtime_client: /home/user/work/wt/agt-pin-d1fa6c13/astrid_runtime_client/__init__.py
```

Agent HEAD/tree guards pass `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c` / `ff6c46d0b5ba420e3fb9e912e5a30c7a9a41e27b`. Frozen producer `runtime.lock.json.source_commit` remains `34eac0041b0891e9011966b39bcbd26053fde5bc`; lock SHA-256 `eb52cbbb3a1f40caca965eb0cb2c87142100adabb4c876a8582b6894c4281c8e`. No new producer adoption.

## Scope integrity

- P1 row SHA-256 before: `469421c806bd502228d058d827d1f9b03abdc5dbc7c1e72123b5eb3bdf0e64b1`.
- P1 row SHA-256 after: `3b27d04fcb9fb3d5a02e28dc0aea68f94da965ca39635c5f96413d92b04411ac`.
- Outside-row SHA-256 before/after: `80009eca65cb605e9a97fa83b6a810de2180a4aef19cbdf7a9983f5286a73e5f` (byte-identical).
- P3 row SHA-256: `48499e7d96c570ce32065d5e4981002d416a471c955ad83a17bda65c451668d1` (byte-identical).
- Mechanically asserted new row equals old row with only the single RT path substitution. Source/snapshot fix, all guards, original commands/selectors/env/timeouts and final body are byte-preserved otherwise. Old results 15187/28486/3016 untouched.

No product/test/schema/client/pin/host-script change, browser, HTTP, body, service, request-test, full/broad suite, build, native 14/58, daemon/hub/dispatcher operation, or package/shared-cache write. C0 §§1–5,7 and PLAN §3 P1 were read; no contract semantics changed.

## Next step

Manager must resolve access to an existing qualified production dist or authorize normal App globalSetup at the appropriate qualification stage. Then install/qualify the bounded actual availability preflight with a true null assertion, exercise the faithful service snapshot prelude through the final body boundary, obtain independent Luna review, and only then queue one changed original service. This report does not authorize or claim that run. KEEP must remain while the shared row points at this worktree. Wrote BLOCKED, not DONE.
