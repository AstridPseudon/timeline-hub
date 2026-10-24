# R5 source-owner review

No tracked edits. Worktree clean.

## Headless media

- Runtime: `458595850c354f4403dabc58a72b98bebbc2c3a3`
- Fixture: `3c46eb0d0dfeaac12e7657b5809f6d7594c96973`
- Agent: `5aee1f361147c7f1b02ba158092889be4efb15da`

**Result: FAIL — Agent G4 causal gap confirmed.**

Runtime’s commit door and media admission path are valid. The faithful positive keeps `AUTHORED`, replaces only synthetic media ID `x` with the ingested digest, and explicitly restores root `parent.clips` after replacing bootstrap config.

The defect is in Agent [`_doc_patch.py`]( /home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/_doc_patch.py:388 ): replacing `parent.config` removes both mirrors, then `native_sites()` sees neither root nor config `clips` and returns no assignment site ([lines 175–200]( /home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/_doc_patch.py:175 )). The requested root `clips` set is therefore not installed, producing Runtime’s `candidate.parent.clips: must be a list`.

This is an Agent root-replacement defect, not an unfaithful harness correction. The bounded fixture recipe is already present: set config, set registry, then set root clips with an absent prior value; retain all original fields and downstream assertions. No fixture-only workaround should add a config mirror or weaken validation.

Runtime C0/source guards: **PASS**. Agent G4: **FAIL**.

## Occupancy

- Runtime: `458595850c354f4403dabc58a72b98bebbc2c3a3`
- Fixture: `51c2d6aaccf29f8c9c261f54e2a5bfaa676ccff5`
- Agent: `bc38aa3eb37008e97bcd85833ac9001eb6523d5f`

**Result: FAIL — Agent G4 semantic-carrier gap confirmed; fixture evidence also incomplete.**

The original scenario creates `other` with main’s historical physical `shot-1`/internal pins, advances the global shot head, then reuses the historical pins. The current fixture instead performs a same-timeline `timeline.inverse` and does not exercise `other` or a cross-timeline source.

The authenticated Runtime source path exists ([`timeline_commit_port.py`]( /home/user/work/wt/rt-R5-source-owner-review-0202/runtime_protocol/timeline_commit_port.py:287 )), but registered Agent operations do not provide the required carrier:

- `timeline.duplicate` reads an authenticated foreign closure but requires an empty destination and complete fresh shot/occurrence IDs ([`native_timeline_duplicate.py`]( /home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/native_timeline_duplicate.py:49 )).
- `occurrence.place-shared` accepts only `occurrence_id` and `on`, with no cross-timeline source pin ([`native_occurrence_shared.py`]( /home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/native_occurrence_shared.py:10 )).
- `timeline.restructure` requires the current timeline’s authenticated closure.
- `doc.patch` rejects managed membership/revision-edge writes ([`_doc_patch.py`]( /home/user/work/wt/agt-pin-5aee1f36/astrid/sdk/timeline/_doc_patch.py:321 )).

The current two missing-head variants differ only in a name string, not retained-vs-new revision identity. The HTTP F1 case checks only status and reason, whereas the original required exact code/message/details equality.

Runtime authenticated source path: **PASS as a read/authentication seam**. Agent G4: **FAIL for the required reuse carrier**.

## Checks

- Registered Agent operations inspected offline: 34 operations; relevant handlers confirmed.
- AST parse: passed for 11 source files plus both branch fixture families.
- `git diff --check`: passed for worktree and reviewed branch diffs.
- Pytest, Ruff, Pyright, HTTP, browser, and full suites: **not run**, per report-only instructions and because known-failed public/body cases must not be rerun.

Recommended next step: Agent G4 must repair the headless mirror assignment and provide an approved authenticated cross-timeline physical-pin carrier. Then restore the exact occupancy inputs, distinct missing-head variants, and full HTTP predicate before qualification.