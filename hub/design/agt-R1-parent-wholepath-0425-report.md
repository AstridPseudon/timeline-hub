# F-D86 report

- Read PLAN, C0 §§2–3, board decisions, b415/4dcb/7e237, and current Agent/Runtime sources.
- Confirmed shared seam: `_registry()` captures `parent/collection:asset`; Runtime expects `scope,parent,[]`; current Agent projects `config/registry/assets`, causing strict-union mismatch.
- The same dependency list feeds rebase guards, so replacing it with the Runtime scope would restore broad parent conflicts. Exact producer representation requires owner decision; no source change made.
- Passing `doc.patch`/`clip.move` paths use atomic `timeline` scopes and do not exercise this alias.
- Exact b415 prepared dependency arrays were not retained: UNKNOWN. No Runtime attribution inferred.

Evidence: [source facts](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-parent-wholepath-0425/evidence/F-D86-parent-read-union-source-facts.md>)

Checks:

- In-memory compile: current, 4dcb, 7e237 — PASS.
- Ruff current/parent/candidate — PASS.
- Mypy current `_commit_patch.py` — PASS.
- `git diff --check` — PASS.
- No pytest, services, probes, or full suites run.

Commit message written; `DONE` created.