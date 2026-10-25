# D139/D139a/D140 final source review

## Verdict

Source packet: **PASS** against all four blocking findings from review2300.

Actual request: **NOT_READY**. This is a separate, intentional status. The
packet contains no bound terminal child receipt, received kit, fresh manifest,
service ID, or durable core evidence, and D140 says Agent issues no child
request and Farm owns the future merged-tuple proof.

## Prior findings

1. **D139-SRC-001 — PASS, corrected.** The shell reference is unconditionally
   inert (`exit 0` at line 11). It has one future normal
   `request-test <worker-name> agent-core-full` reference and one matching
   `wait-test`; the `p4-d73` launcher is identified as service input, not a
   second manual execution. No executable `CORE_COMMAND` or launcher body is
   present.

2. **D139-SRC-002 — PASS, corrected.** Static inspection of the live
   `request-child-venv` source confirms it writes `queue/pending/childvenv-N`,
   prints that the result is in `queue/done`, and exits 0. The returned packet
   treats this as queue admission only and requires the same-key `done` or
   `refused` result, authentic maker provision report/stage stderr or
   `EXACTMISSING`, genuine Store child, and stop-first-refusal/no retry.

3. **D139-SRC-003 — PASS, corrected.** The returned packet preserves the
   one-time child admission `5905580032`, source floor `4600000000`, separate
   one-time core start `4700000000`, ongoing stop `4000000000`, one child
   request, one core service, and no other heavy work. It explicitly does not
   re-require the child floor after its own preparation.

4. **D139-SRC-004 — PASS, corrected.** The packet names the complete pending
   inventory: fresh API/source tuple, received regular non-symlink 0755 kit
   and hash, CAS, independent review, helper/checker, inventory, seal,
   registration/origins, Runtime client, installed module origins for all four
   tuple members, prooflock, dependency/input receipts, in-child check-only,
   fresh manifest, and durable XML/runner/same-ID/start-stop/KEEP custody.
   Unknown final values remain `UNBOUND`.

## Residual findings and Farm handoff

- No residual defect remains in the documentary source packet.
- The actual request is blocked by design until Farm binds every venue-owned
  `UNBOUND` field from fresh normal custody. Historical 1848 a4e/5e9
  manifests/receipts remain measurement evidence only and must not be
  retargeted.
- Farm must bind venue-dependent guards freshly: current four-checkout
  identity/API/source comparison, kit mode/hash, maker/request terminal
  records, registered child and origins, CAS/review/helper/checker, schema and
  dependency/input receipts, check-only, normal manifest, positive-17/poison-0
  controls, core service ID, and durable evidence/KEEP custody.
- D140 controls: Agent performs no child request and no retirement; Farm owns
  the future merged-tuple ship-grade child/core run.

The requested R4 path `/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4/`
was absent in this filesystem. The frozen refs were verified read-only, and
the available C0 contract copy was read from `/home/user/timeline-hub/hub/design/commit-v2.md`.
