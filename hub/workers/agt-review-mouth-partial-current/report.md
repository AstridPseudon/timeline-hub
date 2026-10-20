## Review complete: REQUEST CHANGES

Published [agent-review-mouth-partial-current.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-mouth-partial-current.md).

Key finding: `ee71010a0` changes valid default and raw-invalid presenter renders from KNOWN to UNKNOWN, contradicting the approved KNOWN-preserving behavior. Partial 697 compatibility geometry is valid only if kept distinct from semantic capability.

Evidence:

- SSR/semantic: 6 passed.
- Targeted: 55 passed, 2 existing esbuild skips.
- `git diff --check`: passed.
- Manifest check: expected failure; three presenter source entries require normal regeneration.
- No full suite, browser, physical capture, activation, or private crop/statistics deletion run.

No product files were modified. Worktree is clean. Commit message and `DONE` marker created.