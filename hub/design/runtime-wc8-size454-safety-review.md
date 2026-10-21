# WC8 retained size safety review

## Verdict: APPROVE

Reviewed Agent commit `4542b759c7cdc9074260d8f6d0f193a7147f72a1` against its
parent/current-base ancestor `45729a6be200e48fbe6d92d5be58d09dd3dd3dca`.
The current `tl/integration` head is `7c9ef2ed5e70da1a13e89278496c74321453955a`,
which contains that base ancestor; this review is intentionally bounded to the
candidate's own two-file delta.
The delta is exactly two files: `astrid/sdk/timeline_sheet.py` and
`tests/sdk/test_timeline_sheet_native.py`.

The size path is bounded to the existing retained author-time route:

`rendered detached row -> retained artifact/binding -> _stage_sheet ->
_duration_sheet -> NativeSheet.preview -> capture_clip_set_params`.

`_duration_sheet` requires an existing size cell, canonical `am-type`, and
the existing `size` declaration from `element_schema("am-type")`. That
declaration resolves to the current `astrid_motion` `element.yaml`, whose
`size` property is numeric and strictly positive. The retained bundle and
publication basis remain the originals; no snapshot diff, caller-owned
schema, false owner, submit-time recapture, or side channel was added.

Presence and value are separate: an existing `size` cell is required for
this edit, while unquoted `size=clear` is translated to the existing clear
list. Quoted `size="clear"`, `null`, invalid strings, negative values, and
booleans refuse through the existing native declared-schema validation before
outbox staging. Direct checks confirmed the outbox bytes and draft remain
unchanged for those refusals.

Original guards, opaque siblings, null/absent fields, and parameter order are
preserved by capture against the retained bundle. The focused size coverage
checks JSON reload, disjoint rebase, inverse, and sibling isolation. A direct
same-leaf check produced `CommitConflict` with the size draft and pending
command retained. The mixed refusal fixture correctly changed from a now-
supported size-only edit to `size=33 font=label`; it still asserts exact
checkout and outbox preservation, so no behavior assertion was weakened.

No concrete counterexample found. Existing local-only grammar and prior
text/duration/mixed behavior remain live. This review did not run HTTP,
browser, renderer, native, install, or full suites, as required.
