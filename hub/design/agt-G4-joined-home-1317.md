## Report — PASS (scoped G4 joined proof)

Qualified current join `3db4af43ca`, tree `2e7f6ccb74`, with parents `9b055a93ff` and `23f60c4280`. Corrected prior tree fact: `9b055a93ff^{tree}=ed0043b057…`. No prior reports or tuples were rewritten/re-run.

Results:

- Combined authoring/fork/semantic, duplicate included: **34 passed**
- Authoring acceptance: **78 passed**
- Original authoring: **41 passed, 1 deselected**
- Native fork controls: **8 passed**, including seven negatives
- Replay/post-fork reservation: **2 passed**
- Conformance source lane: **79 passed, 1 policy integration deselected**
- Duplicate/source controls: **72 passed, 1 policy integration deselected**
- Ruff, mypy baseline comparison, vendor lock, artifact manifest, diff check: **PASS**
- Exactly two known mypy errors remain at `timeline_editing.py:525`
- Reviewed source/test blobs and protected ASTs: **byte/AST exact**
- Runtime: `becfe6db88…`, tree `7edc08e3…`, clean; canonical lock contains 15 matching files
- Agent and Runtime worktrees clean before/after

No full suite, gate, child-body, browser/live-socket run, or new realm was used.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-joined-home-1317/evidence/`

Commit message written; `DONE` marker present.