# App2 element PARAM native repair

Base: `d4850f997cf359ee6e95f9313f942721a3a5b4b6` (`tl/ap2-m2-element-param-native-repair`)

The literal `clip.set-params` helper now follows Agent 310e's authoritative
capture order: target identity, scalar clip identity fields, both element
reference aliases, and the bound asset registry's `media_id`, `object_id`,
`digest`, and `content_digest` leaves before PARAM writes. The registry reads
are added only when the clip's effective asset selector is `asset` or
`asset_id`, matching the existing native/old proven PARAM logic.

The element-revision helper was not changed. Existing authored guards,
explicit absent clears, unchanged writes, opaque/unknown literal values, and
selected-pack visible refusal remain intact. One focused asset-backed
occurrence PARAM regression covers the exact read order, changed and absent
clear writes, unchanged writes, opaque sibling preservation, and a changed
registry guard.

The helper remains source-only and unwired; no consumer or legacy writer was
changed.

## Evidence

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts` — **3 files, 155 tests passed**.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/elementCapture.ts src/tools/video-editor/commands/elementCapture.test.ts --report-unused-disable-directives --max-warnings 0` — **passed**.
- `./node_modules/.bin/tsc -p /tmp/element-param-native-repair-tsconfig.json --pretty false` — **passed**; temporary config was outside the worktree and removed afterward.
- Fresh corrected-helper command generation: `node --import tsx /tmp/element-param-native-repair-probe.ts > /tmp/element-param-native-repair-probe.json` — generated both element and asset-backed PARAM commands from the current helper.
- Direct Agent 310e submission: `AG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary; PYTHONPATH="$AG" /home/user/work/venv-app2-native/bin/python /tmp/element-param-native-repair-agent-probe.py /tmp/element-param-native-repair-probe.json` — both `validate_command` and `execute` accepted; element and PARAM each reported `command_exact: true`, `record_exact: true`, and `bundle_exact: true`.

No full, browser, localhost/live-socket, Runtime, dependency, shared-worktree,
package, pin, generated-file, consumer-wiring, or writer-retirement suite was
run. The initially attempted `--configLoader=runner` Vitest invocation was a
config startup failure because this repository config uses `__dirname`; the
successful focused command used the repository config without that loader and
`--no-cache`.
