# G5 retained CLI ports — flat design evidence

Status: draft-only; P1 GO is not claimed.

## Changed surface

Only these assigned test files changed:

- `tests/packs/timeline/test_cli_commit_move.py`
- `tests/packs/timeline/test_cli_commit_trim.py`
- `tests/packs/timeline/test_cli_native_sheet.py`
- `tests/packs/timeline/test_verbs_working_copy.py`

The port preserves the original behavior assertions for raw bodies, physical
working-copy state, shared/order/absence/null behavior, readback/reload,
idempotency/lost acknowledgements, undo/redo, no-write and security/refusal
checks. Retired native edit/apply and publication selector calls were changed
to the normal CLI fronts required by the plan. The working-copy conflict case
uses the existing real Runtime Checkout fixture and retains head/no-write and
force-refusal assertions.

The fake SDK fixture lacked the public history shape expected by the normal
front door. A test-only adapter exposes its already-existing accepted response
records as history; it does not change product code, create a private executor,
or invent a new auth/source pin.

## Verification

The exact required environment with Runtime pin
`/home/user/work/wt/rt-pin-9ce4242b` collected 87 tests. The exact bounded run
finished `80 passed, 7 failed in 42.79s`. Ruff, private mypy, and `git diff
--check` passed.

The seven failures identify integration work still owned outside this worker:

- Five cases use the settled `--commit <id>` contract, but the current CLI
  parser still exposes only numeric positional/`--steps` undo behavior.
- The fake redo scenario cannot reopen the second edit because it lacks the
  canonical publication pin that the normal history route requires.
- The retained detached-duration guard proves ordinary sheet apply still
  calls `_apply_parsed` for that route.

These failures were left as positive behavior tests. No skip/xfail/deletion or
success-to-refusal conversion was used. No full/browser/socket suite was run.

## Handoff

Sol should land the exact `undo/redo TL --commit <id>` parser and public method
route first. Then rerun this bounded 87-test set, repair the real canonical
history fixture/route as needed, and investigate the detached-duration normal
apply path before P1 qualification. No integration merge is recommended from
this draft alone.
