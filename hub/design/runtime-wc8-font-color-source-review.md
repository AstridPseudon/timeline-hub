# WC8 retained font/color source safety review

## Verdict: HOLD

Reviewed Agent commit `5ad4b7c26871c18ba01449a6d3c4d5bde6aa9a2b` against
parent `14356ee69c622cd636ab599d9df7f78380aca92f`. The delta is exactly the
delegated two files:

```text
astrid/sdk/timeline_sheet.py
tests/sdk/test_timeline_sheet_native.py
```

The source boundary is otherwise sound. `_duration_sheet` uses one literal
field loop over exactly `size`, `font`, and `color` and checks each field
against the existing `element_schema("am-type")`. The declaration is in the
existing am-type manifest: `font` is a string enum `display|label`, `size` is
numeric, and `color` is a string. The existing `NativeSheet` exporter emits
JSON values and the existing parser retains raw `field=value` tokens while
parsing JSON values. The translator distinguishes presence from value,
preserves unquoted `field=clear` as a clear operation, and keeps quoted
`field="clear"` as a literal value. It requires an existing field on the
retained row, canonical `am-type`, and an existing binding; it does not add a
caller schema, recapture the head, add a snapshot diff, add fields, or
normalize the source bundle. The retained basis/bundle and stable owner/ref
are fed through the existing `NativeSheet.preview` and `clip.set-params`
capture path.

The source also refuses unknown fields, absent-to-present/present-to-absent
changes, malformed/invalid values, and mixed unsupported edits before
`_stage_sheet` writes pending intent. Existing local Main grammar remains
outside the retained session path, and the qualified size/text/duration
routes remain live. The unchanged opaque/null/order and reload/rebase/inverse
coverage remains present in the target test file.

## Concrete blocking counterexample

The converted refusal test does not exercise an unknown parameter. In
`tests/sdk/test_timeline_sheet_native.py:76-78`, `append_param` appends
`unknown=label` to the *end of the complete row*, after the existing
` # ref "..."` suffix. The call at line 292 therefore produces a malformed
binding such as:

```text
... # ref "occurrence:occ-1/clip:card" unknown=label
```

`NativeSheet._read` rejects that binding while JSON-decoding the suffix,
before `_duration_sheet` reaches its unknown-field semantic refusal. The test
still passes and asserts the bundle/outbox bytes are unchanged, but it proves
only malformed-row rejection, not the required equivalent unknown-neighbor
atomic refusal. This weakens the one-to-one conversion of the former
unsupported `font` case and leaves the requested unknown-parameter failure
surface unproven.

The refusal input must place `unknown=label` before the ` # ref` suffix (while
retaining the full bundle/outbox no-write assertions). No source change is
indicated by this review.

## Focused evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py -k \
  'detached_static_type_string_uses_retained_native_params_command or \
   detached_combined_size_and_type_string_edit_preserves_literal_neighbors or \
   detached_type_string_clear_uses_presence_aware_native_command or \
   detached_mixed_edit_with_supported_font_is_staged or \
   detached_mixed_edit_with_unknown_neighbor_is_not_staged or \
   label_clear_is_distinct_from_empty_and_literal_clear'
```

Result: **21 passed, 48 deselected in 1.75s**.

No HTTP/native/live-socket/full/browser/render/install run was made. The
author's reported 97-test pass was read as prior evidence and not replayed.
