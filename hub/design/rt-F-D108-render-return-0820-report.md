## D108 render-return-0820 report

- Hardened the private candidate checker at the original path:
  `.../rt-F-D108-render-ready-0815/evidence/candidate/d108_render_rehearsal.py`
- Added strict binary, profile, binding, wheel/RECORD, source digest, installer manifest, service declaration, and exact applied-tree validation.
- Removed historical `f4ed`/`0013` defaults and undefined shell variables.
- Preparation remains truthful: `NOTRUN`; no install, service, render, browser, or ZIP was run.
- Missing inputs are named with Agent installer/staging ownership.

Tests:

- Compile: PASS
- Ruff: PASS
- Pyright: PASS, 0 errors
- Targeted pytest: `1 passed`
- Fake wrapper refusal: exit 2
- Fake Node hash mismatch: exit 2
- `git diff --check`: PASS; worktree clean

Evidence: [d108-render-return-0820 evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-render-return-0820/evidence/d108-render-return-checks.txt>)

Blocked until the Agent installer/staging owner supplies authentic profile, seven-key carrier, current Remotion installation, and exact applied deployment identities. Second independent review is still required.