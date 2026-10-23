# P1 / D25 independent actual-result handoff

**FINAL: evidence-quality FAIL; no-weakening PASS; actual P1 FAIL (1 PASS / 1 FAIL); causal result INSUFFICIENT EVIDENCE.**

Exact run: `app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607`, `--no-cache`, App `2107e1870e51c650d59315f4cc1ab6af338f198c` / tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`, Agent `787/treee77ea`, Runtime `2a9/treef79a`, exit 1, 744 s.

Observed facts:

- Original 1055 PASS, 27.4 s: accepted split, merged trim, Agent edit, lost ACK, reload/restart, exact retry, and all body/key/owner/auth-scope/receipt/history/drain/legacy guards.
- Original 1223 FAIL: expected 2 POSTs, observed 1; 300 s test timeout plus 300 s `afterEach` timeout. Agent move, refusal 409, and rollback were unreached.
- First body hash `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`; second `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`; both match the independent 1906 mapping.
- Expected raw log: `tests/app-P1-local-OPS-1830-ap2-P1-chain-h6-1023185313-18607/log.txt`, 26,440 bytes, SHA-256 `a83cc89c1909877b7f01dfe4c83e994a31b8450afae80767a01e87781bf3728b`.

Custody status is not PASS: the 1909 exporter mutated the retained log to 18,661 bytes before publication; the orchestrator stopped it and requires exact-hash restoration. The safe flat markdown/JSON packet is not published/available for direct validation. The console source is capped and has no artifact writer, so a summary or capped log cannot substitute for parseable retained safe JSON. Missing fields include exact byte/hash/source-phase-timestamp verification and correlated `SourceIn`, selected ID, callback patch, capture resolution, mounted head/basis, owner, recovery, and explicit losses.

The second case proves only the no-second-POST observation before timeout. It does not prove a product seam. The old idle case-2/503 evidence cannot be reassigned to case 1 because it has a different case and phase. The new first PASS proves current automatic replay, not historical cause, and does not permit dropping exact POST/body/key/history guards. The 300 s `afterEach` hang is a diagnostic collection limit and must remain reported without changing assertions or timeout expectations.

Next owner: App restores and hash-verifies the original raw result, then publishes the safe normal-flat packet; Proof re-reviews that exact packet. Until then P1 is NO-GO. No duplicate body/service, guessed Runtime behavior, head chase, or product repair is authorized by this evidence.
