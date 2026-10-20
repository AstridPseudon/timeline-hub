# Agent M3 explicit-theme source object — blocked seam

Date: 2026-10-20 23:26 UTC
Owner: Agent
Status: BLOCKED pending an authorized pre-admission Runtime theme carrier

## Result

No Agent product change is safe on the current integration tree. The actual
normal requester-side render-preparation call site is
`astrid/sdk/invocation.py:_prepare_managed_render_inputs()` (lines 1202–1544).
It resolves the Runtime-selected canonical snapshot and candidate projection,
validates the exact config/registry/profile, and returns the task inputs before
`_kernel_invoke()` builds `input_object_ids` and admits the task.

That path has no authorized selected `theme.json` carrier. The snapshot contains
only the projected `config` and `registry`; the timeline's `theme` value is a
metadata slug and `theme_overrides` is config data. The existing pre-admission
CAS helper (`_import_json_object()` / `_store_visualize_objects()`,
`astrid/sdk/invocation.py:2438–2468`) can ingest bytes, but it cannot obtain
authoritative theme bytes.

The only current `theme.json` materialization is post-admission in
`astrid/core/execution/generic_host.py:6888–6903`: GenericHost fetches an
already-authorized named `theme` descriptor, writes `theme.json` beneath the
attempt's `managed-objects`, and exposes `materialized_objects["theme"]`.
There is therefore no requester-side `runtime_theme_path` available before the
task is admitted. The existing resolver at
`astrid/packs/rendering/shared/rendering_backend/__init__.py:89–123` cannot be
called for normal managed render preparation without inventing a source path
or treating a caller slug/inline/browser value as authority.

## Exact missing seam

Runtime/App must first expose the already selected, project-authorized
`theme.json` object to the normal requester-side preparation path, bound to the
same saved `timeline_ref` or closed candidate base, config/override facts, and
render profile. The source-side Agent change can then be made at the existing
pre-admission seam:

1. receive only that authorized materialized `theme.json` carrier;
2. write the exact frozen snapshot config to an attempt-local `timeline.json`
   (not a project path);
3. call exactly one
   `_resolved_theme_for_render(timeline_path, runtime_theme_path)`;
4. serialize only the complete `{id, visual}` result once with canonical JSON;
5. ingest it through the existing project-owned immutable CAS flow;
6. add the existing named descriptor
   `{name: "theme", object_id: digest, digest: object_id,
   filename: "theme.json", required: true}` and preserve its position in the
   ordered `input_object_ids` mirror.

The object identity must be the Runtime-admitted object returned by ingestion.
No slug-derived ID, caller hash, browser-resolved object, new resolver, DTO,
endpoint, store, schema, certificate, renderer credential, or worker
`projects:write` is appropriate.

## Runtime proposal

Extend the existing managed-render admission/binding seam only enough to accept
the producer's already-authorized named descriptor and append its exact object
ID to the existing ordered CAS manifest. Keep the current timeline authority,
snapshot/profile/fact checks, idempotency, saved/candidate base rechecks, and
`remote_worker_deployment` named-input binding unchanged. GenericHost can then
perform its existing `theme.json` materialization, and the existing Agent task
adapter can forward `materialized_objects["theme"]` to the renderer. Absent
theme input must continue to select the approved default fallback and remain
uncertified for explicit-theme parity.

This is a proposal, not an explicit-theme certification claim. The Agent side
must remain fail-closed until Runtime supplies the carrier before admission.

## Scope/forgery controls required when unblocked

- saved input binds to the admitted Runtime timeline identity and current
  authority; candidate input retains its exact base plus forwarded candidate;
- the descriptor's `object_id` and `digest` match exactly and appear once in
  the ordered manifest;
- absent carrier leaves the existing default behavior unchanged;
- a descriptor for a different project, timeline/base, or selected theme is
  refused by normal Runtime admission;
- caller `theme_id`, inline theme JSON, and browser-resolved values are never
  used as authority.

## Evidence

- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_managed_timeline_render.py tests/packs/rendering/test_render_export_task_adapter.py tests/sdk/test_managed_render_invocation.py` — **179 passed, 1 failed, 1 deselected**. The failure is the existing real-MP4 adapter test because the shared Remotion package is absent at `remotion/node_modules/@banodoco/timeline-composition/package.json`; no source-side test failed.
- `PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_managed_timeline_render.py tests/packs/rendering/test_render_export_task_adapter.py tests/sdk/test_managed_render_invocation.py -k 'not writes_real_mp4_and_is_callable'` — **179 passed, 2 deselected**, with 57 existing deprecation warnings.
- The same run passed the existing admitted-theme forwarding and forged/outside/absent-carrier controls. No browser, render qualification, full suite, or public pin was run.

