## Completed

- CLI visualize now reports actual native/rendered revision identity; candidates and unavailable revisions remain explicit.
- Historical input-only reads pin and verify the requested immutable parent closure, without current-head metadata contamination.
- Added divergent-head and CLI label tests.

## Tests

- `python3 -m pytest -q ...` → **78 passed**, 2 environment warnings.
- `git diff --check` → passed.
- `make ruff` → blocked: `/usr/bin/python3` lacks `ruff`; direct Ruff found only existing baseline findings.
- Broader neighbour batch was interrupted after hanging; no full/socket/browser suite run.

Commit message written to the required path.