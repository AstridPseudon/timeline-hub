# D136a independent final validation

## Verdict

- Source: **PASS**.
- Security: **PASS** for the bounded source/provider review.
- Behavior: **PASS** for the complete open-canvas provider matrix and nearest retained controls.
- Release: **HELD**. This review does not authorize normal Agent intake, App original-nine qualification, or a genuine batch proof.

## Source and provenance

The reviewed source is `c99214a227154df5fbaf681c2e0fc52c54500025`, tree `515fca228e943e35ef2d58b5de1300aedbd9fc60`, with pristine candidate parent `ebb32e7598a3ad28fd161332f860f446a21cb3ef`, tree `e75b8d0739e63dec5908641d7db0b6846cec4905`. The worktree was clean before review. The only three changed paths are:

- `astrid/sdk/timeline/validation.py` — SHA-256 `74c14ade6dd564eadaf26f27ff6dc64d5168175f3320029768a3684754e5a0d8`
- `astrid/sdk/timeline/_timing_evaluators.py` — SHA-256 `493fa0a5ee39dfba8a7e878f2a5247fc95fe8590741d0c7232377fd36d7b6268`
- `tests/sdk/test_d136_fps_upstream_compat.py` — SHA-256 `570dc2040dd7f8c1eca887c2a22827d5963e67599f3d69df834f854bde34dfc3`

The first failing validator behavior is correctly attributed to `6f4baa07603776840f0a78cc0cf459831bc026af`. The upstream comparator is `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`, tree `f53cc8426ccef8760021ef6207303bce7b80e777`. Its `_timeline_fps` uses a positive scalar from the open canvas path and falls back to `30.0` for every other JSON form; Python `True` remains a positive scalar and therefore evaluates as `1.0`. The schema keeps `ThemeOverrides.visual` open (`additionalProperties: {}`) and defines `TimelineOutput.fps` separately as a typed number.

The candidate removes strict validation only from the open canvas namespace. Parent `config.output.fps` and child `internal_timeline.output.fps` remain strict and rational-compatible. The production route remains the existing `RuntimeCommitService.commit` dispatcher through `validate_final_candidate`, `validate_candidate_timing`, and `compile_timing`; no public protocol or caller route changed.

## Behavior matrix

The independent matrix ran 23 JSON forms in both accepted and dry-run/preview modes: 46 cases total. It captured the actual `TimingResult` from production `compile_timing`, checked every timing row's FPS, checked accepted/preview result shape, and compared the canonical authored canvas bytes with the input. All 46 cases passed. The complete matrix is in `input-equivalence.json`.

Important boundary cases:

- non-object canvas values and arbitrary object canvas values remain accepted and use fallback 30;
- `canvas.fps` null, booleans, strings, arbitrary maps, zero/negative scalars, malformed arrays, and rational list/map spellings remain accepted and use fallback 30;
- `canvas.fps: true` uses the existing scalar predicate and compiles at 1;
- positive scalar `24` compiles at 24;
- authored `[30000, 1001]` remains exactly `[30000, 1001]` and compiles at upstream fallback 30, not at `30000/1001`;
- typed output FPS controls remain strict, including atomic refusal of malformed list and zero-rational declarations.

## Commands and results

1. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_fps_d12.py tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties` — **101 passed in 3.68s**.
2. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py` — **45 passed in 2.33s**.
3. Private production dispatcher matrix script — **46/46 accepted or preview cases passed; 46 actual compile results matched expected FPS; authored bytes retained**. The additional arbitrary-object-without-fps case also passed in both modes.
4. `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py` — **All checks passed**.
5. `/home/user/work/venv-agent/bin/mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py` — **Success: no issues found in 3 source files**.
6. Private-cache `py_compile` for the three changed Python paths — **PASS**.
7. `git diff --check HEAD^ HEAD` — **PASS**.

The parent source replay still rejects the previously failing open forms (for example `canvas=true`, `fps=null`, `fps="30"`, and arbitrary FPS maps); the candidate accepts them through the production dispatcher. No source edits were made by this review.

## Qualification boundary and receiver handoff

The unchanged App projection source is approved commit `f53b016900c99e46998268e36c7c431ac0eec61e`, SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`. Its nine historical setup errors remain unchanged; this review claims no original-nine functional qualification.

Minimum next receiver inputs, without merge-to-run: Agent candidate `c99214a227154df5fbaf681c2e0fc52c54500025` / tree `515fca228e943e35ef2d58b5de1300aedbd9fc60`, unchanged App projection `f53b016900c99e46998268e36c7c431ac0eec61e`, and the current upstream comparator `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`. Agent normal intake must precede the one genuine original-nine run and subsequent batch proof. Source remains held until those gates.

No full suite, original nine, browser/socket, native, P4, collector/acquisition, build, ZIP, or 5 GB body admission was run.
