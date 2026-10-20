## Report: agt-m2-shot-pool-sync

The merge-forward of `tl/integration` into `tl/agt-m2-shot-pool` is resolved and verified. The branch is ready for a gated merge. I did not commit or push; the harness commits when I exit.

### What I did
1. **Ran `merge-forward agt-m2-shot-pool-sync`.** Git reported one real conflict: `CONFLICT (file location)` on `design/m2-auto-placement.md`. The branch added it under the root `design/` directory, and integration moved contract docs to `docs/design/`. Git's rename detection placed the branch's version at `docs/design/m2-auto-placement.md`, and integration has no version of that path.
2. **Resolved the conflict.** I kept the branch's content at `docs/design/m2-auto-placement.md` and staged it. The file has no conflict markers. `design/` no longer exists, and `tests/reshape/test_repo_hygiene.py` passes (12 passed when run directly).
3. **Checked for stale references.** No file in the repo references `design/m2-auto-placement`, and no other removed `design/` path is referenced by a test or doc.
4. **Regenerated artifacts.** I ran `scripts/artifact_manifest.py` (162 artifacts) and `scripts/gen_cli_surface.py`. `artifacts.json` matches the staged merged state exactly, so there was no drift. `cli-surface.json` was unchanged. I ran both scripts with `--help`, which turned out to run them, and that regeneration is the same result I would have wanted anyway.
5. **Checked the other auto-merged files.** No other conflicts were reported. Integration's additions and the branch's `shot.pool` and auto-placement changes now sit together in the merge.

### Verification
Command, run through the central test service:
```
bin/request-test agt-m2-shot-pool-sync targeted --files "tests/editing_conformance tests/timeline tests/test_artifact_manifest.py tests/reshape/test_repo_hygiene.py"
```
Result (exit 0, tree `2c317415`):
**1821 passed, 4 skipped, 137 deselected, 3 xfailed, 173 subtests passed in 125.80s.**

No failures to classify. The "deselected" count (137) comes from the service's suite configuration. I did not check which tests are deselected, so I can't say whether any were in scope.

### Notes and open items
- **New xfail is inherited, not authored here.** The one `@pytest.mark.xfail(strict=True, raises=ImportError)` in the merge diff is in integration's new `tests/packs/rendering/test_normal_audio_source_phase.py`. It names its requirement (the normal_audio producer must translate the recorded origin) and is strict, so it is compliant with the no-weakening rule. I did not change it.
- **Decision:** I resolved the conflict by keeping the branch's content at the new `docs/design/` path rather than restoring `design/`. This follows the brief and integration's move.
- **Not run:** no full suite was requested, per the brief. Only the targeted set above was run.
- **Worktree hygiene:** `git status` shows no untracked or stray files. I did not use `rm-own` because I created no scratch files inside the worktree.

### Artifacts written
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shot-pool-sync/commit-msg`
- `DONE` marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-shot-pool-sync/DONE`

### Recommended next steps
- Re-submit the merge request to the gated queue. The `design/` conflict that refused it should be gone.
- Optionally run the `quick` or full named suite on the integration side after the gated merge, since the targeted set covers only the files the brief named.
