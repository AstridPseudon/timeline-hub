# App native frame fixture current-root port

## Result

Ported the reviewed five-file native frame fixture/harness unit from Viewing
`e4c7a3792` onto actual App root `b1ef4b9b9`. The working-tree file
contents match the frozen Viewing tree byte-for-byte. No product writer, Runtime
API, root/pin/download/render/admission path, or old ancestry was changed.

The owner commit `dba11c8432` is the direct child of the root, and the reviewed
final-gate commit `e4c7a3792` is its direct child:

- root: `b1ef4b9b910ba72375c34cf319692f90d22edc25`
- owner tree: `79fca36dcc07d83d457bc2db5f822cad28054d71`
- reviewed final tree: `e43c4c34107bb474beb5e86e669cb4d75d961e7a`

## Exact five-file scope

- `tests/e2e/local/support/harness.ts`
- `tests/e2e/timeline/viewing-parity/fixture.ts`
- `tests/e2e/timeline/viewing-parity/harness.ts`
- `tests/e2e/timeline/viewing-parity/native-fixture-helper.py`
- `tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts`

The final integration test retains the frozen Runtime/Agent archive checks,
module-origin checks, ordered explicit Runtime-then-Agent `PYTHONPATH` proof,
and before/after source-manifest guards. The original three-media fixture and
ordinary authenticated `timeline.restore` closure remain intact.

## Compatibility with the root primary setup

- `DirectHarness.start()` keeps the existing default M1 seed behavior; the
  optional `seed: false` and `beforeRuntimeStart` controls are additive.
- The existing non-native `prepareFrameParityFixture` path and its M1
  seed/opaque/transition behavior are unchanged; the native branch is opt-in.
- Native setup uses the existing Runtime closure validation/persistence seam,
  then the existing authenticated `/v1` restore API. It does not create a
  head/history entry or use SQL, a private provider, or a fake provider.
- No App source outside the five requested files changed.

Frozen source attribution checked read-only:

- Runtime commit/tree:
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- Agent commit/tree:
  `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` /
  `75354d38c898729bac09619679f5421faba319ed`
- Runtime archive SHA-256:
  `eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669`
- Agent archive SHA-256:
  `91d4d82f4ee2a251ba6c3706d47efa80411d05e683c64c78a05414d4229b3add`

## Targeted evidence

All commands used the shared App dependencies read-only, with a private worker
temp/cache root and no install.

- Exact source/scope comparison against `e4c7a3792`, root ancestry checks, and
  `git diff --check` — PASS.
- `TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-native-fixture-current-root-port/private12/tmp XDG_CACHE_HOME=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-native-fixture-current-root-port/private12/cache ./node_modules/.bin/eslint --no-cache tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -c 'import ast, pathlib; ast.parse(pathlib.Path("tests/e2e/timeline/viewing-parity/native-fixture-helper.py").read_text())'` — PASS.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts` — 5 PASS.

## Prior central evidence

I did not duplicate the unchanged remote HTTP run. The exact prior successful
tuple remains:

- named suite: `integration-viewing-native-retained-fixture`
- prior App tree: `e43c4c34107bb474beb5e86e669cb4d75d961e7a`
- result: 1 pass, 0 fail
- record:
  `vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141813-18235`

That prior record proved the normal HTTP restore, zero legacy composition
revision POSTs, forged-task refusal with zero object-list writes, frozen
Runtime/Agent module origins, ordered explicit paths, and unchanged extracted
source manifests. The earlier failed guard attempt remains failed and is not
relabeled.

## Owner scheduling command

Run once on the composed owner tree if scheduling a fresh central HTTP check:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-native-fixture-current-root-port integration-viewing-native-retained-fixture) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

No browser, render, frame parity, full suite, project typecheck, build, install,
or local-socket claim is made here.

