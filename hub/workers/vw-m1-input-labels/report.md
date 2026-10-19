Implemented input-only revision labels and artifact provenance.

- Uses immutable `metadata.parent_revision_id` only for the strict input-only closure shape.
- Candidate labels use only `working_copy.base_parent`; contradictory bases remain unavailable.
- Added consistent revision labels to JSON, Markdown, normal PNGs, input-only PNGs, and contact/paired surfaces.
- Added representative historical/candidate and artifact tests.

Tests:

- Requested targeted suite: 99 passed.
- Adjacent filmstrip/overview tests: 52 passed.
- `git diff tl/integration --check`: passed.

No full suite or live Runtime journey run. Commit message written to the requested path.