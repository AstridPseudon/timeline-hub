# P1 Agent real-document case-collection handoff — corrected re-review

## Collection verdict

**PASS for case-collection acceptance only** at author SHA
`b1c25f5c34a346b634210e22eabba3f73c412160`.

This is the correction re-review of the prior failure at
`c241aecaaeac76ddcbd76d2931788739c405726c`. The prior failure was solely the
wrong source-test attribution for `same-field-conflict`; no product code was
changed by this review. Full P1/H3 remains pending R1/A2 integration.

## Correction verified

`tests/sdk/fixtures/p1_feasibility/manifest.json:97` now cites:

```text
tests/editing_conformance/test_recipe_m2_clip_trim.py::test_replay_consumed_source_identity_bounds_and_selection_but_preserves_disjoint_data
```

That existing test constructs a real `capture_clip_trim` plan and its guarded
replay loop includes the trim's `from` field, refusing a head that changes the
consumed source identity/bounds. The corpus's own
`test_same_field_edit_is_a_real_refusal_case` separately changes both mirrored
`from` fields to `3`, expects the existing `CommandError`, and verifies the
conflicting head is not mutated. The corrected source and copied snapshot are
byte-identical (SHA-256
`60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c`).

The added generic validation in
`tests/sdk/test_p1_case_corpus.py:60-126` checks that every provenance file
exists, Python qualified class/function nodes exist after removing parametrized
suffixes, and editing-conformance fixture-family markers appear in the cited
Python provenance. It passes for every manifest case.

## Corpus evidence

The corpus contains 11 real source snapshots:

- nested trim with parent closure, occurrence/shot/internal references,
  mirrored clips, media registry/dependency data, metadata, and unchanged
  sibling;
- created track and clip with ordered collections, stable IDs, null/sourceURL,
  and opaque values;
- absent, null, and object-clear parameter cases;
- disjoint sibling rebase preserving the intervening head value;
- the corrected genuine same-field stale-trim refusal;
- SDK nested text edit and asset-clear effects preserving opaque metadata;
- a mixed sample project loaded and round-tripped by the core timeline loader;
- a historical selected-parameter accepted archive retained as provenance-only.

All 11 snapshots match their claimed source bytes. The 13 retained meaningful
tests execute the canonical cases through existing
`bundle_from_document`/`document_from_bundle`, semantic `execute`/`replay`, SDK
`Checkout`, and the core loader. No new executor, provider, or duplicate golden
engine exists; the canonical files are copied source fixtures with their
existing records/outputs. No skip, xfail, weakened assertion, or test deletion
was found in the correction.

## Contract and acceptance boundary

These cases provide collection evidence for approved commit-v2 §§2–5 concepts:
closure-shaped documents, previous-value guards, ordered/created IDs,
absent/null/clear, opaque metadata, and disjoint versus same-field effects.
They do not execute Runtime's `doc.patch` provider and do not prove the C0c
unique-physical-root resolution principle, undo, or the App chain. The corpus
and test explicitly retain `collection-only; doc.patch execution pending` and
make no H3 claim. C0b is approved; C0c's addressing principle must still be
honored by the integrated implementation.

Full P1/H3 still requires R1 Agent provider execution and A2 App execution of
the split → trim the new clip → intervening Agent edit → lost acknowledgement
→ restart chain, covering accepted, merged, and refused replies. Undo execution
was not requested for this review.

## Exact verification

Environment: Python 3.12.3; pytest 9.0.2 from
`/home/user/work/venv-app2-native`; Ruff 0.16.9 at `/root/.local/bin/ruff`;
mypy 2.3.1 at `/root/.local/bin/mypy`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_case_corpus.py
13 passed, 2 warnings in 4.38s

/root/.local/bin/ruff check tests/sdk/test_p1_case_corpus.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_case_corpus.py
Success: no issues found in 1 source file
```

The two pytest warnings are the shared environment's unknown `timeout` and
`timeout_method` options. No full, browser, localhost, live-socket, or Runtime
service suite was run. The review worktree is clean after removing test/lint
caches.

## Recommended next step

Consume this as a collection-only PASS, then run these real cases through the
integrated R1 `doc.patch` path and separately verify the A2 mixed-command and
restart journey. Do not mark full P1 or H3 complete from this handoff.
