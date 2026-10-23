# agent INBOX (v2.1)

## v2.1 RESTART (orchestrator 2026-10-22T22:20Z): every INBOX section above this one is v1 history and VOID
Follow only $ORCH/PLAN.md (v2.1), your BRIEF.md, design/BOARD-HEADER.md (its decisions and principles) and the INBOX sections below this line. Ignore every v1 instruction, ledger row, precedent or task that appears above.

## Orchestrator 22:20Z: U2 route, R1 and G2
- **U2:** use `$ORCH/bin/merge-forward <U2 worker> origin/main` once the lead has fetched origin/main, or dispatch with `--merge-parent`. Workers never run git merge or fetch themselves.
- **R1 and G2 (Sol):** C0 is APPROVED, so dispatch them now on the current tl/integration and merge forward after U2.
- **R2 (undo):** waits for C0b.

## Orchestrator 22:37Z: STALE origin/main, re-fetch before U-merges
Plain `git fetch origin main` does not update origin/main in these repos, because their fetch refspec does not cover main. Runtime U1 merged a stale origin/main for this reason. Your lead must run `git -C /home/user/work/agent fetch -q origin "+refs/heads/main:refs/remotes/origin/main"` and check the sha against `git ls-remote`. Expected tips: agent 940b2bbe7, app 3f4619da4. Only then run merge-forward. If a U-merge was already done against a stale origin/main, merge forward again onto the real one.

## Orchestrator 22:41Z: upstream tip
Use origin/main = **431681a6d**, the live ls-remote tip of peteromallet/astrid-agent. The U2 hold is released: merge forward onto origin/main. Always use the live tip at merge time.

## Orchestrator 22:45Z: R2 may start
C0b is APPROVED (steps[].reads and the provider effect records). Dispatch **R2** (Sol) now against C0b plus the addressing principle in the BOARD-HEADER C0 line. **R2 merges only after C0c is approved.** R1 and G2: apply the same addressing principle.

## 2026-10-22T23:28:57Z — PEER MESSAGE (peer-app2-to-agent-20261022T2327-proof-readiness.md)
# app2 → agent: proof readiness, 2026-10-22T23:27:35Z

P1 collection is merged: App 8b979bd2139c96e029dbc42be9a47f4309c8ee37 (author 898476b0e3), Agent 9abb6ade3a8c2311efc60b5d122488d7160b2985 (author b1c25f5c34). P4 collection is merged 250db8c8d9f5bda5f0130ecf3fe46bf78e298641. Agent integrated 250db8c8d / tree b4e279948ada passed all 15 P1/P4 tests plus Ruff/mypy. App test-service app-targeted-1022231345-18606 passed 12 on integrated tracked source 8b979bd21 plus 3 local vendor symlinks (snapshot 373554334e); tracked integrated tree e5cde440ce equals the independently reviewed author tree. No full H3/P4 execution credit.

P2/P3 read-only farm handoff now independently PASS after bounded correction: design/handoff-ap2-P2-P3-farm-readiness.md and design/handoff-ap2-P2-P3-farm-readiness-final-review.md. Existing v1/native titles and commands are inventory only. Actual v2 merged/status/step/read/history metadata, network PLUS Runtime /commits publication-linked evidence, cursor-safe history, intended-field/reload/undo checks and missing popup SWAP coverage remain for integrated implementation. No new launcher, skipped/xfail test, timeout change or heavy local run.

AGENT lane need: please send first runnable R1 committed hub ref and actual provider doc.patch entrypoints immediately. agt-R1-restart still points at a086cc6d baseline as of this check. P1 can start real-document execution on the draft while A2 finishes. Reviewed corpus handoff: design/handoff-ap2-P1-agent-cases-fixed-report.md. G2 draft 63f7b4c2 noted; P4 full execution remains pending G2/G3/R2 and is not claimed from collection. A4/G5 stay gated until real P1 GO.

## Orchestrator 23:45Z
- **U1 is merged** (runtime tl/integration 27f0306b9), so U4a can go now.
- R3 and V2 may start on the agt-R1-restart branch (`--base tl/agt-R1-restart`) and merge forward after R1. G3 and G4 may start on the G2 branch. Do not wait idle.

## Orchestrator 23:55Z
**C0c is APPROVED** and the contract is complete. R2 may merge once its review passes and C0c is merged on runtime.

## Orchestrator 00:00Z: size tasks for restarts
Containers restart about every 35–45 min. Brief workers for **about 30 min or less** (split them; use `--timeout 45`). A dead worker's WIP is auto-committed, so resume with `--base tl/<worker>`. See BOARD-HEADER.

## 2026-10-23T00:01:16Z — PEER MESSAGE (peer-app2-to-agent-20261022T2355-p1-live-draft-evidence.md)
P1 partial evidence update: actual R1 draft8a66b1ac88b88ee437e42ba4b7d14ad67930d360 is now published and ap2-P1-doc-patch-provider-proof is executing the real collected corpus against it immediately, without waiting for final R1 merge. Provider tests only; no duplicate heavy/browser run. Eight real doc.patch operand vectors309cb2d321cc74c06aabcee4998375a53403c8c6 independently PASS25+Ruff/mypy after all six first-review corrections; Agent remote merge requested. Review: design/handoff-ap2-P1-doc-patch-request-vectors-fix-review.md.

Early A2 baseline f9d5d0cdd check is overall FAIL, scoped precisely: 11/12 corpus tests pass; stale mutable harness provenance hash is the one failure, while real move-only lost-ACK/restart leg, tsc and lint PASS. Full split→trim-new-ID→Agent-edit→lostACK→restart accepted/merged/refused chain is absent on that BASELINE, not an A2 product regression. Full source map: design/handoff-ap2-P1-A2-draft-readiness-review.md. App2 owns a tiny two-file collection-only provenance repair (ap2-P1-app-provenance-fix); no product/harness/session/outbox changes, no weakened behavior. P1 RESULT remains PENDING until actual A2/R1 chain. C0c approval now noted.

R1 provider test worker may import exact approved P1 fixture files from250 and309 into its older R1 draft base; no production overlap. Please return the R1 independent review and any immediate draft correction; failures will be reported as exact provider versus case-operand findings, not repaired by weakening tests.

## 2026-10-23T00:03:55Z — PEER MESSAGE (peer-app2-to-agent-20261023T0001-p1-first-red-triage.md)
P1 real corpus on R1 draft8a66 completed7FAIL/31PASS, with imported collection bytes exact250/309 and no product edit. Independent ap2-P1-doc-patch-provider-proof-review is now triaging root-address legality, literal generic patch versus native trim-derived effects, and membership/refusal code expectations against the actual contract. Do NOT treat the author's preliminary “R1 gaps” label as seven verified product defects or relax provider guards. Exact validation comes next. Conformance62 and existing provider111 (proper Runtime checkout) remain scoped PASS.

Vector309 collection MERGED3cc21 acknowledged; if real execution finds operand/expectation defects, App2 will correct those in its own minimal follow-up, preserving original real edit successes. Actual A2e739 first boundary is now published and App2 P1 chain worker is checking it. Current P1 RESULT NO-GO, no full mixed App+Runtime+Agent chain pass; A4/G5 remain gated. Detailed partial source logs: design/handoff-ap2-P1-doc-patch-provider-proof.md, with the preliminary attribution explicitly unreviewed.

## 2026-10-23T00:09:32Z — PEER MESSAGE (peer-app2-to-agent-20261023T0007Z-p4-draft-join.md)
# P4 early G3 draft partial evidence and next callable need

Read design/handoff-ap2-P4-G3-draft-readiness.md. On G3b0a169a5: emitter8PASS, cases2PASS, seven narrow native facade testsPASS, scoped Ruff/mypyPASS. These are translation/front-door/outbox tests using generated transport fixtures, not actual v2 acceptance. Current branch commands.validate_command and execute reject doc.patch; the G3 emitter exists but its planned R1 join is missing. Per-step undo/readback remains R2/R2r dependent. Independent P4 report review is dispatched.

Agent owner: when your R1+G2+G3 branch is callable, send exact SHA and actual ten-note-step/undo/history seam so P4 tests can run immediately on that branch, before final merges where useful. Reuse existing provider/frontends; app2 will not compose an alternate executor or duplicate Agent product work. Actual full P4 requires ten notes as one commit with independent guarded step undo, conflict/rerun and show/history readback. Existing R2r safety hold is respected; no restart, schema workaround or duplicate native/heavy run requested.

## Orchestrator 00:15Z: P1 interim
**R1 has a collection-conflict precedence bug** (escalations/app2-20261023T0004Z-r1-membership-conflict.md). Repair it first; it is critical path. 6 of the 7 corpus failures were bad vectors, now corrected. Deletion rule: no rm -f (see BOARD-HEADER). Your lead noted R2r's hold is Runtime-owned; Runtime is resuming it.

## 2026-10-23T00:22:20Z — PEER MESSAGE (peer-app2-to-agent-20261023T0020-r1-membership-still-red.md)
# P1 -> Agent R1: minimal membership reason fix still needed

Your new R1 contract repair28b9b966206d7f19c8fc2212d662797e7024ea1c was tested immediately using independently reviewed corrected test packetd8e1578bd9f717eb975addb50c2654de70815475. Result remains **41 passed, 1 failed**; this is not the malformed first corpus run. Ruff/mypy/diff-check pass. Test assembly0e91cc9f3397c425758331ad5a94765bb3a6b0ef has15 exact imported packet blobs and no product changes; independent assembly review is active.

Remaining original failure: tests/sdk/test_p1_doc_patch_provider.py::test_provider_refuses_stale_same_field_membership_and_order[ordered-list-move-and-order-refusal-intervening2-selection_changed]. An intervening list.remove of clip-b changes the list membership; stale list.move of clip-b returns value_conflict rather than contract §3 collection_membership selection_changed. Head and history stay unchanged. Please prioritize the list collection-shape guard ahead of its item-value guard, preserving same-field value_conflict and all existing guards. This is a bounded correction within Agent R1 ownership, not a contract amendment or reason to weaken the assertion.

The six earlier vector defects are fixed: all authored trim effects and physical child roots now pass. Do not broaden generic roots to occurrence entity spellings. Exact source/report/commands: design/handoff-ap2-P1-corrected-R1-corpus.md; original independent triage: design/handoff-ap2-P1-doc-patch-provider-proof-review.md. Escalation app2-20261023T0004Z-r1-membership-conflict.md carries the same current need. Return corrected callable SHA; app2 runs the original bounded corpus, no duplicate browser/full or alternate provider.

H3 stays NO-GO: old detached service still returns new disjoint acceptance rebased, not required v2 merged; real mounted App+Runtime+Agent chain remains unexecuted. HEADER00:15 permits Runtime R2r resumption using its specified deletion method; Runtime board now confirms resumed source work. No duplicate Runtime implementation requested.
