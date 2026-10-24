## Report

Implemented the smallest public-wrapper compatibility fix:

- `parent_revision_id` now derives from Runtime’s authoritative `accepted_revision_id`.
- Added a complete-reply focused regression test.
- Preserved canonical document, receipt, steps, identity mapping, alias fork/media authority, and original fixture predicates.
- Commit message written to the required path.

Tests:

- Focused wrapper control: **1 passed**
- Alias/publication controls: **24 passed**
- Publication neighbors: **18 passed**
- Real media round-trip: **1 passed**
- Authoring bundle excluding retained original: **36 passed, 1 deselected**
- Ruff baseline: **2145/2145**
- Private mypy changed source: **passed**
- Vendor lock, artifact manifest, `git diff --check`: **passed**

Retained original integration test was run after the source correction. It passes the prior `KeyError` point, then fails because the unchanged fixture expects the pre-fork shot ID while the reviewed alias source correctly persists an `authoring-fork-*` ID. This conflicts with the passing alias oracle, so I did not weaken the assertion or alter alias semantics.

Marked `BLOCKED` with this evidence.