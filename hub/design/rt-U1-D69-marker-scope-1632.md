## U1-D69 report

Read-only assessment completed on `bc227de07262accb702eae8a44c4a666b568c08e`. No tests, production files, markers, or ledgers were modified. Worktree is clean.

### Finding 1: second-client citation

Current test:

- `tests/test_second_client_e2e.py:62-63`
- Test body hash: `0176b958ff6aa431b374ba1f99923b5cc0f6a88ed99c805c4bfe4b380b811734`
- Upstream body hash is identical.
- Current file SHA: `d6622166efc97391f37c34836ebc1c011f47c48c64172df3a550259cd6860561`

The actor executes project-catalog create/read operations before failing:

1. `createProjectShot` — RK02 KEEP, not RT02.
2. `createProjectReference` — project catalog KEEP.
3. Reads both resources.
4. Evaluates all 11 predicates at `conformance/fake-second-product.ts:63`.

Static source proves the failure occurs before D04:

- `create_project_shot`: `runtime_protocol/service.py:2804-2833`, hash `9e3d3b410ec1ac3b7a82c77ba2b60c7d7ce397b10aa91fafdf473134c878063c`
- Catalog resource shape: `_project_shot_resource:2788-2794`, hash `40eee6754b7e6dfc37ef67c7614692d99e8fa9fb1325024a3b694913d304da12`
- The catalog table has no `revision_id` or `internal_timeline_revision_id`.
- Actor lines 61–63 therefore throw on the two old timeline-projection fields before `publishParentComposition` at line 80.

Thus the current whole-test xfail masks the live catalog assertion and all later actor execution. D04 remains valid as a ledger decision, but it is not the failure reached by this test. The prior “createProjectShot is RT02” citation is incorrect.

Retained live replacements include:

- `tests/test_runtime_e2e.py::test_project_shot_crud_isolated_idempotent_and_restart_durable`, lines 222–264, body SHA `076eee400e631339e7b9dfb555c5985328b3742f6095838f4a7c624948c16f95`
- `tests/test_runtime_e2e.py::test_project_reference_crud_isolated_idempotent_and_restart_durable`, lines 185–217, body SHA `363f352dac298e9ca35e2b9b0250e23245b2f8cd3719050576ab82424185314d`
- `tests/test_project_reference_catalog.py::test_catalog_before_any_timeline_is_scoped_ordered_and_restart_durable`, lines 21–91, body SHA `f85c9b18b44e226e76f6263d579491ea4ba34369439a346ab3a009d134f60124`
- Service/HTTP catalog retry tests in `test_timeline_reference_authority.py`.

### Finding 2: exact idempotency citation

Current test:

- `tests/test_runtime_exact_idempotency.py:81-82`
- Current body hash: `bf6b4e8b9bed87de4c50e6f32a29ad59b575c4c3b20799c0f386822325d15a39`
- Upstream body hash: `d02389dd7580187f9be86fc3b7fa90a0f883e1911a2ffc5291a6fed2b3a7895e`
- Current file SHA: `cc9549c86a3793d9977f2adf0f97c3db8668e095470ce23c6166a02f1dfae4f5`

The first direct timeline-shot call is retired:

- `create_shot` aliases `_refuse_direct_shot_write` at `runtime_protocol/service.py:2987`
- Refusal body is `:464-465`, hash `93e789644d460632fb40b47f6198720c22c497c668f9ea782a9011aa7e0c6d7e`
- Timeline reference creation is RT03 via `create_reference:3848-3849`, hash `a6e5df22a8c683d10d2ef708852596458913baae62e8568e14a6b0c4f7dbe903`

The current reason is wrong in two ways:

- The timeline reference is RT03, not RK01 project catalog.
- The project catalog reference is a separate unmarked test at lines 49–78.

The xfail body reaches the malformed-shot probe, then the first retired shot route; it never reaches the timeline-reference call, restart replay, changed-key conflicts, different-key overwrite checks, or SQL no-overwrite assertions at lines 107–122. Statically, the malformed-shot assertion expects 400 while the retired route returns 410; because the decorator restricts expected exceptions to `ApiError`, the following status assertion may produce an ordinary assertion failure rather than a valid xfail. No live HTTP run was performed.

### Minimal reviewable proposal

1. For the second-client journey, remove the blanket whole-test xfail in a follow-up patch and retain every live catalog assertion strictly.
2. Keep the nine genuine catalog/timeline identity predicates at actor line 63.
3. Move the two `revision_id` predicates to the approved commit replacement, where canonical closure supplies shot/internal-timeline revisions; do not require them from RK02 catalog creation.
4. Retire or replace only the old `publishParentComposition` save segment under D04/D52. Do not restore the rejected writer. The approved replacement route is the existing `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit`.
5. For the idempotency test, classify the positive timeline-shot half as RT02 and the positive timeline-reference half as RT03. Dispose of those retired-only positive save assertions under D52 or replace them with the existing explicit refusal/no-write tests. Preserve the live project-catalog create/read/update/restart/idempotency/no-overwrite coverage.

The production route map is already coherent:

- Catalog create: `runtime_protocol/server.py:850-854`
- Catalog read/update: `runtime_protocol/server.py:782-822`
- Retired timeline save stubs call `_require_timeline_command`, whose replacement is the commit route at `runtime_protocol/service.py:1653-1660`.
- Commit routing is `runtime_protocol/server.py:294-319` and `:522-523`.

The v2 replacement must retain the settled contract: `api_version`, project/timeline, exact base pair, commands, label, step patches/reads, merge, declared reads, source, dry-run, and idempotency; accepted/merged canonical/full receipt, records, dependencies, bindings, effects, history, actor, and undo; preview `would_status` with null receipt; conflict/invalid code, path, hint, head, and suggested command. Optional `recorder_abi` 1|2 and the D62 gap remain unchanged. No new contract decision is needed.

### Acceptance commands

Not run because this task explicitly prohibited live HTTP/browser execution:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -m pytest -q \
  tests/test_second_client_e2e.py::test_second_client_core_journey_is_executable \
  tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting
```

Recommended replacement acceptance:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -m pytest -q \
  tests/test_runtime_e2e.py::test_project_shot_crud_isolated_idempotent_and_restart_durable \
  tests/test_runtime_e2e.py::test_project_reference_crud_isolated_idempotent_and_restart_durable \
  tests/test_project_reference_catalog.py::test_catalog_before_any_timeline_is_scoped_ordered_and_restart_durable
```

Existing prior D69 evidence: policy comparator `24 passed`; joined skip suite `28 passed, 1 failed` on the unrelated known `no_ci` checker issue.

Commit message and `DONE` marker were written.