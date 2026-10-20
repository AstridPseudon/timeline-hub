# SDK source-key guard report

## Change

Ported the reviewed seven-line `reject_source_keys` guard into
`astrid/sdk/invocation.py`, immediately after SDK `request_inputs` normalization
and only for `rendering.render` and `rendering.timeline_visualize`. The guard
maps the source helper's `ValueError` to the SDK's honest
`CapabilityValidationError` result contract.

Removed only the strict-xfail marker from the three-key SDK invocation test.
All assertions remain unchanged. The separate Runtime publication and
RenderRequest propagation xfails remain untouched.

## Evidence

All commands ran in this worktree with `PYTHONPATH="$PWD"` and the shared
Agent environment `/home/user/work/venv-agent/bin/python`.

- `git diff --check` — passed.
- `python -m pytest -q tests/sdk/test_capture_closure_source.py tests/sdk/test_timeline_filmstrip_invocation.py tests/sdk/test_capture_source_runtime.py tests/packs/rendering/test_verified_source.py` — **72 passed, 27 deselected, 2 xfailed** in 240.80s. The xfails are the retained RenderRequest propagation cases.
- `python -m pytest -q -vv tests/sdk/test_capture_closure_source.py -k 'sdk_capture_invocation_refuses_source_before_admission'` — **3 passed, 25 deselected** in 45.58s.
- Direct `_invoke_internal_result` evidence for `verified_source`, `timeline_source`, and `ASTRID_VERIFIED_TIMELINE_SOURCE`: each returned `{'type': 'CapabilityValidationError', 'message': 'verified timeline source is host-owned', 'sdk_error': 'CapabilityValidationError', 'sdk_category': 'validation'}` and each left `runtime.created == []`.
- `python -m pytest -q -vv tests/sdk/test_timeline_commit_provider.py -k 'import_no_renderer'` — **1 passed, 110 deselected** in 1.49s.

No full suite was run, per task instructions.

## Decisions and scope

- Used the existing host-owned source helper and its exact boundary message;
  no new authority, caller replacement, provider, verifier, or propagation
  behavior was added.
- Kept the import lazy and capability-scoped, preserving the SDK import fence.
- Ordinary inputs and native CAS behavior were not changed.

## Status

Complete. No blockers. No Runtime, App, Composition, integration, push, or
ledger changes were made.
