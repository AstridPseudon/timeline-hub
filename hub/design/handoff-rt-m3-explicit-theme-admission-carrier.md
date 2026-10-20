# Runtime explicit-theme admission carrier — bounded result

## Decision

**BOUNDED MISSING AUTHORITY.** Runtime has no current, verified normal saved/candidate
carrier for the resolved explicit Theme. App's `theme_id` is only a slug and the
normal render request's `input_object_ids: []` admits no theme object. A slug or a
browser-resolved object must not be certified as theme authority.

## Exact supported Runtime carriers

- Managed render admission is Runtime-owned in
  `runtime_protocol/store.py:_freeze_managed_render_inputs()` (1709 onward).
  It resolves the authenticated timeline, freezes `config`/`registry`, derives
  ordered CAS IDs from canonical registry media (2006–2065), and requires any
  supplied `input_object_ids` to equal that ordered list exactly (2073–2085).
  `create_task()` installs those frozen IDs and the snapshot/profile-derived
  storage estimate (2434–2466).
- The accepted render authority already binds project/timeline, config version,
  head event/hash, config/registry/materialized-registry hashes, parent revision
  and content digest, dependency digests, snapshot digest, and admitted media
  IDs (`store.py:2103–2127`). Historical admission uses the closed
  `project_id/timeline_id/revision_id/publication_id/content_digest` selector
  (`store.py:1729–1734`) and exact replay authority.
- Generic task/CAS custody has a real named-input carrier: project-associated
  `input_object_ids` are validated atomically (`store.py:1518–1560`), and
  `remote_worker_deployment.py:_spec_input_bindings()` maps admitted
  `spec.inputs`/`input_digests` names to those exact ordered IDs (598–651).
  Explicit `execution_request.inputs` is the equivalent named path
  (`remote_worker_deployment.py:710–728`). This is the only existing Runtime
  binding that could carry a `theme` name and immutable JSON object digest.

## Why it does not solve normal explicit Theme today

- The timeline schema stores `theme` as a string and `theme_overrides` as an
  override map (`runtime_protocol/schemas/timeline-commit-bundle.json:4760–4764`);
  Runtime only consults the override canvas for storage sizing
  (`store.py:2198–2209`). It does not resolve or materialize `theme.json`.
- Managed render admission derives IDs from timeline registry assets and refuses
  an additional theme ID by the exact-list check above. Adding only a
  `spec.inputs.theme` descriptor also fails the existing named-binding contract
  unless that object is in `input_object_ids`.
- `snapshot_refs.publish_snapshot()` is an exact project/CAS snapshot carrier,
  but its managed timeline snapshot is `config` + `registry`; it is not a named
  Theme document carrier (`snapshot_refs.py:114–155`, `169–220`). Do not put
  authoritative resolved Theme JSON inline in that snapshot.

## Saved/candidate capture boundary

`capture_validation.validate_capture()` verifies saved captures against the
Runtime-selected revision closure and Agent projection, and verifies working-copy
captures against the retained base plus forwarded candidate (`104–149`). A
working copy without a candidate is explicitly uncertified; a CAS-only capture
has no revision authority. `snapshot_refs.prepare_snapshot()` separately checks
project/timeline scope, saved revision digest, or candidate/publication/base
binding (`114–139`). These controls cover timeline config/registry and ancestry,
not a resolved Theme object.

## Smallest existing-carrier proposal for peer agreement

Have the existing producer/admission seam create or identify the exact resolved
Theme JSON as one project-owned CAS object, selected from the same config,
projection fact, and render profile that populate the existing
`timeline_authority`. Carry it through the existing normal task envelope as:

```text
input_object_ids: [...existing canonical inputs..., <theme object id>]
spec.inputs.theme: {object_id: <same id>, digest: <same id>, ...existing descriptor metadata...}
```

The Runtime change would be limited to admitting that already-authorized named
`theme` object into the managed render's existing ordered input set and retaining
the current timeline authority, snapshot, profile, idempotency, and accepted/base
checks. No new DTO, route, table, resolver, client hash, or inline authority is
needed. Viewing's existing task-adapter forwarding can then consume the named
materialization. Until that object is admitted, the default fallback remains
unqualified for explicit-theme parity.

## Evidence

- `python -m pytest -q tests/test_remote_worker_deployment.py -k 'runtime_binding_preserves or explicit_request_inputs or omitted_request_inputs'` — **10 passed**, 14 deselected. The public `RuntimeService.create_task()` witness ingests project CAS objects, admits named descriptors, and read-only projects them to `InputBinding` names/digests (`tests/test_remote_worker_deployment.py:302–353`).
- `python -m pytest -q tests/test_snapshot_authority_refusal.py -k 'exact_saved_capture_passes_without_canonical_writes or native_unclaimed_cas_capture_does_not_acquire_revision_authority or forged_capture_is_refused_without_writes'` — **11 passed**, 14 deselected. Saved revision capture, native CAS-only capture, and no-write refusal boundaries pass.
- `python -m pytest -q -m integration tests/test_capture_candidate_binding.py -k 'saved_certification_does_not_require_candidate_method or original_saved_forgeries_refuse_before_writes or fresh_working_copy_semantic_forgeries_refuse_before_writes or publication_must_derive_from_forwarded_candidate'` — **blocked at fixture setup**: 16 errors because the expected Astrid checkout `/home/user/work/wt/astrid` is unavailable; 112 tests deselected. Candidate-binding source was inspected directly. No product code, renderer, browser, full suite, contract generation, pin, or release was run.
