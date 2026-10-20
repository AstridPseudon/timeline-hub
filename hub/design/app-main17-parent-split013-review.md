# MAIN17 / current013 parent split review

**APPROVE for a later qualification gate. No blocking source findings.** Current-root/current-tuple qualification remains FIRST. This approves the bounded source port, not integration, deployment, writer retirement, incoming-transition film splitting, or Gate 5/6 closure.

Reviewed App `30b63a28a8ef339becae27549191755192f3106a`, tree `070cd9e6f7d09dec6b8e6d988ba7d3a93b9ea6c9`, directly over `cee68b807017efc8669c7d75318cf51aa70ec855`. Read PLAN, `app-main17-parent-split013-source-port.md`, the prior `app-refreshed-split-source-review.md` PASS and `app-split-mirror-fix-independent-review.md` APPROVE. No product or test changes.

## Source and retained root

The candidate is exactly the approved **16-path** split delta, **+4,438/-33**. Each changed file is byte-equal to approved `f665d5308cc018bc89eff73a5cff21dc8a3bf1b3` against `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`. The two approved CORS paths already match and are unchanged. Every other tracked path equals cee68; existing tests are unchanged and no path is deleted. No new fail/skip/todo marker appears in the four imported test files.

Thus fixed label lifecycle, MAIN17 touch/shell behavior, cold4 config/spec/helper, server/proxy/7M1, render/admission/download, and generated/package/lock surfaces are retained. MAIN17 `17e46de99` remains an ancestor. This is source preservation, not a fresh behavioral qualification of those entire areas.

Runtime remains normal **0.2.13 / S2**, exact source `2c4ac180c2220bdad966bc01e95ad230e99ce26a`: all **13** locked files match producer bytes, manifest and hashes. The edit-command schema SHA-256 remains `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. Public Composition **0.0.12** artifact remains `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; all **77** privately extracted files match it. Package and lock are unchanged.

## Findings

- `commands/clipSplitCapture.ts:57` and `commands/commitSession.ts:325`: eligibility and capture share `parentClipSplitRows`, including complete parent/config array equality, owner and stable-ID validation. A divergent non-target mirror fails preflight before capture. Missing/null/scalar mirror handling follows the existing native selected-collection semantics; the implementation does not repair or normalize either mirror.
- `commands/clipSplitGesture.ts:50` reserves the right ID once through the existing ID seam, checking config and resolved IDs. Frozen capture carries that ID through original-basis replay. `commitSession.ts:336` checks exact project/timeline/displayed head, raw parent binding, unique display/config rows, pinned-group membership and collisions. Opaque `app.canonical` is never ownership authority; no new ownership DTO appears.
- `clipSplitCapture.ts:205` reads the entire original target, its exact registry source, collection topology/insertion boundary, neighbour dependency sites and authored FPS. Source seconds/window/speed remain literal; rational FPS and integer frame sums preserve half-open ownership. Creation records absence and created-ID claims. Replay checks every original claim; it cannot silently recapture or weaken guards.
- `commitSession.ts:356` finishes the frozen basis and executes its original command against the current raw bundle after ACKs. Prepared generation, bundle identity, exact command and full native preview fence submission. `useTimelineCommandSession.ts:173` fences capture, finish and submit behind earlier legacy saves.
- `commitSession.ts:124` and unchanged `commitOutbox.ts:253` retain the original persisted request body/key, explicitly retry unknown ACKs, and release dependent commands only at the accepted predecessor head. Suffix command guards and IDs remain original. `pump(false)` prevents an appended suffix from retrying an uncertain prefix implicitly. Mounted recovery and the capture-before-ACK/finish-after-ACK tests pass without recapture.
- `hooks/clip-editing/useClipSplitting.ts:22` and `hooks/useTimelineCommandsService.ts:808` choose unsupported routing before capture. Once native capture starts, exceptions produce visible refusal without reaching the legacy snapshot writer. Selected/context/keyboard/SDK mirror negatives, successful unsupported/text/animation/relation/transition/occurrence and no-port legacy controls remain positive. Pinned groups retain their existing blocked-edit policy; multi-split retains its existing writer. No broader group/multi native support is claimed.
- Unknown metadata survives whole-row cloning, command replay and full-row preview. The direct tests cover opaque/null/absent values and raw ownership despite misleading `app.canonical`. An additional read-only probe confirms own JSON `__proto__`, `constructor`, `prototype`, nested params and opaque `app.canonical` survive persisted-basis replay and config/resolved preview without prototype pollution or input mutation.

## Exact native cases and golden

Native reference is a private `git archive` of exact Agent **d8749a9ce12a699672faf3ad96b4e4cbea9245c2**, not whichever Agent checkout is currently active. Inspected all seven source-port input documents, their differences, export/comparison scripts and result log; copied the inputs/verifier into this worker and changed only export imports to this reviewed App worktree. No manually fabricated command claims.

| Case | Independently rerun result |
|---|---|
| golden | Exact command, complete record, whole authored bundle, inverse and redo |
| fractional-window | Literal `2.123456789..10.987654321`, speed `1.3`; exact command/record/bundle/inverse/redo |
| null-speed | Own null speed and hold retained; exact command/record/bundle/inverse/redo |
| image-hold | No source window; exact command/record/bundle/inverse/redo |
| target-transition | Same atomic refusal: `clip.split v1 does not support transition` |
| neighbor-transition | Same atomic refusal: `clip.split v1 does not support parent transitions` |
| explicit-null-transition | Accepted; own null preserved on both halves; exact command/record/bundle/inverse/redo |

All seven use the rational `30000/1001` clock. The first input equals the checked-in golden input. Golden SHA-256: `a0e24c1f78d8580f908973745950ed0196c17257831197ec2f75a55abc638f63`. The checked-in verifier independently confirms its full authored output and inverse/redo against d874. For accepted differential cases, actual App commands also produce the same full native immutable document when executed natively. This does not claim that serializing an App preview bundle can independently reproduce Python immutable digests: JSON erases integer/float representation and native execution owns those identities.

Directly inspected d874 `_split_commands.py`: any non-null target transition or any non-null parent-neighbour transition is refused before right-row creation. **No incoming-transition film split qualification**, transition-clearing policy or broader native transition claim follows from these tests. Explicit null acceptance is a distinct case.

## Commands and results

From `/home/user/work/wt/app-m2-main17-parent-split013-review`, define:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-parent-split013-review
N="$W/notes"
```

```sh
node --require "$N/runner.cjs" node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipSplitCapture.test.ts src/tools/video-editor/commands/clipSplitGesture.test.ts src/tools/video-editor/commands/commitSession.split.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.split.test.tsx
```

**PASS, exit 0: 4 files / 124 tests, 11.13s** (`narrow-app.log`). No 1,295-test repetition.

```sh
node --import tsx "$N/native-export.ts"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python "$N/compare-native.py"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_split_parity.py
node --import tsx "$N/opaque-probe.ts"
```

**All PASS, exit 0:** 7/7 actual App/native cases; 1/1 checked-in golden with full record/output/inverse/redo; opaque/prototype-key probe. Logs: `native-export.log`, `differential.log`, `golden-parity.log`, `opaque-probe.log`.

```sh
cd "$W/agent-d874"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/agent-d874" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_split.py -k 'portable_golden_capture or fractional_speed_and_precise_source_end or null_hold_speed_and_intent or bad_identity_mirrors_neighbor_transition'
```

**PASS, exit 0: 10 passed / 70 deselected, 0.97s** (`selected-native.log`). No full 80-case repetition.

Back in App CWD:

```sh
python "$N/source-audit.py"
python "$N/audit-deps.py" > "$N/deps-after.json"
cmp "$N/deps-before.json" "$N/deps-after.json"
git diff --check cee68b807017efc8669c7d75318cf51aa70ec855 HEAD
git diff --check
git status --short
```

**All PASS, exit 0; status clean.** Source audit checks exact allowlist/bytes/tree, retained root, producer pin/manifest and private12 artifact. Dependency comparison covers the recorded package/peer/cache snapshot around differential work; it is not a machine-wide concurrent-write audit. Audit development corrected two verifier assumptions (Git stores the CLAUDE symlink target rather than dereferenced content; producer schema is named `edit-command.json`). No behavior test failed or was weakened.

Node 22.22.0 / Vitest 4.1.5; own private public12 overlay borrowed other dependencies read-only. Only this worktree's `node_modules` link was temporarily redirected, then restored to `/home/user/work/app/node_modules`. Runner loading and `--no-cache`, with cacheDir under this worker, avoided shared Vite cache writes. Native bytecode and pytest cache writes were disabled. Shared dependencies/runtimes/venvs and other worktrees were not modified. Logs and private probes are under this worker's `notes/`; no build output or temporary files remain in the worktree.

## Remaining writers and next gate

No writer was retired. The two explicit single-split legacy call sites remain at `useClipSplitting.ts:39` and `useTimelineCommandsService.ts:821`; intersecting multi-split remains at `useClipSplitting.ts:69`. Group restrictions and established unsupported/occurrence/transition paths remain before native capture. D01 remains OPEN: whole-parent persistence/CAS, popup add/swap and shot graph, bootstrap/repair, duplicate/group/placement, ordinary patch/proposal batches, elements, and the resolved-edit serializer still require their separate migration and qualification. The prior writer census is not evidence that this source port closes any of those rows.

Finish current-root qualification first. Then prepare and centrally qualify the supported split cohort on the exact current wrapper/seed and d874/2c4ac/013/public12 tuple. Required later evidence includes real renderer-off acceptance, complete immutable parent/config/shot/internal reload, guarded Runtime undo/redo, lost ACK plus newer edit plus actual process restart with exact request/key retry and no recapture/reallocation, disjoint success/conflict/ABA with draft retained, and zero legacy snapshot traffic. Old split browser pins must be refreshed before using that lane. Only those qualified consumers can justify a later writer cut.

Not run or claimed: full suite, build, tsc, lint, install, browser, localhost/socket suite, actual Runtime acceptance/restart, publication-history qualification, audiovisual parity or observed zero legacy HTTP traffic. No integration merge/retirement or KEEP marker; no blocker or design deviation. Deliverables: this design review, worker `report.md`, `commit-msg`, and `DONE`.
