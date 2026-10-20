# App peer review: project-data removal source

Date: 2026-10-20 UTC

## Decision

**CONCRETE MISMATCH — do not give a clean source ACK yet.** The exact closed
shape and spelling are correct, but the proposal does not preserve raw
top-level `config.app` insertion order through inverse when the removed target
namespace had a sibling namespace.

Reviewed identities:

- Agent commit `0e341206235da8b9861c618c2a9304de6c50fa98`
- Agent tree `47dfad89eac12597c1ed27410553b9396187eff2`
- schema SHA-256 `23b87833ca837bfafc6972e3dd4702c88525f230cb16a50ace745053afc4289c`

## Contract checks

The proposal keeps exactly one existing `project-data.write` v1 operation,
selected at `parent`: `mode: "replace"` remains unchanged, and
`mode: "remove"` requires only `target`, `key`, and `mode` while forbidding
`value`. Runtime’s earlier `delete` spelling is correctly superseded by the
single `remove` spelling. No alias, second operation, current-392 mutation,
App product/schema change, public DTO/API/store, generation, pin, or activation
is authorized.

The forward semantics match the reviewed Main carrier for ordinary JSON object
namespaces: absent target is a guarded no-op; null/empty target is removed;
one present leaf is removed without confusing present `null`/`false`/`0`/empty
values with absence; the last target and then empty `config.app` are pruned;
other keys, namespaces, opaque values, and key order are retained. Main’s
delete path is `src/tools/video-editor/lib/timeline-patch.ts:1862-1875`, with
empty-app omission at `:1945`/`:1962-1965`.

The source also correctly refuses malformed non-null target namespaces and
reserved/non-canonical keys, and uses the existing parent scope, cell writes,
container claims, accepted records, inverse, replay, and stale/disjoint guard
machinery. The App prerequisite report’s stricter reserved-key and malformed
namespace boundary remains the right native boundary; no null-write or whole
config replacement is introduced.

## Blocking mismatch

For this authored state, in insertion order:

```json
{
  "config": {"app": {
    "com.example.target": {"gone": false},
    "com.example.sibling": {"opaque": [null, 0]}
  }}
}
```

`mode: "remove"` clears the leaf, clears the now-empty target namespace, and
leaves the sibling namespace. The accepted record therefore has no enclosing
`config.app` write to restore. Inverse coalesces the target clear and restores
the namespace with `State.set`; that setter assigns a missing dict property at
the end (`_command_state.py:524-536`). The result is ordered
`["com.example.sibling", "com.example.target"]`, not the original
`["com.example.target", "com.example.sibling"]`.

The proposal’s `test_remove_last_key_prunes_only_empty_namespace_and_app`
asserts `bundle == before`, but Python dict equality ignores insertion order,
so it does not catch this raw-order loss. This is a real inverse/redo lossless
semantics gap, not an App product mismatch. The source should record or
otherwise restore the enclosing app-map position (and add an order-sensitive
inverse/redo regression) before it receives a clean ACK.

## Evidence

Current App targeted controls passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/source-map-runtime.test.ts src/tools/video-editor/commands/projectDataMember.test.ts
=> 3 files passed; 341 tests passed
```

The proposal’s recorded Agent evidence (not rerun in this read-only App review)
reports 21 project-data conformance tests, 121 project-data plus inverse-clear
tests, and 7 focused schema-union tests passing; those tests do not assert
order-sensitive inverse restoration for the sibling-namespace case above.

No full, matrix, browser, localhost, live-socket, dependency, Runtime HTTP,
generation, pin, activation, or App product/schema suite was run.

