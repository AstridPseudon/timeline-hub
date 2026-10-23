# A2 explicit Source In on numeric hold — ready for independent review

The source loss is fixed within the authorized A2 boundary. The retained mounted regression went **old FAIL (expected two intents, got one) → new PASS** with its original assertions unchanged. It now additionally proves canonical split adoption, a second real outbox transport invocation against the accepted pair, the original new ID, exact `from: 0 → 3` guard/read, and final saved state. **174 focused tests pass. H3/P1 remains NO-GO; the original live chain is unqualified.**

## Source and scope

- Worktree: `/home/user/work/wt/ap2-A2-explicit-source-in-sol-0913`.
- Base HEAD: `a196fff2ebb334801a0a33b9c9a3323b1a1469f3`; tree `e2397abb4ef0771593fa9e0a66674ffd302a7975`. This is the exact resumed 0905 branch, retaining prior WIP `679efb0b0fdb3b542edb210d15991784a51cf3f4` and the original mounted test.
- Candidate tree: `c3752a0ff4978f400feb22e45f65b976188c7807` (computed from HEAD entries plus the four changed blobs using Git object serialization, without writing the index/object store; harness has not committed yet).
- Diff SHA-256: `073d1a9656fc39ed2421d87e289defaa5cfa1dd32fe00ce01735278c6c7447f7`; complete diff: `record/source.diff`.
- Four changed files only; no stale branch import, spec/support/fixture file/schema/pin/generated/package/lock/ops/dependency edits. No commits, merges, checkouts, pushes, service requests, build, full suite, HTTP, browser, or socket run.

| File | Base Git blob | Candidate Git blob | Candidate SHA-256 |
|---|---|---|---|
| `src/tools/video-editor/hooks/useTimelineCommit.ts` | `19b0b236a7f40d613d5a08fad4d23136e35d8880` | `ef2569f1ba9a9e609880f69fa91dd4351488962d` | `edee1fad387e3952736cf0bb99c2dd7a9b92133290b1dbdfea40db8a14d7cbfe` |
| `src/tools/video-editor/hooks/useTimelineSave.test.tsx` | `a002b6cad6b7881e8a83dfb000ef823dcc81263e` | `30051661574addf864b5338cc489410bec77bc47` | `a997e3cecff13dd9e827b9ff03c656e29251f098477d5eb814ef7ec757177d55` |
| `src/tools/video-editor/lib/serialize.test.ts` | `30ca4c0d9344ad8e893c93c1434a40d44bac0f48` | `53d92701271deb8cc439d9287b88f0ea6e012c65` | `d206079fd18c2e6a02dc0634e5891b5f02fa934e6fcb9291f79467f4c3f68e76` |
| `src/tools/video-editor/lib/serialize.ts` | `aab660cd3f27925194f23e52f8227458fdc3f22f` | `01776e71915a08015888430aa214df18c28ffd7f` | `a4c4c01fbfd21ab080876d6daf3ae6eee83dd60717568917cea89509b51de309` |

## Causal boundary and correction

Read PLAN §3 A2/P1, C0 §§1–5/7, prior 0858/0905 logs/report, the retained regression, and actual original service2754 log/summary. The production path is `ClipPanelBody` Source In → `useClipEditing.handleSelectedClipChange({from: 3})` with the existing trim gesture basis → `useTimelineCommit.materializeData` → `rowsToConfig` → local handoff → durable session/outbox.

`lib/timeline-data.ts:367` selects the hold-duration branch solely from numeric `hold`, computes hold from row length, then deletes `from`, `to`, and `speed`. The mixed media/hold seed exposes a legitimate Source In inspector; its split leaves right ID at 2 with hold 6 and authored from 0/to 8/speed 1. The edit to from 3 previously vanished in row serialization. The handoff correctly interpreted omissions as a partial view, kept the raw fields, and found no delta; `appendDocument` consequently appended no second intent. This precedes canonical acceptance and is not evidence of a consumed-read refusal or wrong inspector targeting.

The authorized serializer now exports `withHeldClipSourceFields`; authorized `useTimelineCommit.materializeData` applies it immediately after `rowsToConfig`. It restores only supplied from/to/speed metadata for numeric holds, without adding defaults or changing row duration. `getDefaultClipMeta` copies those fields without source defaults. Absent fields remain absent; null stays null; non-hold media continues its existing source-window duration calculation. The existing handoff remains responsible for verified raw binding and raw opaque provenance. No reads, guards, IDs, outbox transitions, provider execution, or reply policy were changed.

Decision: `lib/timeline-data.ts` was not explicitly added to the product allowlist. The correction therefore sits in the explicitly allowed `serialize.ts` and original allowed `useTimelineCommit.ts`, at the actual A2 caller boundary. Direct callers of bare `rowsToConfig` still have its original field-dropping behavior; this change qualifies the authorized A2 materialization path. No control-flow replacement, capture port, TS executor, normalization rule, output default, or label write was introduced.

The existing mounted test's original two-intent/basis/patch/read assertions were retained. Added observations verify the canonical r1/p1 split is displayed before sending B, B uses r1/p1 and its original new ID, declared reads survive, step patch equals submitted command changes, no legacy save runs, and the r2 canonical trimmed clip keeps hold 6/to 8/speed 1 plus its raw app data. Serializer negatives cover held media, true hold, absent source fields, null source fields, unchanged app.for/app.until/opaque null and labels/output, input immutability, and non-hold speed/source duration.

## Original service2754: exact evaluation boundaries and separate counterexample

Original run: `orch/tests/ap2-P1-provenance-original-spec-port-0820-ap2-P1-chain-h6-1023085133-2754/`, App tree `7821bc8430c85190f00e52c2a8d6db91ecca8c7d`. Actual first failure is original spec line 423: expected two POSTs, got one after 90 seconds. Thus preceding accepted-split/new-ID/raw closure assertions (including lines 410–412) completed. The second case fails at line 509 in the separately owned Python helper: literal backslash-newline SyntaxError. No helper changes here.

The original spec SHA-256 is still **`d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`**. Seed line 98 authors from 0. Lines 410–412 require each split clip to equal that original except ID/at/hold, so the right clip retains from 0. Later line 431 requires trim.before.value to equal SPLIT_AT (2). Line 431 was **not evaluated** in service2754 because line 423 failed first. It is a distinct source-versus-oracle counterexample: a truthful guarded trim after the specified split has previous value 0, not 2. Manufacturing previous 2 would violate the accepted raw document and guard semantics. This patch preserves from 0 and does not alter the original spec, waive it, or claim its future pass. Owner judgment on the incompatible oracle remains required under the settled-plan process.

The original service snapshot path is no longer present according to the prior handoff; trace ZIP/error-context names are referenced in the retained log. I inspected the log, not a browser trace; no trace-level gesture or live-request repair claim is made.

## Commands and results

All commands below ran in this worktree. Harness `tmpdir` is a file pointing to `/tmp/w-23874c3518`; scratch files were written there. Copies of logs/private configs and source diff are retained under this worker's `record/` directory. Vitest uses the durable exact Composition graph and a private cacheDir, `--configLoader runner`, and `--no-cache`; `node_modules` still resolves to read-only `/home/user/work/app/node_modules`.

Causal command, before the product fix (`record/causal-old.log`, exit 1: expected length 2, got 1 at the unchanged mounted assertion), immediately after the fix (`causal-new.log`, exit 0: 1 passed, 20 deselected), and after canonical-adoption assertions (`causal-adoption-wire.log`, exit 0: 1 passed, 20 deselected):

```bash
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-23874c3518/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx -t 'persists an inspector trim'
```

Final targeted run (`focused-final.log`): **exit 0, 9 files / 174 tests passed**, 7.82 seconds:

```bash
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-23874c3518/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-data.test.ts
```

Initial serializer/neighbour run used the same prefix/options with only `src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-data.test.ts`: **exit 0, 49 tests passed** (`serializer.log`). Existing full-v2 local session, accepted/merged/conflict/invalid/restart/dependent/late-reply/strict mounted cases, raw provenance, and undo/dependency negatives remain passing in the final targeted run. These are source/unit transport tests, not live Runtime authentication/compiler qualification.

Checks, all **exit 0**, with no diagnostics:

```bash
timeout 180s node --max-old-space-size=6144 node_modules/typescript/bin/tsc -p /tmp/w-23874c3518/tsconfig.app.json
timeout 45s node node_modules/typescript/bin/tsc -p /tmp/w-23874c3518/tsconfig.node.json
timeout 45s node node_modules/eslint/bin/eslint.js src/tools/video-editor/lib/serialize.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0
git diff --check
git diff --exit-code HEAD -- src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts src/tools/video-editor/hooks/useClipEditing.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/commands/localSaveSession.ts
```

App completed within the practical 180-second ceiling, without repeated 45-second churn. Private App/Node configs use explicit typeRoots and exact graph declaration paths. Subsequent edits were confined to tests, which these configs exclude.

Development extension attempts used the same causal command: `causal-adoption.log` and `causal-adoption-timer.log` exited 124 at 45 seconds; `causal-adoption-observe.log` exited 1 with retry versus saved. The inline response was using structuredClone on an editor config containing undefined values, unlike finite JSON from the wire. Matching existing tests' `JSON.parse(JSON.stringify(config))` response serialization corrected that test setup; the final run passes without product policy changes or weakened expectations.

## Exact graph and Python origins

Read-only archive comparison (`record/graph.log`) passed: normal worktree `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` is 73,451 bytes, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`. All 80 tar file bodies equal the durable `orch/workers/ap2-P3-env-final-0407/record/private/node_modules/@banodoco/timeline-composition` tree; no synthetic generated root entries. Comparison used Python tarfile reads only, with no extraction or install writes.

Exact source refs checked with `git -C <path> rev-parse HEAD HEAD^{tree}`:

- Agent b8: `b8e5076250cc37cadf88c1ce699f2a05511fb909`, tree `eee66dc206817b16f0621087a12505389ec41630`.
- Runtime a5d: `a5d4258312c979024865ee704da2d632ca5b2730`, tree `f74b016ea837f8148db4a602c972073a226ed177`.
- Normal Runtime 34e: `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.

Both origin checks **exit 0**; commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004:/home/user/work/wt/agt-pin-f894c3c9" timeout 45s /home/user/work/venv-app2-native/bin/python -P - <<'PYORIGINS'
import astrid, astrid.sdk, astrid_runtime_client, runtime_protocol
for mod in [astrid, astrid.sdk, astrid_runtime_client, runtime_protocol]:
    print(mod.__name__, mod.__file__)
PYORIGINS
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-a5d42583:/home/user/work/wt/agt-pin-b8e50762" timeout 45s /home/user/work/venv-app2-native/bin/python -P - <<'PYORIGINS'
import astrid, astrid.sdk, astrid_runtime_client, runtime_protocol
for mod in [astrid, astrid.sdk, astrid_runtime_client, runtime_protocol]:
    print(mod.__name__, mod.__file__)
PYORIGINS
```

Normal imports resolve astrid, astrid.sdk, and astrid_runtime_client beneath `agt-pin-f894c3c9`, runtime_protocol beneath `rt-pin-34eac004`. Exact imports resolve those three Agent modules beneath `agt-pin-b8e50762`, runtime_protocol beneath `rt-pin-a5d42583`. This verifies origins only; no service/provider call was made.

## Limits and next owners

This bounded source task is complete; no source blocker remains. No original P1 body, live lost-ACK/restart, real intervening Agent merge/refusal, or latest App owner integration is claimed. No request/reply/schema validation was removed: existing ABI 1 scope/base/commands/label/steps/merge/reads/dry_run/key, accepted/merged canonical and evidence fields, and conflict/invalid code/path/hint logic remain unchanged.

Next: independent Luna review of this four-file delta and the separate oracle contradiction; then current App owner port/merge preserving later move/Undo/shared work, separately reviewed helper fix and OPS ownership. Only after that should Proof run ONE original chain under its assigned service policy. Preserve the original line-431 failure unless its owner explicitly resolves the counterexample; do not silently rewrite it. H3 stays NO-GO until the original integrated behavior is proven.
