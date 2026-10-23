# R2 nested emission — independent Luna review 1617

**Verdict: FAIL / not landable.** Candidate `6aec04e8b` preserves the exact
captured nested positive but has a legacy redo regression and accepts forged
nested stage identity metadata. No product files were changed.

The focused captured test passed **11/11**, including one outward `undo-0` /
`[0]` identity with internal native/effect partitions `[0,2]`/`[0,4]` and
`[2,3]`/`[4,9]`, exact source history and physical bindings, current attribution,
and refusal/no-write checks for gap/overlap/foreign publication/owner/source
digest/source scope/tampered effects. Source review found no fabricated accepted
edge, retarget, root copy, history injection, or competing-media guard waiver.

The bounded original tests yielded **34 passed, 2 failed**:

- `test_one_of_ten_notes_preserves_other_steps_and_redoes_exactly`
- `test_semantic_creation_reversal_preserves_unselected_root_and_redoes`

Both crash at `_step_undo.py:152` with `KeyError: 'effect_range'` because valid
existing `inverse.stage` records may have a native range without an effect range.
This is an unintended compatibility regression.

An exact-capture mutation probe also **accepted** forged nested
`boundary.step_id` and `boundary.command_ordinals` (two stages returned), while
missing-stage and extra-range mutations refused. `_step_undo.py:149-161` checks
publication/range contiguity but not the accepted step/ordinal identity. This
violates the required wrong-step/ordinal refusal.

Static checks: Ruff `2149/2149`, mypy `1912/1912`, scoped mypy clean, vendor and
artifact checks PASS, diff check PASS. Authored causal counts are baseline
**7 FAIL/4 PASS** and slices-only **1 FAIL/10 PASS**; not rerun here. The
lossless packet SHA-256 is
`3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`; emission
SHA-256 is `0d8ea4eded46ff7b0e9a0eef6e58a248eb0511ad98d4bbb0dc9def62c4138174`.
Candidate source hashes: `_commit_patch.py`
`06e35825df4f6578ef192de92ab27dbc5131484d99c4953f001293f9bad9490c`,
`_root_inverse.py`
`0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`,
`_step_undo.py`
`6cedff390a06ff74a957b962199efb4144b82e2e7e48664269098f39fbae8915`,
`inverse.py`
`4e00ec2e1c629af6d0fa84a4b6f8992b0990b38460561849cb0bb11c70921325`, and
focused test
`36e2ea620e558e7516ccf93e0090c65d4f3fa85a3487ecc4c0d001a741b20fa4`.

No Runtime/public acceptance or full suite was run. Recommended next step is to
repair both findings, rerun the focused and bounded original tests, then obtain
the separate Runtime review before joint acceptance.
