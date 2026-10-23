# Agent V2 D12 review — FAIL

Reviewed `266e8eac6faeda5d6502926894395c2ccd818564` over
`e24f91385434f7702747eeffc051f1ce6cf44056` under ruling D12
(`2026-10-23T03:23:52Z`).

## Verdict

FAIL: `_legacy_exemptions()` in
`astrid/sdk/timeline/_commit_timing_validation.py:100-118` recognizes only
same declaration/value/reference basis, not baseline unresolvability. The
evaluator then suppresses every matching `on`/`until` at
`_timing_evaluators.py:506-509`.

An independent production-adapter probe with a valid unchanged legacy child
declaration (`cut: c1`, `on: c1`) passed both baseline/no-baseline validation,
but changed the derived start from `29029/30000` to `1` when the baseline was supplied;
the supplied-baseline run recorded the declaration as exempt. This violates the
settled D12 boundary and needs an owning-worker correction plus a regression.

## Evidence

The required focused lane passed **95 tests**; P1 provider collected **21 tests**
(17 original plus 4 added D12 cases). Scoped Ruff, private mypy, no-growth Ruff
(`2151=2151`), no-growth mypy (`1915=1915`), structure/cycles (0 new), and
`git diff --check` all passed. No product edits were made by this review; no
full/browser/farm/live-socket suite was run.

