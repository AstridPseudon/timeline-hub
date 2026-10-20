# Agent `occurrence.resize@1` source review

## Decision

**APPROVE the private Agent source, exact tree, and schema. HOLD normal
generation, pin/release, Runtime pairing, App adoption, native HTTP, and public
activation until their separately required qualifications and peer ACKs exist.**

Exact reviewed source:

- branch `tl/agt-m2-occurrence-duration-carrier`
- commit `61abe2c5a3cfaf370addcc96fa3f4fa352abbd40`
- tree `cb18addba5b5a4a746d938dc8fcad5693061a236`
- parent/base commit `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`
- parent/base tree `0699f877a4c809005536a80f5956b8051a814ef7`
- changed-files digest (sorted path + NUL + bytes + NUL):
  `ed5a57a1f72e8efb7266f7fe3290a2081341825792065e2356e15809f6992881`
- candidate schema SHA-256:
  `79c54f0ba6ddb1028a90f8e5545ece68a34fa156a3642b14fea550a8f02da0c2`

The schema remains a single closed additive operation: 59 definitions and 33
operation clauses. Removing `OccurrenceResizeArgs` and its `occurrence.resize`
clause reconstructs the prior group-floor schema hash
`27f2e3edaffdfc49665a858c5c1d6985dd89ef200932679b77367bc459329cfb`.

## Source findings

The implementation is bounded to `astrid/sdk/timeline/native_occurrence_resize.py`
plus registry/schema wiring and conformance/schema-floor tests. It accepts only
an exact `occurrence:<stable-id>` root and positive integer authored
`duration_ms`. The recorder reads and selects the occurrence identity, shot
identity, optional shot revision, occurrence collection, owner membership, and
existing timing codecs. It writes exactly the existing
`occurrence.duration_ms` leaf.

The Main voiceover fixture proves the raw-unit result `o1: 3000 -> 4150 ms`
with the same occurrence identity. Placement start, shot pin, maps, child
content, opaque values, and sibling occurrence state remain unchanged. Guarded
inverse/redo, ABA/intervening-write refusal, disjoint opaque/sibling rebase,
invalid-value refusal, and missing-identity refusal all pass without mutating
the rejected draft. There is no alias of `group.move`, Runtime DTO, root/whole-
entity writer, or silent legacy-group migration.

The handler's `pinnedShotGroups` check is additionally preceded by the existing
global `execute` legacy-group preflight; when that key exists, the actual error
kind is inherited `unsupported_dependency` before the handler's
`migration_needed` branch. This is the same behavior on the base tree, and it
still refuses atomically without migration; no candidate regression was found.

The operation deliberately does not author parent `config.duration`, following
occurrence starts, parent holds, or the complete ripple batch. In the fixture,
parent duration remains `6`; this carrier must not be described as solving the
full ripple proposal. A separate reviewed lowering/batch remains required.

Existing rational-fps and half-open timing controls pass unchanged; the carrier
does not quantize or invoke a second compiler. This is control evidence for the
unchanged compiler boundary, not a claim of a new compiler integration.

## Evidence

Independent runs from this exact worktree, with shared dependencies read-only:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_resize.py tests/sdk/test_timeline_materialization_schema_union.py
29 passed in 1.70s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_resize.py tests/editing_conformance/test_recipe_m2_group_move.py tests/sdk/test_timeline_materialization_schema_union.py
58 passed in 4.11s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties tests/sdk/test_timing_compiler.py::test_after_word_end_at_source_out_is_included_and_onset_at_source_out_is_refused tests/editing_conformance/test_recipe_m2_clip_trim.py::test_rational_fps_source_contact_and_half_open_intervals_are_not_requantized tests/editing_conformance/test_recipe_m2_group_move.py::test_rational_fps_quantization_and_half_open_adjacent_boundary
5 passed in 1.36s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_resize.py tests/editing_conformance/test_recipe_occurrence_create.py tests/editing_conformance/test_recipe_occurrence_delete.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_occurrence_media.py tests/packs/video_editing/test_draft_voiceover.py
204 passed, 3 failed in 7.97s

python3 -m json.tool astrid/core/timeline/schema/edit-command.schema.json
PASS

/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/native_occurrence_resize.py astrid/sdk/timeline/commands.py tests/editing_conformance/test_recipe_occurrence_resize.py tests/sdk/test_timeline_materialization_schema_union.py
All checks passed

git diff --check c0644cf1..HEAD
PASS
```

The source handoff says the second targeted aggregate is 53 tests. On the exact
reviewed tree it collects and passes **58**; the 53 count is stale. This does
not hide a failure or alter an expectation.

For the broader three failures, I archived and ran the same neighbor set from
actual base `c0644cf1` (no checkout or source mutation): **196 passed, 3
failed**. The candidate's failures are exactly the same nodes and causes:

1. `test_recipe_occurrence_delete.py::test_legacy_group_refuses_with_migration_needed_and_no_mutation`
2. `test_recipe_occurrence_delete.py::test_closed_schema_and_portable_native_capture_golden`
3. `test_recipe_occurrence_duplicate.py::test_legacy_group_refuses_with_migration_needed_and_no_mutation`

The first and third observe inherited `unsupported_dependency` versus the
tests' expected `migration_needed`; the second is the inherited portable
golden mismatch. Candidate-only resize tests account for the eight-pass
difference between 204 and 196. These are therefore pre-existing failures, not
same-node different-cause failures.

## Limits and handoff

No full/full* suite, localhost/live sockets, native HTTP, Runtime generation,
pin/release, App writer, or consumer activation was run. The source proposal
and this review do not authorize those boundaries. No product files or shared
worktrees were modified by this review.

