# Runtime inverse record null-mutation cause — diagnosis

Date: 2026-10-21 UTC  
Scope: Runtime `d653442` (`product42`) with read-only Agent6c
`/home/user/work/wt/agt-pin-6c1989ad`

## Result

The owner of the `capture32618` operand difference is **not proven** by the
available evidence. In particular, the post-inverse observer does not prove
that Runtime persisted `gone: null` and later lost it, and the source trace
does not find an Agent mutable alias that can mutate `records.entries` through a
borrowed `before.value`.

The one confirmed disappearance is earlier and has a different meaning:

1. `astrid/sdk/timeline/_project_data_commands.py:121` calls
   `ctx.clear(ref, [*target_path, key])` for `gone`.
2. `astrid/sdk/timeline/_recording.py:145-151` captures the leaf `before`, then
   invokes `State.set`.
3. `astrid/sdk/timeline/_command_state.py:561` removes `gone` from the live
   authored namespace.
4. The following `ctx.clear(ref, target_path, ...)` at
   `_project_data_commands.py:124` therefore reads `{}` at
   `_recording.py:145`; its second write legitimately has
   `before.value == {}` in the ordinary recorder output.

That is an in-memory authored-state transition before Runtime persistence. It
is not evidence that an already accepted history object was mutated.

## Persistence and reconstruction evidence

Runtime writes the accepted recorder as `canonical_json(records)` at
`runtime_protocol/timeline_commit_store.py:1096-1100`, specifically the
`records_json` argument at line 1098. Runtime reconstructs a history entry by
calling `json.loads(row["records_json"])` at
`runtime_protocol/timeline_commit_store.py:278`.

The retained integration source asserts, after closing and reopening Runtime,
that the accepted remove record's second write is:

```json
{"before":{"state":"present","value":{}},"after":{"state":"absent"}}
```

at `tests/test_timeline_owned_reference_integration.py:447-464` in the
retained `32618` source. The retained observer also sees `{}` in the
flattened `records.entries` operand. This proves the reconstructed accepted
entry used by that source/test path is `{}`. It does **not** retain the exact
`records_json` bytes immediately before the SQL insert, so it cannot by itself
separate serialization/persistence from an earlier Agent/provider value.

The observer's other operand has `gone: null`, but it is sampled only at the
inverse guard. That is too late to establish the value at `_records()` return,
at `AcceptedRecords` construction, or at the Agent-to-Runtime acceptance
boundary.

## Agent copy/alias trace

The relevant boundaries are:

- `astrid/sdk/timeline/commit.py:613-628`: `_records()` validates each
  accepted entry and uses `copy.deepcopy(recorder["commands"])` at line 627.
- `astrid/sdk/timeline/_collections.py:189-194`: `AcceptedRecords` stores the
  copied flattened records in the list base and stores `entries` separately.
- `astrid/sdk/timeline/inverse.py:158-160`: `coalesce()` deep-copies every raw
  write before patching it.
- `astrid/sdk/timeline/inverse.py:180`: the only write to a `before` value in
  this path is to that already-deep-copied coalescing record; it cannot write
  into `records.entries`.
- `astrid/sdk/timeline/inverse.py:31-39` and `84-97`: `_patch()` deep-copies
  its input value before any `pop`/assignment.
- `astrid/sdk/timeline/_command_state.py:27-29, 311-347`: `present()` and
  `State.get()` deep-copy returned values.
- `astrid/sdk/timeline/_command_state.py:556-563`: `State.set()` deep-copies
  present replacement values; its line 561 mutation is against the working
  bundle, not an accepted record.
- `astrid/sdk/timeline/_recording.py:137-151`: `Recording.assign()` stores the
  `before` returned by `State.get()` and then sets the working state; those are
  separate objects.

The pure isolated reproduction in the worker's `alias_probe.py` used the exact
two-write shape and verified:

```text
entry_vs_flattened_identity= False
before_value_identity= False
coalesced_before= {"state": "present", "value": {"gone": null}}
flattened_unchanged= True
setter_source_retains_gone= True
```

Thus no concrete Agent line currently explains a mutation from
`records.entries[*].records.commands[*].writes[1].before.value ==
{"gone": null}` to `{}` through a borrowed alias. The captured difference may
instead reflect an unobserved pre-guard transformation or an inconsistent
capture/source pairing; that cannot be resolved from the retained report.

## Exact values and ownership disposition

| Boundary | Value supported by evidence | Disposition |
| --- | --- | --- |
| Authored working namespace after the first leaf clear | target namespace `{}` | Agent in-memory state, `_command_state.py:561` |
| Ordinary recorder's second namespace-write `before` | `{}` | Agent recorder observation at `_recording.py:145`; expected from the preceding clear |
| Durable/reloaded history entry shown by retained source | `{}` | Runtime history carrier is the reader, but raw pre-insert bytes are absent |
| `capture32618` flattened operand at the guard | `{"gone": null}` | Observed, but its creation/mutation time is unknown |
| `capture32618` entries operand at the guard | `{}` | Observed after inverse execution; does not establish stored bytes |

No product, generated client, history schema, fixture, or guard correction is
justified. Do not exempt the equality guard, strip nulls, or add global deep
copying.

## Single missing checkpoint and smallest next observation

The single missing checkpoint is the exact serialized recorder bytes at
`runtime_protocol/timeline_commit_store.py:1098`, immediately before the SQL
`INSERT`, captured non-mutating as the `records_json` string (or its SHA-256)
alongside the publication/idempotency key. Compare that string with the
reloaded `timeline_commit_history.records_json` and the existing pre-guard
operand snapshot; do not execute another ordered body.

- If the pre-insert bytes already contain `{}`, the loss occurred before
  Runtime persistence and the owning Agent/provider boundary must be captured
  next; the currently visible line 561 is only ordinary working-state
  mutation, not yet the observed history mutation.
- If the pre-insert bytes contain `gone: null` but the reloaded bytes do not,
  the correction belongs to Runtime's persistence/carrier path around
  `timeline_commit_store.py:1098`/`:278`.

The direct regression should assert explicit-null member presence through that
single serialization/reload boundary and separately assert that the flattened
accepted records and `entries` are equal before inverse execution. It should
retain the existing guard and insertion-order assertions.

## Tests/evidence run

- Pure Agent alias/recorder reproduction (read-only imports):
  `PYTHONPATH=/home/user/work/wt/agt-pin-6c1989ad PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python alias_probe.py`
  passed, with the five output lines above.
- Retained central result `32618`: 1 failed in 1.83s at
  `astrid/sdk/timeline/commit.py:181-183`; not rerun here, per the instruction
  not to replay the ordered node.
- No full, central/body/native/HTTP/socket/browser/render/old44/old186 suite
  was run.
