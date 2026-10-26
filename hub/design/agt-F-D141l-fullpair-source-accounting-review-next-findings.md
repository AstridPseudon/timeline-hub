# D141l source-accounting independent review

Verdict: `PASS_EVIDENCE` for source/accounting only; product acceptance is `INCOMPLETE`.

- Terminals: cut `24814` XML `6710f7fe1b4b1a0b4d43614f0fe58d437b0b6fff76990e4a717022cef773fcd5`; pristine `25513` XML `9d36fcecf662cc9138cd30cb6ad674a57db30209b18593f29da08ed961792bba`.
- Fresh accounting: `9561 = 9388 + 173`, `3255 = 3082 + 173`, cut bad `397 = 201 FAIL + 196 ERROR`; membership `3018 matched`, `6370 cut-only`, `64 pristine-only`; `19 FAILS_BOTH` retained.
- Five cut-only identities: pristine exact function `0`, current exact function `1`, D63 renamed-body exact match `0`; actual five cut `FAIL`s remain accounted as source-backed `N_A`, never PASS/REG/deduction.
- All 64 pristine-only IDs map to inverse `38`, CLI/publish/native create `18`, schema/installer `8`. Nine have current XML parameter/path-display counterparts, all PASS (`6` schema/installer, `3` CLI); no approved migration/retirement or exact pristine selector result exists, so all remain unresolved. The other `55` have no current XML counterpart; `38` have no current source file and `17` have a current file without exact function identity.
- Behavior proven: `0`; unresolved: `64`; no `REG0` or complete product acceptance.
