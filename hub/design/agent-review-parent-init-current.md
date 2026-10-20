# Agent review: parent media and pristine initialization

Read-only independent owner review, 2026-10-20. No product fixes or repo process documents. No git mutation, push, dependency writes, full/full* or live-socket tests.

| Candidate | Verdict |
| --- | --- |
| `tl/agt-m2-parent-media-real-gap-fix` / `905cdcfaea512062f616d514035b2e9891331342` | **APPROVE bounded ordinary-parent source delta on current. HOLD standalone schema publication and producer/App cutover.** |
| `tl/agt-m2-pristine-initialize-native` / `487ca1e0d74edf4aecdd2b4e045294ab089fc273` | **APPROVE bounded Agent initialization source delta on current. HOLD App bootstrap retirement pending Runtime/App qualification.** |

No blocking product-code defect found in either bounded scope. PLAN decisions are unchanged. Tests used exact candidate archives and independently applied authored deltas over integration `73d8a237bc235aa9606b4f2a84e534aa9fa5f6b6`. Integration advanced to `86405964ecb713ad42a375f9de7960b3f9dc259b`: all seven intervening files are rendering/remotion extent code/tests, with no timeline SDK/schema or selected-test changes. Final inspected integration is `6a59522421a8a5c0e93fca080aa2d1fd478952f1`, adding trim precision/model/unit helpers, catalog/environment fixes and neighboring tests/docs. Those deltas were inspected; parent/init handlers, provider/recorder/inverse/schema and selected tests are unchanged. Both authored patches apply there with zero fuzz. Execution claims remain pinned to 73d8a237; later changes were not executed. Schema floors were checked against all three heads.

Parent: canonical closed `{row,media}` only; scalar completion constructs it. Explicit replacement uses assembled-target + after-boundary birth + delete and preserves original order. Missing registry/assets creation records storage shape and scoped writes; null/malformed/conflicting authority refuses; direct/config/equal mirrors and opaque siblings round-trip exactly. Real fresh bootstrap `registry:{}` missing-assets birth now passes, as does historical replacement with an unrelated child transition still present. Completely absent raw registry has native conformance coverage, not a manufactured actual historical baseline. Known child transition adjacency is local; unknown reference-bearing shapes and real declared dependencies still refuse. Actual selected-media custody, old immutable source tuple after primary promotion, collision, accepted dependents/ABA, reload, inverse/redo, retired identities and exact retry pass. Ordinary requests have no producer pin; these tests do not qualify an assembler proposal.

Init: matches actual App 1280x720@30/output.mp4/two explicit background nulls, exact name/slug and full V1/A1 rows. Four scoped missing-field writes, exact raw-empty guard, no root replacement. Authenticated original bootstrap history plus exact current base pair, rechecked after CAS races, prevents reapplication after edits or equal-byte undo. Actual create→restart→init→lost-ACK/restart→undo→original-key retry→redo passes; retry runs with provider and engine disabled. Durable Agent Outbox models caller intent, not an implemented App workflow. Same-ID headless repair remains Runtime-owned.

**Full-schema composition is required before freeze.** S2 is commit `26ef2bbb` / raw schema SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` (the a6f1aaa9 prefix is not a commit). Parent schema is 45 definitions/23 conditions and fails frozen S1/S2: missing five producer definitions, producer.guard and S2 optional element schema_source. Init is 49/23, preserving S2 additively. A review-only S2+parent+init schema is 51/25 and passes all retained/current/published floors. It was never substituted into service tests or published. Shared source paths are schema, commands.py and commit.py; retain both registrations/provider hunks, current capture inputs and current consumed guards. Do not copy a whole old candidate file or resolve the schema by selecting one side. Update init's per-candidate exact-count additive proof when composing the union, retaining every behavior.

Private versus public: Agent lock remains pinned to Runtime94114269 (0.2.9). Parent real tests use unchanged Runtime8609333's generic unknown-op envelope plus Agent's closed schema, not a typed generated public parent release. Init real tests archive pinned94114269. S2's generic media-free producer and the normal declared-file/upload experiment are not authentic assembler qualification; the normal host still has its old pre-settlement publisher. Keep old writers/positive tests until the complete generated pair and replacement journeys qualify.

Independent commands/results (exact full commands, working directories and logs in the detailed report):

- Candidate parent: **36 actual passed**; **309 neighboring passed, 5 existing strict xfailed**.
- Parent delta on current: **36 actual passed**; **596 neighboring/current-guard/schema passed, 5 existing strict xfailed**.
- Candidate init: **32 focused passed**, **1 actual passed**.
- Init delta on current: **32 focused passed**, **1 actual passed**.
- Full-schema containment: exact expected parent S1/S2 failures; init and illustrative union preserve c456b328/df2739f9/frozen S1/published Runtime0.2.10/S2/all three integration heads. Diff check passed; assigned worktree clean.

Actual tests instantiate RuntimeService in process with normal Agent provider; no schema override, fabricated acceptance, SQL-seeded history, lifecycle bypass, sockets or shared-dependency mutation. Xfails remain four deferred parent auto-placement cases and the separate assembler/requester case. No full suite, actual App, browser, HTTP Door, render, public-pair or joint feature execution is claimed.

Next: owner integrates authored source deltas, freezes complete reviewed successor, Runtime generates normally, consumers adopt that pair, then preserve and pass the original producer/repair/default/retry/undo/zero-legacy journeys before writer deletion.

Detailed absolute report: [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-parent-init-current/notes/report.md).
