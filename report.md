# Gate7 current extras actual-tree dryrun

## Result

The one central `delivery-owner-extras-actual` run was submitted after a
read-only freeze of the four-repository tuple and completed with exit 1 after
184 seconds. This is a classified private dryrun failure, not a final delivery
claim. The builder produced a retained staging directory with 12 files and no
ZIP.

Central request:

`rt-m4-gate7-current-extras-actual-tree-delivery-owner-extras-actual-1021013933-28953`

Installed carrier:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`

Carrier SHA-256:

`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`

## Frozen source tuple

Printed immediately before the request at `2026-10-21T01:39:33Z`; all source
worktrees were clean.

| repo | `tl/integration` commit | tree |
|---|---|---|
| Agent | `57d6635616f2982b814cfcc059b670ea1a7c9f2c` | `0174fd49bd175a726a44542d1d6e31bca13c0f02` |
| Runtime | `9d1c43c647301da48a6e86ad82e466b501bd2418` | `50e74e3243c5da4cf77b6e6cc76605fae8aeb649` |
| App | `813a85106ecb4abbaf224081abe6c33b8dab0df7` | `2a19a78bb1bdfb3fd779f568a1b513b094318982` |
| Composition | `4788e107f183e0523a740b691a20eb8261d7183c` | `585e8c4784ee78ccbfbff4b6ce26f577b8eda05e` |

Free space at freeze was `10,104,200 KiB` (`df -Pk`); the named light suite
passed the central service preflight. App remained shallow and its source Git
and borrowed dependencies were not modified by this worker.

## Exact command and verification

The existing allow-listed suite ran this exact command, including both guarded
extras:

```text
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --repos "agent runtime app composition" --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

Retained stage:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/build-20261021T013934Z`

The installed verifier reported:

| repo | patch tree | bundle tree | frozen source tree | result |
|---|---|---|---|---|
| Agent | `0174fd49bd17` | `0174fd49bd17` | `0174fd49bd17` | PASS |
| Runtime | `50e74e3243c5` | `50e74e3243c5` | `50e74e3243c5` | PASS |
| App | `2a19a78bb1bd` | `2a19a78bb1bd` | `2a19a78bb1bd` | FAIL: ref moved |
| Composition | `585e8c4784ee` | `585e8c4784ee` | `585e8c4784ee` | PASS |

For App, the builder explicitly recorded:

`tl/integration moved from pinned 813a85106ecb4abbaf224081abe6c33b8dab0df7 to 692765846fef511047445fecef3e55ec8bb6a5bf`

Thus the App patch/bundle/applied equality itself passed for the frozen tree,
but the source identity guard failed. This is the genuine remaining blocker;
the run was concurrent with an App integration ref update.

The stage contains the README, four bundles, four patches, SHA256SUMS, and the
two requested extras. `sha256sum -c SHA256SUMS` passed for all 11 non-self
members. The staged extras are byte-exact with the frozen inputs:

- scanner ZIP: `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- owner instructions: `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`

## Post-run source state and limits

After the run, read-only inspection found the App ref at
`692765846fef511047445fecef3e55ec8bb6a5bf` (tree
`e615c0a3aafca34504ba3544560de3887e4de38d`) and the Agent ref had also advanced
to `859d662f6f0cbe4a75b3d56c712b4f99edaad741` (tree
`36da43aed1d211f906abc78f76646b644cf6bf69`). Runtime remained `9d1c43c...`,
and Composition remained `4788e107...`; all source worktrees were clean.

No retry was made. No final ZIP, owner-film scan, browser/render run, macOS
check, physical parity check, or Gate7-complete assertion follows. A future
run requires an orchestrator-controlled freeze that keeps all four integration
refs fixed through the builder’s post-build identity checks, then a new
deliberate request.
