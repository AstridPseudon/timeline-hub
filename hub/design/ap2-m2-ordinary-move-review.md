# AP2 M2 ordinary move member review

Verdict: **APPROVE for the two-file member; HOLD the mixed hold/label/move proof.**

Reviewed commit `157675c37` (`tl/ap2-m2-ordinary-move-member`), with the
worktree unchanged. No new private locked graph was present in the named
artifact area, so this review uses the exact current move-only proof and calls
out the missing mixed prerequisite explicitly.

The native App input is the closed shape
`{ op: 'clip.move', target, payload: { at }, order? }`. `at` is required to be
a finite, non-negative absolute timeline value; `order`, when present, is
finite and remains batch ordering metadata. `track`, `before`, `after`, and
other payload fields are refused. The raw Agent `select` is an explicit
argument and is not inferred from or rewritten from `target`.

The member delegates capture, finish, quantization, execution, and all safety
semantics to the existing `captureClipMove`, `finishClipMove`, and
`executeClipMove` helpers. The helper emits the current Agent `clip.move` v1
form (`args.on`, in seconds), while preserving the original authored basis.
For parent clips absolute `at` maps directly to `on`; for occurrence clips
the existing occurrence origin is applied. Existing source pins, track and
owner bindings, FPS quantization, duration checks, occurrence-map and boundary
guards, relation clearing, and full reads/writes/expectations remain in the
delegated path. The frozen basis prevents refresh or clamping. Ordinal `2`
was exercised in the local sequence and is applied to both the record and
derived writes; replay uses the captured command and exact authored bundle.

Evidence:

- `node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts` — **4 files, 162 tests passed**.
- `node_modules/.bin/eslint src/tools/video-editor/commands/ordinaryMoveMember.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts --max-warnings 0` — **passed**.
- `node_modules/.bin/tsc --noEmit --pretty false` — **passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-app2-native/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_parent_track_label.py` — **147 passed**, two existing pytest-config warnings.
- The same command with `test_recipe_clip_scalar_fields.py` and
  `test_parent_track_label.py` — **117 passed**, two existing pytest-config warnings.
- A fresh TS-generated move command, record, and bundle piped directly to
  Agent passed exact `execute`, `replay`, guarded inverse, and redo assertions:
  **TS output accepted by Agent: command/record/bundle/replay/inverse/redo**.
- A direct non-test probe refused negative, NaN, infinity, string, extra
  `track`, `before`, and `after` values, plus an occurrence destination that
  crossed its next boundary. No clamping or unsupported fallback was observed.

The mixed hold/label/move cross-language regeneration remains incomplete: the
TS import graph fails before producing JSON because the installed
`@banodoco/timeline-composition/evaluation` package does not export
`computeMediaTrim`. This is an environment/package prerequisite failure, not
evidence against the move-only golden. The existing local mixed-sequence test
proves ordinal sequencing and immutable local execution, but not the complete
TS-to-Agent mixed batch.

Not run: full suite, browser, localhost/live socket, Runtime door, or locked
graph qualification. No product source, new test, shared install, dependency,
pin, generated contract, Git ref, or ledger was changed. Recommended next step:
repair/provide the locked Composition graph (including `computeMediaTrim`) and
rerun the mixed hold/label/move TS-to-Agent command/record/bundle/inverse/replay
proof before approving the enclosing batch integration.
