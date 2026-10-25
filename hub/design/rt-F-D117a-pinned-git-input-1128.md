## D117a report

- Fetched the exact OMP pin once via authorized git proxy:
  - Commit: `9e282751c0059e37d2f6fbc14ffa0b450710bd23`
  - Tree: `2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f`
  - Exit: `0`
  - `GIT_LFS_SKIP_SMUDGE=1`
  - LFS pointer blobs: `0`
- Existing installer `local_source` → `extract` path passed with exit `0`.
- OMP version: `17.4.0`
- Bun lock SHA-256: `f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee`
- Source-tree SHA-256: `3a84ac8be7d11434de8b22f4f0f1d643582ecc01c644e347bb0e056401da7b2e`
- Existing codeload archive SHA-256 retained separately: `ee8b3117370f6f2b3aa1a7f0f3ba8948113fb61fd1abc963b47cb82716c1bbdf`; no equivalence was inferred.

Checks:

- `git fsck --full`: no garbage.
- Installer Python AST and recipe JSON validation: passed.
- `git diff --check`: passed.
- No tests/typecheck/lint run; this was read-only source validation.
- No product, integration, manifest, pin, cache, or shared-dependency changes.

Stage was not run because exact applied Agent/Runtime deployment inputs were unavailable; using current or near-match sources would violate the brief. Evidence: [d117a-source-check.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D117a-pinned-git-input-1128/evidence/d117a-source-check.md), [d117a-source-receipt.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D117a-pinned-git-input-1128/evidence/d117a-source-receipt.json).

`DONE` and commit message were written.