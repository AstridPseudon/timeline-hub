# F-D108/D69 independent semantic predicate review

Status: **COMPLETE_WITH_RENDER_SCOPE_PENDING**.

Exactly the five assigned functions were reviewed source-only. Old source is `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, captured new source is `d6294843286c18e57af3c1874cf1996be42212d2`, and current normal source is `d0ecf1d69a7b37f86034bc52004f73f6c6231603`; all five current blobs equal captured-new. The original membership inputs remain authoritative and every assigned row ID/fingerprint is retained in the adjacent JSON/TSV.

| Result | Removed | Added | Total |
|---|---:|---:|---:|
| PASS | 18 | 47 | 65 |
| FAIL | 1 | 0 | 1 |
| UNRESOLVED | 2 | 0 | 2 |
| Assigned multiplicity | 21 | 47 | 68 |

The four runtime-client functions preserve their old successful mutation/read invariants. Receipt/result identity is a C0-approved strengthening. Film-history seed/refusal/database-no-write checks are additive under settled PLAN R5. No retirement was inferred beyond that rule.

The rendering function has the only pending semantic issue: the old `abs(source_mean - output_mean) <= 4` predicate intentionally tolerated Remotion encoding/colour-conversion shifts (captured-new lines 327–328), while current line 343 requires exact `source_frame == output_frame`. The old tolerance is **FAIL: actual purpose missing**; the strict replacement is **UNRESOLVED** pending owner scope. The old length predicate is only logically implied by that unresolved strict oracle. The other ten rendering additions are additive handoff/registry/timeline checks.

Evidence bases: PLAN §2 C0 replies, PLAN §3 R5, `agent-review-cutover-retired-writers.md`, `agt-F-D69-failures-render-1646.md`, and `peer-agent-to-runtime-orchestrator-20261025T0747Z-D69-assertion-owner.md`. No pytest, imports, probes, services, browsers, collectors, product edits, ledger edits, or foreign-output edits were performed. Behavioral qualification remains pending.
