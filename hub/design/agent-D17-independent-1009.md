# Agent D17 independent review — 2026-10-23

Verdict: **FAIL** for stopped saved `tl/agt-D17-current-port-0916`, exact
`80680fab5` over `c424ee9a5`.

The saved tree adds a strict xfail to the new repeated-copy guarded-undo
positive at `tests/editing_conformance/test_commit_runtime_source_copy.py:297`.
The known failure is a real `inverse_conflict` on `config`; the no-weaken rule
requires the positive to remain a required pass. No expected failure is
approved.

The two original restructure positives pass directly (**2 passed in 2.05s**)
and their revised fixtures are source-backed: accepted Runtime closure rows,
ingested media, and authenticated `source_mapping`/`physical_content` checks.
The repeated fixture correctly asserts one canonical physical shot while
distinguishing two working aliases after reopening.

The production caller uses `duplicate_timeline -> _duplicate -> normal durable
session.submit` with the exact five-field source reference. Provider-side
scope, fresh-ID, empty-destination, order/sharing, media/document input, and
dependency guards are present. Runtime's separate D17 authority handoff
qualifies exact pair/digest/access, stale-capture, and forged-media rejection,
but does not qualify Agent repeated-copy undo.

Remaining blockers are real repeated-copy guarded inverse, real retained-input
undo, lost-ack/unknown-outcome restart cleanup, isolated stale and forged-media
Agent counterexamples, and complete G5 route retirement. The exact tree still
contains commands-file/native CLI, `document_diff.py`, `store.three_way`,
`store.publish_bundle`, and the old publish route.

Independent checks: vendor lock PASS; artifact manifest PASS; py_compile PASS;
Ruff FAIL (four changed-test errors); diff-check FAIL (EOF blank line); mypy
unverified. No full or known-red whole-suite run.
