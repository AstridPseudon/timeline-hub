# AP2 P1/P2/P3 receipt-return-1410 handoff

Status: READY for one manager-queued changed preflight; no service/body qualification.

The three permitted rows now recognize the actual complete dispatcher receipt and verify its lock, installed Agent marker, immutable env Agent/Runtime declarations, package-lock, and Node 20.19.4/npm 10.8.2 toolchain. App is owner-merged 411ff10bd7043d55b4d83f2dfbbbd841af7b4806 / tree 0b19a5a9e33165b5fabe7d0425ae755aa58adfa2.

Tuple: Agent 8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe / tree c4d72b065d6e68c92e4335120cc016cadf53b06a; Runtime 8592822fd11275540f596562f43c715676f2bc0f / tree ed9856f43a4e44a058bf2230badea2c4c7080050; Remotion agent-remotion-ap2-current-8c355-1402.

Rows: 35 full-e2e-three-products, 36 ap2-P3-gate5-h6-0348, 37 ap2-P1-chain-h6.

Evidence:

- bash syntax: all three rows PASS.
- real published-artifact static preflight through the exact receipt/identity/toolchain checks and before global setup: P2/P3/P1 PASS.
- bounded offline controls: positive complete receipt accepted; failed/partial and wrong Agent/Runtime/env/lock identities refused.
- exact unchanged bodies: P1 blob 221d... / SHA-256 f28334...; Gate 5 blob 37caf... / SHA-256 0e69b...; P2 remains the three original files and eight selectors.
- row hashes: P2 82531afaddb9b3bc4fbc7a22a605eea7e1435274b32ce7e33ef9abd820957ff6; P3 b414a9c14122437ef6035c0e855cd5588f5042510177a15c33237a451511d4b0; P1 07e0d99e421653a301bb4ba0357b3abbe1f285c5f31902e4b1fee2003e9b2d86; outside-three-row hash 8adc8deedbd5e9c83da07e79ea7516dc386b2a670ea0adeae0e0446a4871b293.

The earlier service 6986 NOTREADY result remains preserved and is not reclassified; it stopped before global setup/body. No worker service request or live setup was made. Manager next step: queue one changed preflight run, preserving P1/P3 port serialization and all existing body/source guards.
