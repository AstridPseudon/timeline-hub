# App2 ordinary compiler-canary native slice

## Result

No App product source change is safe for this row. The current compiler-canary
snapshot ingress is the source/source-map `project-data.write` batch at
`src/tools/video-editor/lib/compiler-canary.ts:421-441`. It is authored
extension project data, not derived timing and not a clip edit. The canary
keeps that batch together, then creates a separate generated-clip proposal.

The smallest App-local command recipe already exists as the inert
`captureProjectDataMember` helper: it captures the complete batch as one
ordered `commands[]` intent and preserves exact target/key/value/absence and
opaque siblings. Its tests also compare the native projected bundle with
`compileTimelinePatch` output. It cannot be activated because the current
Agent command registry has no `project-data.write` operation.

No shared session/Provider/useTimelineOps/door/outbox file was changed. No
sequential submissions, partial batch, second compiler writer, new wire/store/
API, fallback deletion, pin/adoption, or ordinary26437 rerun was performed.

## Actual producer and boundary

- `buildDslWriteOps` emits one `project-data.write` for the serialized DSL.
- `buildSourceMapOps` emits one `project-data.write` per source-map entry.
- `processDsl` submits `[...]` as one `dataPatch` through `timeline.apply`.
- The generated clip `mainPatch` is a separate proposal; it is not the
  source/source-map ingress and must not be combined with it.
- DSL `duration` is source intent in the stored artifact. It is not a reason
  to rewrite derived timing or to manufacture a clip command for project data.

The exact current producer operation is:

```json
{
  "op": "project-data.write",
  "target": "com.example.compiler-canary",
  "payload": {
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "{\"version\":1,\"sourceUri\":\"dsl://com.example.compiler-canary/main.json\",\"clips\":[{\"id\":\"canary-clip-1\",\"track\":\"V1\",\"at\":0,\"duration\":1,\"clipType\":\"hold\",\"sourceLine\":3}]}",
    "mode": "replace"
  }
}
```

The App helper’s command-shaped form is the existing supported row recipe,
but it is only a staging helper until Agent and Runtime publish the matching
operation:

```json
{
  "schema_version": 1,
  "op": "project-data.write",
  "version": "1",
  "select": "parent",
  "args": {
    "target": "com.example.compiler-canary",
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "{\"version\":1,\"sourceUri\":\"dsl://com.example.compiler-canary/main.json\",\"clips\":[{\"id\":\"canary-clip-1\",\"track\":\"V1\",\"at\":0,\"duration\":1,\"clipType\":\"hold\",\"sourceLine\":3}]}",
    "mode": "replace"
  }
}
```

It must remain one command batch for source plus source-map entries. A
supported clip command cannot substitute for this target/key namespace without
changing authored state and losing project-data limits and guards.

## Executable absent-recipe witness for Agent

Against the current Agent checkout `/home/user/work/agent` (commit
`57d66356`, tree `0174fd49bd175a726a44542d1d6e31bca13c0f02`), this exact
probe was run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent \
  /home/user/work/venv-app2-native/bin/python3 - <<'PY'
from astrid.sdk.timeline.commands import CommandError, validate_command

command = {
    'schema_version': 1,
    'op': 'project-data.write',
    'version': '1',
    'select': 'parent',
    'args': {
        'target': 'com.example.compiler-canary',
        'key': '__dsl__:dsl://com.example.compiler-canary/main.json',
        'value': '{"version":1,"sourceUri":"dsl://com.example.compiler-canary/main.json","clips":[{"id":"canary-clip-1","track":"V1","at":0,"duration":1,"clipType":"hold","sourceLine":3}]}',
        'mode': 'replace',
    },
}
control = {
    'schema_version': 1,
    'op': 'clip.set',
    'version': '1',
    'select': 'parent/clip:canary-clip-1',
    'args': {'values': {'hold': 1}, 'clear': []},
    'intent': {},
}
for label, candidate in [('project-data.write', command), ('existing clip.set control', control)]:
    try:
        validate_command(candidate)
    except CommandError as error:
        print(f'{label}: REFUSED kind={getattr(error, "kind", None)!r} message={error}')
    else:
        print(f'{label}: ACCEPTED')
PY
```

Observed:

```text
project-data.write: REFUSED kind='unsupported_operation' message=unsupported operation 'project-data.write'
existing clip.set control: ACCEPTED
```

This is an absent-recipe witness, not permission to map project data onto
`clip.set`, `track.set`, or a whole-document restore. Agent must publish the
closed target/key command and Runtime must publish the byte-compatible schema
and provider registration before App can wire the existing helper through the
shared command session.

## Verification

Passed the exact affected canary and generic-capture neighbors:

```text
TMPDIR=<private temporary directory> ./node_modules/.bin/vitest run --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/source-map-runtime.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/commands/projectDataMember.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 5 files, 418 tests passed
```

Also passed `git diff --check`. No full suite, browser, localhost/socket,
central test service, dependency/cache/venv mutation, Runtime HTTP, or
ordinary26437 gate was run.

## Changed exports and live callers

Changed exports: none; the worktree is source-clean.

Relevant existing exports and actual callers, verified with `rg`:

- `createCompilerCanary` and `createCompilerCanaryExtension` — called by the
  compiler-canary tests and the extension factory in `compiler-canary.ts`.
- `captureProjectDataMember` / `captureProjectDataPatch` — called only by
  `projectDataMember.test.ts`; no live App consumer imports them yet.
- `compileTimelinePatch` — called by `useTimelineOps.ts`,
  `useTimelineCommandSession.ts`, and the test environment; the compiler
  canary itself intentionally calls only the public `TimelineOps.apply`.
- `useTimelineOps` — mounted by `useTimelineState.ts`; its shared dispatch seam
  remains untouched.

## Recommended next step

Agent should add the smallest closed `project-data.write` recipe with exact
target/key presence/value recording, guarded inverse/replay, and source-map
batch ordering; Runtime should pair its existing `/v1` command schema/provider
registration. Then App can activate `captureProjectDataMember` through the
existing command-session batch port in a separate owner-approved shared-seam
change. Until that pair exists, retain the current all-unsupported snapshot
fallback and keep the compiler canary source/source-map batch intact.
