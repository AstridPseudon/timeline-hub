# Qualified registered assembler requester handoff

2026-10-20. Worker `agt-m2-registered-proposal-requester`. Ready for orchestrator review/composition of this bounded requester unit. PLAN 4.1 remains the sole writer.

Exact qualified source tuple:

- Worker source: `/home/user/work/wt/agt-m2-registered-proposal-requester`, branch `tl/agt-m2-registered-proposal-requester`, base `0536d2467aa73bb89d16657bc21fd9b856a4a149`.
- Final central source tree: **`4c000d64c9048910889266f00fd4036a47ffebd3`**. The harness has not yet committed this worker's changes; this is a source-tree identity, not a claimed release/source lock.
- Private native Agent parent: `b5cfce5096f91f39bfb86d39823f97f0f59ce8a2`, with the exact current overlays listed by `tests/helpers/registered_native_pair.py`. It retains reviewed native parent media and producer semantics and the complete 53-definition candidate including FULL S2. This worker's complete `sync.py` is overlaid, preserving reviewed queue_proposal and adding the existing admission/current requester behavior.
- Private Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Private generator input contract version: `0.2.14`.
- Full candidate schema SHA256: `fafb1985a326e6121aa8c9fb34bbda196edc3dfaf462352070372e631bea1f52`.
- Normally generated artifact manifest: `sha256:48c7b6533e2774a70e36517948a18fd5cee07f4d30e8f339776be9b3ec74ed4e`, all 75 artifact hashes checked. Normal Python/TypeScript generation and all generator/manifest check modes pass. No partial schema, hand-built artifact, public version mutation or fabricated source identity.

Product overlay SHA256 values (unprefixed):

```json
{
  "astrid/core/contracts/runtime_orchestration.py": "7da83b80b1141348417238c3d9eee5058fd672d0cff52536dce2bff451dc0b3d",
  "astrid/core/execution/generic_host.py": "ef68542086b59bfa12d5477dfadbc4b6df3fd559748d6438e0dd88e4050ced9a",
  "astrid/packs/rendering/actions/assemble_timeline/run.py": "b59df505beae43812cce1af7d5f1252521df7924b1a1ee53cbdadcea52c49e64",
  "astrid/packs/rendering/pack.yaml": "c5f26f604b2059eeb98c3ef7d9f7b5bf28d781ec8f4c7cd16942baf2eb3c02fb",
  "astrid/sdk/timeline/assembly.py": "7da21b3dab0e7665bd59ca19b71741cade724fab29b411e43bec3b11b0b3b066",
  "astrid/sdk/timeline/sync.py": "f209d406096f15334eeff48af3caed482f5837cd0df78a4622e08336d3592c31",
  "astrid/sdk/workspace_client.py": "d5108617b35c88d04de72ca616148da6603f0ecceb914b692f8f94ce9951ee4b"
}
```

Existing API consumption: authorized TimelineSession admits `rendering.assemble_timeline`, then calls `queue_assembly(task_id, attempt_id=...)` on the exact completed registered task/attempt. The requester reads public getTask plus task-scoped managed outputs, requires the declared authoring_proposal association with exact provenance, downloads/hashes its object bytes, strictly decodes/validates the frozen SettledProducerProposal and verifies its inner digest. It calls existing `queue_proposal` and `flush`; only the requester sends the normal `/v1/projects/{project}/timelines/{timeline}/commit`. Runtime atomically rechecks settled producer authority. The worker never commits or publishes.

Final evidence: central request `agt-m2-registered-proposal-requester-identity-pin94114269-integration-1020124516-25049`, exit 0; inner **9 passed, 2 xfailed**, outer **4 passed** (three unchanged identity controls plus private wrapper). It proves authenticated HTTP createTimeline, original authorized admission, actual registered action and normal file settlement, native acceptance and immutable history, distinct and duplicate CAS order, original-base disjoint rebase versus real membership conflict after admission/before settlement, request ACK loss followed by requester+Runtime restart and byte-exact retry, changed value/rationale/digest/key refusal, cancellation/read-boundary tampering refusal, complete exact undo preserving the peer label edit, and guarded inverse refusal after a peer edits a born clip. The two legacy completion positives retain their unchanged strict xfails.

Run through the central service (no full suite):

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test agt-m2-registered-proposal-requester identity-pin94114269-integration --files tests/packs/rendering/test_registered_native_pair.py
$ORCH/bin/wait-test agt-m2-registered-proposal-requester-identity-pin94114269-integration-1020124516-25049
```

Local focused requester/neighbour tests: **123 passed, 1 xfailed**; Ruff and `git diff --check` pass. Exact commands/development results are in the worker report.

Named remaining requirement: **registered assembler admission ACK recovery requires the original create body/key durably retained in the existing outbox before send**. This is NOT qualified. A new strict xfail keeps the expected exact original-body retry across admission ACK loss/restart live, without imposing a new outbox field or journal. The qualified restart above begins after the settled proposal is queued and the normal commit flight is durable.

No new Runtime consumer gap on the reviewed pair. This is private native-cohort qualification; public native release activation must compose reviewed source/schema/generated artifacts normally. It is not render restoration: STITCH aliases remain rendering.render, the legacy hook is not deleted, and render admission/ACK recovery, historical render, film decode and pixel/audio parity remain separate. Do not close D13 or the held legacy completion requirements from file production/native authoring acceptance.

Next steps: review/compose this requester patch with the reviewed native full-schema/source cohort; solve original assembler task-create durability using the existing outbox; qualify render separately before restoring claims or deleting its legacy path.

Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-registered-proposal-requester/notes/report.md`.
