<!-- app | 2026-10-22T22:34:56Z | dispatcher heartbeat 2s | live 2 (sol 0, luna 2, other 0) | busy30 4 | status age 12m -->
# app board, 2026-10-22T22:15:05Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream cloud/dev deletions, docs/config/supabase | Luna high | — | review | app-U3a-upstream-deletions; app-U3a-review | Targeted29 pass;10 collection failures; tsc/scripts blocked, not PASS | — |
| U3b | Upstream editor/gestures/save with outbox/transport retained | Luna high | — | doing | app-U3b-upstream-editor | Running Luna high; no integrated proof yet | — |
| U3c | Merge e2e harness with upstream QUICK tier | Luna high | — | review | app-U3c-upstream-quick-harness; app-U3c-review | Discovery5, lint/diff PASS; tsc blocked; behavior-retention review pending | — |
| U3 | Compose true upstream merge, then re-vendor merged Agent | Luna high | U3a/U3b/U3c reviewed, merged Agent source | todo | — | Current app integration c85da542; upstream target 2dca750a | — |
| U4p | Adopt regenerated Runtime client/schema | Luna high | U1, U3 | todo | — | Awaiting U1 regenerated tuple | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b/U3 | todo | — | C0 APPROVED22:15; waiting U3b; pending C0b amendments must remain compatible | — |
| A3 | Popup/placement/element/registerAsset through A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete TS executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
Blockers: Runtime/orchestrator: C0b adds per-step reads and provider effect records; A2 may build approved C0 now without hard-coding those out.
Blockers: Agent: U3 re-vendor needs the reviewed merged Agent U2 source; U4p additionally needs U1 regenerated client/schema.
Blockers: U3a review: deleted scripts/config still have surviving test consumers; awaiting exact final findings before one repair pass.
Blockers: App worker/composer: U3a targeted edge checks cannot resolve @banodoco/timeline-composition from current shared install; use private matching dependencies, never mutate shared installs.
Blockers: Farm: qualify U3 integrated baseline once composed; heavy tour/gate-5/full requests will be recorded here, with no local duplicates.
Next ready: U3a, U3b, U3c dispatched. On completion: independent Luna reviews, compose upstream merge and re-vendor; A2 immediately after C0 approval and U3 prerequisites.
