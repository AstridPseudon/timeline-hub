# P1 anchor/operand audit review — 2026-10-23

## Result

**FAIL for the preceding audit handoff as written; PASS for its narrower
source-binding conclusion.**

The original `recipe_m2_scalar_disjoint.json` provenance and P1 conversion are
sound. The source fixture first appears in `84db8bde`, retains SHA-256
`0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866` through
exact base `1a0ea1a40`, and contains no transcript/word/pin/binding object.
Both shared placements point at `s/sr/main/ir` and have empty `item_id_map`.
The four canonical P1 copies are byte-identical to their source recipes and
retain `app.astrid.on="old-anchor"`, `app.astrid.until="end"`, and
`app.on=null` in every relevant input/output/head/rebased child image.

The prior handoff's stronger claim is incorrect: the M1 baseline clip is not
byte-for-byte equal to the M2 scalar child because M1 has no `params` key while
M2 has `old`, `opaque`, `x`, and `y` params. Only the non-parameter fields
match. Correct this provenance wording; do not use it as evidence of full clip
identity.

The source recipe retains scalar golden, inverse, and disjoint replay
assertions. The P1 source/provider expectations retain the four parameter,
opaque/null, shared-child, and disjoint outcomes, but the required filtered
request test is only one source-side pass (1 passed, 11 deselected), not four
provider passes. No provider matrix was rerun in this audit.

Under approved C0, final-candidate timing validation is mandatory and no
unchanged-unresolved-legacy exemption is written. The current timing adapter
has no authentic source binding for these child declarations. Consequently,
the four original child positives cannot be certified as accepted/merged under
current C0 without either authentic bindings or an explicit narrow policy
clarification. No transcript was invented, declaration removed, validator
bypassed, positive changed to refusal, or policy changed.

## Orchestrator scope question

Should unchanged unresolved legacy child timing declarations survive an
unrelated `doc.patch`? A yes answer requires a narrowly scoped C0 policy
clarification before counting these four positives; a no answer leaves them as
source preservation witnesses, not provider-success evidence. Do not alter the
fixture or validator as part of this audit.

## Unproven boundaries

The Agent production caller is visible, but App mount and Runtime HTTP H3 are
unproven. Full C0 ABI-1 request/reply scope—base/publication, commands, label,
steps and authoritative dependencies, `fields|atomic`, reads, dry-run,
idempotency, accepted/merged/conflict/invalid/preview/history envelopes—also
remains unproven. No H3 or P4 completion is claimed.

## Checks

`git diff --exit-code` PASS; `git diff --check` PASS; Ruff PASS; mypy PASS;
the required request test PASS (`1 passed, 11 deselected`, one existing
unknown-`timeout` warning). The worktree command checks ran on descendant
`956e633d`; exact-base source/provenance evidence was read from `1a0ea1a40`.

