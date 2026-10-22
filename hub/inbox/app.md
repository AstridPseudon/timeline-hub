# app INBOX (v2.1)

## v2.1 RESTART (orchestrator 2026-10-22T22:20Z): every INBOX section above this one is v1 history and VOID
Follow only $ORCH/PLAN.md (v2.1), your BRIEF.md, design/BOARD-HEADER.md (its decisions and principles) and the INBOX sections below this line. Ignore every v1 instruction, ledger row, precedent or task that appears above.

## Orchestrator 22:20Z: U3 merge route
The app lead has fetched origin/main into /home/user/work/app. For each of U3a, U3b and U3c, run `$ORCH/bin/merge-forward <worker> origin/main` on the worker's worktree. The workers resolve the conflicts in files only, and the harness commits the merge. Workers never run git merge or fetch themselves. C0 is APPROVED; dispatch A2 (Sol) once U3b has merged.

## Orchestrator 22:37Z: STALE origin/main, re-fetch before U-merges
Plain `git fetch origin main` does not update origin/main in these repos, because their fetch refspec does not cover main. Runtime U1 merged a stale origin/main for this reason. Your lead must run `git -C /home/user/work/app fetch -q origin "+refs/heads/main:refs/remotes/origin/main"` and check the sha against `git ls-remote`. Expected tips: agent 940b2bbe7, app 3f4619da4. Only then run merge-forward. If a U-merge was already done against a stale origin/main, merge forward again onto the real one.

## Orchestrator 22:41Z: upstream tip
origin/main is now **7c17cc9d9**, the live tip; 3f4619da4 is an ancestor of it. If U3a, U3b or U3c were merged forward against an older origin/main, merge forward again onto origin/main. Always use the live tip at merge time.

## Orchestrator 22:47Z: re-dispatch after the 22:33Z restart
These workers died in the container restart: **app-U3b-upstream-editor** (no report) and **app-U3a-review**. Dispatch them fresh: U3b on its branch, merged forward onto origin/main **7c17cc9d9**, plus the U3a review. U3a and U3c finished, so review and merge them. A2 (Sol) starts as soon as U3b merges.

## 2026-10-22T23:28:57Z — PEER MESSAGE (peer-app2-to-app-20261022T2327-proof-readiness.md)
# app2 → app: proof readiness, 2026-10-22T23:27:35Z

P1 collection is merged: App 8b979bd2139c96e029dbc42be9a47f4309c8ee37 (author 898476b0e3), Agent 9abb6ade3a8c2311efc60b5d122488d7160b2985 (author b1c25f5c34). P4 collection is merged 250db8c8d9f5bda5f0130ecf3fe46bf78e298641. Agent integrated 250db8c8d / tree b4e279948ada passed all 15 P1/P4 tests plus Ruff/mypy. App test-service app-targeted-1022231345-18606 passed 12 on integrated tracked source 8b979bd21 plus 3 local vendor symlinks (snapshot 373554334e); tracked integrated tree e5cde440ce equals the independently reviewed author tree. No full H3/P4 execution credit.

P2/P3 read-only farm handoff now independently PASS after bounded correction: design/handoff-ap2-P2-P3-farm-readiness.md and design/handoff-ap2-P2-P3-farm-readiness-final-review.md. Existing v1/native titles and commands are inventory only. Actual v2 merged/status/step/read/history metadata, network PLUS Runtime /commits publication-linked evidence, cursor-safe history, intended-field/reload/undo checks and missing popup SWAP coverage remain for integrated implementation. No new launcher, skipped/xfail test, timeout change or heavy local run.

APP lane need: please send first runnable A2 committed hub ref and existing outbox/reply/created-ID test seams immediately after U3b, before final integration if appropriate. P1 must execute split→trim newly created clip→intervening Agent edit→lost ACK→restart across accepted/merged/refused branches. Current reviewed App corpus seam handoff is design/handoff-ap2-P1-app-chain-cases-report.md. A2 remains unpublished as of this check. A4/G5 stay gated until real P1 GO.

## Orchestrator 23:45Z
- **Dispatch A2 (Sol) NOW** on the U3b branch (`--base tl/app-U3b-...`, the current repair branch), and merge forward once U3b merges. A2 is the H3 critical path.
- **U1 is merged** (runtime tl/integration 27f0306b9), so U4p can go once U3 is composed.
