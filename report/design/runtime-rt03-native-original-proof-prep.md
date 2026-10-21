# RT03 original owned-raw native proof preparation

Status: prepared only; not qualified on current public Runtime/Agent pins.

## Source authority

- The preserved original is `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting` on Runtime b92 (`b92d3e7a05eec65c142294ef4873edd059e9b31`). Its strict marker and expectation were left unchanged.
- The settled Agent witness is `docs/design/agent-rt03-original-unplaced-reference-witness.md` from the Agent handoff at `5e1a0595b11073cd5fa65695b9ba5afe3b61fe1e`.
- Agent’s future `timeline.reference` recipe is from `d1f5f7824` and its composed schema/round-trip follow-up is `85c90d526`. The complete1022 source-review pin is `10226a7f08a739ba3e41f8e91de6971eed63aa9d`; it is a review/source authority, not a claim that the current Runtime pin carries this operation.
- Runtime’s future raw custody read is `f53bf588bf70b090ce8e0bed5ccb7d91157771b`; its unplaced projection is `449d13d291cc3b62ebbdd780d38d8c58732e4e1b`.

The required execution tuple is therefore a matched private Runtime pair carrying f53 + 449 and a matched private Agent pair carrying d1f + 85c (with its generated/client contract from that same cohort). Current `tests/astrid-agent.pin` is `1a407fefad05c498836a25594ed603e9a543705d`, the historical C3d client/source and not this future tuple. The manager must add the concrete named suite only after the normal private pins are installed together.

## Test prepared

`tests/test_timeline_owned_reference_integration.py` is one integration case using the existing `test_timeline_commit_integration.agent` fixture and the normal `astrid` provider. It creates a fresh project/timeline, ingests owned raw bytes through `RuntimeService.ingest`, obtains raw metadata through `MediaReads.raw_media_info`, captures Agent’s `timeline.reference`, and sends it through `commit_timeline`. No provider double, SQL accepted-history insert, catalog reference, generation, placement, or fake media metadata is used. Future-only imports are lazy so b92 can collect the case without executing it.

## Exact assertion mapping

| Original strict assertion | Prepared native case |
| --- | --- |
| `reference_id == exact-reference`, `object_id == object-digest`, `role == source` | The owned CAS digest is carried as the exact `MediaManifestEntry`; the accepted receipt and `timeline_references` row assert `exact-reference`, that digest, and `source`. |
| First keyed acceptance | `exact-reference-key` is asserted on the native receipt; the receipt result equals the accepted data. |
| Exact retry after restart | Runtime is closed/reopened; the same body/key returns the identical receipt/result, the whole SQLite dump is unchanged, and the provider is patched to fail if replayed. |
| Changed payload under the same key | The same key with `role: target` returns 409 and leaves the store unchanged. |
| Different key cannot overwrite occupied identity | A newly owned replacement raw pin with the same `exact-reference` is submitted under `occupied-reference-key`; it returns visible 409 `occupied`, with unchanged row, head, and history. |
| Reference is not a shot/clip placement | Accepted canonical payload asserts empty `occurrences` and `clips`; the projection is only the timeline reference row/snapshot. |
| Inverse/restore behavior | Inverse targets the exact accepted receipt. Only `exact-reference` disappears; the unrelated accepted reference remains, and the restored parent payload plus exact Runtime closure/read match the pre-exact document. |
| Unsafe arbitrary raw input | A raw object owned by a different project is read only for command capture, then submitted to the target project; normal Runtime custody visibly refuses it at 409 with no writes. |

The original strict test remains the historical/legacy control and is not
converted or marked differently by this preparation.

## Qualification boundary

Only collection/static checks were run. The integration body was not run:
current public95 Runtime b92 rejects the future raw/reference operation and the
current Agent pin still has the historical client. Gate2 exact-retry/no-partial
proof therefore remains OPEN pending the matched private source/client tuple.
