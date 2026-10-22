<!-- app | 2026-10-22T22:16:14Z | dispatcher heartbeat 2s | live 3 (sol 0, luna 3, other 0) | busy30 3 | status age 0m -->
# app board, 2026-10-22T22:15:05Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream cloud/dev deletions, docs/config/supabase | Luna high | — | doing | app-U3a-upstream-deletions | Running Luna high; no integrated proof yet | — |
| U3b | Upstream editor/gestures/save with outbox/transport retained | Luna high | — | doing | app-U3b-upstream-editor | Running Luna high; no integrated proof yet | — |
| U3c | Merge e2e harness with upstream QUICK tier | Luna high | — | doing | app-U3c-upstream-quick-harness | Running Luna high; discovery/targeted only; farm owns browser proof | — |
| U3 | Compose true upstream merge, then re-vendor merged Agent | Luna high | U3a/U3b/U3c reviewed, merged Agent source | todo | — | Current app integration c85da542; upstream target 2dca750a | — |
| U4p | Adopt regenerated Runtime client/schema | Luna high | U1, U3 | todo | — | Awaiting U1 regenerated tuple | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b/U3 | blocked:runtime | — | C0 NOT YET APPROVED in BOARD-HEADER; no contract implementation dispatched | — |
| A3 | Popup/placement/element/registerAsset through A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete TS executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
Blockers: Runtime/orchestrator: C0 approval gates A2. Existing draft is not implementation authority.
Blockers: Agent: U3 re-vendor needs the reviewed merged Agent U2 source; U4p additionally needs U1 regenerated client/schema.
Blockers: Farm: qualify U3 integrated baseline once composed; heavy tour/gate-5/full requests will be recorded here, with no local duplicates.
Next ready: U3a, U3b, U3c dispatched. On completion: independent Luna reviews, compose upstream merge and re-vendor; A2 immediately after C0 approval and U3 prerequisites.
