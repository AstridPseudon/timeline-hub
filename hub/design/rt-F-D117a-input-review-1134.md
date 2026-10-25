## D117a report — PASS

Confirmed unchanged production seam:

`Installer.run` → `Backend.stage` → `install_tools(...)` → `_install_omp_source(...)` → `local_source(repo, sha, source.download)` → `extract(...)`.

Supported offline input is `tools.omp.source.repo` as an absolute local path or `file://` URL, with the exact pinned commit SHA.

Verified retained receipt:

- Commit: `9e282751c0059e37d2f6fbc14ffa0b450710bd23`
- Tree: `2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f`
- Fetch/local_source/extract exits: `0`
- LFS pointers: `0`
- Local archive hash and codeload hash remain distinct; no equivalence inferred.

Checks passed:

- Python AST validation
- Recipe JSON/pin validation
- Current installer hashes match retained source hashes
- `git diff --check`
- Evidence JSON parsing

No tests/typecheck/lint or stage were run. The temporary OMP artifact is absent; exact applied Agent/Runtime deployment inputs are unavailable, so full-stage profile, service argv, render, and peak footprint remain unverified. No source or product files changed.

Evidence: [d117a-input-review.md](/home/user/work/wt/rt-F-D117a-input-review-1134/evidence/d117a-input-review.md), [d117a-input-review.json](/home/user/work/wt/rt-F-D117a-input-review-1134/evidence/d117a-input-review.json).