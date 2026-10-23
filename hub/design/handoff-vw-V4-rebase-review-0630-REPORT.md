# V4 independent source-failure review — FAIL

## Verdict

FAIL for readiness. The mandated real-provider run did not reach the fresh
status assertion. This is one selected case, one failure, zero passes, and 53
deselected from the original 54 collected tests. It is not a 1/2, 52/54, or
overall-suite result.

The failure belongs with the existing Agent/stale-window (0549) invalidation
scope. No new escalation file is needed. There is no basis to waive the
source/word/physical-owner guard or to request an extra policy exception.

## Exact source and baseline audit

- Reviewed HEAD `706fb017ecb662c2bb940467d39200445298de6f`, whose parent is the
  required integrated Agent base `3e4261e9694c7bd7c1b5fada9bf01d91007bcc80`.
- The parent-to-HEAD diff contains exactly one line in
  `tests/editing_conformance/test_native_word_anchor.py:235`:
  `status == "rebased"` → `status == "merged"`.
- The fixture and test at the retained `5292b388a` state are otherwise
  unchanged; `git diff 5292b388a..HEAD^` is empty for the fixture and target
  test, and `git diff 5292b388a..HEAD` is only that one status hunk.
- Runtime pin used by the source run: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.
  The normal integration Runtime worktree is `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`;
  the pin's merge parent is `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Current Agent source includes the landing metadata path from the c793
  change: replay passes `commit_request`/`evaluated_head` through the provider
  (`astrid/sdk/timeline/commit.py:1106-1111`), while Runtime distinguishes
  modern `merged` from historical `rebased` (`runtime_protocol/timeline_commit_store.py:63-73,
  216-220, 1064-1077`).

## C0 status decision

The permitted literal correction is independently correct: the current v2
reply for a stale disjoint landing is `merged`; historical ABI-1 receipt
validation still accepts/retains `rebased`. The target hunk changes no
historical receipt expectation and does not broaden status acceptance.

This C0 result does not make the run pass: the actual provider fails earlier in
`move-source`.

## Required execution and census

The source worker ran this exact command once, with no rerun:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k follow_rebases_original_choice_after_source_move_and_reorder
```

Result: exit 1, `1 failed, 53 deselected in 1.91s`. The only executed node was
`test_follow_rebases_original_choice_after_source_move_and_reorder[True]`.

Read-only collection census:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q --collect-only -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py -k follow_rebases_original_choice_after_source_move_and_reorder
```

Result: exactly `[True]`; `1/54 tests collected (53 deselected) in 0.18s`.
The original function has `@pytest.mark.parametrize("retained", [True],
indirect=True)` at lines 222-223. No second retained parameter case exists in
that original 54-test file. A similarly named copy in
`tests/editing_conformance/test_word_binding_recipe.py` is outside this
mandated collection and was not executed.

Additional static checks:

```text
/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_native_word_anchor.py
```

Passed: `All checks passed!`

```text
git diff --check 3e4261e9694c7bd7c1b5fada9bf01d91007bcc80..HEAD
```

Passed with no output. Typecheck is N/A because the only retained delta is a
literal assertion spelling. No full, native14, browser, heavy, or other test
suite was run or requested.

## First-failure causal trace

The worker log's first failure is:

```text
RuntimeErrorBase: candidate.timing: legacy word anchor is missing
```

It occurs during the first `move-source` commit, before the stale-anchor
submission and before the changed status assertion. The traceback reaches
Agent `astrid/sdk/timeline/native_word_anchor.py:169` through
`_commit_timing_validation.py:379`, `validation.py:609`, and the pinned
Runtime service at `runtime_protocol/service.py:2483`.

The source geometry and guard path are concrete:

1. The seed starts with the parent card's legacy declaration
   `"again" in line #2 +1f` (`tests/editing_conformance/native_word_anchor_fixture.py:112-118`),
   not an exact `word_anchors` binding. The reused source has physical clips
   `voice` at 1 and `other` at 4, both using the same media, source window
   `from=2,to=6`, and speed 2 (`native_word_anchor_fixture.py:89-94`).
2. The test captures an exact choice locally, then captures an occurrence-owned
   `clip.move` to global 8 (`test_native_word_anchor.py:225-230` and
   `capture.py:252-255`). This move changes the `voice` clip's local geometry
   (`capture.py:217-225`) and preserves the ordinary timing/physical-owner
   guards (`capture.py:185-221`); it does not carry a transcript choice.
3. Provider hydration loads transcript captures only from the immutable
   dependency manifest or an explicit `clip.anchor` choice
   (`commit.py:432-462`). The legacy seed has no exact transcript pin, so the
   real provider's `source_mapping.pinned_documents` is empty during this
   move.
4. D12a's legacy exemption requires the declaration and its complete reference
   basis to remain equal (`_commit_timing_validation.py:244-263`). That basis
   intentionally includes pinned documents, parent ownership, placements,
   source-shot mappings, physical source clips, and source timing inputs
   (`_commit_timing_validation.py:70-101`). The `voice` clip's changed `at`
   therefore invalidates the prior basis; the unchanged legacy declaration is
   not exempted.
5. Final validation calls `validate_candidate_timing` and then
   `legacy_binding` (`validation.py:603-611`, `_commit_timing_validation.py:357-379`).
   With no exact source capture, the legacy search has no hits and raises
   `TimingCompileError("legacy word anchor is missing")` at
   `native_word_anchor.py:166-170`, which Runtime reports as
   `candidate.timing`.

This is a genuine invalidation like the existing stale-window scope, not an
unrelated source defect or an overcount that should be waived. The source move
changes the physical search geometry of an unbound legacy word; retaining the
original word, source, reorder, DocPin, physical-owner, and no-write guards is
required. The later assertions about retained source `other`, merged landing,
restart timing, second move, and recorded reads remain unverified because the
first move is rejected.

## Changes and next step

No product, fixture, recipe, guard, generated, pin, package, assertion, or
deletion changes were made in this review worktree. The target tree is
unchanged from HEAD. There is no merge readiness until the actual source case
can complete; the existing Agent owner / 0549 scope should decide whether the
fixture must carry an authorized exact pin or remain an intentional refusal.
