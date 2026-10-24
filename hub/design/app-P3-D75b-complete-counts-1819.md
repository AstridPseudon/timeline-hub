## P3/D75b report

Implemented and applied the candidate on this branch.

- Retains both automatic-recovery mounts.
- Enforces exact ordered counts: observed `A,A,A,A,B` (5); forwarded `A,A,B` (3).
- Asserts exact body/key/URL/origin identity for every attempt.
- Preserves downstream B, history, canonical, preview, Agent, and guarded-undo assertions byte-exact.
- Added retained controls, evidence, hashes, and patch:
  - [three-products.spec.ts](/home/user/work/wt/app-P3-D75b-complete-counts-1819/tests/e2e/local/three-products.spec.ts)
  - [proposal-controls-v4.mjs](/home/user/work/wt/app-P3-D75b-complete-counts-1819/proposal-controls-v4.mjs)
  - [proposal-evidence-v4.txt](/home/user/work/wt/app-P3-D75b-complete-counts-1819/proposal-evidence-v4.txt)
  - [proposed-v4.patch](/home/user/work/wt/app-P3-D75b-complete-counts-1819/proposed-v4.patch)

Validation:

- Gate5 controls: 3/3 passed.
- Retained D75b controls: 4/4 passed.
- Virtual lint: zero diagnostics.
- Virtual types: 23 baseline / 23 candidate, zero new.
- Playwright list: exactly 15 cases; none executed.
- Patch/index and whitespace checks passed.
- No browser, service, original journey, or full suite run.

Commit message written to the requested path. `DONE` marker created.