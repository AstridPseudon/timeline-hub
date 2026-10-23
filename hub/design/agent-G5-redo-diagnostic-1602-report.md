# G5 corrected lossless diagnostic — agt-G5-redo-diagnostic-1602

Status: **FAIL / incomplete diagnostic**. The single authorized invocation ran once with the corrected lossless observer and timed out at 30 seconds (`exit 124`). No final artifact or redo verdict was produced. The durable packet was retained and exported; there was no retry, source repair, guard change, or owner attribution.

Locked source pair: Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`, Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`; preserved reproducer SHA-256 `153be3ff0db9e473bde9289e9964ea7900e8666713073677a8d4251c42c91740`; target body SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d` (6798 bytes); corrected observer SHA-256 `2188e04aeafd32e088f59438bac8efd56ff4a7cd67d80c8b8635a6c7010fb3d3`.

Evidence:

- [hashed packet](./agent-G5-redo-diagnostic-1602-6bb399e99e86ca41b78cd1a584f7fe06a6540f542eca6d3ddb2abd769452882d.packet.jsonl), SHA-256 `6bb399e99e86ca41b78cd1a584f7fe06a6540f542eca6d3ddb2abd769452882d`, 105 events / 1,105,098 bytes.
- [hashed manifest](./agent-G5-redo-diagnostic-1602-6bb399e99e86ca41b78cd1a584f7fe06a6540f542eca6d3ddb2abd769452882d.manifest.json), SHA-256 `b404aad160fd61660b373b0f08b3158aea6ece052ae74c3e424f9f0fc74dff13`.
- Worker report and preflight: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-diagnostic-1602/report.md` and `preflight.json`.

The packet preserves the observed `inverse-cut` full-v2 request and transport idempotency key, provider/port/guard observations, and canonical records/bindings/effects/dependencies reached before timeout. Final error, `theirs`, redo guard/preview/accept result, SQL no-write data, final origins/history aggregate, and precise owner are unavailable. No cause is inferred.

Exact offline checks passed: 10 preflight checks; `agent-G5-redo-capture-1552-lossless.py --offline-smoke` (`checks=5`); source compilation. Exact live command and all limits are recorded in the worker report and manifest. No pytest/P1–P4/full/native14/browser suite ran; no product files changed.
