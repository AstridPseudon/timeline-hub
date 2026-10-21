# vw-m3-partial-crop-raw-evidence-retention-source-0916

## Result

READY for manager review. The smallest source/runner-only correction is complete.
No browser, helper, render, socket, central suite, or physical capture was
started.

The partial test now emits one compact JSON line after all existing assertions,
containing only its already-computed PNG hashes, crop tuples, natural pair
fractions, and planted scalar controls. The worker-owned future command captures
that line, copies the exact four PNGs and `inspection.json` from the owned
pytest scratch directory before cleanup, and verifies destination realpaths,
leaf links, regular-file link counts, distinct inodes, SHA-256, and bytewise
equality. The normal EXIT trap removes only ordinary scratch. The command's
pure `--retention-control` branch refuses foreign, symlink-leaf, and
symlink-ancestor destinations.

## Source change

- `tests/packs/rendering/presenter_crop_capture.py`: three added output-only
  lines at the end of `test_actual_registered_presenter_partial_crop_pixels`.
- No assertion was converted, removed, weakened, or duplicated.
- Capture collection remains exactly two tests. The future command selects only
  `test_actual_registered_presenter_partial_crop_pixels`; the explicit 799 px
  physical result is not replayed.
- The changed source SHA is
  `791bad8f50398c32e4f81798afa40b1f356db3cd61ac134b882294fcfdffd653`.

The command pins all four presenter-crop source/helper bytes, public13,
Node20.19.4, Chromium1194, artifact link absence, central grant, shared flock,
10 GiB floor, source cleanliness, and cleanup scopes. Optional
`ASTRID_EXPECTED_REVISION` and `ASTRID_EXPECTED_TREE` variables allow the
manager to add the post-harness commit/tree pin; the source-byte pins remain
mandatory because this worker cannot know the harness-created commit hash.

## Checks

- `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_presenter_crop_equivalence.py --basetemp=/tmp/vw-m3-partial-retention-pure`
  — **10 passed in 4.18s**. This was run with the pinned Node override,
  read-only runtime peers, and a temporary symlink in this worker checkout
  only; the symlink was removed afterward.
- `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_private_node_modules_staging.py --basetemp=/tmp/vw-m3-partial-retention-staging`
  — **3 passed in 0.08s**.
- `/home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/packs/rendering/presenter_crop_capture.py`
  — **2 tests collected in 0.18s**.
- `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-partial-crop-raw-evidence-retention-source-0916/COMMAND --retention-control`
  — **PASS**.
- `bash -n .../COMMAND` — **PASS**.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/presenter_crop_capture.py`
  — **All checks passed**.
- `git diff --check` — **PASS**.

Two earlier diagnostic attempts lacked the repository Runtime PYTHONPATH, then
lacked the renderer worktree's local dependency link; they failed at setup
before test behavior. The final run used only a temporary link in this worker
worktree to the existing read-only peer graph and removed it. No shared
dependency path was changed.

## Not run / next step

The partial physical case remains **NOT RUN by this worker**, as required.
The manager should review and register the exact command, supply the normal
central grant/flock and (if desired) the post-harness revision/tree variables,
then execute it once. It must not replay the unchanged explicit 799 px run.

