## Report: agt-viewing-reviews (partly blocked)

Items 3 and 4 are done and committed to the worktree. Items 1 and 2 could not be reviewed because their proposal files are not readable. I wrote `BLOCKED`, not `DONE`. The worktree changes and `commit-msg` are in place for the harness to commit on exit.

**1. Mouth proposal: no verdict.** `workers/vw-m3-mouth-proposal-preserve-known/{ORCHREPORT.md,proposal.patch}` does not exist in the orch workers dir or anywhere I could reach. The branch `tl/vw-m3-mouth-proposal-preserve-known` is at `751dd75e` (03:14Z), which is not the corrected proposal. I can neither approve nor reject it. The escalation's "approve by 03:25" deadline predates its 04:26Z timestamp, so the orchestrator should confirm whether approval is still needed.

**2. D09: HOLD (agrees with the escalation).** `tl/vw-m3-d09-current-deletion-unit` and `tl/vw-m3-d09-known-caller-preservation` both point at integration `4a75f68f`, with no D09 commit, and the patch is not readable. So the "does not erase M1" diff check could not be done. The unhold conditions are in `design/agent-review-viewing-20261020.md`. They cover the +80 netproduct item, trusted source/label forwarding, the SDK caller positives, and keeping M1 commits `a76c6537`, `a610cd30` and `d9a849e8` with their tests green.

**3. Popup rows: settled, no xfail needed.** I read the six rows as start, end and duration frames for each occurrence, since the brief did not define them. Frames: A `[0,240)` (duration 240), B `[240,540)` (duration 300). The clock is `fps_rational: [30, 1]`, and main's source is cited in the design doc. The brief's NaN premise did not reproduce. A `Fraction` gives the right frames. A `{num,den}` dict or `[num,den]` list raises `ValueError`. I updated the fixture and test accordingly.

**4. Fade `curve=`: honoured.** Main already stores the curve at `params.fadeInCurve` and `params.fadeOutCurve`, but playback never reads it. The public envelope reads the same keys. Three new vectors pass. The two prepared-envelope xfails now say the join must apply the curve. I also fixed a test bug: an absent dotted key was checked against top-level keys, so it could never fail. `design/owner-film-differences.md` lists v0.0.7 differences, which include transitions and element speed remap as well as the clip look. It also covers the continuous-gain note. The owner-film list is empty because no owner film was reachable, so it is not a clean result.

**Tests run (targeted, my own):**
```
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py -rxX
20 passed, 2 xfailed
```
Both xfails are the strict audio join vectors, unchanged in status. No full or browser suite was requested.

**Not verified:** no frames or PCM were rendered, and the pinned 0.0.8 artifact was not read. A `rm -rf` cleanup of my `.pytest_cache` and `__pycache__` was denied, so those gitignored caches remain in the worktree.
