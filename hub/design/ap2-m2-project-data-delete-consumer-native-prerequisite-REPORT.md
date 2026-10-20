# App project-data delete consumer prerequisite

Date: 2026-10-20 UTC
App base: `20ea14c26526fe4924354f10a177aebbaf6002bc`

## Decision

**No App source change and no native consumer activation.** There is no
official native carrier for project-data deletion in the live SDK or Runtime
pair. The reviewed `e010e6a3868e963471244491bb6672c3e4a5135e` Agent source
adds only the closed `project-data.write` v1, `mode: "replace"` carrier. It
does not add deletion or `unsetData`.

The existing App `project-data.delete` operation remains the legacy public
TimelinePatch path. It must stay reachable until Agent and Runtime provide a
matched native carrier and the existing `/v1` path is qualified. No write-null,
empty-value, undo-as-delete, frozen-schema (`39211e63…`) change, or current
generation change was made.

## Live source evidence

- Current Agent `tl/integration` has no `project-data`,
  `project-data.delete`, or `unsetData` operation in its SDK
  registry/schema.
- Agent e010 source registers exactly `project-data.write` in
  `astrid/sdk/timeline/commands.py`; its handler is
  `astrid/sdk/timeline/_project_data_commands.py` and requires
  `select: "parent"`, a canonical target/key, finite JSON, and
  `mode: "replace"`.
- The e010 schema has only the `project-data.write` operation clause and
  `ProjectDataWriteArgs`. Its own conformance test uses
  `project-data.delete` only as an intentionally unsupported member to prove
  a mixed batch is rejected atomically.
- Current Runtime has no project-data native provider/registry operation.
  Its reviewed contract remains a consumer of the Agent provider, not a
  second project-data writer.
- App's public `project-data.delete` is validated and compiled in
  `src/tools/video-editor/lib/timeline-patch.ts`. SourceMapRuntime calls it
  for `delete(extensionId, entryId)` after proving the exact
  `__sm__:<entryId>` key exists. Scene marker “Clear/Delete Data” currently
  writes an empty marker list; it does not delete the project-data key.
  There is no `unsetData` API in the live App/Agent path.

## Main delete semantics observed

The current App compiler is the live Main behavior. For a declared
`target = extensionId` and `key`:

1. It reads the raw extension namespace from `config.app[target]`, using an
   empty object only when the namespace is absent or `null`.
2. It deletes exactly the declared key. A present key whose value is `null`,
   `false`, `0`, `""`, `[]`, or `{}` is still present and is removed as
   a key; the value is not replaced with a sentinel.
3. Sibling keys and opaque sibling values are preserved. If no enumerable
   keys remain, the extension namespace is removed. If no extension
   namespaces remain, `config.app` is omitted from the next config.
4. An absent target namespace or an absent key is a no-op: no diff entry and no
   affected extension ID.

Representative raw transitions are therefore:

```json
// Delete ext/gone; preserve siblings and their opaque values.
before: {
  "config": {"app": {
    "ext": {"keep": {"opaque": [null, false, 0]}, "gone": null, "zero": 0},
    "sibling": {"leave": true}
  }}
}
declared deletion: {"target": "ext", "key": "gone"}
after: {
  "config": {"app": {
    "ext": {"keep": {"opaque": [null, false, 0]}, "zero": 0},
    "sibling": {"leave": true}
  }}
}

// Deleting the last key removes the namespace, rather than leaving {}.
before: {"config": {"app": {"ext": {"gone": null}}}}
declared deletion: {"target": "ext", "key": "gone"}
after: {"config": {}}

// Main treats a null or empty target namespace as empty for deletion.
before: {"config": {"app": {"ext": null}}}
declared deletion: {"target": "ext", "key": "gone"}
after: {"config": {}}
```

The native request must preserve this distinction between a missing key and a
present null/false/zero/empty value in its raw `before` recording. It must not
infer presence from truthiness or from `value !== undefined` alone.

## Exact Agent/Runtime peer request

Please add and pair one official native deletion carrier, with the operation
name, wire envelope, and DTO chosen and owned by Agent/Runtime. This report
does **not** invent or authorize a new operation name, DTO, endpoint, store,
or schema branch, and must not relabel `project-data.write` as deletion.
The carrier must be generated and qualified from the agreed source; do not
change frozen schema `39211e63…` or current generated artifacts in this App
prerequisite.

The carrier's semantic contract must be:

- **Raw before / declared deletion / after:** capture the raw presence state
  and exact value for the target key, including absent versus present `null`,
  `false`, `0`, empty string, array, and object. Delete only the declared
  extension target/key. For a missing target or missing key, leave the bundle
  unchanged. For a null or empty target namespace, match Main by treating it
  as empty and removing the target namespace. For a last-key deletion, remove
  the namespace and omit an empty `config.app`.
- **Guards:** retain exact target/key identity and raw before/after guards;
  refuse malformed non-null/non-object namespaces, stale leaf state,
  dependent later writes, and intervening writes including A→B→A. Preserve
  the normal project scope and parent selection guards. Never use a null write,
  empty-value sentinel, whole-namespace replacement, or undo command as a
  deletion substitute.
- **Limits and opaque data:** enforce the existing extension ID/key rules,
  including canonical non-empty keys, the 256 UTF-8-byte bound, and reserved
  outer keys. Deletion must not broaden any value/namespace limits. Do not
  parse, normalize, or rewrite opaque sibling values; retain sibling order and
  all sibling keys exactly.
- **Ordering and atomicity:** preserve input command order for source-map and
  other cleanup batches. A batch containing an unsupported member must refuse
  before capture, mutation, owner resolution, enqueue, or fallback; do not
  submit a filtered supported subset. Runtime must use the existing `/v1`
  transaction and provider registry so there is no partial write or second
  semantic writer.
- **Retry and inverse:** use the existing accepted-revision and idempotency
  behavior: a lost response/restart retry with the same identity returns the
  original accepted result, while a changed payload under the same key is
  refused. Inverse must restore absent keys as absent and restore exact raw
  values (including null/false/zero/empty/opaque values), with the normal
  guarded-intervening-write and dependency refusal behavior.

After the exact Agent source, Runtime generated counterpart, provider
registry, and `/v1` acceptance are paired, App can add a bounded inert delete
member using the existing public cleanup call sites and direct-neighbor proof.
Until then, the legacy App writer remains the valid path.

## Evidence

Targeted App neighbors, run on the unchanged worktree:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  src/tools/video-editor/lib/compiler-canary.test.ts
=> 3 files passed, 391 tests passed (3.29s)
```

The equivalent `--configLoader=runner` invocation was attempted first and
failed before collection because this repository config uses `__dirname`,
which is unavailable in runner mode. The normal bundled config run above
passed. No full, browser, localhost, live-socket, dependency, pin,
generation, or Runtime HTTP suite was run.

