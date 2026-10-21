# WC8 retained font/color refusal delta review

## Verdict

**SOURCE APPROVE** for Agent `fd90a99575d795869faa6cbc5573613783c79664`,
bounded to the corrected refusal-test delta against
`5ad4b7c26871c18ba01449a6d3c4d5bde6aa9a2b`.

This closes the exact finding in `runtime-wc8-font-color-source-review.md`.
The delta is test-only: `tests/sdk/test_timeline_sheet_native.py` changes
the helper and strengthens the refusal assertions.
`astrid/sdk/timeline_sheet.py` is byte-identical between `5ad4b7c` and
`fd90a9957`; no product, schema, generated client, pin, or source behavior
changed.

## Finding closure

- `append_param` inserts `unknown=label` before the ` # ref ` suffix,
  while retaining its legacy append behavior for detached text without that
  suffix.
- The old append-after-suffix form is separately shown to raise
  `invalid sheet row binding`.
- The corrected form parses, retains the exact original binding
  `occurrence:occ-1/clip:card`, and retains `unknown=label` as a row
  parameter.
- `NativeSheet.preview` then reaches and raises the intended semantic guard:
  `unsupported parameter unknown`; the negative is not satisfied by setup
  parse failure.
- The actual `apply_sheet` refusal retains the draft bundle and outbox bytes,
  and leaves the original hold/text unchanged.
- The supported-font counterpart remains present and stages its retained
  native batch.
- No `skip`/`xfail` marker was introduced, and prior assertions were not
  removed; the delta is 17 insertions and 2 deletions in the test file only.

## Evidence

Directly rerun on the exact `fd90a9957` worktree with
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH="$PWD:/home/user/work/runtime"`,
and `/home/user/work/venv-agent/bin/python`:

```text
python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py -k 'detached_static_type_string_uses_retained_native_params_command or detached_combined_size_and_type_string_edit_preserves_literal_neighbors or detached_type_string_clear_uses_presence_aware_native_command or detached_mixed_edit_with_supported_font_is_staged or detached_mixed_edit_with_unknown_neighbor_is_not_staged or label_clear_is_distinct_from_empty_and_literal_clear'
21 passed, 48 deselected in 2.27s

python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py -k 'detached_static_text_uses_retained_native_params_command or detached_static_size_uses_retained_native_params_command or detached_static_type_string_uses_retained_native_params_command or detached_combined_size_and_type_string_edit_preserves_literal_neighbors or detached_type_string_clear_uses_presence_aware_native_command or detached_mixed_text_and_duration_is_one_retained_native_batch or detached_mixed_edit_with_supported_font_is_staged or detached_mixed_edit_with_unknown_neighbor_is_not_staged'
12 passed, 57 deselected in 2.19s
```

The author's preceding repair evidence is reused: the same corrected
helper/refusal lane reported 21 passed and the direct changed-neighbor lane
reported 12 passed. The original source review's broader findings and the
retained font/color source identity remain unchanged.

The actual one-case HTTP evidence remains the result recorded in
`runtime-wc8-font-color-http-proof.md`: one `/v1`
`clip.set-params` case passed on the identical product source
(`5ad4b7c`), with the test-only `fd90` delta not involved. This review does
**not** claim that HTTP case as a new run.

No all-97 rerun, full suite, native/live HTTP, browser, render, install,
schema, or pin test was run for this delta review.
