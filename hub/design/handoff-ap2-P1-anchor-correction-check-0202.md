# P1 anchor correction check — 2026-10-23

## Result

**PASS.** The corrected handoff precisely narrows the failed M1 identity
assertion: M1’s baseline clip and the M2 scalar child match in all
non-parameter fields (`app`, `at`, `from`, `id`, `speed`, `to`, and `track`).
They are not byte-identical. M1 has no `params` key; M2 has `params` with
`old`, `opaque`, `x`, and `y`.

## Exact source fact

Direct inspection of
`tests/editing_conformance/fixtures/recipe_m1_move.json` and
`recipe_m2_scalar_disjoint.json` confirms that M2’s complete
`source_mapping.shots` has two placement-local keys:

- `shot-placement-365d0383838d687737f499dfcdc96e880baaf8d4747ecf5f657993be89d8522b`
- `shot-placement-d39cbabf00e35d7c1a02a08ae75329c7b3e7435708397a263835e72a0544b06d`

Each value points to `shot_id: s`, `revision_id: sr`,
`internal_timeline_id: main`, and `internal_timeline_revision_id: ir`, with
an empty `item_id_map: {}`. The fixture has no transcript, word, pin, or
authentic timing-binding object.

## Retained boundaries

The no-authentic-binding finding and policy escalation stand. Under C0,
unchanged unresolved legacy timing declarations are not automatically
permitted by an unrelated `doc.patch`; preserving the original source
positives requires a narrow policy clarification. This check makes no
provider4PASS or H3 claim. Whether the production caller uses the path and
whether full v2 requests/replies work remain outside this correction.

## Verification

- `git diff --exit-code` — PASS (exit 0)
- `git diff --check` — PASS (exit 0)
- Reused independent evidence: Ruff PASS, mypy PASS, and filtered request
  test PASS (`1 passed, 11 deselected`; existing unknown-`timeout` warning).
- No new product/test/fixture/generated/pin/lock/launcher changes; no broad
  audit or unchanged test matrix was run.
