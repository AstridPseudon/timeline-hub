# Independent App trim exact-policy review

Verdict: **APPROVE the App source port for the settled binary64 numeric contract.** No new App source blocker. This is not approval of Agent integration or a paired release. The frozen Agent correction is still unmerged into the observed Agent integration head, and its independently reproduced exact-Python-integer bound defect remains a separate upstream review blocker. Actual Runtime pairing and browser qualification are **OPEN**.

Product was read-only. PLAN and `design/agent-trim-interior-rounding.md` governed the review; the earlier refusal proposal was not substituted. No implementation, test expectation, fixture, schema, dependency, pin or branch was modified. No applicable AGENTS.md/CLAUDE.md/CONTRIBUTING file was found in the App tree or searched ancestor locations. No delegation.

## Frozen identities and size

- App reviewed branch: `tl/app-m2-trim-exact-interior-policy-port`.
- Final source commit: **`aa0531ec704d3f14500c7f0d54c02e424acd0b67`**; tree **`54055916d6c38fed482b377111d1b68eac4014c2`**. Branch still resolved to that SHA after tests.
- Comparison base: `349cf9c77a04f4f4f887ef4b8f539782e1ca1609`.
- Reviewer worktree HEAD: `7bb885b638838588a0dff81b64b7c34960ac07f3`. Tests used a private archive of the exact reviewed SHA, not this unrelated HEAD or a moving worker checkout.
- Agent comparison source: **`e4bec724bec39865b9b6b73b8754abd82d4f4449`**, privately archived from `/home/user/peteromallet/astrid-agent`.

Exactly three App paths differ:

| Path under `src/tools/video-editor/commands/` | Added | Deleted | Net |
| --- | ---: | ---: | ---: |
| `clipTrimCapture.ts` | 27 | 5 | +22 product |
| `clipTrimCapture.test.ts` | 67 | 0 | +67 tests |
| `fixtures/recipe_m2_clip_trim_boundaries.json` | 107 | 0 | +107 fixture |
| Total | 201 | 5 | +196 |

All three frozen Agent product blobs match the handoff exactly:

| Path | Git blob SHA |
| --- | --- |
| `astrid/sdk/timeline/units.py` | `f30260efaef8f0d9d6735d4d13a042a8eadf4bee` |
| `astrid/sdk/timeline/_trim_commands.py` | `c5dd666a676d09c2a232e3f81031b736feb50916` |
| `astrid/sdk/timeline/model.py` | `2101f1e6611518b43a1c4f5bf57060df1ac6dbc5` |

Original App golden equals both base and frozen native bytes: SHA-256 **`4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`**. New App boundary fixture equals both frozen native fixture and shared `design/agent-trim-interior-rounding-vectors.json` bytes: SHA-256 **`5cf496137b9387ef05e8f3b9a5fc7762c529f30670db2c0114d689cba4959d97`**. There are 17 boundary cases.

## Numeric and contract findings

1. `clipTrimCapture.ts:53–70` correctly decodes the binary64 significand/exponent, including subnormals, scales the exact rational with BigInt, and chooses nearest integer with ties to even. `Number(integer + "e-6")` converts the final exact decimal rational to binary64 once. It does not infer the input from decimal spelling, use `Math.round`, or introduce double rounding through `Number(units)/1e6`. Huge finite inputs do not overflow the scaling operation. An independent Fraction oracle matched 24,020 nearest/floor numeric comparisons over 12,010 deterministic values, including maximum finite, minimum normal, subnormals, decimal-tie neighbours and true binary ties.
2. `clipTrimCapture.ts:183–212` retains authoritative, unrounded `registry.assets[asset].duration`. Missing/null endpoints resolve from the existing source window, then zero/raw D defaults. Finite checks and `0 <= in < out <= D` run before rounding/writes. A raw one-step overrange request is refused even when rounding could fit; a smallest-negative-subnormal in point is also refused before mutation.
3. The inward floor uses the exact input fraction. `D=1.0485929999999999` becomes `1.048592`, never the erroneous `Math.floor(D*1e6)/1e6` result. The 9.9999999 below/exact-end requests become 9.999999. Collapse and submicrosecond files refuse; no minimum window is manufactured.
4. Hold is rounded from the binary64 subtraction of the applied endpoints. The supplied counterexample yields `{from:1.000001,to:3,hold:1.999999}`. Hold remains source seconds; speed is retained and playback applies it once. Rational 30000/1001 fps and half-open boundaries are unchanged. No generic `_r`, fps, source duration, stored hold/window, read, compile, restore or inverse normalization was added. No epsilon, new argument/unsupported alias, source map support, frame quantization or unrelated helper changes.
5. Recording remains ordered `from`, `to`, `hold`, then original intent cleanup. Source identity/read dependencies, parent-only target shape, raw source pin, authored guards, original capture comparison, replay and inverse paths are unchanged. Exact command/record/bundle comparisons and native tests cover opaque own fields, null/absence, sibling order, child pins, publication mirrors, unchanged writes, guarded ABA undo and redo. All old App tests remain literally present; additions only, with no skip/xfail/expectation weakening.

### Signed zero: inherited representation caveat

A supplemental full capture/execute with `{in_s:-0.0,out_s:1}` confirms Python writes `from=-0.0`; App writes `from=+0`. The old App `Number((-0).toFixed(6))` also produced +0, so this is not introduced by the patch. Whole records/bundles agree after ordinary JavaScript JSON serialization, and the numeric/range contract treats the zeros equally. Do not claim bit/sign identity for negative zero: it is absent from the 18 shared exact comparisons. This review treats it as a disclosed inherited representation difference, not grounds to change the settled numeric policy. No product change was made.

### Separate upstream Agent blocker, independently reproduced

Frozen Agent accepts the exact Python integer `D=9007199254740995`. Native capture/execute at exact `out_s=D` writes `to=hold=9007199254740996.0 > D`; native correctly refuses `out_s=D+1`. The real model registry lookup converts D to float and accepts both requests, also writing the out-of-bound value. Reproduced with actual capture/execute and real `Clip._source_duration`, without monkeypatching its lookup. This agrees with `design/agent-review-trim-interior.md`.

That accepted Python integer is not representable as an App Number. The App binary64 port matches the explicitly handed-off formula; the upstream defect must not be silently described as fixed, nor used to substitute a new App refusal policy. Supplemental tests did not rewrite semantics or expand the shared fixtures. Agent integration at observed `e2ad59584addc892f1a6dd9fd644c75f80a2e28f` does not contain e4bec724 (read-only ancestry command exits 1); its review report remains blocking. Resolve through the Agent owner/orchestrator before paired qualification.

## Independently rerun commands and results

Aliases used below:

```bash
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-trim-exact-policy-independent-review
A=$W/app-source
S=e4bec724bec39865b9b6b73b8754abd82d4f4449
T=aa0531ec704d3f14500c7f0d54c02e424acd0b67
```

Private archives were created with `git archive` at those explicit SHAs; `$A/node_modules` was a worker-owned link to the existing read-only `/home/user/work/app/node_modules`. No install occurred. The review-local Vitest config imports `$A/config/testing/vitest.config.ts`, uses `$W/vite-cache`, and aliases the existing read-only `/tmp/app-coherent-deps12/node_modules/@banodoco/timeline-composition` 0.0.12 exports. `vitest-runner.cjs` supplies the existing config's `__dirname` under the runner loader. Supporting scripts/config/logs are in `$W`; parity scripts were inspected and relocated from the implementation worker, then rerun against these fresh pinned archives. Numeric oracle and supplemental probes were written independently.

Archive preparation (exit 0):

```bash
mkdir -p "$A" "$W/agent-source"
git archive "$T" | tar -x -C "$A"
git -C /home/user/peteromallet/astrid-agent archive "$S" | tar -x -C "$W/agent-source"
ln -s /home/user/work/app/node_modules "$A/node_modules"
```

App targeted regression, cwd `$A`:

```bash
node --require "$W/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "$W/vitest.public12.config.ts" --configLoader=runner --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/clipTrimCapture.test.ts src/tools/video-editor/commands/clipTrimGesture.test.ts src/tools/video-editor/commands/commitSession.trim.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.trimSession.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
```

**14 files / 643 passed, exit 0, 60.80s.** Log: `$W/app-targeted.log`. Cache-free, one worker; no socket/browser test.

Native targeted regression, cwd `$W/agent-source`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py
```

**98 passed, exit 0, 7.18s.** Log: `$W/native-targeted.log`. Includes all 17 portable vectors with model parity, native publications, retry/replay and guarded undo/redo.

Native/App exact comparison, cwd `$A`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python "$W/native-parity.py"
TSX_DISABLE_CACHE=1 node --import ./node_modules/tsx/dist/loader.mjs "$W/native-compare.mts"
```

**18 exact cases passed, both exit 0**: unchanged original golden plus every shared vector. Full command, record, authored bundle, native-command replay and publication mirrors agree, or both refuse the specified invalid request; original inputs preserved. Native separately verifies original full compiled publication against the untouched golden. Logs: `$W/native-export.log`, `$W/native-parity.log`; native results: `$W/native-results.json`.

Supplemental numeric/edge probes (needed because shared vectors omit negative zero, subnormals, huge finite values and exact Python integers):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python "$W/numeric-oracle.py"
node "$W/numeric-check.mjs"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-source" /home/user/work/venv-agent/bin/python "$W/native-edge.py"
TSX_DISABLE_CACHE=1 node --import ./node_modules/tsx/dist/loader.mjs "$W/negative-zero.mts"
```

**All final commands exit 0.** Numeric probe: 12,010 values / 24,020 exact numeric nearest/floor comparisons; every positive raw endpoint stays bounded. It evaluates the unchanged frozen App `rounded` function body, erasing only its TypeScript declaration annotations; it is helper-level numeric evidence, not full-project acceptance for astronomical durations. Native edge probe reproduces the upstream integer defect using real APIs; signed-zero probe confirms the disclosed sign difference and otherwise equal whole record/bundle, plus negative-subnormal refusal. Logs/results/scripts retained privately. The initial edge script used the internal model import and hit its existing circular initialization; switching the probe to the normal public `timeline_checkout.Clip` import (as the native suite does) resolved this. No product workaround.

Scoped lint, cwd `$A`:

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipTrimCapture.ts src/tools/video-editor/commands/clipTrimCapture.test.ts
```

**Exit 0**, `$W/lint.log` empty. Read-only Git checks in reviewer worktree:

```bash
git diff --stat 349cf9c77a04f4f4f887ef4b8f539782e1ca1609 aa0531ec704d3f14500c7f0d54c02e424acd0b67
git diff --numstat 349cf9c77a04f4f4f887ef4b8f539782e1ca1609 aa0531ec704d3f14500c7f0d54c02e424acd0b67
git diff --check 349cf9c77a04f4f4f887ef4b8f539782e1ca1609 aa0531ec704d3f14500c7f0d54c02e424acd0b67
git status --short
```

All exit 0; exact three-path counts above, clean diff formatting and no reviewer worktree modifications. `git rev-parse "$S:path"` plus byte comparisons confirmed all source/golden/vector identities above. Read-only `git merge-base --is-ancestor "$S" HEAD` in Agent integration exited **1**, documenting unmerged status, not a failing App test.

No full suite, build, browser, live socket, tsc, install, commit, merge, checkout, rebase, push or shared dependency/cache write was performed. Private source archives and generated caches are removed after review; scripts and small results remain under the assigned worker directory. No worktree build/temp output remains.

## Decisions, limitations and next steps

No settled policy decision was changed. Exact bit decoding and one final decimal-rational conversion are appropriate for the specified binary64 policy. Supplemental review only targeted independent coverage gaps; no new production abstraction or fixture semantics.

Recommended: accept the App source finding independently, have Agent resolve/record its exact-integer review blocker, freeze the final approved native identity and recompare if it changes, then qualify the installed matching Runtime/Agent/App tuple. Actual receipt retry, persistence/reload, guarded publication undo through Runtime, browser preview/render and zero-legacy traffic remain **OPEN**. These domain tests do not establish Gate 5/6, release readiness or activation. Review task itself is complete and unblocked; upstream qualification is explicitly separate.
