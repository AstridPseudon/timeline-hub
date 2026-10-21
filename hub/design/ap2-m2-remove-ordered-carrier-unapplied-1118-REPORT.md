# App ordered project-data remove: unapplied patch

Date: 2026-10-21 UTC

## Result

No App product source was changed. The worktree remains clean at App base
`0cc2583aa`. This is the smallest reviewed source-stage proposal for HOME to
apply only after the normal generated `AgentWrite` successor is available.
The current public014 live snapshot and its pin remain unchanged; no activation,
adoption, writer routing, or pin mutation was performed.

## Exact proposed source delta

The private candidate was applied only in a temporary copy, then removed. It
touches the requested paths:

1. `src/tools/video-editor/commands/projectDataMember.ts`
   - Accept the already-public `project-data.delete` input with a closed
     `{key}` payload and lower it to the normal Agent command
     `project-data.write` with `{target, key, mode: "remove"}`.
   - Keep `project-data.write` replace/merge lowering unchanged.
   - For remove, read the target namespace; refuse malformed non-object,
     non-null namespaces; clear one leaf; prune an empty namespace and then an
     empty `config.app`; preserve absent-key as an explicit absent→absent
     guarded write.
   - When pruning a namespace, pass the raw `Object.keys(config.app)` order to
     the existing `MoveRecording` write. Do not replace the parent or invent a
     second carrier/store.

2. `src/tools/video-editor/commands/clipMovePrimitives.ts`
   - Add an optional `insertionOrder` argument to `MoveRecording.assign/clear`
     and copy it only when present into `AgentWrite.insertion_order`.
   - Add the corresponding optional argument to `AuthoredState.set`; on a
     present-property restore, validate the historical sibling order and
     reinsert the key at its recorded position, failing with
     `history_unavailable` on a missing target or incompatible current order.
   - Preserve the existing append/replace path when the carrier is absent.

3. `src/tools/video-editor/commands/projectDataMember.test.ts`
   - Add direct coverage for delete lowering, full record replay, middle-key
     prune/reload/restore order, absent-key omission of the carrier, null
     namespace pruning, sibling presence, opaque values, and ordinary
     replace/merge compatibility.

This proposal deliberately does not edit the generated
`src/integrations/runtime/timeline-commit-types.ts`. The exact private test
copy reused Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c`’s normal
generated binding, whose `AgentWrite` is:

```ts
{ ref; path; before; after; insertion_order?: Array<string> }
```

The current App public014 type has only the original four fields. A normal
generated App binding refresh is therefore a prerequisite; a cast or hand edit
would hide the inverse/reload loss identified by blocker 0436.

## Offline parity review

The private candidate was checked against the authoritative Agent6c recipe:

- remove is still one `project-data.write` command with `mode: "remove"`;
- a non-empty namespace clears only the requested key;
- an absent key records an absent→absent write without `insertion_order`;
- null/empty namespaces are pruned;
- a pruned namespace records its original app sibling order;
- serialized command/record replay retains exact opaque/null/sibling data;
- inverse restoration uses the recorded order and redo returns the removed
  order.

Runtime lifecycle/accepted-history proof is intentionally not duplicated here.

## Evidence

Baseline on the unchanged App worktree:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 3 files passed; 31 tests passed
```

Private, temporary candidate (with the exact normal generated AgentWrite
binding copied from Runtime42a):

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 3 files passed; 33 tests passed

./node_modules/.bin/tsc --noEmit --strict --skipLibCheck --target ES2022 \
  --module ESNext --moduleResolution bundler \
  /tmp/ap2-m2-remove-private/private-agent-write-proof.ts
=> passed; ordered optional and ordinary omitted AgentWrite shapes typecheck

./node_modules/.bin/eslint \
  src/tools/video-editor/commands/projectDataMember.ts \
  src/tools/video-editor/commands/clipMovePrimitives.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed
```

Final unchanged worktree checks:

```text
git diff --check
=> passed
git status --short
=> clean
```

No full, browser, HTTP/socket, install, generated-schema update, pin,
activation, or live producer test was run. The temporary private copy and its
test-only files were removed.

## Handoff / prerequisite

HOME can apply the source proposal only after the normal generated binding is
landed and the existing App carrier is widened at the exact seam above. The
public014 snapshot remains the current live baseline until that paired review;
there is no product landing in this worker.
