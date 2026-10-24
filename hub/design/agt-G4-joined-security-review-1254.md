# D30 Report — FAIL

Reviewed stacked commits `19b81e1`, `1966156`, `fe53f81`. No product changes made; worktree remains clean.

Passing evidence:

- Authoring fork/continuation: 23 passed, 1 duplicate deselected.
- Original author command: 41 passed, 1 duplicate deselected.
- Native fork controls: 8 passed, including 7 forgery negatives.
- Reservation replay regression: 1 passed.
- Conformance: 79 passed, 1 integration test deselected.
- Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`: all passed.

Named failure: after a valid fork publication, a later valid reservation-creating `track.create` is refused with `history_unavailable`. `commit.py:838–842` compares the historical fork binding boundary (`bootstrap`) against the later request base (`publication-1`). This blocks legitimate reservation replay.

Durable XML and failure details: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-joined-security-review-1254/evidence/`

Next step: fix replay to validate each historical record against its own accepted predecessor boundary, then add and run a regression for a post-fork reservation commit.