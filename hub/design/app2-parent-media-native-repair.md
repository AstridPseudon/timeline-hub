# App2 parent media native repair

Implemented only the two independent review repairs over `3d47f353c`:

- Equal `parent.registry` and `parent.config.registry` mirrors without an
  `assets` map now create one recorded effective-container write and apply the
  new binding to both registries, preserving opaque fields.
- Equal empty `parent.clips` and `parent.config.clips` mirrors now both receive
  the birth and the record includes the authoritative `parent.config.clips`
  derived write/order.

The existing five-field media selection, detached verified response, alias,
stable IDs, command/record ordering, and prior positive behavior remain
unchanged. Exactly two focused regressions were added in
`parentClipAddCapture.test.ts`.

## Evidence

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/media.test.ts`
  — 2 files, 102 passed.
- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.parentClipAdd.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts`
  — 4 files, 221 passed.
- `node_modules/.bin/eslint src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts --max-warnings 0`
  — passed.
- `git diff --check` — passed.
- TS-to-Agent-310 parity probe:
  `node --import tsx /tmp/ap2-parent-media-repair-probe.mjs`
  followed by
  `AG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary; PYTHONPATH="$AG" /home/user/work/venv-app2-native/bin/python /tmp/ap2-parent-media-repair-compare.py`
  — both mirror cases passed Agent validation/execution with equal commands,
  records, authored bundles, projections, guarded inverses, and replay.

## Limits

No full suite, browser/socket journey, Runtime durability/reload gate, or
consumer wiring was run. No shared dependency, Runtime/App integration
worktree, legacy producer, generated file, or UI/session path was changed.
