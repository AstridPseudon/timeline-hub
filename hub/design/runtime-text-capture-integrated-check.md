# Runtime text + capture integrated check

Date: 2026-10-20 UTC

## Verdict

The combined Runtime integration source is verified at commit
`a51267ec3dd94ea465a3161e3b4d8fbcd061009e`, tree
`964485ff5bd50cad835f30de95193e658d6cc46e`. It contains the approved capture
merge `27ad20bf45f7840c26dfefc69f32d52222abc33a` and independently approved
retained-text correction `e41f3d1e655a005904bbdc90f04b3ab825f4f225`.

No Runtime product, schema, client, artifact, pin, merge, publish, or shared
dependency change was made by this check.

## Source composition

- `runtime_protocol/capture_validation.py` SHA-256 is
  `572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75` in
  the combined tree, exactly matching approved capture `27ad20b` and source
  `0a04782e`. It is intentionally not the published-base `2c4ac180` bytes.
- The retained-text fixture functions `_freeze_text`, `_resolve_text_binding`,
  `_record_text_binding_event`, `_materialize_text_object`, and
  `set_project_shot_text_binding` in `tests/legacy_text_binding_fixture.py`
  have matching AST-source SHA-256 values against reviewed `e41f3d1e`.
- `runtime_protocol/service.py:create_timeline_view` is the documented S2
  view-method difference from the e41 review; its AST-source hash matches
  published `2c4ac180` exactly.
- A read-only path comparison against published `2c4ac180` found no changes in
  `contract/`, `packages/`, generated clients, schemas, artifact manifests,
  conformance, generators, or tooling. The published schema digest remains
  `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.

The complete Agent archive used by the marked capture suite is the persistent
exact archive at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m3-capture-actual-agent-current-pair/agent-source`

It is Agent `cf7448ed6c1298b172d004914cfe2bb8c99048e7`, tree
`c8a5e0cb320095129e9a1be125295dfa7adc2793`, as recorded by the persistent
`capture-agentcf7448-integration` suite. The four RenderRequest propagation
requirements and three SDK invocation guards remain open and are not relabeled
green here.

## Central service evidence

All three requests followed the current integration HEAD until start and ran
against Runtime tree `964485ff5bd50cad835f30de95193e658d6cc46e`.

### Text neighbors

Request:
`rt-m2-text-capture-integrated-check-restore-integration-1020120340-2592`

Exact service command:

```sh
request-test rt-m2-text-capture-integrated-check restore-integration --files "tests/test_timeline_text_selection.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py tests/test_shot_text_bindings.py tests/test_timeline_history_boundaries.py tests/test_timeline_commit_restore_port.py tests/test_timeline_commit_baseline.py tests/test_shot_composition_runtime.py tests/test_runtime_control2.py::test_backup_restore_and_structured_export_verify_cas_and_sqlite tests/test_doctor_timeout_reporting.py tests/test_restore_history_fixture.py"
```

Result: **233 passed, 1 deselected, 4 unchanged strict xfailed** in 116.78s;
exit 0. The four xfails retain the documented RT02 reason that the old
shot-bound writer is retired while the text-source seam restores the
capability.

### Capture controls on combined source

The already-qualified post-`27ad20b` 141- and 25-case selections were reused,
not duplicated. The combined-source request selected only the remaining
controls:

```sh
request-test rt-m2-text-capture-integrated-check capture-agentcf7448-integration --files "tests/test_capture_candidate_actual.py::test_original_working_copy_forgeries_refuse_before_writes tests/test_capture_candidate_binding.py::test_fresh_working_copy_semantic_forgeries_refuse_before_writes tests/test_capture_candidate_actual.py::test_working_copy_without_candidate_is_admitted_uncertified tests/test_capture_candidate_actual.py::test_forged_working_copy_certificate_refuses_before_writes tests/test_capture_candidate_binding.py::test_candidate_comparison_uses_detached_pure_inputs"
```

Request:
`rt-m2-text-capture-integrated-check-capture-agentcf7448-integration-1020120340-20503`

Result: **20 passed** in 16.56s; exit 0. This is 12 forgery cases, 2
candidate-less UNCERTIFIED cases, 4 forged-certificate controls, and 2
parameterized valid retained-candidate binding cases.

### Commit neighbors

```sh
request-test rt-m2-text-capture-integrated-check commit-integration --files "tests/test_timeline_commit_integration.py"
```

Request:
`rt-m2-text-capture-integrated-check-commit-integration-1020120340-24003`

Result: **9 passed** in 18.92s; exit 0. The named suite already contains the
same file, so the service command shows the explicit path twice; pytest
deduplicated collection and ran nine tests.

## Scope and limits

No broad or full suite was requested. RenderRequest/SDK3 remain open, and this
check does not qualify renderer execution, public consumer pin refresh,
Composition parity, browser journeys, or delivery artifacts.

