The transition SET slice is finished except for one test, which stays a strict expected failure. The targeted tests pass: 153 passed, 1 xfailed.

**Tests.** I ran them through the test service, not directly, because direct pytest runs needed approval in this sandbox. The command was `request-test agt-m2-transition-set-c targeted --files "tests/editing_conformance/test_recipe_transition_set.py tests/sdk/test_timeline_transition_schema.py tests/sdk/test_timeline_clip_scalar_provider.py tests/editing_conformance/test_recipe_clip_scalar_fields.py"`. I did not run any full suite.

**What I did**
1. **Design doc.** I updated `design/m2-transition-set.md`, which lives in the orchestrator's design directory, not in the worktree. It now has the exact `clip.set` args, the App capture mapping, the refusals, the guards and the clear semantics. The mapping covers `ClipTransitionSection` and `ElementsLibraryPanel` → `timeline.apply_transition`.
2. **Neighbour windows.** `test_recipe_transition_set.py` now has a table of ten cases, all passing:
   - first clip, alone and as a tie that keeps collection order;
   - gap, exactly adjacent (half-open) and overlap;
   - oversized authored window;
   - rational 30000/1001 first, adjacent and oversized, plus the exact half-frame case.

   A new golden file, `fixtures/recipe_m2_app_transition_windows.json`, pins the commands and records for those ten cases. A separate test covers the whole-frame boundary at 30 and 30000/1001 fps: 0.5 frame is accepted and just under it is refused.

   The `clip.set` code already allows all of these windows, so I added no product code for them.
3. **Strict xfail kept.** `test_first_selected_transition_exact_document_inverse` stays a strict expected failure, with its original expectation unchanged. Dropping a newly introduced DocumentPin on undo is not small. It needs three things:
   - a record of which pins an edit introduced;
   - a scan for later edits that still depend on the pin, built like the existing media-removal check (about 100 lines in `commit.py` and `_recording.py`);
   - Runtime accepting the smaller manifest.

   Authored undo and redo are already exact; only the manifest keeps the extra pin.
4. **Trimming.** I made no product-code trims. Nothing was clearly removable, and I weakened no tests.

**Not verified.** I did not run the broader editing_conformance directory or any full suite; the targeted run covered only the four files above.

The commit message is written and `DONE` is created in the worker directory.
