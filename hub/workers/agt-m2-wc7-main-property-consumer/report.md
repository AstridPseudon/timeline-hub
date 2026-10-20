Implemented WC7 consumer migration in `/home/user/work/wt/agt-m2-wc7-main-property-consumer` from `a760ecca`.

- Numeric detached clip moves now use existing `clip.move` via `TimelineSession`/outbox.
- Preserved rationale, reload, undo, and lost-ACK retry behavior.
- Property/annotated edits remain on the existing path; no ambiguous `hold` interception.
- Added bounded consumer regression test proving no legacy publication traffic.

Tests:

- `57 passed` targeted SDK suite.
- `13 passed, 1 skipped` checkout history/boundary suite.
- `git diff --check` passed.

Commit message written and `DONE` created.