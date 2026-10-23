# P4 independent review: note-04 conflict rerun

**Result: PASS**

Candidate: `755d6e7a4a179e74ce5ed497edab88e8b7a292af`  
Reviewed against: `5a313eb8`  
Reviewed worktree: `/home/user/work/wt/ap2-P4-note-rerun-review-0157`

The candidate is test-only and has exactly the permitted new path,
`tests/sdk/test_p4_note_rerun.py`; there is no G3/R2 ancestry merge, product
change, new ABI stub, skip, xfail, or relaxed expectation.

The test uses the original collected note-04/peer/suffix case through the real
public `timeline.open()` / `tl.commit(fn)` API. It exercises the production
G3 emitter chain (`Timeline._capture_free_edits` →
`emit_document_commands` → `TimelineSession.submit`) and asserts:

- first conflict at `r0/pub0`, then actual callback reevaluation after fetching
  `peer-revision/peer-publication`;
- changed retry key and exact changed base pair;
- first `before: absent`, then `before: present` with the peer value;
- the suffixed note-04 result and exact preservation of the other nine notes,
  raw/opaque/null fields, closure/child data, dependency manifest, and both
  parent mirror copies;
- ABI-1 request scope, `doc.patch`, label, per-step patch metadata, omitted
  reads, conservative atomic mode, Python source, and non-preview behavior;
- no leftover pending/flight outbox state.

The neighboring G2 tests cover the persisted maximum of three function
evaluations. This test’s two-attempt success therefore does not overclaim a
new bound.

Evidence:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_commit_cases.py
3 passed, 1 warning in 0.98s (unknown pytest `timeout` config option)

/root/.local/bin/ruff check tests/sdk/test_p4_note_rerun.py
pass

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_note_rerun.py
Success: no issues found in 1 source file

git diff --check
pass
```

Qualification boundary: `Generated`/`Client` is the existing fake generated
transport, so `accepted` here is local Python/provider-fixture evidence, not a
claim of official Runtime acceptance. C0 full v2 ABI/wire scope, authenticated
replies/receipt/digest/heads, durable history, CLI/sheet/show, per-step undo,
full-suite coverage, and H3/P4 completion remain unproven. No product changes
were made and no full suite was run.
