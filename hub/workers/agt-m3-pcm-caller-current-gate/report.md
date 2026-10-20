Implemented the exact approved four-file caller patch (`ebe571…5397`) and verified all four files byte-match `b6ec4922a`.

Tests:

- Focused caller/neighbor suite: `210 passed`
- Ruff approved scope: passed
- Central HTTP lane: 22 cases passed via private helper wrapper
- Broader `run.py` lint reports pre-existing unrelated findings; unchanged
- No full suite run

Deployment needs are documented: managed asset server, Remotion helper modules, public Composition 0.0.12 package graph, and Node 20.19.4.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-pcm-caller-current-gate/notes/report.md)

Commit message and `DONE` marker written.