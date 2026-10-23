# Handoff — ap2-P1-22122-evidence-review-1649

Evidence-quality review is **PASS with bounded loss**; actual selected App4c4/Agent98ef/Runtime259 P1 service result is **FAIL2**, exit 1, 510s, no GO.

Service log custody:

- path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P1-P2-P3-OPS-sol-1625-ap2-P1-chain-h6-1023163904-22122/log.txt`
- 85 lines / 27,606 bytes
- SHA-256 `770847ebd767dbca94e8559ed7f4b1df11e4dd17438acdac10f1e75ce38baa1c`
- command: `npm run test:e2e:three-products -- tests/e2e/local/three-products.p1-chain.spec.ts`

Exact boundaries:

- Case 1 reached accepted split, dependent trim, accepted Agent edit, merged trim, lost-ACK retry persistence, reload, restart, and reconnect through source line 893. It failed waiting for recovery POST at line 894; line 895 page-closed is secondary. Recovery state/cause is unknown.
- Case 2 reached accepted split and SourceIn trim setup, then line 943 expected two POSTs and observed one. Agent move at line 967 and all 409/refusal/rollback assertions were unreached. Do not infer Runtime 409.

Line 10 priority JSON is 5,370 bytes and parseable with no truncation/redaction markers. It records one observed commit, 13 summarized reads, projected split head, idle/no-intent/no-pending outbox, unknown connection, hidden recovery, no page/request failures, and four 503 console errors. Line 11 full diagnostics is capped at 16,384 bytes, has 2 truncation and 102 depth-redaction markers, and is not parseable. No mounted `dataRef`, SourceIn `from/at/hold`, capture/adoption, or recovery POST state is present; these remain UNKNOWN.

The sanitized flat priority projection is [handoff-ap2-P1-22122-evidence-review-1649-priority.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-22122-evidence-review-1649-priority.json). Principal/session-like identifiers and raw bodies are omitted; no credentials, Bearer/JWT, or auth-like patterns were found in the retained log. Original traces/error contexts are LOST from the service snapshot.

Read-only source qualification reused independent1538/1603 and OPS1625 by exact identity; no new tests or probes were run, no code changed, and no competing diagnosis or product fix is proposed. Full details are in the worker report at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-22122-evidence-review-1649/report.md`.
