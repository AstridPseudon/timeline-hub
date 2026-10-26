# F D141 Agent failure notes CAS — independent findings

Verdict: **PASS_EVIDENCE** for the requested read-only post-CAS installation review. This verdict is bounded to the supplied evidence and actual canonical delivery state; it is not a product, full-suite, REG0, service, build, ZIP, or continuous-history claim.

1. The actual canonical `delivery/README.template.md` is regular `0644`, 52,052 bytes, and SHA-256 `c39e4509a0829a15b6076192888de8c2a204fe02666d6e0654b4bc563fe82169`. The actual canonical `delivery/gate-results.md` is regular `0644`, 48,240 bytes, and SHA-256 `5b12901967d75e9e581b8a8ef6a5f27bde49d2a44c180b59abb772929d322399`.

2. Both canonical files equal the exact candidates. Their complete predecessor prefixes are preserved exactly: `60b938ff...42008f` for README and `7cacdb3d...2ddd7` for gate results. The same 3,241-byte factual suffix occurs exactly once in each candidate and is byte-identical between them.

3. The author’s 568-entry outside-file before/after maps are byte-for-byte equal, and an independent readback of all 568 current paths matched the after tuples (bytes, mode, SHA-256). Exact predecessor backups are present and hash to the required prefixes. The recorded author CAS controls report preimage guards, staged-file fsync, atomic replacement, directory fsync, and readback; this review did not repeat or alter that CAS.

4. The independent source accounting verifies the actual historical context separately from current qualification: 370 unique historical rows across 52 roots; final1051 has 9,798 records = 9,452 concrete + 346 null-ID aggregates; cut-bad is 397 = 378 `N_A` + 19 `FAILS_BOTH`; 64 `PRISTINE_ONLY` rows remain unresolved. `managed105=105` and `media48=48` remains nested/non-additive. Identity remains exact `node_id` equality only; missing IDs remain `UNKNOWN`, with no fuzzy rename or aggregate identity invention.

5. Current Agent evidence remains separate: integrated53 is 53 PASS / 0 failures / 0 errors / 0 skips at `ec0a9f5baef2c31bc5179087b83f044524575182` / tree `83b84c79941917fde535ee3ddba5533a776cace3`; the historical `ecdc` pair is not retargeted. The exact disposition counts are 9 qualified moves + 38 retained upstream-inverse purposes + 15 protected writer migrations + 2 owner-approved retirements, with kept53=53.

6. Prefix conservation retains the known gaps and original history, including SWAP and Element, the App 32-failure/collection-error/2-inherited-Node disclosure, the three inherited `AgentSetupCard` lint findings, App `fc24` conflict/upstream context, Runtime 7,300/35/18 history, custody/monitor limits, and the bounded-not-global language. No continuous history is invented, and the 53 result does not retire own failures or establish global behavior GO.

7. The production caller `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` was independently hash-checked at `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`. Its actual `render_readme` function was imported through the established source loader and called only with four controlled repo rows (`agent`, `runtime`, `app`, `composition`) and a missing-gate path. The fallback marker rendered, the candidate suffix rendered, no README was written, and CLI/main was not invoked. Earlier `render_box` evidence is not credited.

8. The author’s renderer-loader error before writes is retained as a disclosure. This review also discloses its own first-tool sampler gap: the task brief had already been read before sampling. A fresh ordinary sampler recorded three 5-second samples, minimum 4,932,874,240 available bytes (>4,000,000,000), PID 4, exit 0, waited and reaped. This is bounded monitor evidence and does not backfill first-tool or continuous-history coverage.

9. The original pre-CAS `check_join.py` was not modified and was not falsely required to pass the current post-CAS state. Independent post-state checks were used instead. No canonical/source/product/test/generated/pin/schema/kit/registry/hub/Git/Store/oldvenv/agent-remotion/KEEP/sealed1811/D130/refused-smoke mutation or merge request was made.

10. C0 remains normative as specified by the plan (request identity/base/commands/label/steps/merge/reads/idempotency/dry-run/source metadata and accepted/merged/conflict/invalid/preview replies). This documentary review is not wire input and does not claim a C0 transport exercise.
