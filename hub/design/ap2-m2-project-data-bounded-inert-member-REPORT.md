# App project-data bounded inert member

Implemented the requested row-local, unregistered App source unit on
`tl/ap2-m2-project-data-bounded-inert-member`.

## Changes

- Added `src/tools/video-editor/commands/projectDataMember.ts`.
- Added `src/tools/video-editor/commands/projectDataMember.test.ts`.
- Uses the existing `EditCommand`, `CommandRecord`, `AuthoredBundle`, and
  `MoveRecording` carriers.
- Emits only the agreed private Agent shape:
  `project-data.write` v1, `select: "parent"`, explicit `mode: "replace"`,
  and `args.target/key/value`.
- Captures one ordered `commands[]` and records exact raw parent
  `config.app` container/leaf reads and claims. Property claims use Agent
  spelling for dotted extension IDs and opaque keys.
- Supports absent/null/object container birth, exact leaf null/absence guards,
  sibling preservation, finite JSON, canonical keys, size/count limits, and
  nested reserved-key refusal.
- Refuses order-bearing operations, merge mode, malformed namespaces, unsafe
  values, and mixed batches before materialization. No dispatcher, UI,
  outbox, Runtime wire/API, public export, vendor, or legacy-writer change.

## Tests and checks

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/projectDataMember.test.ts
8 passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/genericPatchCapture.test.ts
8 passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/lib/compiler-canary.test.ts -t 'project-data|source-map|source map|DSL source'
6 passed, 53 skipped

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/lib/source-map-runtime.test.ts -t 'project-data|persists|delete removes|updated'
3 passed, 28 skipped

./node_modules/.bin/tsc --noEmit --pretty false
passed

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PRIVATE_DIR" /home/user/work/venv-app2-native/bin/python -m pytest -q -o addopts= -p no:cacheprovider "$PRIVATE_DIR/tests/editing_conformance/test_recipe_m2_project_data.py"
17 passed, 2 warnings
```

The Agent lane ran from a private archive of commit `0a774e4968f5a9728c4ee6b5bbbfe286e26f29a3`; the archive was removed after use. A bounded subprocess probe sending actual TS-generated carriers into that private Agent timed out at five seconds, so TS-to-Agent execute/inverse/replay parity is **not claimed**. The direct App replay test and the Agent’s own 17-test contract lane pass.

No full, browser, localhost, socket, Runtime HTTP, dependency, generated
artifact, public pin, or adoption test was run.

## Decision / next step

Keep this member inert until the matched Runtime `project-data.write` artifact
and paired App consumer are qualified together. The existing generic/legacy
writer remains untouched and is not authorized for retirement by this source
proof.
