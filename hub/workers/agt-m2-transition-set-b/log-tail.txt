## Report: agt-m2-transition-set-b

**What I did**
- I carried over the previous worker's uncommitted WIP from `/home/user/work/wt/agt-m2-transition-set`. Its branch `tl/agt-m2-transition-set` had no commits beyond base. I applied the tracked diff with `git apply` and copied the three untracked test files.
- `clip.set` now accepts a canonical incoming `transition` SET. It takes type, positive duration, optional revision and params. It also takes an optional matching `elementRef`, and a `schema_source` pin for project-pack transitions.
- Changed known params are validated against the exact selected declaration: the shipped builtin descriptor, or the pack schema from `schema_source` through the existing resolver. Unknown params stay opaque.
- A new `transition.predecessor` selection guards membership and lane changes. Writes on other lanes don't conflict.
- Clear semantics are unchanged.

**One fix of mine:** the WIP test `test_actual_app_selected_builtin_uses_exact_shipped_catalog_reference` failed. It assumed cross-fade declares an `easing` enum, but the shipped schema only declares `durationFrames` (number, minimum 1). I changed the test to set `durationFrames` to 0 and expect a refusal, and to keep an opaque param. This corrects a wrong test assumption; no behaviour expectation was weakened.

**Tests** (run through the central test service, targeted suites only)
- First run of the four touched test files: 147 passed, 1 xfailed, 1 failed (the test above).
- Second run of those files plus all of `tests/editing_conformance` and `tests/sdk`, after the fix: **3082 passed, 6 skipped, 186 deselected, 1 xfailed, 0 failures**, in 637s.
- The one xfail is a strict-xfail in `tests/sdk/test_timeline_transition_schema.py` that the previous worker added. It covers exact inverse removing newly introduced DocumentPins when no later dependent needs them.
- I did not request a full suite.

**Not done or unverified**
- No `design/m2-transition-set.md` and no `notes/report.md` existed in the old worktree. I did not write the design doc, so the brief's goldens/mapping doc is still missing.
- I didn't count product lines against the 100-line target. The product diff is roughly 190 added lines, so it overruns.
- The brief text was garbled, with spaces stripped. I worked from the WIP's evident intent, so I can't confirm every brief item is covered. In particular I did not check the "oversized authored window / rational fps / overlap follows the ratified compiler policy" requirement against the WIP. It only enforces positive whole frames.
- The old App writer deletion is held until there is proof of an actual consumer, as the brief says.

**Next steps**
- Write the design doc.
- Trim the product diff toward 100 lines.
- Decide on the xfail DocumentPin-removal requirement.

The commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-transition-set-b/commit-msg`. I left no temp files in the worktree. `wip.patch` is in the scratchpad, outside the repo.
