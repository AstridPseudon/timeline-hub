## Changes

- Enforced exact immutable readback via `bundle.base_parent.revision_id`.
- Strictly validated frozen history pages, ancestry, heads, publications, and cursors.
- Removed private generated-client access and guessed head APIs.
- Added malformed/cycle/duplicate/gap/changing-head/readback tests.
- Commit message written to the requested path.

## Tests

- Targeted: `38 passed`
- Neighbours: `166 passed, 1 skipped`
- Ruff: passed
- `git diff --check`: passed

No full suite run, per instructions. No blockers.

Net diff: `+126` lines.