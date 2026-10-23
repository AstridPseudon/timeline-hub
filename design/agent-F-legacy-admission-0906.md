# Agent F legacy admission handoff

Date: 2026-10-23 UTC

## Decision and delta

The source-backed failure from `agent-F-unconfirmed-env-0900.md` was
reproduced: `_run_task_impl` called `_renderer_selection` on a supported
minimal `SimpleNamespace` capability record without `adapter`, producing an
`AttributeError` before the required legacy assembler refusal. The smallest
correction is in `astrid/core/execution/generic_host.py`:

```diff
-    if record.adapter.remotion != "selected":
+    adapter = getattr(record, "adapter", None)
+    if adapter is None or adapter.remotion != "selected":
```

This makes the helper preserve the existing no-selection path for a record
that has no adapter. It does not guess a renderer, default acceptance, bypass
scope/fence/lease/security checks, restore an old route, or add an executor.

Base commit SHA: `2e21af300abbefc8afbad217189fa4715cf82616`.

## Commands and counts

Targeted acceptance, with the durable 0856 Runtime projection:

```text
PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages" \
/home/user/work/venv-agent/bin/python -m pytest -q \
tests/packs/video_editing/test_runtime_publication_chain.py::test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts
```

Result: `1 passed in 4.86s`.

Adjacent renderer controls:

```text
tests/test_generic_host.py::test_a_task_selecting_remotion_fails_at_lease_with_the_remotion_reason
tests/test_generic_host.py::test_an_omitted_selector_renders_with_ffmpeg_when_remotion_is_unavailable
tests/test_generic_host.py::test_an_omitted_selector_renders_with_remotion_when_available
tests/test_generic_host.py::test_an_explicit_ffmpeg_task_runs_whatever_the_remotion_state
tests/test_generic_host.py::test_a_timeline_ffmpeg_refuses_still_fails_with_both_reasons_when_the_host_chose_ffmpeg
tests/test_generic_host.py::test_a_failed_render_is_not_blamed_on_remotion_unless_the_host_chose_ffmpeg_for_it
```

Result: `8 passed in 89.08s` (the parametrized node contributes two cases).

Required checks:

- `make ruff PY=/home/user/work/venv-agent/bin/python` → `current=2149 baseline=2149`
- `.../venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` → `current=1912 baseline=1912`
- `.../venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` → `ok`
- `.../venv-agent/bin/python scripts/artifact_manifest.py --check` → current
- `git diff --check` → passed

## Limits and review

Only the existing generic-host production helper changed. No full suite or
browser/render/heavy journey was requested or run. The 2149 Ruff and 1912
mypy ceilings are unchanged. Independent review is required before merge.
