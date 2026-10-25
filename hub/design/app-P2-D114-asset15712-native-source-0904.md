# D114/P2 report

Implemented the minimum App-only oracle correction for native asset Undo attribution.

- Exact mismatch: `data.steps[0].dependencies`
  - Old expected: `scope parent []`
  - Actual authoritative reply: field guards `parent.registry` and absent `parent.config.registry`
- Source owners:
  - Agent `_commit_patch.py:542-546`
  - Runtime `timeline_commit_auth.py:399-402`
- HTTP evidence: 2 commit POSTs returned 200; Undo was `accepted`. History and canonical reads returned 200.
- Changed only the two authorized test files; D113’s two-line change remains intact.
- Facts: `notes/asset15712-facts.json` and `.md`
- Commit message written; `DONE` created.

Tests:

- Receipt/neighbour suite: PASS, 4/4; receipt oracle 138/138.
- TypeScript checks: PASS, all three configs.
- ESLint changed paths: PASS.
- `git diff --check`: PASS.
- Semantic-oracle command: blocked by missing `@astrid/packs`; no dependency installation or mutation performed.
- Environment was Node v22.22.0; Node 20 was unavailable.

File SHA-256:

- Spec: `777966e…e7e` → `7cca782…d637`
- Support: `8247e9a…f8f` → `a093282…671e`

Recommended next step: independent review and ledger entry before merge, followed by the orchestrator’s permitted browser/service rerun.