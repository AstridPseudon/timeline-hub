# Root-join current-coverage audit

Verdict: ROOTJOIN READY under the orchestrator's accepted 08:20 CURRENT-coverage criterion. This is not a history-join claim.

## Source and coverage

- Current `tl/integration`/worker HEAD: `024f69501cfceb7f80d1c0c3fd26e6dd52568784`, tree `628286fa4d3128d53f2fc3a37fb3402b51d3232c`, 111 paths.
- Main `67b8aa3d0d6831d3e3504a340ff583c3da253707`, tree `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`, 29 paths.
- Four-tree union (main, original root `f9da6c0`, frozen R4 `c82eb7c`, current HEAD): 157 unique paths; TSV has 157 unique rows; table-minus-union and union-minus-table are both zero.
- Current-vs-main classification: 6 equal, 21 intentional/source-backed changes, 2 replaced absences. The two replaced paths are the retired `typescript/tests/scaffold.test.ts` and `typescript/tests/theme-api-smoke.ts`.
- Current HEAD's Makefile blob is `def553c6...`, identical to main, and is present through merge `024f69501` of the approved Makefile work. `.gitignore` and both tsconfigs are present in current HEAD.

Replacement ledger names:

- Registry/scaffold coverage: `scripts/gen-registry.test.mjs`, `typescript/tests/registries.test.ts`, and the public registry import in `scripts/smoke-package.mjs`.
- Theme API smoke coverage: `scripts/smoke-package.mjs`, `typescript/tests/theme.test.ts`, and the strict source/declaration build.
- Candidate extension status: `1ffb8d7` adds explicit `useTheme`, `AnimationReferenceList`, `THEME_PACKAGE_CLIP_TYPES`, and `THEME_PACKAGE_REGISTRY` consumer references; `44e9de5` adds runtime registry assertions. Neither candidate is in current HEAD, so this report does not claim those edits merged.

## Commands and results

Read-only enumeration and hash checks passed:

```sh
git ls-tree -r --name-only origin/main                 # 29
git ls-tree -r --name-only HEAD                       # 111
for ref in origin/main f9da6c0 c82eb7c HEAD; do git ls-tree -r --name-only "$ref"; done | sort -u | wc -l  # 157
awk -F '\t' 'NR>1{print $1}' design/composition-root-join-files.tsv | sort -u | wc -l                 # 157
git rev-parse origin/main:Makefile HEAD:Makefile      # identical def553c...
git merge-base origin/main HEAD                       # no SHA, exit 1 (join not performed)
```

No product tests, full suite, install, browser, socket, render, build, merge, push, or ref mutation was run. This worker only performed the requested source/tree audit and ORCH design/table updates.

## Lead handoff

After this coverage evidence, the lead must perform the authorized `ours` history join and verify unchanged tree, `git merge-base ... = 67b8aa3d...`, and `git merge --no-commit origin/main` cleanliness. The exact command block is in `design/composition-root-join.md`; this worker did not execute it.
