# App private392 current consumer gate source

## Result

Composed the approved private392 generated Runtime counterpart and project-data
membership seam onto current App HOME (`35814b16a`, current `tl/integration`
line). The generated files are byte-identical to the reviewed counterpart
from `acc27e8dcf13b2296e7738d2e06199777ab3cb1f`; the membership implementation
preserves the reviewed source guards and public `ProjectDataPatchArgs` /
`projectDataValue` boundary. No public pin, DTO/API/store, schema edit,
delete/unset admission, or broad JSON admission was added.

Added one source-level native consumer driver to the existing generic
command-session harness. It uses the App generic port, command session,
outbox, and existing Runtime client/data-provider test seam. The driver covers:

- ordered project-data merge and replace lowering;
- original namespace/leaf expectations and opaque `null`/`false` values;
- lost acknowledgement, dispose/reload, persisted owner recovery, and exact
  idempotent request retry;
- disjoint stale-head rebase preserving a remote opaque sibling;
- same-leaf stale refusal with no accepted revision;
- guarded undo retaining the intervening disjoint data; and
- no non-handshake POST outside the `/commit` path (zero legacy save traffic).

This is consumer-native source proof, not a mounted UI gesture proof.

## Exact reviewed identities

- Runtime producer: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Runtime producer tree: `8be43e13acb436120f8a63b1a178d64c49422461`
- Runtime artifact manifest: `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`
- Runtime schema/health digest: `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`
- Agent normal private pin: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`
- Agent private source tree: `2f2685d85c3f65b458795100a8045371eb19ee06`
- Agent schema392 digest: `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- Reviewed App membership candidate: `3b4d84089119d09d5b7e9b7ee5fba33d17e3594c`

## Changed paths

- `runtime.lock.json`
- `src/integrations/runtime/generated-contract-metadata.ts`
- `src/integrations/runtime/generated.ts`
- `src/integrations/runtime/timeline-commit-types.ts`
- `src/tools/video-editor/commands/genericPatchCapture.ts`
- `src/tools/video-editor/commands/genericPatchCapture.test.ts`
- `src/tools/video-editor/commands/projectDataMember.ts`
- `src/tools/video-editor/commands/commitSession.genericPatch.test.ts`
- `src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts`

## Evidence

Passed in the assigned worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts
=> 3 files, 30 tests passed

node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d
=> ok runtime.lock.json (matches pinned producer commit)

node_modules/.bin/eslint src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts src/integrations/runtime/generated-contract-metadata.ts src/integrations/runtime/generated.ts src/integrations/runtime/timeline-commit-types.ts --ext ts --max-warnings 0
=> passed

node_modules/.bin/tsc --noEmit --pretty false
=> passed

git diff --check
=> passed
```

The focused App test uses the repository's existing fake transport harness;
it does not start HTTP, a live provider, Runtime Door, localhost, browser,
socket, or central test service. No full suite or public/integration adoption
was run. Matched live Runtime/provider/Door evidence remains the next gate.

## Decisions and next step

The generated files were copied as the exact reviewed producer output rather
than hand-edited. The current HOME's later generic ordinary test was retained
while adding the reviewed project-data cases. Unsupported delete/unset remains
outside native membership and therefore unchanged. The staged branch remains
isolated; the harness should commit it without integration merge/adoption.

Next step: independently review this current-root diff, then run exactly one
central matched private392 native/provider/Door qualification against the exact
Agent/Runtime identities above. A future mounted gesture remains separate.
