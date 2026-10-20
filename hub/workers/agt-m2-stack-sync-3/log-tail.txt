`tl/agt-m2-stack-sync-3` now has the current `tl/integration` merged into stack-sync-2, and the targeted tests pass. The merge is uncommitted in my worktree, so the harness commits it when I exit. I wrote the commit message and the `DONE` file.

- **Conflict:** `merge-forward` left only `artifacts.json` conflicted (shown as `UU`). I couldn't run `git checkout --ours` because `.git` is read-only. I didn't need it: `scripts/artifact_manifest.py` rewrites the whole file, so I regenerated it instead, with no hand-merging.
- **Regeneration:** I first ran `scripts/gen_cli_surface.py`, which rewrote `cli-surface.json`. Then `scripts/artifact_manifest.py` wrote `artifacts.json` with 162 artifacts, and no conflict markers remain. I didn't run the script's `--check`. `tests/test_artifact_manifest.py` in the run below covers the same check.
- **Staging:** git still lists `artifacts.json` as unmerged (`UU`); I couldn't `git add` it (`.git` is read-only), so the harness's commit has to mark it resolved.
- **Hygiene:** the root `design/` directory does not exist, and neither `inverses.py` nor `core/extensions` is present.
- **Tests:** I requested the targeted suite from the test service with exactly the files you listed.
  - **Result:** 1743 passed, 4 skipped, 169 deselected, 3 xfailed, 173 subtests passed, in 132 s.
  - **Failures:** none, so nothing to classify as conflict-induced or pre-existing.

The `xfailed` count is from tests already marked in the merged tree. I didn't add or change any tests.
