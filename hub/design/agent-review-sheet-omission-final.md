# AG03 final review — APPROVE bounded slice

**Candidate:** `tl/agt-m2-native-sheet-delete-http-case`
`021a375db53954f2056e65dce967c5b6d826668d`, tree
`2fc50570ba4e5bfc0980e248da93960106bdf4bd`.

**Decision:** APPROVE merging only `b24144d9759641980c0d072ddaa80373733d7308`
and `021a375db53954f2056e65dce967c5b6d826668d` onto Agent integration
`30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`. Read-only merge simulation is
clean: no conflict, and integration touched none of the affected paths since
common base `8130a401bf44a518d5a40ae274d398b8c560be55`.

The product delta is narrow and correct. A missing bound
`parent/clip:<id>` row emits the existing `capture_clip_delete`; the command
requires that exact parent identity and the executor consumes the complete
captured row, preserving opaque/order data in surviving rows. The retained
export bundle/basis is the source for preview, load, retry and rebase. Track,
occurrence, shot/nested, addition, rebinding, grammar and whole-writer paths
are not inferred and remain refused.

Central proof request
`agt-m2-native-sheet-delete-http-case-commit-integration-1020152736-25044`
passed **16 tests** in 51.61s on exact tree `2fc50570...`, including the
actual generated WorkspaceClient/Runtime HTTP omission regression, exact lost-
ack restart retry, reload, guarded undo/redo, disjoint rebase, and zero-write
membership/target-change negatives. Runtime source was
`81f8c7e0b22c34804015c054762af3d737e4698a` / tree
`0e3a5b938d9ca489fc760b09d34b02d4ac9aad51` (public013).

Local targeted row-delete command:

`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py tests/packs/timeline/test_cli_native_sheet.py -k 'omitted_native_clip_row or clip_row_omission or row_omission'`

Result: **4 passed, 60 deselected** in 2.16s.

AG03 is still **partial**. The detached legacy `apply_sheet` other-grammar
omission consumer remains (`astrid/sdk/timeline_sheet.py:849`, `:1109`), and
is intentionally outside this approved merge. Current integration `30fc8dd`
and public013 remain unchanged by this Agent-only scope.
