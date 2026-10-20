# WC4 current-source gate — bounded approval, writer closure held

**APPROVE the bounded legacy-HOLD / native retry behavior on current source. HOLD the source candidate for unconditional integration, whole-writer deletion and WC4 closure.** Same-element PARAM still silently establishes current admission authority; the original selected-PARAM rule is proposed, not wired. This worker did not change that policy or claim its implementation. Keep this source on its worker branch pending the authority fix and review.

Current base: `9cb1090458428fb09067e359be92cdbb6608a206`. Sources reviewed: helper `a6098b5ddd1f3621e4467343875f705aab6c339e`; latest committed legacy correction `5aef6ac3c0f800386abaefe1b147f52680a79d05`. The latter adds only two product/two existing test file changes over a609 (323 added / 14 removed lines). Read the original P1 review, handoffs and settled original-pin rule; no decision was relitigated.

The narrow port applies read-only path diffs onto current 9cb10904 using `patch`, without Git mutation or integration edits. Four product paths match 5aef exactly. `sync.py` remains current and byte-identical: BOTH sheet-base and producer-pending guards survive before retry matching. Current duplicate correction 68a51203, history recovery, CLI trim, native sheet/checkout/frontends and safe13 artifacts survive unchanged.

## Qualified behavior

- Same raw selected element, no changed PARAM: HOLD emits only existing guarded `clip.set`, with no element reselection, admission read, portable read or save-time re-admission. Genuine digest-only original-admission fixtures pass normal Runtime013 acceptance, reload, inverse/redo and exact lost-ACK/restart retry. Explicit unchanged params keep their writes; this is compatibility evidence, not original-PARAM authority qualification.
- Actual revision reselection without portable snapshot visibly refuses `pack snapshot unavailable; re-admit pack`; explicit admission remains outside save. Genuine portable reselection retains native schema/snapshot/element binding and membership/order/identity guards.
- Original body/key are durable before POST. Old/new batch shapes retry exact frozen requests; changed target/key/base/intent and explicit native pin refuse. Acknowledged recovery uses original `base_revision_id`, including initially rebased acceptance, lost ACK, restart, pagination and disjoint newer head. Bool/number intent remains distinct; numeric equivalence remains valid.
- Raw aliases, opaque/mirror/order/registry/transcript/shot/internal data remain covered. Added six raw-HOLD replay/inverse guard cases and two current `_stage` guard cases pass.

## Remaining P1: implicit same-element PARAM reselection

`astrid/sdk/timeline_elements.py:24–49,185–202` still makes `[clip.set-element, clip.set-params]` for changed/clear-only PARAM on unchanged E. Independent actual Runtime probes establish accepted E/P1, then admit another element while retaining E byte-for-byte, yielding P2. Both fresh `seed=9` and clear-only `future` edits succeed using **P2/version 3**, instead of **accepted P1/version 2**. Required `element=` does not turn ordinary PARAM into an explicit user reselection.

Two new strict expected-failure main-suite probes retain success, exact P1 and PARAM-only expectations. Running them with `--runxfail` gives two genuine assertion failures on the source pin after real acceptance. No passing behavior test was weakened or relabelled. Native unchanged/clear-only/empty PARAM authority also remains unqualified under owner12:16. A refusal guard would prevent some unsafe edits but would not restore accepted-original-source PARAM success or implement the settled stage/head/lineage rule. No partial resolver, admission-as-old-authority, manifest-order winner, cache, new endpoint or browser validator was added.

**Do not treat the 75 passing actual cases as WC4 closure, and do not mark WC4 DELETED.** Integrate and qualify accepted-selection authority, then make these two strict expected failures pass normally before unconditional source approval.

## Evidence and immutable boundaries

| Evidence | Result |
| --- | --- |
| Independent original digest-only helper successes, before port | 2 passed (draft→admitted and same-selected); old transport mocked, real resolver/build/validator/preparation |
| Requested actual Runtime013 helper/schema/scalar cases | 75 passed + 2 new strict expected failures; exit 0 |
| Requested 359 neighbors plus 8 new raw/current guards | 367 passed; exit 0 |
| Current duplicate/native-sheet/frontends/CLI-trim/producer/schema checks | 186 passed; exit 0 |
| Central named commit-integration plus current HTTP trim/sheet/frontends | 20 passed; exit 0 |
| PARAM original-pin counterexamples under `--runxfail` | 2 failed at P2 != P1; exit 1, genuine held finding |
| Ruff and `git diff --check` | passed |

Central result: `agt-m2-wc4-current-source-gate-commit-integration-1020124824-22847`; exact final source tree `7989eac83b613e90cecdf036d3639c844fc99170`. No full/full* suite requested. No broad/full, browser/App, renderer/pixel/audio or macOS qualification.

Command-schema SHA256 is unchanged: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. Runtime remains immutable normal `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, contract 0.2.13. `runtime.lock.json`, generated clients/DTOs and `artifacts.json` are untouched. Protected-byte comparisons and exact hashes are in the detailed report/notes.

Exact source path diff (nine files; four product files net +152 lines):

```text
astrid/sdk/remote.py
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline_elements.py
tests/core/test_timeline_element_publication.py
tests/core/test_timeline_element_publication_runtime.py
tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json
tests/editing_conformance/test_recipe_clip_set_element.py
tests/sdk/test_timeline_sync.py
```

No shared dependency writes, other-worker writes, pin/schema mutations, ledger mutation or Git mutation by this worker. Private archive removed; only assigned source changes and worker notes remain. Task complete with no execution blocker; source/writer approval remains held for the concrete P1.

Detailed report, exact commands/results, run corrections and limits: [worker report](../workers/agt-m2-wc4-current-source-gate/notes/report.md). Patch, final diff, probes and logs are beside it. Recommended next step: implement the settled accepted-selection authority through existing Runtime port reads, preserve successful PARAM and exact retry behavior, then request a fresh source gate before any orchestrator merge/closure decision.
