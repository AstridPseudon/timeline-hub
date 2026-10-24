**Blocked: confirmed Agent G4 semantic-carrier gap. No tracked edits.** Read PLAN, original `458595850`, and findings 0132/0159.

The authenticated source-read path exists. Runtime verifies the source’s project/timeline, accepted revision/publication pair, immutable digest and closure, then rechecks that capture at acceptance. The missing part is an operation that carries those historical physical pins into another timeline:

- [`timeline.duplicate`](/home/user/work/agent/astrid/sdk/timeline/native_timeline_duplicate.py:49) requires fresh shot IDs and creates new physical shots.
- [`occurrence.place-shared`](/home/user/work/agent/astrid/sdk/timeline/native_occurrence_shared.py:97) requires an occurrence already in the destination timeline. Its arguments contain no cross-timeline source pin.
- `timeline.restructure` requires the current timeline’s authenticated closure.
- `doc.patch` prohibits changing managed occurrence membership and revision edges.

Thus the original first link—`other` referencing `main`’s existing physical `shot-1` revision—has no faithful registered carrier. Advancing the global head afterward cannot repair that missing edge. The registered inputs also provide no distinct inline/reference contract for this reuse.

**Owner:** Agent under existing G4 promises. The missing contract must retain the exact physical shot/internal revision pins from an authenticated cross-timeline source, distinguish the required source-input forms, and avoid recording an existing shot as a new birth. Runtime’s production guards remain unchanged; no new API or authority mechanism was introduced.

Original-to-current mapping remains:

| Original scenarios | Current fixture assessment |
|---|---|
| Unrelated destination ×4 | Preserved by prior review; untouched |
| HTTP F1 ×1 | Full code/message/details predicate still missing |
| Missing head ×2 | Inputs still differ only by name; new/retained revision distinction missing |
| Current update/exact retry ×1 | Preserved by prior review; untouched |
| Closure tamper ×5 | Preserved by prior review; untouched |
| Historical reuse ×2 | Local inverse substitution remains; cross-timeline coverage absent |
| Additional retired-route ×1 | Untouched |

Validation performed:

- In-memory AST parsing/compilation of original and current fixture: passed.
- Loaded `load_timeline_commit_provider("astrid")` and inspected actual registered handlers and parameter schemas: passed.
- `git diff --check`: passed; worktree clean.
- Pytest, Ruff and Pyright were not run: no meaningful fixture fix was possible, and unchanged known-deficient bodies were not rerun. No 16-case or zero-new-diagnostics qualification is claimed.

Runtime: `51c2d6aaccf29f8c9c261f54e2a5bfaa676ccff5`. Loaded Agent: `bc38aa3eb37008e97bcd85833ac9001eb6523d5f`. C0, production callers and guards are unchanged.

Wrote the required `commit-msg` and `BLOCKED`. Next: route the carrier/source-pin contract to Agent G4, then repair the three fixture gaps and run the required exact 16-case `--net` qualification.