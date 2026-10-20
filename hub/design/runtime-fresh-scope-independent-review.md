# Runtime fresh-bootstrap scope independent review — APPROVE

## Verdict

**APPROVE** the exact source identified by commit `70102ac966b9d2cc5b9c52afa010a67e435dfb6e` and tree `708df14c75ef739a2c6130ca39f9e67b2758a571`, compared with merged `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`.

This is the requested narrow qualified corrupt-state fix. It is not a new normal-API exploit finding or an M1 blocker. The orphan `timeline:<id>` document setup is explicitly injected corrupt state, as settled by the plan and owner classification.

## Source review

- `git rev-parse 70102ac^{tree}` equals `708df14c` exactly.
- `70102ac` is based on `129493b2`; its source diff against `b748` is only:
  - two product lines in `runtime_protocol/service.py`;
  - the new `tests/test_timeline_fresh_bootstrap_scope.py`.
- The guard is after exact create replay and existing-row adoption (`service.py:1671-1675`), and immediately before the first fresh timeline insert (`service.py:1676-1679`). It is gated on a registered timeline commit provider, so no-provider Main creation is unchanged.
- It reuses the existing project-scoped `timeline_scope_is_empty` helper and existing typed `ConflictError` refusal with reason `headless_content_not_empty`; no new error/API/schema/table/DTO/writer was introduced.
- The helper's strict JSON reader rejects duplicate/non-finite/corrupt legacy JSON as non-empty for this preflight, while valid genuinely empty shapes remain empty. The preflight only reads the retained `timeline:<id>` bytes; it does not rewrite or delete them.
- The helper query is project-scoped. Same-project orphan content blocks fresh provider-backed bootstrap; foreign-project documents, unrelated catalog documents, and unrelated media do not block it.

The exact diff over `b748` leaves the approved ff9 shell repair and existing capture/text/render guards and current published artifacts untouched. Representative byte checks show `runtime_protocol/timeline_commit_store.py`, `runtime_protocol/capture_validation.py`, `contract/openapi/workspace-v1.yaml`, and the generated Python/TypeScript clients unchanged from `b748`.

## Evidence reviewed

- Recorded targeted lane: **124 passed**.
- Recorded audit/original-probe lane: **13 passed, 1 deselected**.
- Recorded central bounded lane: **14 passed, 7 deselected** — nine original commit cases, four absent/null-head repair cases, and the real-provider fresh-bootstrap case.
- Recorded regression discrimination against verified ff9: the two retained plain/duplicate orphan negatives both failed with `DID NOT RAISE ConflictError`, as expected for the pre-fix source.
- Independent private-overlay run against the exact `70102ac` archive:

  ```text
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m 'not integration' \
    tests/test_timeline_fresh_bootstrap_scope.py \
    tests/test_timeline_empty_shell_repair.py::test_duplicate_legacy_json_is_refused_before_missing_head_bootstrap \
    tests/test_timeline_empty_shell_repair.py::test_distinct_empty_legacy_json_still_repairs_missing_head \
    tests/test_timeline_headless_overwrite_refused.py::test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched \
    tests/test_timeline_headless_overwrite_refused.py::test_genuinely_empty_headless_timeline_still_accepts_expected_head_null
  ```

  Result: **21 passed, 1 deselected in 24.92s**.

The recorded refusal tests compare the complete SQL dump, CAS/staging trees, raw document bytes, and SQLite `total_changes` across repeated attempts. Positive authority is created through Runtime APIs; SQL is used only to inject the explicitly labeled corrupt orphan setup.

## Limits and next steps

No full suite, schema generation, browser/App journey, pin, merge, publication, or product edit was performed by this review. Those omissions are within the task boundary. The implementation evidence is sufficient for this exact source approval; integration/publication remains orchestrator-controlled.

