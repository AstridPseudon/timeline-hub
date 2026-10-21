# Ordered inverse record transformation: Agent ownership proven

Date: 2026-10-21 UTC. Source diagnosis only; no product changes.

## Result

**Agent owns the `32618` operand difference.** In exact Agent6c,
`astrid/sdk/timeline/_command_state.py:582` discards an earlier deep copy
during ordered restoration and installs the original accepted record's mutable
`before.value` into the inverse scratch bundle. The next leaf restoration at
line 563 inserts `gone: null` through that alias. This changes the flattened
`AcceptedRecords` command, while its independent `entries` history stays `{}`.

The pure reproduction below uses the exact retained `32618` entry and canonical
document. Running the actual unmodified `apply_inverse()` produces **the entire
captured left operand**, not just the first differing field, and then the real
`_inverse_media_removals()` raises the exact original refusal. No Runtime
persistence change is needed to explain this failure.

The earlier `1114` report's ownership remained unproven; its proposed pre-insert
checkpoint is no longer needed to distinguish this failure. The Runtime
persistence ownership conclusion in `1110` is contradicted by this evidence.
Neither report established that a historical `{gone: null}` namespace value
was lost. `{}` is the correct sequential namespace-write `before`.

## Exact sources and evidence

- Agent read-only checkout `/home/user/work/wt/agt-pin-6c1989ad`:
  commit `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`, clean before diagnosis.
- Runtime assigned checkout: commit
  `d6534421043386548a0c41a8c2a688dd072d0562`, tree
  `ab5a6548c8d158e1952961cc681af737ff211ce0`. Its diff from product
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c` is confined to
  `tests/test_timeline_owned_reference_integration.py` (156 additions,
  3 deletions); product code is unchanged.
- Retained central run
  `rt-m2-ordered-observer-serialization-repair-1110-private017-agent6c-integration-1021111244-32618`:
  one original ordered node failed at the unchanged guard, **1 failed in 1.83s**.
  This run was read, never rerun here.
- Exact JSON source: call 2 of
  `design/runtime-ordered-inverse-operands-diagnosis-1105.md`.
  The probe reads its `records_argument.entries`, verifies their command list
  equals the captured right operand, and opens the entry's actual
  `receipt.result.canonical_document`. It creates no acceptance or history.
- A newer peer report,
  `design/agent-private017-inverse-dynamic-operands-diagnosis-1102.md`, independently
  identifies line 582 and reports an Agent fix/regressions. This diagnosis
  corroborates the cause independently against original Agent6c and original
  captured JSON; it does not independently qualify that peer's changed tree or
  reported test results. Its referenced worker diagnostic directory was absent
  when inspected, so those external diagnostic files were not verified here.

## Causal call order and identities

All Agent line numbers below refer to exact Agent6c.

1. **The original writes are legitimate sequential observations.**
   `_project_data_commands.py:121` clears the leaf, and line 124 clears the now
   empty namespace, carrying `insertion_order`. `_recording.py:145-151` reads
   the live pre-write state separately before each assignment. Thus the exact
   accepted writes are leaf `present(null) -> absent`, followed by namespace
   `present({}) -> absent`. The original proof at Runtime
   `tests/test_timeline_owned_reference_integration.py:295-309` asserts precisely
   these writes. Its namespace expectations/capture can legitimately describe
   `{gone: null}` while its later sequential namespace write describes `{}`.

2. **Runtime carries those raw records, and Agent initially detaches them.**
   Runtime `timeline_commit_store.py:1096-1100` stores `canonical_json(records)`;
   line 278 reloads `records_json` with `json.loads`. Agent `_history()` at
   `commit.py:598` also copies returned entries. `commit.py:1047-1048` constructs
   `AcceptedRecords(accepted, _records(...), load_boundary)`. `_records()` at
   line 627 deep-copies the raw command list. `_collections.py:192-194` stores
   these flattened command objects in the list and stores `entries` separately.
   The probe proves equality and distinct command/namespace-before identities
   at this boundary. No borrowed history alias exists here.

3. **Coalescing changes only its returned view.**
   Before execution `_hydrate()` at `commit.py:1105-1106` reaches `coalesce()`
   at line 435. `execute()` at lines 1109-1113 passes the same `inverse_records`
   into `commands.py:309 -> apply_inverse()`. The latter checks intervening and
   staged records (`inverse.py:449-451`), computes `changes` and
   `guarded_changes` (`452-454`), then captures immutable input (`455`).
   `coalesce()` deep-copies each write (`158-159`) and folds the earlier leaf's
   `before` into a copied namespace `before` (`179-180`, `_patch()` at `31-97`).
   Its one returned namespace write correctly has `{gone: null}`. Neither
   `_hydrate()` nor `apply_inverse()` replaces the raw list with that output.
   The probe asserts the raw list and entries remain unchanged by coalescing.

4. **Scratch restoration introduces the alias after those copies and guards.**
   After the after-state guards (`inverse.py:463-464`), line 465 copies the
   working bundle. Lines 466-490 walk the original accepted records/writes in
   reverse; `490 -> _set_recorded():101` passes each original `write['before']`
   and optional insertion order into `State.set()`.

   The first call restores the namespace. At `_command_state.py:563`,
   `value[target] = copy.deepcopy(state['value'])` is detached. But ordered
   reconstruction pops that target (`570`), excludes it from `values` (`581`),
   then **`values[target] = state["value"]` at 582** installs the raw caller
   object; `584` writes it into the scratch app. At return:

   ```python
   scratch.bundle['parent']['config']['app'][target] is records[0]['writes'][1]['before']['value']
   # True; both still equal {}.
   ```

5. **The next scratch write is the first operand change.**
   The next `inverse.py:490 -> _set_recorded():101 -> State.set()` restores the
   leaf `gone`. Traversal at `_command_state.py:539-546` reaches that aliased
   namespace, and line 563 assigns its `gone` member to `None`. This mutates
   `records[0]['writes'][1]['before']['value']` from `{}` to `{gone: null}`.
   The history namespace remains `{}`. No flattened list replacement or
   coalesced-record substitution is involved.

6. **Public inverse installation and the media helper expose the damage.**
   `inverse.py:516-540` installs the previously coalesced change through
   `Recording.assign()`. The candidate document/order is correct, but this
   does not undo the earlier mutation of `inverse_records`. In normal provider
   execution the same object survives `execute()`; at unchanged head,
   `commit.py:1122-1123` selects that plan, and `1141-1142` passes the same
   `inverse_records` to `document_from_bundle()`. Its line 362 calls the media
   helper. The helper's lines 181-183 compare the now-mutated raw list with the
   untouched raw history and correctly refuse, before any new acceptance at
   this boundary. The retained `32618` call stack includes exactly these final
   caller lines.

## Pure exact-JSON result

The diagnostic uses read-only imports, the real `_records()`, `AcceptedRecords`,
`coalesce()`, `bundle_from_document()`, `Recording`, `apply_inverse()`, and
`_inverse_media_removals()`. A `sys.settrace` observer snapshots entry/return of
`State.set()` without patching or replacing any source/function. Boundary
loading is an assertion failure if attempted; it is never called. No provider,
Runtime service, native command execution, accepted-history fabrication, or
ordered-body replay occurs.

| Checkpoint | Flattened namespace `before.value` | History namespace `before.value` | Scratch aliases flattened value | Equal operands |
| --- | --- | --- | --- | --- |
| `_records()` / `AcceptedRecords` | `{}` | `{}` | no | yes |
| After pure `coalesce()` | `{}` | `{}` | no | yes |
| Scratch namespace `State.set()` return at 584 | `{}` | `{}` | yes | yes |
| Scratch leaf `State.set()` entry | `{}` | `{}` | yes | yes |
| Scratch leaf `State.set()` return at 564 | `{"gone": null}` | `{}` | yes | no |
| Public installation / inverse return | `{"gone": null}` | `{}` | earlier scratch alias persists | no |

Assertions passed for: complete left operand equal to `32618`'s captured
`accepted_records`; complete entries unchanged; correct restored namespace and
exact app insertion order; original guard raising
`media inverse records differ from accepted history`.

This explains why the `1114` alias probe missed the defect: ordinary
`State.set()` detaches values, while the **ordered branch** subsequently
overwrites that detachment. A pure coalesced `{gone: null}` result is valid but
cannot on its own explain a changed raw record.

## Minimal correction boundary and targeted regression

**Peer-ready proposal, Agent-owned; no implementation in this task:** preserve
detachment in ordered `State.set()` by changing only line 582 to:

```python
values[target] = copy.deepcopy(state["value"])
```

This matches line 563's existing assignment semantics. Reusing the already
detached value before popping it is another valid local implementation, but
the one-line copy is the smallest review boundary and matches the peer's
reported correction. No correction belongs in Runtime's history carrier,
`_records()`, coalescing, or the media guard.

Keep the two sequential writes exactly as accepted, including namespace
`before == present({})`, explicit null leaf, and `insertion_order`. Preserve
raw accepted-list/history equality, all inverse conflict/ancestry/ABA guards,
and exact history custody. Do not rewrite history to store a coalesced value,
strip nulls, exempt project data from the media guard, or globally copy inputs.

Recommended focused Agent regressions:

- In the existing ordered project-data reload/inverse/redo test, snapshot the
  raw records before inverse; assert both value equality and unchanged raw
  records after inverse and redo. Check explicit null presence and exact order.
  A final-state-only assertion misses this defect because the restored
  document is already correct while records are corrupted.
- At the provider boundary, create before/target/after namespaces through
  ordinary commands, remove the target's sole null leaf, then inverse/redo
  through the unchanged accepted-history/media equality guard. Assert the
  original history remains byte/value-equivalent and the raw removal retains
  its intermediate `{}`. Include a non-null mutable/scalar leaf neighbor if
  needed; the alias is independent of null semantics.

The peer `1102` report describes these regression boundaries and a fix. Have
Agent review/integrate that existing work rather than producing another patch.
Runtime then owns requalification of the original ordered proof on the reviewed
Agent source; this report grants no new execution authorization and claims no
passing qualification for original `12634`/`32618`.

## Commands, limits, and disposition

Executed once, exit **0**:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-pin-6c1989ad /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-ordered-record-transform-hard-cause-1119/record_transform_probe.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-ordered-record-transform-hard-cause-1119/record-transform-result.json
```

The retained script and compact JSON contain all diagnostic assertions and
six setter checkpoints (scratch namespace, scratch leaf, public namespace;
entry and return each). This is a diagnostic pass proving the original
defect/refusal, not a product test claiming repaired behavior.

No suite was run or requested: no central, full, node/native, HTTP/socket,
browser, render, generation, or install. No source overlay/patch bypass,
shared-dependency write, product/generated/pin/schema/fixture/guard edit, or
body replay. No blockers. Runtime and Agent product worktrees remain unchanged.
