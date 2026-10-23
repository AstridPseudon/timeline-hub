# Runtime R2r sequential owner review

## Result

**FAIL for qualification; PASS for Runtime refusal/classification.** Runtime 859 correctly refuses the moved-head normal sequential request. The missing authority is not a valid accepted-history successor and must not be blindly retargeted. The held Agent candidate is not qualified because the provider-to-Runtime handoff does not carry the original source-bound capture needed to authenticate the staged step-2 physical ID.

Owner disposition: **Agent/provider source-bound transport/provenance**, with a bounded Runtime auth verification seam after that evidence exists. This is distinct from the inverse-leaf work.

## What is actually available

- The complete offline packet is present at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json`, SHA-256 `23d309fb6f841fbb...c0f7ca7` (full hash recorded below).
- The request claims include the original `commands`, `steps`, `reads`, `base_revision_id`, `base_publication_id`, `merge`, and ordinary metadata. In the captured case, command 2 claims `ref=internal-revision:authoring-timeline-revision-dca4...`, `path=[clips,id:cross,at]`, and `before=4.0`.
- The provider-computed prepared result contains the landing execution: `records.commands[].writes/reads/derived_writes/bindings`, `records.steps[].patch/dependencies`, `expected_head`, canonical document and digests. Its bindings carry `ref`, landing `physical_ref`, image `revision_id`/`content_digest`, owner/owners, managed edges, and base/landing invocation boundary fields.
- Runtime constructs `source` at the expected landing head, `base` at the requested base, accepted-history continuations, and inverse history in `runtime_protocol/timeline_commit_store.py:777-813`; `timeline_commit_auth.validate()` then receives those trusted closures and the prepared records.
- The Runtime provider call is only `provider.commit(provider_context, port)` (`runtime_protocol/timeline_commit_execution.py:83-89`). `RequestCommitPort._provider_context()` returns the request context unchanged (`runtime_protocol/timeline_commit_port.py:103-127,173-174`). The port exposes authenticated `head`, closure and history reads, but no original Agent `Plan` or replay-binding map.

## What is missing

The packet's `current_capture` is an offline artifact, not proof of a private Runtime carrier. The current provider code proves the omission:

- Agent keeps the original plan locally at `astrid/sdk/timeline/commit.py:1072-1076` and creates landing `replay_bindings` at `:1110-1122`.
- It then emits only `prepared_records(plan)` at `:1159-1173` and calls `port.preview/accept(prepared)` at `:1175-1181`.
- `replay_bindings` is an argument to the local Agent `commands.execute()` call (`astrid/sdk/timeline/commands.py:185-219`); it is not part of the Runtime request or the prepared result.

Therefore Runtime receives no trusted original-side tuple for each staged sequential input: original physical ref, original revision/content digest, source step and command/change ordinal, owner/complete owners, source managed edges, original base/evaluated-head pair, and the corresponding landing physical ref/digest/edge tuple. The public alias and `before` value are caller claims, not source authority. The packet includes these facts in its capture JSON, but that does not transport them into `prepared`/`port.accept`.

The concrete moved-head failure is `invalid_records: provider alias is outside its authenticated boundary` while normalizing the submitted step-2 claim, before write/accept. An unlanded staged ID is not accepted-history continuation; matching payload bytes or a new unique landing ID would not prove provenance.

## Minimum bounded verification seam

After Agent supplies the missing source-bound capture through the existing private provider result, Runtime should keep the current refusal guards and verify, for both original-base and landing-head execution:

1. each step/command/change is evaluated at its sequential input (`command_inputs[ordinal]`), with exact read states, patch `before` values, step ordinal and dependency union;
2. each original submitted physical alias resolves to exactly one original image, then to exactly one landing image through the provider-computed materialization/owner edge, never through guessed history or payload equality;
3. every mapped image retains revision ID, content digest, owner/complete owners, edge-before/edge-after, base/evaluated-head pair, step ID, command ordinal and change ordinal;
4. landing effects, final canonical/head/revision/digests, dependencies and pins agree with those mappings, while foreign, stale, ABA, ambiguous, unrelated-owner, order and no-write refusals remain unchanged.

The bounded Runtime locations are `runtime_protocol/timeline_commit_auth.py:306-350` (`validate_step`), `:353-454` (`validate_bindings`), and `:1342-1418` (`validate`), with existing accepted-history lookup in `runtime_protocol/timeline_commit_store.py:752-764`. In particular, `validate_step` currently normalizes submitted step reads/claims against the static `boundary` at lines 309 and 344 rather than the per-command `command_boundary`, and `validate_bindings`'s original-alias check at lines 399-403 is limited to `ordinal == 0`; any correction must add sequential source proof, not a broader history continuation. No contract, schema, client tuple, guard waiver, blind retarget or fabricated continuation is authorized by this review.

## Evidence

- Packet SHA command:

  `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R1-sequential-current-runtime859-packet-23d309fb6f841fbb.json`

  Result: `23d309fb6f841fbba8560317c336b495ec4fcf2700a7e4c69bb7e1ea5c0f7ca7`.

- Existing causal offline command from the packet:

  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_doc_patch_sequential_rebase.py`

  Result: `2 failed, 7 passed in 8.95s`; the two failures are the moved-head positive cases, while fresh-head and strict refusal controls pass. I did not rerun the Agent-owned targeted suite or any full/live suite.

- Runtime source was clean before adding these two requested report artifacts; `git diff --check` passed; HEAD `8592822fd11275540f596562f43c715676f2bcf0`. Final status contains only `ORCH/` and `ORCHworkerreport.md`.

No product, test, contract, generated, pin, or Git changes were made.

