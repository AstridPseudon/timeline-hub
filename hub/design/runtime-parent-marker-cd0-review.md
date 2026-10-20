# Runtime parent ownership marker review

## Decision

**APPROVE the corrected tests-only patch for gated merge; do not merge here.**

The reviewed candidate is `cd0b0dcbea57c2a140e970eda59bea1161d6ff06`,
whose parent is the required base
`6ab3243972f8dc49105819e6d7ba7aef1a2888b8` and whose tree is
`c7c06100471820a43805657ea405646966f7f3a9`. The candidate correctly removes
the imperative `pytest.xfail`, adds the current-013 ownership-enum refusal,
and puts the unchanged full acceptance body under a strict exact-`ValidationError`
xfail.

One small correction is included in this worker's `tests/test_timeline_clip_replacement.py`:
the refusal assertion calls `_native_commit(...)`, not `validate_request(...)`
directly. This keeps the exact error assertion while proving the denial crosses
`RuntimeService.commit_timeline`'s normal request-validation boundary. The
candidate's direct helper call was insufficient for the explicit owner
requirement. The harness-produced commit from this worker (or an equivalent
successor carrying this one-line correction) is the merge target.

## Checks

- Current Runtime targeted command:

  ```text
  PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m integration --tb=short \
  tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema \
  tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media
  ```

  **1 passed, 1 xfailed, 0 failed**, exit 0.

- The refusal is an exact `ValidationError` matching the ownership enum text
  ` 'parent' is not one of ['shared', 'occurrence'] ` and reaches
  `service.commit_timeline` through `_native_commit`.
- The acceptance test retains both positive assertions: accepted/rebased status
  and replacement of the parent clip asset. Its strict xfail is explicitly
  `raises=ValidationError`, with the D04/schema-0.2.14 reason.
- `git diff --check` passes for the worker patch.
- Existing frozen evidence, not rerun here: Runtime `a0dca169` with Agent
  `310e548` and `--runxfail` gives **1 passed**, proving the preserved positive
  body on the intended future pair.

## Scope and limits

This is a tests-only current-013 compatibility marker. It does not claim D04
complete, schema 0.2.14 availability, product behavior, snapshot parity, or
the frozen positive as current-013 acceptance. No full or broad suite was run;
no duplicate central run was requested. No product, schema, snapshot, fixture,
dependency, shared cache, branch, or integration worktree was modified.

