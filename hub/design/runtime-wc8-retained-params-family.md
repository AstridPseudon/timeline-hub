# Runtime WC8 retained parameter-cell family

## Implementation

The Agent retained-sheet path now uses the already published ordinary
NativeSheet/`clip.set-params` carrier for existing literal parameter cells.
`NativeSheet.preview` permits changes to existing opaque JSON values because
the live provider validates known changed properties and preserves unknown
ordinary JSON values. It still refuses selected-pack parameters, formula-bound
parameters, expression tokens, added parameter cells, timing/source clauses,
and structural edits.

`_duration_sheet` no longer hard-codes only `size`, `font`, and `color`; it
translates the union of existing before/after parameter keys in one loop and
lets NativeSheet/provider validation decide known declarations. Text and static
duration handling, author-time bundle/basis preservation, and explicit clear
semantics remain unchanged.

## Source/caller evidence

- Main carrier: `astrid/sdk/timeline_sheet.py:780-837`.
- Retained translation: `astrid/sdk/timeline_sheet.py:908-1010`.
- Provider policy: `astrid/sdk/timeline/_scalar_commands.py:68-145`.
- Live detached caller: `astrid/sdk/timeline/checkout.py:564-601`.

## Behavior proof

Existing tests cover size, font, color, text, duration, reload, inverse,
stale/disjoint guards, basis retention, and no-write refusal. The changed
existing native test adds one parameterized presence-aware roundtrip covering
set-null, clear-null, clear-value, and rename, plus an opaque object/array
roundtrip. The opaque test also keeps a refusal for an expression token and a
new unknown cell.

Known declaration validation remains exact. In particular, `color=null`
continues to refuse under the existing string declaration; null success is
proved only for an existing opaque key accepted by the ordinary provider.
There is no synthetic support for absent cells, aliases, selected-pack
parameters, or unrepresentable grammar.

## Verification

Targeted direct and neighboring tests: 180 passed in 20.36s. The direct
changed tests: 5 passed. `git diff --check` passed. Full, HTTP/native actual, browser,
render, install, and independent data-safety review were not run.
