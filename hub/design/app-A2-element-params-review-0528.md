# A2 review: FAIL

Reviewed `tl/app-A2-element-params-sol-0505` against PLAN A2/A3/P2 and C0 §§1–5.

Findings:

- The candidate’s 284 tests pass, and the strict handoff tests cover v2 encoding, raw child/sibling closure, unknown/null/absence values, reads, rollback, and idempotent recovery.
- However, the claimed complete chain is not genuinely tested. `PropertiesPanel.test.tsx` mocks the panel and editor ops; the positive handoff test manually invokes the hook callback and custom route. No test mounts the actual form → actual `PropertiesPanel` → actual `useClipEditing` → actual `useTimelineSave` → persisted outbox path.
- `saveElementParameterEdit` validates diffs, scope, head, version, selection, and params, but uses copied `basis.context` and does not visibly enforce the shared adapter/editor-owner authority before save/dispatch. This leaves the required forged/stale/wrong-editor ownership guarantee unproven.
- The `child-ownership-unavailable` RED is a current source defect in the candidate handoff path, not the historical element13583 trigger.
- No broad child-ownership waiver, legacy writer, or TS executor restoration was introduced.

Evidence:

```text
PATH=/opt/node20/bin:$PATH node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mjs" --configLoader runner --no-cache \
  --maxWorkers 1 --no-file-parallelism [10 requested files]
```

Result: `10 passed`, `284 passed`.

```text
flock -w 600 /home/user/work/.app-tsc.lock bash -lc '
  PATH=/opt/node20/bin:$PATH node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
  PATH=/opt/node20/bin:$PATH node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
  PATH=/opt/node20/bin:$PATH node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
'
```

Result: all three passed.

Changed-file ESLint with `--max-warnings 0`: passed.  
`git diff --check`: passed.  
Protected original census: only the six intended files changed; no protected journeys/schema/client/pin/graph/kit files changed.

No source edits were made. Required commit message and `DONE` marker were written. Recommended next step: add a real mounted end-to-end property-edit test and enforce adapter/editor-owner authority in the production callback path.