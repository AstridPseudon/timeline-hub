# D136a typed-location final source/security review

## Verdict

PASS for the bounded Luna source/security review. Release remains HELD.

The candidate is `20dbfdef45f71fa28a63f5382c154f5cca50b83a`, tree
`f790baff841baea889c1fdd8a92422a7aecf68a4`, against parent
`c99214a227154df5fbaf681c2e0fc52c54500025`, tree
`515fca228e943e35ef2d58b5de1300aedbd9fc60`. The exact binary diff hash is
`1f3f7af792722507c9d61ad7f4c6f13468424fb75b7a5fe60daa3b44e9cdde91`.

Only `astrid/sdk/timeline/validation.py` and additive
`tests/sdk/test_d136_fps_upstream_compat.py` differ. The timing evaluator,
provider/auth boundary, initialization source, protected fixture, schema,
generated files, and pins are unchanged.

## Source/security findings

No findings. The product change is limited to changing strict FPS typed-path
equality into baseline-location subset retention. This permits the genuine
`capture_initialize`/`timeline.init` command to add canonical
`parent.config.output.fps` to a pristine baseline, while every existing typed
location must remain present. Candidate values are still parsed before the
guard; strict finite/positive scalar or exact positive integer rational parsing,
parity, and D12 owner-basis checks remain active. The unchanged-legacy escape
cannot apply to a newly authored location because the candidate basis differs.

The additive tests exercise the real provider path, accepted and preview modes,
the canonical output and explicit null preservation, no mutation of the input or
old revision, wrong base-pair refusal, and eight negative removal/relocation/
rate-change cases. AST comparison confirms all original test functions and all
non-FPS validation functions are unchanged. The open-canvas authored JSON and
upstream fallback semantics, including `True -> 1`, remain in the unchanged
timing evaluator and are covered by the retained tests.

## Exact controls run

1. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/sdk/test_d136_fps_upstream_compat.py`
   — **57 passed in 2.59s**.
2. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_timing_validation.py tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties`
   — **138 passed in 4.21s**.
3. `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py`
   — **All checks passed**.
4. `/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy-cache" astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py`
   — **no issues in 3 source files** (private cache under `/tmp/w-f1a2572b19/d136a-review`).
5. `PYTHONPYCACHEPREFIX="$TMPDIR/pycache" /home/user/work/venv-agent/bin/python -m py_compile astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py`
   — **exit 0** (private cache under `/tmp/w-f1a2572b19/d136a-review`).
6. `git diff --check` — **exit 0**.

The handoff’s detached registered-loader evidence is retained as bounded
source-unit evidence: parent 2 RED, candidate 2 GREEN, with actual
`compile_timing` execution. It is not RuntimeStore/HTTP/coordinator/body or
original9 credit. The author’s isolated source reviewer PASS is likewise
retained without treating it as an independent rerun.

## Qualification boundary

This review did not run RuntimeStore, HTTP, production coordinator, original9/
27, full/core/P4/tour/socket/body/acquisition/profile/child/D130, or genuine
5 GB admission, and did not redispatch the App whole path. The prior App2100
source/custody review preserves the actual unchanged original9 result: 9 setup
errors, 0 passes, 0 failures, 0 skips, at the common typed-location seam.

Keep release held until the sole unchanged App original9 is run after meaningful
source/independent PASS and genuine admission. No merge-to-run gate or normal
home release is authorized by this review.
