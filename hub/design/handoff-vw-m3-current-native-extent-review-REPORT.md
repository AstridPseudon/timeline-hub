**Verdict: DEFECT for whole-unit merge readiness. APPROVE extent ONLY for the plain original-window/extent behavior tested below.** The explicit-tail old positive remains lost, and five CURRENT M2 assertions newly fail. No product fix or merge request was made.

Reviewed frozen producer **626eed656edf2a6398703e9e5318343069e47019**, tree **845db31a54bde351a46fcac9967d430980ef4729**, direct parent **c456b3281497653cecf44f61acd6fa30565d83c8**. The producer finished with harness exit 0, BLOCKED, and recycled source. This review waited for that final commit, archived it under its own worker directory, verified all **2,997 tracked blobs**, and bound Python imports and Root source loading to that archive. The initial reviewer checkout was only the integration baseline. All archived tracked bytes still matched after testing; both refs remained fixed and the reviewer checkout remained clean.

The diff contains exactly service `_segment_request`, runner extent parsing/forwarding/props/bounds, Root, the new extent Python test file, and the exact Root test file. Root equals approved `61f1a420f` byte-for-byte. Its seven-case test equals `20d4ab1aa9` byte-for-byte (SHA-256 `181950efa7e91f646d57496b33897e4e40ec6723c695f6bb6d8ffe940443b6cc`). No foreign parent, serializer/precision change, PCM helper or activation, package/root pin change, global clock-validator change, tail ownership bypass, authored stamp, DTO, factory, or second projector. Existing M2/callback/Three.js and duration-helper bytes are unchanged. Service computes extent before isolation from the existing render view, removes caller reserved metadata, and retains original selected clips and the absolute window. Support and locked execution enforce the same fact; Root reads and validates that fact without changing tail placement.

Independent results, each with actual targeted execution:

| Lane | Frozen CURRENT baseline | Frozen candidate |
|---|---:|---:|
| Existing native-window + capture-callback files | 36 passed | 36 passed |
| Service window/segment neighbors | 5 passed, 47 deselected | 5 passed, 47 deselected |
| Exact Root file | 4 passed, 3 failed | 7 passed |
| Extra Root 300/600/rational-FPS/boolean cases | 2 failed | 2 passed |
| Independent empty/sparse original300/600 service→bounds probe | 4 failed | 4 passed |
| Producer extent/bounds file | absent | 73 passed |
| Existing scene-composition file, excluding real render | 15 passed, 1 deselected | **10 passed, 5 failed**, 1 deselected |
| Held tail file: original three cases + added old-route positive | old-route/control: 2 passed, 2 deselected | **2 failed, 2 passed** |

Passing coverage includes no-window/full/native absolute selection, legacy local-window duration, selected PNG, alpha/default encoding flags, Three.js adaptation, current capture callbacks, source exclusions, identical empty layers with distinct originals, rational FPS, original-window overrun, forged authored/request metadata, safe-integer/type/length bounds, consistent layer stamps, FPS/speed/source-range refusal, and matching support/locked refusal before allocation. The new Three.js test also proves its downstream local slice and pinned scene match the old slice despite the service representation change. This is in-process source and command-assembly evidence.

**Defect 1 — explicit-tail bounded positive.** With original authored extent 300, rendered extent 330, top clip covering [0,30), and selected [0,30), the real old slicer and both Root callbacks produce duration 30; the tail Sequence starts at local 30 and contributes no selected frames. The candidate service retains extent 330 and the clock, then `_native_window_argument` at `run.py:918–920` refuses them together. Root at `Root.tsx:164–166` independently refuses the same combination. Both unchanged positive assertions fail with `composition duration conflicts with an existing render clock`; ordinary full-tail/no-clock controls and the independently exercised old route pass. These are covered sparse windows, not the pre-existing empty/gap tail issue. The held three-case source was archived exactly from `e2d926319`; replay changes only source-root location and the tarball filename to CURRENT's pinned **0.0.10**, then adds one old-route positive. Expectations were neither weakened nor marked xfail. No broad tail qualification follows.

**Defect 2 — five new CURRENT M2 suite failures.**

- `test_service_layered_plan_native_renderer_isolates_and_adjusts_once[0]` and `[1]`: expected sliced `(at,from,to,speed,hold)=(0,63,65,2,2)`, received original `(2,55,75,2,20)`.
- `test_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[0]` and `[1]`: expected null service window, received original [180,210).
- `test_layer_materialization_retains_null_window_support_rejection`: expected null-window/full-timeline rejection seam, received native window.

All five passed on the exact baseline. These establish a changed service/support contract and unmet CURRENT-suite qualification; they alone do not prove a pixel or audio regression. The downstream Three.js equality test passes. The orchestrator must resolve this mismatch without recoding lost behavior as refusal or deleting/weakening the original assertions.

Exact replay entrypoints (all absolute):

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-review-tests.py candidate
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-review-neighbors.py candidate
```

Both drivers exit 0 after asserting the expected lane exits; failed pytest lanes themselves exit **1**. Baseline used the same entrypoints with `baseline`. The corrected independent probe was rerun after adding the explicit `am-sprite` element type required by CURRENT; its initial inherited untyped fixture failed serialization and was not accepted as behavior evidence. The corrected baseline fails on the absent native window, and the unchanged corrected candidate expectations pass. Original logs remain.

Every Python lane uses `/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short`, cwd and `PYTHONPATH` set to this review's frozen `baseline` or `candidate` archive and `PYTHONDONTWRITEBYTECODE=1`. Root uses `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`, `ROOT_SOURCE_DIR` set to that archive's `remotion/src`, and `NODE_PATH` set to this worker's real private `root-modules/node_modules` containing only a TypeScript 5.9.3 leaf link. Root runtime imports are stubbed; tail probes extract the actual pinned 0.0.10 duration chunk into temporary storage. The checked-in tarball matches lockfile sha512. No shared package/cache/venv/runtime was written. `git diff --check c456b3281 626eed656` passes. Full commands/environments, logs, source hashes, patch, and post-test checks are adjacent flat artifacts with this report's prefix (`-candidate-results.json`, `-candidate-neighbors-results.json`, `-sourcebytes.json`, `-all-blobs.json`, `-scope.patch`, `-postcheck.json`).

Recommended next step: retain the **plain extent-only** approval; hold whole-unit integration until the orchestrator settles the CURRENT M2 contract and authorizes preservation of the covered pre-tail positive. Review is complete, with no review execution blocker. No full/browser/socket/render/install/network/git mutation/push was performed. Runtime certification, public0.0.12 adoption, normal PCM activation, MP4 output, parity, real films and source certification remain unverified and unapproved here.
