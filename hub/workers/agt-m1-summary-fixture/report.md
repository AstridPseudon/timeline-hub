## Report

- Updated only `tests/packs/rendering/test_timeline_visualize_motion_views.py`.
- Added the existing committed `R1` snapshot-label fixture.
- Asserted exact provenance at `lines[1]`; preserved timing/tile checks at `lines[2]`.

Tests:

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_timeline_visualize_motion_views.py` — **31 passed, 2 skipped**
- `git diff --check` — passed
- Diff scope — exactly one test file

Known revision proof: existing `test_input_only_is_a_materializable_compact_filmstrip_bundle` fixture uses canonical committed revision `R1`.

Commit message written to the requested harness path.