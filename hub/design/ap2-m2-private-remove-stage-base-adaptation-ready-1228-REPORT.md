# Ordered project-data removal on REAL9ea

## Result

Applied the already-reviewed three-path ordered-remove semantic patch to the
REAL9ea App baseline, adapting only the legitimate `AuthoredState.set`
context difference: REAL9ea had already removed the obsolete asset/clip
special-case body. The optional `AgentWrite.insertion_order` carrier already
present in the protected generated binding was used; no generated, lock,
caller, pin, activation, or public-integration files changed.

Changed paths:

- `src/tools/video-editor/commands/projectDataMember.ts`
- `src/tools/video-editor/commands/clipMovePrimitives.ts`
- `src/tools/video-editor/commands/projectDataMember.test.ts`

The implementation accepts closed `project-data.delete` `{key}` operations,
lowers them to the existing `project-data.write` command with `mode: "remove"`,
records absent-to-absent writes without a carrier, prunes null/empty
namespaces, preserves raw app sibling order for namespace pruning, and
restores ordered properties with `history_unavailable` refusal on incompatible
state. Existing replace/merge lowering and ordinary four-field writes remain
unchanged.

## Verification

All commands ran in this worktree with the shared dependency installation
read-only and Vitest cache disabled:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/visualSeamProjectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/clipMovePrimitives.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts
=> 5 files passed; 136 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 \
  src/tools/video-editor/commands/projectDataMember.ts \
  src/tools/video-editor/commands/clipMovePrimitives.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts
=> passed

flock /home/user/work/.app-tsc.lock \
  ./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
=> exit 2 on 23 pre-existing diagnostics outside the changed paths; zero
   diagnostics in projectDataMember.ts, clipMovePrimitives.ts, or the test
   file. The failures are in travel-between-images, shotSetCapture, and
   Composition-dependent preview/composition/hooks/lib files.

git diff --check
=> passed
```

Protected-file identity check passed: `runtime.lock.json`,
`src/integrations/runtime/generated-contract-metadata.ts`,
`src/integrations/runtime/generated.ts`, and
`src/integrations/runtime/timeline-commit-types.ts` each hash exactly to its
REAL9ea `HEAD` blob. `git status --short` contains only the three authorized
paths.

## Independent review

A second pass over the final diff compared it with the approved UNAPPLIED
patch and the 1127 approval. The only source-baseline adaptation is the
signature/body context around `AuthoredState.set`; the ordered restore logic,
recording carrier, remove lowering, pruning, claims, and tests are retained.
The local discriminated operation type and replace-only limit helper were
tightened solely to make this REAL9ea TypeScript baseline narrow correctly,
without casts or runtime changes.

No browser, full, HTTP/socket, private-provider, frozen-proof, install, or
generated-binding rerun was performed, per task scope. No genuine semantic
baseline gap beyond the authorized context difference was found.
