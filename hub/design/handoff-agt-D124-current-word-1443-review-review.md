# D124/D107 protected current-word source review

Verdict: `PASS_SOURCE`.

Candidate: `a0eacc676c71945de7fb08e99c2d511141d4aeb4` (direct child of normal
`a4e016b6a9f91fbe372672bdcf382c630bf59186`). Donor reviewed:
`2e3331ee2f035e302f5ca52488832cd0e22bb3aa`, independently source-approved by
`handoff-agt-D107-sol-review-0715.md`. The predicate inventory reviewed was
`handoff-agt-D107-current-sol-0659-predicates.tsv`.

## Source conservation

- The candidate changes exactly the two allowed paths:
  `tests/editing_conformance/test_m1_current_equivalent.py` and
  `tests/editing_conformance/current_word_baseline_fixture.py`.
- Candidate and donor test ASTs are identical after normalizing only the
  fixture module name (`native_word_anchor_fixture` →
  `current_word_baseline_fixture`). This preserves predicate order, inputs,
  guards, calls, and scenario structure; it is not a count-only comparison.
- Both donor and candidate contain 131 `assert` nodes and 5
  `pytest.raises` contexts.
- The exact protected D107 original-ten selector set is unchanged: two
  outbox cases, two keyed-view cases, and six auto-placement cases
  (`anchor|fallback|shared` × `image|video`). The new candidate adds only the
  two IDs `disjoint-rebase-undo` and `touched-basis-conflict`.
- The TSV has 111 rows: 87 assertions, 8 raises, 9 helper-call purposes, and
  the recorded input/review/scope rows. Its disposition counts are
  `STATIC_CURRENT_MAPPING_HELD=80`,
  `EXPLICIT_CURRENT_SCOPE_MAPPING_HELD=9`,
  `ORIGINAL_UNCHANGED_OUTSIDE_COMBINATION=21`, and
  `NOT_AN_ORIGINAL_M1_PREDICATE=1`. All candidate file locations resolve.
- Normal protected blobs remain unchanged, including the original M1 test
  (`sha256 23451aa80279f47d126e5e5699f51272b8a6418402ba559617c243bcd6b15041`),
  native fixture/test, and all non-target tree blobs.

## Current fixture and source flow

`current_word_baseline_fixture.py` is the seven-line adapter. It aliases the
actual native fixture's `current_retained` and re-exports only its existing
`DECLARATION` and `FPS` values plus the pytest fixture alias `retained`; it
does not author transcript text, history, pins, media identity, or a legacy
seed.

The native seed creates Runtime media and a transcript, admits the current
source and binding through the registered `agent.create_runtime_commit_service()`
provider, and records the genuine current pin. Candidate setup calls the
existing `RuntimeService.commit_timeline` seam only to prepare that source and
peer topology. The journey then starts the real Runtime daemon with the same
registered provider and uses public `AstridClient`, CLI, and
`TimelineSession` outbox/undo paths. CLI and Python source/provenance,
idempotency key, base pair, canonical replies, receipt, records, history,
conflict, retry, inverse, and redo are statically visible in the candidate.
The separate public sheet route remains downstream scope and is not claimed
as executed by this source-only candidate.

The C0 request construction visibly includes API version, project/timeline
scope, base revision/publication, command list, label, ordered steps with
patch/reads, fields merge, reads, dry-run, source, rationale, group ID, and
the idempotency-key call argument. No alternate authority, fake acceptance,
legacy fixture rewrite, production/schema/client/pin change, or original-ten
retirement is present.

## Validation boundary

All evidence is source-only. Python AST parsing/in-memory compilation and
`py_compile` were run to the resolved temporary directory; scoped Ruff and
the existing Ruff/mypy baseline comparisons passed. No pytest collection or
execution, provider/service/socket/browser/body/collector/full-suite,
qualification, P4, original-ten, 95, or retirement run was performed.

This PASS_SOURCE does not establish current behavior, ABA closure, Farm core,
functional qualification, D107 closure, or permission to retire the protected
original ten or remaining 17 selectors. The existing HELD dependency and
downstream behavior gates remain in force.
