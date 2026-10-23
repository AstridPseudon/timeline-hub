# G4 final join review: SOURCE PASS / WIRE FAIL

Reviewed exact join `tl/agt-G4-reviewed-current-join` at
`5243eca7354db667eaa33ac69c725ddb33147d15` with no product edits.

## Findings

### SOURCE: PASS

- `astrid/sdk/timeline/publish.py:168-270` routes fresh narration binding
  through `TimelineSession.submit`, using native `text-binding.set` commands,
  `label`, per-command steps, `merge="fields"`, and `reads=[]`. It imports
  exact UTF-8 bytes, checks Runtime media identity, preserves occurrence
  ownership, and retries a persisted flight with its original key/body.
- `astrid/sdk/timeline_elements.py:290-315` routes fresh update-element
  batches through the same `TimelineSession.submit` engine with the v2 label,
  semantic step, merge mode, frozen base and idempotency key. Existing pending
  or flight state stays on the exact persisted `flush` retry path; native
  capture remains authoritative for schema/source inputs, opaque fields and
  compiler mirrors.
- `astrid/sdk/timeline/sync.py:421-528` constructs the scoped base pair,
  commands, label/steps, optional reads, merge mode and dry-run request,
  freezes the idempotency key/body, and returns Runtime `{data, receipt}`
  acknowledgement data. No caller-side metadata-dropping workaround is used.
- Source behavior and conformance evidence passed: schema/source/opaque,
  no-write, inverse and retry assertions remain green in the targeted lanes
  below. The excluded remote create_empty/media/render writers were not
  inspected as acceptance claims.

### WIRE: FAIL (Runtime contract mismatch, not an Agent source failure)

- Exact Runtime text-binding acceptance against `rt-pin-95bd3c5f` ran
  `9 passed, 12 failed`. The first failure trace is Runtime
  `runtime_protocol/timeline_commit_validation.py:97`: `PreparedCommit.records`
  rejects additional properties `label`, `merge_mode`, and `steps`; it
  propagates through `timeline_commit_store.py:598/726` as
  `invalid_prepared` / `validation_error`. This is the original Runtime-side
  v2 response-schema rejection. The Agent source correctly emits the required
  fields; omitting them would violate commit-v2 and was not done.
- Central socket-backed `wc6-exact95-http-env-qualification-integration`
  failed before the test assertion at `AstridClient.open`: the Runtime health
  digest was `sha256:7d4afa...`, while the joined Agent client expected
  `sha256:55abcf...`. This is a separate environment/schema tuple preflight
  failure, not evidence against the caller source.

## Exact checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G4-current-join-review-0045-tests tests/sdk/test_timeline_narration_commit.py tests/core/test_timeline_element_publication.py tests/sdk/test_timeline_open_commit.py tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_requests.py`
  → `144 passed`.
- `PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/timeline/test_timeline_elements_catalog.py tests/sdk/test_timeline_commit_provider.py`
  → `114 passed`.
- `PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py tests/test_canonical_aliases.py tests/v10/test_domain_cli_projects_timelines.py`
  → `170 passed, 1 skipped, 46 subtests passed` (existing skip; no test was changed).
- Narration/original-positive lane from the prior review command, with joined
  source and normal Runtime import:
  `env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/runtime" PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_narration_commit.py tests/sdk/test_timeline_checkout.py::test_narration_comes_from_the_lines_and_is_re_pinned_only_when_it_changes tests/sdk/test_timeline_checkout.py::test_narration_cas_conflict_is_not_retried_at_actual_head tests/sdk/test_timeline_restructure.py::test_pin_narration_adopts_a_binding_the_document_lost tests/sdk/test_timeline_restructure.py::test_pin_narration_does_not_adopt_a_different_text_and_reports_the_conflict tests/editing_conformance/test_recipe_text_binding_native.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/sdk/test_shot_text_bindings.py`
  → `59 passed`.
- Exact Runtime acceptance command:
  `env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f /home/user/work/venv-agent/bin/python -P -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_text_binding.py`
  → `9 passed, 12 failed`; all failures are the Runtime prepared-schema rejection described above.
- Central service request:
  `R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-G4-current-join-review-0045 wc6-exact95-http-env-qualification-integration) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"`
  → failed before assertions on the health schema-digest mismatch described above.
- `PY=/home/user/work/venv-agent/bin/python make ruff`
  → `current=2150 baseline=2150`, pass.
- `PY=/tmp/astrid-u2-typecheck/bin/python make mypy`
  → `current=1915 baseline=1915`, pass.

No full, browser, render, shared-dependency, schema, or product-file writes
were performed. No tests were weakened or marked newly.

## Recommendation

Runtime must adopt the approved commit-v2 request/reply schema and refresh the
Agent/Runtime contract tuple so the exact text-binding acceptance and central
socket journey can be rerun. The Agent source is ready for that wire rerun;
this review does not claim end-to-end wire acceptance until then.
