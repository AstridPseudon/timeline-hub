The placement correction is applied. The duplicate re-derivation is **not** implemented, because two factory inputs aren't available. I documented the extension that would supply them, and the xfail stays. I created DONE and wrote the commit message. Nothing is committed (the harness does that).

**Tests:** `request-test … targeted` on `test_recipe_m2_placement_create_unplace.py` and `test_recipe_occurrence_duplicate.py` gave 69 passed, 1 xfailed (the expected strict xfail). I did not request a full suite.

**Merge:** The worktree already contained the placement-create-unplace branch. I applied only the duplicate branch's own commit (`e445e3db`) with `git apply --3way`. The only conflict was in `astrid/sdk/timeline/commands.py`, where I kept both operation entries. The schema merged cleanly.

**Placement:** The design doc no longer has the same-ID remove-then-create guidance. It now says:
- Re-placing unchanged media at an explicit time is `placement.move`.
- A separate replacement needs a NEW reserved clip ID.
- Callers pass an explicit occurrence owner and a media pin.
- Auto, pool, null, shift, video and registry refresh stay on the legacy writer.

The undo section now says undo is strict ABA, not a LIFO stack. Undoing a create after any intervening write to the created clip is refused (`intervening_write`).

I added two tests in `test_recipe_m2_placement_create_unplace.py`:
- Undoing a create refuses after an equal-value intervening write.
- Re-running the create for an already-occupied clip ID refuses.

I dropped a test for create → unplace → undo(unplace) → undo(create) because I couldn't make it assert cleanly. The old design note on that case is now replaced by the strict-ABA wording, but that exact sequence has no test.

**Duplicate:** `stable_occurrence_deep_link` and `stable_output_identity` in `shot_composition.py` need two inputs that aren't available:
1. The parent `document_id`. The authoring bundle has only `project_id` and `timeline_id`; the `document_id` fields in `commit.py` belong to media pins.
2. The destination `shot_revision_id`. It is content-addressed at compile time and doesn't exist when the command is captured.

Inventing either would be fabricating authority, so I left `test_copy_does_not_carry_source_derived_identity_fields` as a strict xfail with an updated reason. `design/m2-occurrence-duplicate.md` now records the exact extension: carry `parent_document_id` into the authoring bundle, then re-derive the two root fields in the compile step that sets `shot_revision_id`. If the Agent shouldn't own `parent_document_id`, the fallback is an App-supplied value. Which of the two to use is your call.

**Notes:**
- The two design docs live in the orch `design/` directory, not in the repo, so I edited them there.
- The merge left `commands.py` marked conflicted in the index. I staged it as resolved, since `.git` rejects commits but accepted `git add`.
