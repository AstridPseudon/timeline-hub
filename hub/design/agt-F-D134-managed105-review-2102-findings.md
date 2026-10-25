# D134 independent source assessment

Verdict: FINITE_SOURCE_ASSESSMENT_UNAPPLIED.

The shared105 author packet is source-clean and the representative is a genuine
setup refusal, not behavior-green. The 105 exact members are preserved in
predicate-map.json: 102 are classified setup/expectation-proved and the three
tests/timeline/test_authoring_media.py nodes are UNKNOWN and untouched.

## Seam and preservation

All nine files converge on the retained S1 setup sequence: empty bootstrap,
accepted semantic occurrence.create with items: [], then restoration of the
authored closure whose shot has item-1. Current doc.patch managed-edge checks
remain at _doc_patch.py:359-377; current item correspondence checks are
_command_state.py:316-395, with the first meaningful refusal at line 369. The
exact source/topology/media/item-1 predicates are recorded in the predicate map
and source manifest. Target files, imported fixture sources, and golden JSON
inputs are byte-identical to both shared author 96a6 and prior base a30a. The
only current delta from shared author is the unrelated
tests/editing_conformance/test_occurrence_fork_source_baseline.py; no helper or
managed105 fixture edit remains.

## D100 applicability challenge

The previous minimum-source claim that D134 needs an authenticated accepted
source closure already containing item-1 is too strong. It conflates:

- semantic creation of an empty occurrence (which still creates no shot item and
  has no existing clip/media command that allocates one); with
- the D100 first-physical-item correspondence correction.

Held 9486 is applicable to the latter exact shape. Its guarded branch authenticates
the physical shot/revision/internal source and empty item_id_map, admits unique
non-empty physical item IDs, and keeps copied/remapped correspondence strict.
D134's accepted occurrence.create provides the authenticated empty physical
source needed by that branch. A separate accepted item-bearing source is not
proved necessary.

This remains UNQUALIFIED: held 9486 is not applied in this checkout and no
behavioral rerun was authorized. The next input is the existing Agent provider
owner's qualified 9486 behavioral receipt on pinned Runtime ab1e, then the
unchanged protected representative. No source, guard, test body, fixture, seed,
mapping, history, or product change is recommended by this assessment.

## Production caller/comparator

The real setup helper submits C0-shaped requests (base revision/publication,
commands, per-command steps/patches, atomic merge, source and idempotency key)
through service.commit_timeline after registering the Astrid provider
(test_commit_runtime_occurrence_media.py:21-114, 55-67, 124-227). The static
production chain is commands.execute:201 -> Recording.write:132 ->
State.set:493 -> project_shot_items:371/shot_item_map:316, with managed closure
checks in _doc_patch.py:359-377. The retained genuine comparator at
test_recipe_occurrence_media.py:90-149 proves existing-item media preservation
and guarded inverse/redo; it does not prove first-item birth.

No behavior, provider, collection, runtime, browser, socket, or full suite was
run under this read-only brief.

