# App exact trim interior policy port

Status: **source port READY; frozen native comparison PASSED; activation/release qualification OPEN**. App base is `349cf9c77a04f4f4f887ef4b8f539782e1ca1609`, branch `tl/app-m2-trim-exact-interior-policy-port`. PLAN and the Agent-owned policy were read first. No settled decision changed.

The App mirror keeps the finite raw guard `0 <= in < out <= D` against unrounded authoritative registry duration. Only new trim writes round source endpoints to six decimals with exact binary64 nearest-even; when nearest out exceeds D, out uses the exact interior floor specified by Agent. Source hold is rounded from the applied endpoint difference; collapsed windows refuse before recording writes. Existing windows are never normalized on read/compile/restore. Speed and rational fps are unchanged.

The local trim helper decodes IEEE-754 bits with DataView and performs scaling, remainder comparison, ties-to-even, and floor with BigInt. Decimal parsing is used only to convert the final exact integer-times-10^-6 rational to binary64 in one rounding, avoiding `Number(integer)/1e6` double rounding. It does not infer the input fraction from decimal text. No generic numeric helper was exact for this operation: move's decimal-rate conversion has a different input contract, so it remains untouched. This is the only implementation choice beyond the settled policy.

Exact App allowlist and line counts:

| Path | Added | Deleted | Net |
| --- | ---: | ---: | ---: |
| `src/tools/video-editor/commands/clipTrimCapture.ts` | 27 | 5 | +22 |
| `src/tools/video-editor/commands/clipTrimCapture.test.ts` | 67 | 0 | +67 |
| `src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim_boundaries.json` | 107 | 0 | +107 |
| Total | 201 | 5 | +196 |

Only one product path changes, net **+22 LOC**. No UI, bulk, split, session, client, pin, upstream root merge, generic `_r`, other operation, legacy data, wire/schema, JSON/prototype handling, recording, guards or inverse implementation changes. Original tests were retained literally; no skips/expected-failures/weakening were introduced.

## Contract and source identity

Agent policy: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-trim-interior-rounding.md`.
The source contract was harness-commit pending at dispatch but became available through local hub refs during this run. Native comparison uses a private `git archive` of **`e4bec724bec39865b9b6b73b8754abd82d4f4449`**, observed at `refs/remotes/hub/timeline/agent/tl/agt-m2-trim-interior-rounding` in `/home/user/peteromallet/astrid-agent`. No moving checkout or edits to Agent were used. All three documented product blob identities were verified at that exact commit:

| Agent path | Git blob SHA |
| --- | --- |
| `astrid/sdk/timeline/units.py` | `f30260efaef8f0d9d6735d4d13a042a8eadf4bee` |
| `astrid/sdk/timeline/_trim_commands.py` | `c5dd666a676d09c2a232e3f81031b736feb50916` |
| `astrid/sdk/timeline/model.py` | `2101f1e6611518b43a1c4f5bf57060df1ac6dbc5` |

The original golden is byte-unchanged and equals the frozen native golden: SHA-256 `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`.
The new fixture is copied byte-for-byte from the shared Agent vectors, and also equals the frozen native boundary fixture: SHA-256 `5cf496137b9387ef05e8f3b9a5fc7762c529f30670db2c0114d689cba4959d97`. All **17** vectors run exactly: raw overrange refusals, below/exact source end, the multiplication-floor trap, binary/decimal tie directions, true even ties, applied-endpoint hold, inward collapse and submicrosecond windows.

Successful vectors assert exact row and both authored mirrors, speed=2 source units, rational 30000/1001 fps, unchanged registry/provenance/child pins/placements/siblings/opaque data, immutable input and replay. Additional direct tests cover omitted/null endpoint defaults and nonfinite endpoints/duration. Existing own-prototype/null/absence/read-guard controls remain passing.

## Validation

All commands below ran directly as focused tests; no full suite, build, browser, socket, tsc or install was run. Shared dependencies/venvs and their caches were not modified. Vitest used the runner loader, no cache, a worker-local cacheDir, read-only private public Composition 0.0.12 aliases from `/tmp/app-coherent-deps12/node_modules`, and max one worker. The worktree's existing shared node_modules link was unchanged. Python used `PYTHONDONTWRITEBYTECODE=1` and disabled pytest cache. Temporary source archive was removed after verification; scripts/results remain in the worker directory. The initial TSX comparison made four temporary entries in `/tmp/tsx-0`; only entries whose source maps exclusively identify this worker were removed, then comparison was rerun with `TSX_DISABLE_CACHE=1`.

Use these exact path aliases for the commands:

```bash
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-trim-exact-interior-policy-port
A=/home/user/work/wt/app-m2-trim-exact-interior-policy-port
S=e4bec724bec39865b9b6b73b8754abd82d4f4449
```

1. App focused regression run, cwd `$A`:

```bash
node --require "$W/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$W/vitest.public12.config.ts" --configLoader=runner --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/clipTrimCapture.test.ts src/tools/video-editor/commands/clipTrimGesture.test.ts src/tools/video-editor/commands/commitSession.trim.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.trimSession.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

**14 files / 643 tests passed**, exit 0, 50.55s. This is the previous **621** passing App cases plus **22** new cases. Full output: `$W/app-targeted.log`.

2. Frozen native trim controls and new vectors:

```bash
mkdir -p "$W/agent-source"
git -C /home/user/peteromallet/astrid-agent archive "$S" | tar -x -C "$W/agent-source"
cd "$W/agent-source"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py
```

**98 passed**, exit 0, 6.30s, `$W/native-targeted.log`. All original **79** controls remain; native adds 17 boundary vectors and two speed parameters, with original expectations retained. Native tests exercise model parity, actual publication mirrors, exact retry/replay, guarded inverse/redo and refusal before writes.

3. Direct frozen native/App comparison:

```bash
cd "$A"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python "$W/native-parity.py"
TSX_DISABLE_CACHE=1 node --import ./node_modules/tsx/dist/loader.mjs "$W/native-compare.mts"
```

**18 exact cases passed**, exit 0: unchanged original golden plus all 17 shared vectors. Native script changes only raw registry duration and required native digest; it separately verifies original native records and full compiled output against the unchanged golden. App comparison checks exact full commands, records, authored bundles, native command replay and parent/config mirrors, or the specified refusal, with input preservation. No tolerance comparison. Artifacts: `$W/native-parity.py`, `$W/native-compare.mts`, `$W/native-results.json`, `$W/native-parity.log`.

4. Scoped lint and diff validation, cwd `$A`:

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipTrimCapture.ts src/tools/video-editor/commands/clipTrimCapture.test.ts
git diff --check
```

Both exit **0**. Byte comparisons against both frozen native fixtures and the shared source vectors pass; exact three-path allowlist and all source identities pass, recorded in `$W/source-identity.txt`.

## Remaining release gates

No source blocker and no evidence requiring a policy deviation. This worker neither reviews/merges the Agent correction nor activates an App release. Agent review/merge of the frozen source, coordinated App integration, installed matching provider identity and actual paired qualification remain open. Required paired checks include Runtime receipt retry and persistence/reload, original guarded publication undo, browser preview and zero-legacy traffic. Browser/render/Runtime acceptance is not established by these native/App domain tests. Existing writer retirement follows qualified replacement; no Gate 5/6 or release readiness claim is made.

Handoff: worker report and conventional commit message written, `DONE` and `noKEEP` markers created. App commit is assigned by the harness after exit; no git commit/merge/rebase/checkout/push was performed.
