# App `project-data.write` closed-contract review: recovered handoff

Date: 2026-10-20 UTC. This is a recovery of the lost
`ap2-m2-project-data-closed-contract-review` report from its worker log, with
the requested before/after examples and classification made explicit. No new
product review, source edit, schema edit, pin, adoption, or broad test run was
performed here.

## Decision

**Hold App activation / request the paired consumer and Runtime gate.** The
private Agent operation is a suitable source floor for a bounded v1, and its
focused contract lane passed. Current App project-data behavior is broader in
some places, narrower in unsafe-value handling in others, and has no native
consumer for this family. Do not generate, adopt, pin, release, or retire the
App snapshot writer based on this review alone.

Reviewed Agent candidate: commit
`0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3`, tree
`2f3eee4e9a7d37db80374b5e98d16f1e08082a35`, schema
`89ed90ce0a4a95559a6d086d57f851fbcc6d224c9e7658f41467dfa9280eb0c3`.
Reviewed App tree: `83cf9199f2f858147d8ebbfc6648f01962bbe333` (commit
`ddd9e7824`).

The closed Agent shape is:

```json
{
  "schema_version": 1,
  "op": "project-data.write",
  "version": "1",
  "select": "parent",
  "args": {
    "target": "com.example.compiler-canary",
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "...",
    "mode": "replace"
  }
}
```

Its semantic destination is exactly
`parent.config.app[target][key]`. It preserves sibling keys, other extension
namespaces, enclosing config fields, input command order, and finite JSON
values. This carrier is only extension configuration data; it is not project
catalog state, transcript selected pins, or `itemsBySchemaRef`.

## Six mismatch classifications

The labels below are deliberately about the interoperable cut, not a reason
to silently widen either implementation.

| # | Reported mismatch | Classification | Handoff decision |
|---|---|---|---|
| 1 | App admits `merge` and `replace`; Agent v1 is `replace` only. | **(a) bounded v1 subset** | Known compiler-canary/source-map producers emit explicit `replace`, so they are eligible. A merge can only be lowered safely by reading the original guarded value, applying the producer's declared deterministic merge to a clone, and emitting the resulting whole-cell `replace`; otherwise it remains legacy/unsupported. Requiring explicit replace is the current minimal recipe. |
| 2 | App checks `key.trim().length` but stores the untrimmed key; Agent requires an already-trimmed key. | **(a) bounded v1 subset** | Accept only an already-canonical, non-empty key within 256 UTF-8 bytes. Reject `" key "`; never trim it to `"key"`, because that changes identity. |
| 3 | App rejects reserved object keys anywhere in a value; Agent's focused test accepts nested `__proto__`, `constructor`, and `prototype` as opaque JSON. | **(b) true contract/safety mismatch for normal App behavior** | The normal App safety boundary stays refusal. Do not sanitize or rewrite the value to make it pass. The candidate's acceptance is broader than the App contract and cannot be used to force unsafe input through the native path; it needs an explicit contract decision before any broadening. |
| 4 | App's generic compiler spreads a malformed namespace such as an array; Agent's container claims refuse malformed non-dict shapes. | **(b) true contract mismatch for normal behavior** | The native contract must fail closed on malformed enclosing state. Absent, `null`, and dictionary namespace birth are supported; array/string/other malformed namespace adoption is not. Do not silently adopt it. |
| 5 | Limit checks are nominally aligned, but App `JSON.stringify` and Agent compact `json.dumps(..., allow_nan=False)` can differ for non-finite values and exact numeric-exponent byte boundaries. | **(a) bounded v1 subset** | Use ordinary finite JSON from the known producers and let the paired Agent/Runtime contract own exact byte accounting. Do not pre-normalize or claim parity from the generic compiler. At an ambiguous exact boundary, refuse visibly and retain the draft. |
| 6 | App's generic compiler stable-sorts operations carrying `order`; Agent executes the supplied command list in order and has no `order` arg. | **(a) bounded v1 subset** | The known data patch has no `order` fields and emits source then source-map members, so input order is compatible. A generic project-data operation carrying `order` is refused by the native adapter rather than reordered. |

Category **(c)** is the family-level prerequisite, not a seventh semantic
reinterpretation of one row: the current App has no native project-data
consumer, and the current ordinary Runtime candidate has no matching
`project-data.write` schema/registry entry. Therefore the whole project-data
writer stays on its guarded legacy/refusal path until the paired App
`commands[]` consumer, Agent contract, and Runtime `/v1` provider/schema are
qualified together. A mode subset by itself is not an automatic contract
reject: unsupported modes may remain on the guarded legacy path, and a mixed
batch must refuse atomically before any supported member is submitted.

## Concrete before/after examples

### Positive bounded replace

Before:

```json
{
  "config": {
    "app": {
      "com.example.compiler-canary": {
        "keep": {"opaque": true}
      }
    }
  }
}
```

Input data patch (in this order):

```json
[
  {
    "op": "project-data.write",
    "target": "com.example.compiler-canary",
    "payload": {
      "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
      "value": {"version": 1},
      "mode": "replace"
    }
  },
  {
    "op": "project-data.write",
    "target": "com.example.compiler-canary",
    "payload": {
      "key": "__dsl_sm__:sm-1",
      "value": {"id": "sm-1", "sourceLine": 3},
      "mode": "replace"
    }
  }
]
```

After the native projection/accepted commit:

```json
{
  "config": {
    "app": {
      "com.example.compiler-canary": {
        "keep": {"opaque": true},
        "__dsl__:dsl://com.example.compiler-canary/main.json": {"version": 1},
        "__dsl_sm__:sm-1": {"id": "sm-1", "sourceLine": 3}
      }
    }
  }
}
```

The two operations become one ordered `commands[]` intent and one Runtime
commit. Each leaf keeps its original absence/null/value guard; the namespace
is preserved and only the requested cells are written. The focused Agent test
also proves absent, `null`, and empty namespaces can be born/rebased without
losing a disjoint key, while `A -> B -> A` on the same leaf refuses undo.

### Merge is not silently treated as replace

Before:

```json
{
  "settings": {"theme": "dark", "volume": 1}
}
```

App legacy input:

```json
{
  "key": "settings",
  "value": {"theme": "light"},
  "mode": "merge"
}
```

App's existing compiler produces:

```json
{
  "settings": {"theme": "light", "volume": 1}
}
```

If this family later admits merge lowering, the adapter must capture and guard
the original `settings` value, compute that exact result on a private clone,
then submit a replace of the complete resulting cell. It must not submit only
`{"theme":"light"}` as replace, because that would silently lose `volume`.
With no such original-value guard and deterministic declared merge, keep the
operation on the legacy/refusal path. Missing mode must not be upgraded by
guesswork on the native path.

### Unsafe key and malformed namespace refusal

These remain visible refusal/draft cases, not normalization cases.

```json
// unsafe nested value: App refuses; do not delete/sanitize the key
{"key": "settings", "value": {"__proto__": {"safe": true}}, "mode": "replace"}

// unsafe outer key: reject; do not trim/adopt/rename
{"key": " key ", "value": 1, "mode": "replace"}

// malformed existing namespace: reject; do not spread/adopt the array
config.app["com.example.compiler-canary"] = ["legacy"]
```

The caller receives the complete unsupported diagnostic and keeps the draft.
No partial native command, preview, outbox intent, snapshot fallback, or
per-key submission may occur for a mixed batch containing one of these.

### Ordering and limits

An input carrying `order: 2` on source-map followed by `order: 1` on source is
not a native project-data batch: App's generic compiler would reorder it, while
the Agent command preserves supplied order. The adapter refuses it rather than
silently changing intent. The known compiler-canary batch has no `order` and
is therefore source-then-source-map in input order.

For limits, both sides target 64 KiB per entry, 1 MiB per extension, 128
entries, UTF-8 key sizing, and atomic refusal before materialization. Exact
serializer differences matter at byte boundaries (for example JS and Python
format `1e-7` differently). Do not trim, stringify, reparse, or otherwise
normalize the caller's value to cross a limit; use the paired contract's
authority and retain the draft on refusal.

## Exact App consumer recipe

1. At the command-session batch seam, preflight the complete patch before
   capture, owner resolution, preview, enqueue, or save. Check every member
   and collect every unsupported reason.
2. For the bounded positive, accept only:

   ```text
   TimelinePatchOperation {
     op: "project-data.write",
     target: valid extension ID,
     payload: { key: canonical non-empty key, value: finite JSON,
                mode: "replace" }
   }
   -> EditCommand {
     select: "parent",
     args: { target, key, value, mode: "replace" }
   }
   ```

   Require exact payload shape, valid target, already-canonical key within
   256 UTF-8 bytes, and finite JSON value. Preserve value shape and input
   order. Do not map `project-data.delete`, `app.update`, catalog fields,
   transcript pins, selection carriers, or any other carrier into this op.
3. Build every command against one original authored bundle. Keep the exact
   leaf guards, namespace claims, reads, writes, bindings, and any created
   identities. Produce one local native projection for display only and one
   ordered `commands[]` outbox intent for the durable edit.
4. Submit once through the existing Runtime `/v1` commit/outbox path. Retry
   with the identical request body and identity; do not recapture after ACK or
   submit one key at a time.
5. If any member is unsupported (including merge-mode unless the guarded
   lowering above is explicitly qualified), malformed, ordered, unsafe, or
   outside the exact recipe, refuse the complete batch before any submit. Return
   all operation intentions/reasons and retain the caller's draft. Do not
   filter supported members, trim keys, adopt namespaces, upgrade modes, or
   fall back to a durable `commitData(nextData, {save: true})` for a
   native-capable batch.
6. Keep the current guarded legacy snapshot writer reachable for an
   all-unsupported standalone project-data patch until the paired Agent and
   Runtime operation is qualified. Delete that branch only after the complete
   family has native coverage and the relevant journey proves no legacy save.

The current App path does not meet this recipe: `genericPatchCapture.ts` does
not classify `project-data.write` as native, and `useTimelineOps.ts` reaches
the legacy `commitData(..., save: true)` path for an all-unsupported
project-data patch.

## Source floor and Runtime gate

The source floor is the exact Agent candidate above. The current ordinary
Runtime candidate `202074110717146fc7f08af2306a8dd7f695b0b1` / tree
`ee39286bd0eb27d4075074cc4785d6d15e33f243` has no `project-data.write` in its
schema/registry. The recovered Runtime review records 48 definitions/22
operation clauses versus Agent's 56/30. Hold App activation until Runtime
consumes the same Agent schema/registry through the existing `/v1` provider
and proves accepted-revision identity, idempotent retry, and mixed-batch
atomic refusal. Runtime remains a compatibility/transport owner, never a
second project-data semantic writer.

Do not mix this 56/30 project-data carrier with the separately reviewed
357/613 carrier.

## Evidence recovered from the worker log

The prior worker ran these focused lanes; no new tests are claimed by this
recovery:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PRIVATE_DIR" \
  /home/user/work/venv-app2-native/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider \
  "$PRIVATE_DIR/tests/editing_conformance/test_recipe_m2_project_data.py"
17 passed, 2 warnings in 1.04s
```

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/lib/timeline-patch.test.ts -t 'project-data'
68 passed, 233 skipped (301)

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  -t 'project-data|source-map|source map|DSL source'
6 passed, 53 skipped (59)

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  -t 'project-data|persists|delete removes|updated'
3 passed, 28 skipped (31)
```

The log also records a broader historical App lane (2 files/360 tests) and a
private Agent probe showing atomic refusal and inverse/redo/replay controls.
Those are evidence from the original review, not rerun here. No full suite,
browser, localhost, socket, Runtime HTTP, source edit, test edit, dependency,
schema, generated artifact, pin, or public adoption was performed.

