## Verdict: REJECT for owner scanner 1.0.6 (sha256 `1df2ee0a…`)

The three 1.0.5 reject reasons are fixed. A new fail-open remains: a malformed look value makes the scan `complete` and silently drops the look.

Review written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-scanner-1.0.6.md`. DONE file created. No repo changes, no commit-msg.

## Inputs
- The archive's sha256 matches the metadata. Members were read in memory with `tarfile` under `venv-agent/bin/python -I -B`, and their hashes match the metadata. The flat `scanner.py`, `tests.py` and `conftest.py` copies match too.
- Code and tests were copied to my session scratchpad and run from there. The archive was never extracted or executed in place.

## Tests
- Command: `/home/user/work/venv-agent/bin/python -I -B -m pytest -q -p no:cacheprovider <scratch>/tests --agent-root /home/user/work/wt/agt-review-scanner-106`
- Result: **36 passed in 7.74s**.
- The Agent checkout was my worktree (`tl/agt-review-scanner-106`, head `481e600b`, clean), not the owner's extracted checkout.

## 1.0.5 reject reasons
1. **Audio-fade source paths: fixed.** Fade and curve paths are input-space (`…clips[n].params.fadeIn`, or `internal_timeline_revisions[i]…` for occurrence children). The parametrized test covers In/Out and payload/config layouts and passes.
2. **Malformed transitions: fixed.** `{"id": ["…"]}`, a string, and a nested `type` all give `incomplete` with an exact error and no raw value. My probes of `[]`, `{"id": ""}` and `{"id": null}` also gave `incomplete`.
3. **Duplicate internal revision ids: fixed.** The scanner raises on any repeated id, and the Agent projector also rejects it (`shot_composition_projection.py:531-532`). The test would fail if either row were silently chosen.

Re-checks passed: one projector call (`owner_film_cliplook_scan.py:549`), IDs-only output, canonical incoming transition, and `asset=None` clears.

## New blocker
`owner_film_cliplook_scan.py:600-602` swallows a `clip_fields.describe` exception and sets `described = {}`. There is no closure error and no `unknown` row. The comment claiming the look "remains unknown" is wrong.

Probe: `element-a` with `opacity: "bad"` gives `status: complete` with no errors. The clip vanishes from `media_look_inventory`, and its overlap finding is lost (11 → 10 findings). This breaks the README's rule that unreadable metadata is never clean.

Required fix: add a bounded `<source_path>.<look> is unreadable` closure error, add a test for a malformed look (asserting `incomplete`, the exact error, and no leaked value), and correct the comment.

## Not verified
- No owner closure and no run in the owner's qualified environment.
- Linux only.
- The describe fail-open is shown by the probe output and the code's `except`; I did not call `describe` directly because the sandbox blocked that command.
