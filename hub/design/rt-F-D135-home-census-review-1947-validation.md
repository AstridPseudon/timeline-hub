# Validation

Task: `rt-F-D135-home-census-review-1947`. Source-only review; implementation lint/tests are N/A.

## Result

PASS. The independent review is recorded in `evidence/review.json` and the literal conflict-marker crosswalk is recorded in `evidence/actual-conflict-map.json`. The original inputs under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-tail-Agent-retarget-1939/evidence/` were not modified.

## Exact read-only verification commands and results

- `git -C /home/user/peteromallet/astrid-agent show-ref` plus `git rev-parse` on the authority refs: PASS. `refs/remotes/hub/timeline/agent/tl/integration` and `refs/remotes/hub/tl/integration` resolve to `a30e74e901a28b39c28facba3deb00d76f186e23` / tree `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`; local `refs/heads/tl/integration` is stale `547e10456250c1b5bcf63b44a50c90ff0563ce1e`.
- `git -C /home/user/peteromallet/astrid-agent merge-base a30e74e901a28b39c28facba3deb00d76f186e23 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`: PASS, `92443771676ef2bbb547d0a103d708fa8bec4c63`.
- `git -C /home/user/peteromallet/astrid-agent merge-tree --trivial-merge 92443771676ef2bbb547d0a103d708fa8bec4c63 a30e74e901a28b39c28facba3deb00d76f186e23 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`: PASS/read-only, 583973 bytes, SHA-256 `641d298edc9a34bd0618b5d0f1e07d7c5fba6ee67a8e2101edc9c593ee888284`.
- `git diff --name-only` from base to actual home/upstream: PASS, 928 / 98 paths.
- Direct `git diff --unified=0` over the 41 changed-in-both paths: PASS, 92 ours hunk headers / 190 upstream hunk headers.
- `git cherry -v 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55 a30e74e901a28b39c28facba3deb00d76f186e23`: PASS, 0 minus / 725 plus.
- Recorded blob crosswalk loop using `git rev-parse <commit>:<path>` for every census row: PASS, 41 rows and 0 mismatches.
- Source object loop using `git cat-file -e <commit>^{commit}` and `<tree>^{tree}`: PASS, 5 objects and 0 missing.
- Captured merge-tree marker scan: PASS, 7 literal marker blocks across 6 paths. The 41 changed-in-both paths / 107 preview hunks are not all marker conflicts; `tests/test_installer_windows_tasks.py` has zero literal markers.
- Classification partition check: PASS, exact 38 + partial 2 + new 1 = 41 unique paths; old first20 remains 20 exact and old last20 remains 18 exact plus 2 partial.
- Active future `547e...` correction review: PASS. Evidence/provenance references remain historical; executable delivery-build and future ZIP-tail inputs are the stale-tip risk and require explicit D59 tuple binding. D59 remains pending.

## N/A and boundaries

No product implementation, proposer patch, source merge, checkout, rebase, fetch, network, clone, ref update, pin, ZIP, store, E2E, core, full suite, lint, typecheck, or implementation test was run; those are out of scope for this source-only review. No source objects or author evidence were changed. Final lead freshness check and the concrete D59 production tuple remain owed.

