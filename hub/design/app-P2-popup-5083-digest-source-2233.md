## Report

- Exact cause: App’s JS canonicalizer turns retained `12000.0` into `12000`; Runtime/Agent Python canonical JSON preserves `12000.0`.
- Hashes:
  - Runtime/Agent authoritative: `sha256:dd264762d1813774416abcb3fbd7016de660aba94468278c039fffbe51a8b2c8`
  - Existing App helper: `sha256:446afd120855f6b8df8a67304d6b0d107f6e604c6bbcf5fee91e9345b3f15707`
- Prepared review-only patch: `/tmp/w-1ec0b221c9/review-p2-popup-digest.patch`
- Worktree restored clean at base `bceb0350326f22beefdde5c5ba275412bb09b419`.

Checks passed:

- Scoped ESLint.
- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` typechecks.
- `git diff --check`.
- Retained-response authoritative digest control.
- Mutated canonical field changes digest control.

No browser, service, full suite, or product changes run. The patch preserves all existing strict response, canonical-document, receipt, reload, undo, and guard assertions. Next step: independent review, then central targeted ADD/SWAP qualification.