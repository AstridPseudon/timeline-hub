# D136a validation

## Source decision

The open `parent.config.theme_overrides.visual.canvas` path is no longer
collected by strict typed FPS validation, and its open forms are not required
to be objects. Strict validation remains for `parent.config.output.fps` and
each `shots[*].internal_timeline.output.fps`; baseline presence checks retain
the typed declaration locations. `_fps_basis` now treats malformed/open canvas
containers as opaque while preserving its D12 owner/parity guard.

The production timing view marks an explicitly authored open canvas path only
inside the detached validation input. The production evaluator then follows
the qualified upstream rule: a positive scalar is used, `True` is `1.0`, and
all other JSON forms fall back to `30`. Direct detached compiler callers retain
their existing exact rational behavior. The authored candidate and persisted
canonical document are never rewritten.

## Parent red / candidate green

- Parent-source replay from `a30e74e901a28b39c28facba3deb00d76f186e23` with
  `[30000, 1001]` at the production path: **RED**, `FinalCandidateError:
  candidate.parent.config.theme_overrides.visual.canvas.fps: must be a finite number`.
- Candidate production matrix: **GREEN** for all listed open forms in both
  accepted and dry-run modes; authored canvas bytes retained.

## Tests

Command, using the existing Agent interpreter and `PYTHONPATH` runtime
binding:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_timing_validation.py tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties
```

Result: **126 passed in 3.82s**.

The additive provider matrix covers non-object canvas values; null, bool,
string, mapping, scalar, wrong-length, non-integer, zero, negative, and exact
rational-pair FPS values. It checks both accepted/dry-run replies, effective
FPS, and canonical authored bytes. Existing typed-output refusal controls and
the D12 parity/owner controls remain green.

Quality commands:

- `ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py`: **All checks passed**.
- `mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py`: **Success: no issues found in 3 source files**.
- Private-cache `py_compile` for the same 3 files: **PASS**.
- `git diff --check` against parent and worktree: **PASS**.

## Limits

Filesystem free space was 4,576,248 KiB, below the 4.6 GB source-only body
floor. The heavy 5 GB body admission is therefore **NOTRUN**, with no invented
admission. Full, browser, live socket, native, collector, install, merge, and
App original-nine suites were not run under the task rule.
