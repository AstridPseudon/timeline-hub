# Runtime reference-projection scoped-fix review

## APPROVE

Reviewed source commit `361fb911c7e1825bbe2f0c853e7b454a877f7040`, tree
`a429ebf5894ab705547495bbd657829ece84fa27`, against the rejected source
`4e562de0de44335ea29add039d1e0a6dfcfc3a64` and
`runtime-reference-projection-authority-review.md`.

The concrete fix closes the prior data-loss boundary without deleting the
legacy projection:

- `_prepare_reference_projection` derives candidate additions and removals
  from `_reference_projection_desired` over the accepted candidate closure and
  the accepted current-head/before closure. The caller records are ignored;
  project/timeline membership is checked by `revision_closure` and the
  projection queries.
- Candidate and prior identities are checked against exact
  `timeline_references` rows joined to their owning timeline/project. A
  mismatched occupied row refuses before persistence, including same-timeline
  mismatches and foreign-timeline identities.
- Duplicate occurrence bindings for one `reference_id` now refuse instead of
  coalescing. Missing/contradictory asset identities and out-of-manifest media
  custody remain fail-closed, including the existing normalization to the
  `sha256:` identity.
- Removal is limited to IDs proven by accepted prior provenance. Unproven
  same-timeline legacy rows are retained, and `timeline_reference_state`
  deletion is additionally guarded by the exact project/timeline reference
  row. The restore-shaped positive and revision snapshots remain intact.
- The original strict native-film positive remains OPEN; these fixtures do not
  claim native authoring qualification.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_reference_projection.py`
  — **9 passed**.
- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_projection_occupancy.py`
  — **18 passed**. This covers populated occupied, foreign, same-timeline,
  race, restore/source-proof and no-write cases.
- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_reference_authority.py -k 'service and not genuine_accepted'`
  — **72 passed, 73 deselected**.
- `git diff --check 4e562de0de44335ea29add039d1e0a6dfcfc3a64 361fb911c7e1825bbe2f0c853e7b454a877f7040`
  — passed.

No code, schema, DTO, pin, merge, or table changes were made. No full,
socket, browser, or broad suite was run.

