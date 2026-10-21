# Agent complete-document presence repair review

## Verdict

**DO NOT APPROVE** commit `f137c06a58a6a957af5fc0836ba690bff74eeb29`, tree
`c5feb99cff850d5b5a50843294493efd7196bdf2` (`tl/agt-m2-document-presence-complete-boundary-repair-0645`).

The four bounded repairs close all twelve diagnosis counterexamples and preserve
the checked native positives, but one ordinary complete-document edit still
passes when combined with a valid move.

## Blocking counterexample

Starting with `tests.timeline.test_authoring_feedback.bundle()`:

```python
work = bundle()
base = copy.deepcopy(work)
work["parent"]["clips"][0]["at"] = 4
mirror = work["parent"]["config"]["clips"][0]
mirror["at"] = 4
mirror["app"] = {"astrid": {"fixed_start": True, "for": 1.0}}
compile_authoring_candidate(work)
result = document_diff_to_commands(work, base)
```

The candidate compiles and the adapter returns `['clip.move']`, retaining the
explicitly added mirror `app` field. The field is absent from the pinned
`parent.config.clips` row and has no authored native recipe. The same `app`
shape is produced by native `clip.move`, which is why the replay comparison
currently accepts it; that coincidence must not turn an authored mirror edit
into a successful save. This violates the settled requirement that every
unrepresented authored edit, alone or beside a valid move, either replay
losslessly or refuse atomically.

The relevant boundary is
`astrid/sdk/timeline/document_diff.py:54-76`, especially
`_require_explicit_rows()`. It compares the union of pinned and candidate keys
against replay, but does not reject a candidate-only key before allowing a
native-derived field to match it. The parent primary row is protected by
`_check_clip_shape`; the config-mirror row is not.

Recommended bounded repair: reject candidate row keys absent from the pinned
row for the mirror/result check (or otherwise fail closed for explicit
candidate-only fields), while continuing to permit native-derived fields that
are absent from both pinned and candidate. Add this exact regression and retain
the existing identity-map/move positive.

## What passed

- The twelve original diagnosis cases all refused, with candidate and base
  unchanged, under the `--runxfail` probe run.
- Focused adapter/media selection: **11 passed, 131 deselected**.
- Complete touched test files: **140 passed, 2 deselected**.
- Ruff on the four changed source/test files: passed.
- `git diff --check`: passed.
- Native trim, ordinary params value/clear, hold clear, track-label clear,
  script/slot preservation, identity-map spelling, and media rebind positives
  remained green in the touched suite.

The legacy diagnosis artifact's final planner test still expects the old
`AttributeError` for malformed `registry=None`; the repaired behavior is the
intended structured `ValueError`, so that stale assertion is not counted as a
product failure.

No source edits, HTTP, browser, Runtime-door, or full-suite runs were made.
