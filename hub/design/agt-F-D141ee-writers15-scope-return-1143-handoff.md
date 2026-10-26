# Handoff: U2 G4 G5 F D141ee writers15

Verdict: `SOURCE_SCOPE_CORRECTED_REG_PENDING`.

The packet corrects the prior accounting/action without mutating product or tests. IDs 4–18 are present exactly once. All 15 protected purposes remain REG-pending: none is a same-body/assertion current PASS, and none has an owner-approved retirement. The prior five-second historical sampler is not repaired or backfilled. Tests restored at `445b9c1` and merged at HOME `14ccf296f376` are not restored or rerun here.

Finite findings addressed:

1. F1: this worker owns the only credited sampler; `disk-trace.txt` is continuous through exit at five-second intervals with the 4,000,000,000-byte stop line.
2. F2: stale restore instructions are removed; the existing restored originals and targeted failures remain immutable evidence.
3. F3: live predicates are separated from old-interface literals. Current replacement selectors are proposals only; all remain REG-pending until exact assertions pass or MAIN records an exact retirement.
4. F4: row 7 is split. Key propagation, one-call, success/head, and authority remain protected; force=True forwarding is not adapted, and explicit force refusal remains mandatory.
5. F5: `_cmd_restructure` → `tl.publish` is a live wrapper call, but `_commit_restructure` and `_publish_narration` both submit through `TimelineSession`/`commitTimeline`. No second writer is proven. The bounded G4/G5 owner task is to preserve receipt/partial-failure/idempotency/no-retry on the actual caller if the wrapper is removed; no implementation is made here.
6. F6: row 8 keeps exact human-summary/JSON-envelope expectations unresolved; rows 12 and 13 remain distinct editor-head and generic-head actor cases with separate conflict-presenter decisions.
7. F7: Agent `publish_parent_composition` remains exposed and dispatchable, but Runtime’s implementation immediately refuses through `_require_timeline_command`. Runtime refusal and Agent-surface retirement are separate owner decisions; no old writer is revived.

Next bounded actions:

- MAIN/Agent owner: decide row 8 exact summary/envelope and rows 12/13 exact actor-specific diagnostics.
- Agent G4/G5 owner: verify the actual restructure/narration caller and preserve both parameterized partial-failure cases; if removing `_PublishMixin.publish`, migrate only to the existing commit-aware path with no new cache/interface/writer and no guard weakening.
- MAIN/Agent/Runtime owner: decide the exact retirement of the exposed `publish_parent_composition` compatibility surface separately from its already-proven Runtime refusal.
- After those decisions, one manager-owned targeted same-kind verification may classify rows as a rename/move only when the protected assertions actually pass. No unchanged test restoration is needed.

Unchanged holds: D130, 19479, 8912, Store/staging/KEEP/child holds. No safety or permission denial was encountered.
