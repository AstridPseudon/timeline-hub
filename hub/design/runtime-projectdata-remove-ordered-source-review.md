# Runtime bounded review — project-data removal ordered inverse

## Decision

**SOURCE ACK** for the repaired Agent source/schema, limited to the removal
and guarded inverse behavior reviewed here.

Exact source tuple:

- Agent commit: `b4493c75947f8605e61852f340e56b27e24c4adb`
- Agent tree: `24c0900be7d469d1250ca9883b7714c72308ed81`
- Parent: `ff5edd9ab3b52005d5b97788902ed5b597c8ff7d`
- Schema SHA-256: `0357ef34fbac2416be59dc906fa5a9d9173e322ff1d1e53b758f5c890d543906`

The candidate changes only `_project_data_commands.py`, `_recording.py`,
`_command_state.py`, `inverse.py`, and the focused project-data conformance
test. The existing `project-data.write` operation retains the sole
`mode: "remove"` spelling; `mode: "replace"` is unchanged. No delete alias,
new operation, DTO/store change, broad replacement, or frozen-392 mutation was
found.

## Bounded evidence

The exact committed Agent tree was extracted privately and tested with the
shared Agent venv:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private exact b449 tree> \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_m2_project_data.py \
  -k 'remove_pruned_namespace_restores_exact_order_after_reload_and_redo or ...'
=> 10 passed, 12 deselected
```

This included the repaired `before/target/after` namespace-order witness
through serialized remove, inverse, serialized redo; opaque/null values;
disjoint-key rebase; and same-key ABA/intervening-write refusal.

A one-off probe against the same extracted tree tested malformed target
namespaces of list, string, number, and boolean shape. Every remove refused
atomically and the complete input bundle remained unchanged.

`git diff --check b4493c75947f8605e61852f340e56b27e24c4adb^ b4493c75947f8605e61852f340e56b27e24c4adb` passed.

No Runtime product files changed. Runtime95bd was not invoked because this
source-only witness did not require an imported Main helper. No full suite,
live service, generation, pin, release, integration adoption, or App
activation was run or authorized.
