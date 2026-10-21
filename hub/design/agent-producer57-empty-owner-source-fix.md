# Agent producer57 empty-owner source fix

Status: **bounded source fix ready for Runtime/App2 source re-review**.

This is Agent source only. No Runtime/App activation, HTTP/socket work,
generated output, writer, DTO, schema, pin, public014 mutation, or 5672
mutation was made.

## Exact source identity

The reviewed starting source is the requested Agent candidate:

- source commit: `57af3fffe192ad369c4282d9ab3a67efd57dc51c`
- source tree: `319013e799d244497deac26719282595c213b658`
- parent: `f448c4b40c60d08f4092e232688b0de99bb07243`
- parent tree: `d4508b9fa5db9b2a2774fc5acc811fc34814c53d`

The harness will create the worker commit after exit. Before that commit,
the exact fixed candidate tree calculated from the clean starting tree and
the two changed file blobs is:

- fixed candidate tree: `5badf69a01ac0d79141efd4e94cd96b336520de3`
- `astrid/sdk/timeline/_clip_scalar_commands.py` blob:
  `3dac0aedc518319ac784e85b795a8c50a0823965`
- `tests/editing_conformance/test_recipe_producer_clip_set.py` blob:
  `b788184c4375e69015c8736564443932debc76c2`

The command schema is unchanged. Its exact pretty-printed JSON-plus-final-
newline SHA-256 remains:

`0b747d87c763a8f0ba0dcc5027390ab04d6296cfddfffa8c049020334ca3ec92`

## Source correction

`_producer_app` now requires the persisted `app.managedBy` value to be a
string that is not exactly empty. It keeps the existing value for all later
ownership comparisons; no trimming, truthiness normalization, owner guessing,
or incoming-value substitution was added.

The permanent producer negative uses a mirrored clip whose persisted
`app.managedBy` and `app.__generated__.extensionId` are both empty. The
incoming update carries only the matching generated metadata leaf. Capture
refuses with `unsupported_ownership` and the source bundle remains unchanged.
The existing nonempty-owner metadata-refresh positive, foreign/user
exclusions, opaque sibling preservation, inverse/redo, source floors, and
unknown-byte behavior remain covered.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_producer_clip_set.py
3 passed in 0.86s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py -k 'only_carrier_additions or private_remove or private_extent_floor or literal_three_union or extent_proposal or voiceover_property or complete_reviewed_private_s2'
7 passed, 17 deselected in 1.16s
```

`git diff --check` passed. No full, browser, localhost, live-socket,
Runtime, App, renderer, activation, or public-pin suite was run.

## Bounded re-review request to Runtime/App2

Please re-review the fixed Agent source at the worker branch after the
harness publishes its commit, using the exact source/tree/schema identities
above. Confirm that an existing empty `app.managedBy` refuses before capture
or writes even when the existing and incoming generated `extensionId` are
both empty; confirm that nonempty owner refreshes still succeed and that
foreign/user clips, opaque siblings, unknown bytes, and all frozen schema
floor hashes remain unchanged. This request is source-only: do not activate a
Runtime/App route, change a Runtime pin or DTO, mutate public014 or 5672, or
claim live/native acceptance from this handoff.
