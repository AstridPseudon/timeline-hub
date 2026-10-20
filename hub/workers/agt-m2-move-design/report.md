Published [PROPOSED M2 draft](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-move-draft.md), linked from `edit-recipe.md`. Updated coordination and App inbox; requested App review.

- Proposes one reusable `clip.move-set` operation plus existing track creation, with simultaneous planning and immutable capture.
- Maps all three original App success tests to concrete commands and acceptance results.
- Flags manager decisions on collision handling, equal-start boundaries, group/order inverse support, and frontend conformance wiring.
- `git diff --check`: passed. Python draft checks: passed for JSON, links, whitespace and fences. Product tests were not run; this is design-only.
- Repository remains clean. No product/test edits or git mutation. Required commit message written.

Next: App review, then Agent manager approval before freezing. Implementation remains gated on the real M1 path passing.