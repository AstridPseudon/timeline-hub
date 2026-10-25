# D136a findings

## Verdict

NO_GO. The current evidence does not qualify a release or a next-body run.

## Proven finding

All nine exact original9 selectors share the same first dynamic refusal at `runtime_protocol/timeline_commit_auth.py:2209` in immutable Runtime pin `ab1e4f6141987706132916e2da16477f5a019464`:

`provider intermediate command lacks an authenticated physical observation`

The guard is a real C0 contract check: it resolves the authenticated native site and requires the physical result reference to be present before projecting command output. This is a product REG, not a setup classification. The retained run had 9 setup errors and no selector body reached.

## Unknowns kept explicit

The safe evidence does not contain the raw provider payload, capture ref/path, command ordinal, or authenticated observation record. Therefore this review does not claim whether the missing/misbound record was produced by Agent core, the provider, or the Runtime adapter. Every downstream guard from B023 through B036 and every final predicate B-FINAL-001..009 is statically listed but dynamically UNKNOWN/unreached.

The pristine 886a comparison is source custody only: the joined D136 timeline files are absent there, so absence cannot establish an upstream REG. The located D54a paired-cause report qualifies zero rows and preserves its causes as open/unproven; no D54a proven upstream REG is imported here.

## Prior evidence retained

The prior D136a source-custody/PASS and actual NO_GO are retained. The final20db source fixed the earlier Agent typed-output boundary; the remaining observed boundary is separate and is in Runtime C0 sequential observation validation. No new actual body, pytest, collection, fixture execution, browser, collector, profile, benchmark, child, acquisition, full suite, source edit, fixture conversion, retry, alternate qualification, or release action was performed.

## Required handoff

Runtime should review B022 and the complete downstream table, address all proved product items in one pass, and return qualified changed source. Only then should the exact original9 be rerun under the settled harness and the final predicates be re-qualified. Until that happens, keep release and next-body work held.
