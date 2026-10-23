# Runtime R2r sequential owner review handoff

## Disposition

**FAIL qualification / PASS Runtime refusal.** Runtime 859 is correct to reject the moved-head normal sequential request at `invalid_records: provider alias is outside its authenticated boundary`. The held Agent candidate is not qualified: its private original source-bound execution proof is not carried into the prepared provider result consumed by Runtime.

The original staged physical ID is not an accepted-history successor. Do not waive the boundary, retarget by bytes/entity ID/newest revision, or invent a continuation. This is normal sequential replay, not inverse-leaf materialization.

## Source causality

Runtime receives `provider.commit(provider_context, port)` only. The provider context is the request context (`request`, invocation identity, request hash, idempotency key, publisher and realm); the port is an authenticated read/capture interface. Runtime does not receive Agent's local `original` plan or `replay_bindings` map.

Agent's current path is:

- `astrid/sdk/timeline/commit.py:1072-1076`: execute original plan;
- `:1110-1122`: calculate `rebase_patch(...)`, then replay with `replay_bindings`;
- `:1159-1173`: serialize only the current landing `plan` via `prepared_records(plan)`;
- `:1175-1181`: pass that prepared result to `port.preview/accept`.

The packet's `current_capture` shows the original and landing executions, but is not an execution carrier. It cannot authorize Runtime to use those offline JSON fields.

## Exact proof required

Agent/provider must carry a trusted source-bound capture for each sequential command/step, not merely the caller's staged alias:

- original/base physical ref and exact revision/content digest;
- original source step ID, command ordinal and change ordinal;
- original base/evaluated-head pair;
- owner and complete owner set, plus managed edge-before/edge-after;
- exact original read/patch-before state and dependency/effect custody;
- corresponding landing physical ref, revision/content digest, landing boundary and the same ordinals/owner/edge facts.

Runtime can then verify original sequence against base plus preceding commands, and independently verify the corresponding landing sequence against the actual head plus preceding landed commands. The accepted-history continuation map remains only for accepted publications; it must not be extended with an unlanded staged ID.

## Bounded code seam after proof arrives

Runtime-only verification remains in existing code: `runtime_protocol/timeline_commit_auth.py:306-350,353-454,1342-1418`, with history continuation construction in `runtime_protocol/timeline_commit_store.py:752-764`. The current `validate_step` normalizes submitted step reads/claims against `boundary` at lines 309/344, not the per-command `command_boundary`, and `validate_bindings` checks the original alias only for `ordinal == 0` at lines 399-403. A fix must use the supplied source proof at each `command_inputs[ordinal]` and bind source-to-landing uniquely by owner/effect/digest/pin/ordinal/dependency; it must not broaden accepted-history continuation. Preserve all foreign/stale/ABA/binding/order/no-write refusals.

## Evidence

Packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json`, SHA-256 `23d309fb6f841fbba8560317c336b495ec4fcf2700a7e4c69bb7e1ea5c0f7ca7`.

The packet's exact causal command produced `2 failed, 7 passed in 8.95s`; failures are the two moved-head positives. No Runtime code or tests were changed in this review.

