## Verdict: APPROVE, bounded to the scene-label join the unit claims

The review is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-scene-current-owner.md`. I found no blocking defect. The D09 check half is not in this unit and stays open.

## What I checked

- **Scope:** merge-base with tl/integration is 931d7ec5, which is the current head, so there are no conflicts today. The diff is exactly the five paths in the handoff report, +811/-19.
- **Renderer-free save:** `host_frames_at` is reached only through the capture observer. `prepare_filmstrip` is called only by visualize paths.
- **Fail-closed callback:** the observer runs at `run.py:1169` on the final merged props. Any mismatch raises, the capture cleans up, and no cache or scene facts are kept. That matches the decided semantics.
- **Fresh-only labels:** only frames in the fresh copy set get scene labels, and only after the whole batch succeeds. Cache hits fall back to legacy labels.
- **Tests:** the named tests exist and the new file has no skip or xfail. The closure-source file is unchanged.

## Conditions

1. **Commit message count is wrong.** It says "201 passed"; the report's count is 229 passed / 9 xfailed. Fix it before commit.
2. **D09 check half is missing.** Only labels consume scene facts. Keep the check half open in the D09 record.
3. **PCM trap.** The observer requires the final timeline to equal the retained compiled unsliced timeline. If the PCM helper adds `audio.render_source` before `run.py:1169`, every composed capture with audio fails closed. Settle this when the PCM join lands.
4. **Production shape not verified.** The registry must equal the retained registry exactly, and the scene mapping depends on projector stamps. Check both against one real materialized capture.
5. **fps derivation changed** in `prepare_filmstrip`. Malformed canvases now raise instead of falling back to 30, and the envelope uses the builtin theme.
6. **Theme never reaches visualize.** No caller passes `theme_path`, so both sides use the builtin theme. This is consistent with the render but means the runtime theme is not used.

## Expected conflicts

- Not merged and touching the same files: `tl/vw-m3-scene-stage-four` (09cfd10a), `tl/vw-m3-uncertified-capture-labels` (2a862eaf), `tl/vw-m3-scene-stage-three` (7b8c4dc4). Whichever lands second conflicts with this unit. Do not merge two competing joins.
- PCM branches share no paths by name, but their planned `run.py` hunk sits next to the callback at 1169.

## Tests

I did not re-run the suites. My pytest run was refused by the sandbox for approval, and I did not work around it. The counts above are Viewing's, as cited in the handoff report.

## Housekeeping

- I wrote the DONE file, and the worktree is clean.
- `rm` was denied, so my scratch export and `candidate.tar` remain in `orch/workers/agt-review-scene-current-owner/`. They can be deleted by the orchestrator.
