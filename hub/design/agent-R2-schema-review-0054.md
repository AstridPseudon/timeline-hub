# R2 canonical inverse schema review — FAIL (bounded floor scope)

Source: `tl/agt-R2-canonical-inverse-schema-0046`

- commit: `7689fd97b72d93061b50d3d85922b33a13703cd5`
- tree: `d8c893da393408852f4e4504c6b3117fb83109a4`
- schema: `astrid/core/timeline/schema/edit-command.schema.json`
- schema SHA256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`

The two-file delta is semantically correct: optional publication→nonempty
unique step-ID `args.steps`, omitted whole undo unchanged; provider retains
complete-key/unknown-ID validation. Direct validation passed (2 positive, 7
negative), inverse/provider targeted evidence passed 169 tests with one
pre-existing missing-`doc.patch`-fixture failure, Ruff and private mypy passed.

Review verdict is **FAIL only for the historical-floor gate**: parent current
union was 34 passed; candidate is 99 passed/3 failed at the three frozen-floor
equality assertions. The intentional schema addition means those old snapshots
no longer reconstruct and needs one-to-one updated source identity while
retaining old positives. Do not weaken, skip, or mark this unconditional PASS.
