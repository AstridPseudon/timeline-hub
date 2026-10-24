# D30 Report — PASS

Reviewed stack `19b81e1 → 1966156 → fe53f81 → 156f2eb` read-only. No source changes; worktree clean.

Source identities:

- HEAD: `156f2ebba9eef2f13b3334f1c28405c9dabc03f2`
- Tree: `2e345cd208ee048538976e00e8b13f7b1cf572db`
- `commit.py`: `0cc24223…` → `f78c8f0e…`
- Replay test: `44f5758b…` → `7a4b8f663…`

Results:

- Replay controls: **2 passed**
- Authoring/fork/semantic: **33 passed, 1 deselected**
- Original authoring fork: **41 passed, 1 deselected**
- Native fork: **8 passed**, including 7 negative cases
- Conformance: **79 passed, 1 integration deselected**
- Post-fork reservation: old `history_unavailable` reproduced from prior exact evidence; new path accepted and preserved parent occurrences, source shots, and internal timelines.
- Ruff, mypy, vendor lock, artifact manifest, diff check: **PASS**
- Protected original ASTs: **exact**
- Production caller confirmed through `publish_authoring_candidate → writer.commit_timeline`.

XML evidence retained under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-reservation-security-review-1304/evidence/`

No blockers. No full, gate, or child suite run.