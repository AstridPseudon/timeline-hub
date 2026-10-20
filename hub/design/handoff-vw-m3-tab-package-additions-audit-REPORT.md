# App tab-package additions audit

Status: read-only recovery audit; no repair, deletion, install, grant, browser, socket, full-suite, or central run performed.

## Result

The supplied discovery-fix result identifies source `19c1f1f7b44a4c46a18db024a3c7d8042cc439fc` and one discovered test, but it must not be used with the old approved grant. The old grant comparison correctly fails for the intentional source identity change (`e421b5d4…` to `19c1f1f7…`) and for the package graph discrepancy: six package trees each contain one additional symlink entry:

| package | added tree entry | target | mtime (UTC) |
|---|---|---|---|
| `@playwright/test` | `test` | `/home/user/work/app/node_modules/@playwright/test` | `2026-10-20T07:57:23.781Z` |
| `@remotion/player` | `player` | `/home/user/work/app/node_modules/@remotion/player` | `2026-10-20T07:57:23.889Z` |
| `@remotion/media` | `media` | `/home/user/work/app/node_modules/@remotion/media` | `2026-10-20T07:57:23.881Z` |
| `@remotion/web-renderer` | `web-renderer` | `/home/user/work/app/node_modules/@remotion/web-renderer` | `2026-10-20T07:57:23.901Z` |
| `@remotion/layout-utils` | `layout-utils` | `/home/user/work/app/node_modules/@remotion/layout-utils` | `2026-10-20T07:57:23.873Z` |
| `@banodoco/timeline-composition` | `package` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-current-viewer-cut/overlay/public12/package` | `2026-10-20T07:57:23.560Z` |

All six are `symlink` entries under the controller's `hashTree` framing. The first five target their containing package root; the Composition entry targets the named overlay package path.

## Old-hash recovery diagnostic

The controller framing was reproduced exactly: recursively sort entries; hash regular-file bytes with their relative path and `file`/`executable` tag; hash symlink target bytes with its relative path and `symlink` tag; hash the JSON entry list. Only the six relative entries listed above were excluded, one from each affected package.

| package | current count/hash | filtered count/hash | approved old count/hash | restored |
|---|---:|---|---:|---|
| `@playwright/test` | 12 / `795ac395…a0538d` | 11 / `f60bd1f…05eb7e` | 11 / `f60bd1f…05eb7e` | yes |
| `@remotion/player` | 109 / `a1f42977…0d84b8` | 108 / `6de51351…68493d` | 108 / `6de51351…68493d` | yes |
| `@remotion/media` | 785 / `91aa5dca…dab69` | 784 / `7c7117a5…d112d4` | 784 / `7c7117a5…d112d4` | yes |
| `@remotion/web-renderer` | 97 / `eeadbf15…fc42c` | 96 / `cfa5ffb3…59544f` | 96 / `cfa5ffb3…59544f` | yes |
| `@remotion/layout-utils` | 14 / `6507524f…47f01` | 13 / `76a94579…59581a` | 13 / `76a94579…59581a` | yes |
| `@banodoco/timeline-composition` | 78 / `16c590b6…0ceccb` | 77 / `704827f4…86dffd4` | 77 / `704827f4…86dffd4` | yes |

With those same six exclusions, the full package graph hash is exactly the approved old `215e32c6fc86ba57ad36f766a273e43b8c9d328341308fafcda752b03e9eb858`. This is strong evidence of zero old-file byte corruption in the retained package entries. It does not establish historical mtimes, and it is not a license to alter the shared App `node_modules`.

The six added symlinks are newer than every retained entry in their respective package tree by `lstat` mtime. The current package graph, without exclusion, is the new fingerprint's `0de7e7a5318cfcb13483957178be1a09b16460952799e6c010836edc7ff9753a` and therefore correctly fails the old grant comparison.

## Other identity checks

- Source: old approved grant `e421b5d4438d8b27b689e9ae8c0218b7a30c68c6`; new discovery-fix source `19c1f1f7b44a4c46a18db024a3c7d8042cc439fc`.
- Source delta between those commits is one intended file only: `tests/e2e/timeline/tab-audio-capture.probe.ts`, 3 insertions and 2 deletions for the fixture destructuring fix.
- Tracked-file count remains 5,879.
- Node remains `v20.19.4`; Playwright core remains 106 files with the approved hash; Chrome remains 255 files; the six recorded Remotion/render hashes are unchanged in the supplied fingerprints.

## Safe lead recovery list

1. Keep the old grant and old fingerprint unchanged as the approved record; preserve the new fingerprint as a failed comparison, not a silent baseline.
2. If recovery is required, reproduce the six-entry exclusion only in a disposable/private dependency copy or an owner-controlled fresh environment. Do not delete or rewrite shared App `node_modules`, install packages, copy credentials, or run a live capability probe as part of this audit.
3. Before any future grant decision, require the exact six old package hashes/counts and old package-graph hash above, plus the intended new source SHA, to be reviewed by the manager/orchestrator.
4. Treat the source discovery result as the only completed new evidence: one Playwright test was listed. No browser, socket, grant, or capability result is claimed here.

## Verification commands

Read-only diagnostics run from the audit worktree:

```text
node (pinned /tmp/vw-m3-agent-gate-node20.19.4/bin/node) importing tests/e2e/timeline/tab-audio-capture.controller.mjs: packageGraphFingerprint and exact hashTree-compatible filtered hashes — passed; all six package hashes/counts and the old graph hash restored.
git diff --stat e421b5d4..19c1f1f7 — passed; one intended source file, 3 insertions/2 deletions.
git status --short --branch — passed; audit worktree clean.
```

No test suite was run because this task is a review-only dependency recovery audit and explicitly forbids browser/socket/full/central execution.
