# P1 Agent real-document case-collection handoff

## Review verdict

**FAIL for case-collection acceptance** at author SHA
`c241aecaaeac76ddcbd76d2931788739c405726c` (parent/integration base
`a086cc6db7928dc4a3516d304dd9a472b050f1cf`). The corpus is usable after one
provenance correction; no product code was changed by this review.

This is a collection verdict only. It is not full P1 acceptance and is not an
H3 GO. Full P1 still requires the integrated R1 Agent `doc.patch` provider and
A2 App mixed-command chain. C0b step-read/effect amendments remain pending;
undo proof was not requested here.

## Corpus location and coverage

The candidate branch stores the corpus at
`tests/sdk/fixtures/p1_feasibility/manifest.json` and the data-driven checks at
`tests/sdk/test_p1_case_corpus.py`. It contains 11 exact source snapshots:

| Case | Source/provenance | Coverage |
| --- | --- | --- |
| `nested-closure-trim` | `tests/editing_conformance/fixtures/recipe_m2_clip_trim.json`; `test_recipe_m2_clip_trim.py::test_portable_golden_and_closed_schema` | Parent closure, occurrence/shot/internal revisions, media/dependency manifest, mirrored clips, trim, metadata, unchanged sibling |
| `created-track-and-clip` | `recipe_m2_clip_add.json`; `test_recipe_m2_clip_add.py::test_empty_bootstrap_explicit_track_then_first_clip_golden` | Created IDs, ordered collections, null/sourceURL, opaque values, sequential track then clip creation |
| `params-absent` / `params-null` / `params-object-clear` | The three `recipe_m2_scalar_*` fixtures; parameterized scalar golden test | Absent vs null vs object, explicit clear, dotted/bracketed literal keys, opaque values |
| `disjoint-rebase` | `recipe_m2_scalar_disjoint.json`; parameterized scalar golden test | Disjoint sibling edit and native rebase preserving head-only data |
| `same-field-conflict` | `recipe_m2_clip_trim.json`; intended stale trim refusal | Real trim fixture and conflicting `from` head mutation |
| `sdk-tiny3-text-edit` | `tests/editing_scenarios/fixtures/tiny3.json`; look scenario and `test_fixtures_v2.py::test_edit_on_tiny3_shows_in_edits` | SDK nested clip text edit and edit diff |
| `sdk-publishable-clear` | `tests/fixtures/timeline_editing/tiny_publishable.json`; clear-asset look scenario | SDK asset clear while preserving opaque app metadata |
| `sample-project-closure-reference` | `examples/hype.timeline.full.json`; core round-trip test | Real mixed sample project, tracks/clips/effects/transitions/passthrough metadata |
| `sdk-selected-param-accepted-history` | `tests/sdk/fixtures/selected-param-legacy/accepted.zip`; README/runtime selected-schema tests | Authenticated historical closure/history archive, retained as provenance-only |

The manifest’s SHA-256 checks show every copied snapshot is byte-identical to
its claimed source. The canonical cases execute through existing
`bundle_from_document`/`document_from_bundle`, semantic `execute` and `replay`;
SDK cases use `Checkout`; the sample uses the core loader. No provider,
executor, or synthetic golden executor was added. The copied canonical files
are exact source snapshots, including their existing records/output, rather
than modified expected-output data.

## Blocking review finding

`manifest.json:97` claims the `same-field-conflict` provenance is
`tests/editing_conformance/test_recipe_m1_commands.py::test_changed_map_source_owner_and_query_order_refuse`.
That test constructs a `capture_move` for
`occurrence:occ-1/clip:picture-1` and checks owner/source/rate/blocker/order
dependency changes. It does not load the trim fixture or test a stale trim’s
`from` field. The corpus’s own test at `test_p1_case_corpus.py:112-121` is a
real replay refusal and leaves the conflicting head unchanged, so the defect is
the source attribution, not fixture realism. The matching existing trim test is
`tests/editing_conformance/test_recipe_m2_clip_trim.py::test_replay_consumed_source_identity_bounds_and_selection_but_preserves_disjoint_data`
(line 238; its `from` mutation is in the guarded loop). Correct the manifest
provenance pointer and rerun the targeted checks before acceptance.

No other ownership, skip/xfail weakening, duplicate executor, synthetic golden,
or false `doc.patch`/H3 claim was found. The candidate handoff also correctly
states that doc.patch execution is pending and lists R1 prerequisites.

## Verified commands

Environment: Python 3.12.3, pytest 9.0.2 from
`/home/user/work/venv-app2-native`; ruff 0.16.9 and mypy 2.3.1 from
`/root/.local/bin`.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_case_corpus.py
13 passed, 2 warnings in 11.01s

/root/.local/bin/ruff check tests/sdk/test_p1_case_corpus.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_case_corpus.py
Success: no issues found in 1 source file
```

Pytest’s two warnings are the shared environment’s unknown `timeout` and
`timeout_method` options. No full, browser, localhost, live-socket, or runtime
service suite was run. The review worktree is clean.

## R1/A2 integration prerequisites

After the provenance fix, keep these source cases and map them to actual
approved-contract requests; do not replace them with synthetic patch goldens:

1. Add the real Agent `doc.patch` path for closure roots and logical entity
   addressing, previous-value guards, absent/null/remove semantics, ordered
   identity-list operations, created-ID claims, opaque metadata, and declared
   reads. Preserve each source command and expected effect as provenance.
2. Execute the nested, creation, absent/null/clear, disjoint, and stale-field
   cases through the provider/runtime path with accepted, merged, and refused
   replies. Verify refusal leaves the head unchanged and merged preserves the
   intervening disjoint value.
3. Add the App chain separately: split → trim the new clip → intervening Agent
   edit → lost acknowledgement → restart, covering accepted, merged, and
   refused replies. This collection does not prove that chain.
4. Only when both R1 real-document execution and A2 mixed-command/restart
   execution pass can P1/H3 be considered; current native/SDK checks are
   collection evidence only.
