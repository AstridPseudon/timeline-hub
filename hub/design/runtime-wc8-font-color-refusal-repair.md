# WC8 font/color refusal-boundary repair

## Exact source

- Agent commit: `5ad4b7c26871c18ba01449a6d3c4d5bde6aa9a2b`
- Parent: `14356ee69c622cd636ab599d9df7f78380aca92f`
- Changed source: `tests/sdk/test_timeline_sheet_native.py` only
- Product identity: `astrid/sdk/timeline_sheet.py` is byte-identical to the
  source commit; no product guard or schema change was made.

## Repair

`append_param` now inserts a new parameter before an existing ` # ref ` suffix
and retains its legacy append behavior for the detached legacy text used by
the retained-draft test. The refusal test explicitly checks the boundary with
the existing `NativeSheet` row: the old append-after-binding form raises
`invalid sheet row binding`; the corrected form parses and retains the exact
original ref `occurrence:occ-1/clip:card`, then `NativeSheet.preview` raises
`unsupported parameter unknown`. The existing retained-draft assertion still
checks `SheetError`, unchanged draft bundle, unchanged outbox bytes, original
hold, and original text.

## Focused evidence

Environment for all commands:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH="$PWD:/home/user/work/runtime"
/home/user/work/venv-agent/bin/python
```

1. Font/color, combined, converted refusal, and quoted-clear controls:

```text
python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py -k 'detached_static_type_string_uses_retained_native_params_command or detached_combined_size_and_type_string_edit_preserves_literal_neighbors or detached_type_string_clear_uses_presence_aware_native_command or detached_mixed_edit_with_supported_font_is_staged or detached_mixed_edit_with_unknown_neighbor_is_not_staged or label_clear_is_distinct_from_empty_and_literal_clear'
```

Result: `21 passed, 48 deselected in 1.76s`.

2. Changed helper and direct text/size/duration neighbors:

```text
python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py -k 'detached_static_text_uses_retained_native_params_command or detached_static_size_uses_retained_native_params_command or detached_static_type_string_uses_retained_native_params_command or detached_combined_size_and_type_string_edit_preserves_literal_neighbors or detached_type_string_clear_uses_presence_aware_native_command or detached_mixed_text_and_duration_is_one_retained_native_batch or detached_mixed_edit_with_supported_font_is_staged or detached_mixed_edit_with_unknown_neighbor_is_not_staged'
```

Result: `12 passed, 57 deselected in 2.29s`.

3. Boundary probe output:

```text
old helper: invalid sheet row binding
corrected binding: 'occurrence:occ-1/clip:card' -> 'label'
corrected refusal: unsupported parameter unknown at occurrence:occ-1/clip:card; selected pack/opaque editing requires exact inputs
```

No HTTP/native actual/full/browser/render/install/schema/pin/generated run was
made. Existing font/color actual proof remains independent and was not
replayed.
