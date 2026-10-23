# Handoff: ap2-P2-auto-return-review-1043

**Verdict: FAIL.** The first-return tree resolves the prior production-caller
metadata blocker and preserves the original automatic-placement journey, but it
is not ready for central qualification.

Blocking source findings:

- `assertFullV2Reply` requires `rebased_onto: expect.anything()` and then
  requires null for accepted replies. Playwright rejects null for
  `expect.anything()`, while C0 requires accepted `rebased_onto: null`.
- `isExpectedV2InverseRequest` conditionally copies required `label`, `steps`,
  `merge`, and `dry_run` only when present, so the exact wait predicate accepts
  a legacy-minimal inverse body. The later full-request assertion catches it,
  but the predicate itself is not the required exact v2 matcher.
- `undo_steps` checks are broad/vacuous (`typeof object` and
  `expect.objectContaining({})`) rather than proving the contract shape.
- Network legacy POST absence is asserted, but Runtime `/commits` is not scanned
  for old-route publications; the requested dual zero-old-route proof is
  incomplete.

Source controls passed: exact Playwright list (1), scoped ESLint, App and Node
TypeScript checks, private 819acf Composition resolution (`0.0.14`), diff check,
and EOF check. No browser/body/full/service run was performed. Full details and
line references are in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-auto-return-review-1043/report.md`
