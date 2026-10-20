# RT02 text retired-positive migration

## Result

The four Runtime endpoint positives remain separate strict-xfail refusal
controls.  They are not deleted, renamed, or changed to expect refusal as a
replacement behavior:

| Original Runtime assertion | Endpoint control | Native positive replacement in the reviewed private pair |
|---|---|---|
| `tests/test_shot_text_bindings.py::test_set_is_deterministic_project_scoped_and_replays` | The retired `set_project_shot_text_binding` endpoint still refuses. | `tests/editing_conformance/test_commit_runtime_text_binding.py::test_first_use_capture_projects_exact_text_and_retry` (including dry-run, accepted readback, exact UTF-8, retry, and integrity) |
| `tests/test_shot_text_bindings.py::test_set_rebind_and_event_order` | The retired set/rebind endpoint family still refuses. | `tests/editing_conformance/test_commit_runtime_text_binding.py::test_rebind_retains_v1_after_v2_restart_exact_inverse_and_redo`; event/presence and ordered clear/readback are covered by `::test_clear_removes_row_and_undo_restores_empty_exactly` and the recipe `tests/editing_conformance/test_recipe_text_binding_native.py::test_empty_clear_and_original_noncanonical_order` |
| `tests/test_shot_text_bindings.py::test_invalid_utf8_and_size_are_zero_write` | The retired endpoint remains a refusal path. | `tests/editing_conformance/test_commit_runtime_text_binding.py::test_exact_project_text_selection_refuses_before_writes[utf8]` and `[limit]` (the parameterized test also covers project, digest, size, MIME, and missing-object scope guards) |
| `tests/test_shot_text_bindings.py::test_identity_digest_is_sha256` | The retired endpoint remains a refusal path. | `tests/editing_conformance/test_recipe_text_binding_native.py::test_exact_capture_inverse_and_same_value_write` plus `tests/editing_conformance/test_commit_runtime_text_binding.py::test_first_use_capture_projects_exact_text_and_retry` (exact digest/media pin, projected content hash, bytes, and accepted document readback) |

The original names and assertions remain discoverable in the Runtime refusal
file.  The positive assertions run through the real `text-binding.set`
command, not the retired endpoint and not a fake provider.

## Required semantic coverage

The same private pair also covers the requirements that must accompany the
four replacements:

- Empty UTF-8 is present, not clear: `test_first_birth_undo_restores_absence`
  proves first-birth inverse returns to absence, while
  `test_clear_removes_row_and_undo_restores_empty_exactly` proves explicit
  clear removes the live row and inverse restores a present zero-byte row.
- Authentic retained legacy MIME is exercised by
  `test_rebind_existing_main_descriptor_undo_is_exact` and
  `test_clear_existing_main_descriptor_and_inverse_are_exact`.  Both restore
  the genuine main film's `text/plain` descriptor/bytes/order after restart;
  both were executed as positives with `--runxfail` in the private pair.  The
  strict markers remain in the archived source and must not be promoted or
  removed here.
- `test_clear_removes_row_and_undo_restores_empty_exactly` and
  `test_retained_v1_after_v2_clear_restart_group_inverse_is_exact` preserve
  historical readback, presence events, restart/retry, accepted inverse, and
  Runtime integrity checks.

## Exact private source and evidence

The pair was already qualified without changing this Runtime worktree:

- Runtime S2 base: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Agent source/test base: `9bf654387c8c1aaa2bc3ef74210fa4a6825956ad`.
- Native Agent provenance: `cb1e907c6846341997e50d7f51aed65a84b6c335`.
- Private generated contract: version `0.2.14`, schema
  `sha256:ab8b5dba56f777b935518f2fdaf348e10813224b9aa8cabb2a8b2c1905a3885c`.
- Native test source archive:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/agent-source`.
- Runtime private generated archive:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-text-clear-native-private-pair/runtime-candidate`.
- Qualification report: `design/runtime-text-native-private-pair.md` and
  `workers/rt-m2-text-clear-native-private-pair/notes/report.md`.

The central private-pair command ran exactly the two existing native files
with `--runxfail` and reported **46 passed**.  Its Runtime neighbor lane
reported **199 passed**.  No public 0.2.13 schema, generated client, release,
pin, endpoint, DTO, table, or Agent product/test file was changed.

The current Runtime tree's bounded controls were also run centrally:

```text
pytest -q tests/test_shot_text_bindings.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_legacy_custody.py tests/test_timeline_text_selection.py
69 passed, 4 xfailed in 24.52s
```

Result: the private positive pair is proven, but RT02 is not marked
`DELETED` or merge-ready.  The four endpoint controls stay open until the
owner-approved full schema union, fresh authorized public release, and real
consumer qualification promote the native command onto the public tuple.
