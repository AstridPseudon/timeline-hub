# App M2 embedded shot-name fallback test conversion

## Scope

Converted only the three pre-existing `ShotEditorView` NAME cases exposed by
the bounded embedded fallback deletion. Product source and prompt code were
not changed. The canonical shot-settings row remains **OPEN**.

Each converted case now has both sides of the settled one-to-one contract:

- missing mounted `shot.set` authority visibly refuses the same dirty input,
  keeps the canonical graph unchanged, and makes zero canonical adapter or
  legacy/Supabase mutation calls;
- the identical input is then submitted through a supplied `shotSet` port,
  asserting occurrence capture, exact `{ values: { name }, clear: [] }` finish,
  and `shot.set` submission without canonical adapter publication.

The existing `useNameEditing` control continues to prove exact dirty-draft
restoration after a refused asynchronous completion. Existing settings,
opaque-field, and Runtime-payload assertions remain unchanged for the settings
case; standalone/unplaced catalog behavior is outside this conversion.

## Three old → new mappings

1. `rejects a competing name edit instead of silently adopting its new head`
   — old direct canonical fallback/stale-head publication → missing-authority
   refusal with the same `My older name` input, then the same competing graph
   input through supplied `shotSet` capture/finish/submit.
2. `publishes an uncontended name edit from its captured head` — old direct
   canonical publication → missing-authority refusal with the same `My name`
   input, then successful supplied `shotSet` submission of that exact input.
3. `keeps every unrelated raw field in the name writer graph and Runtime
   payload` — old raw graph/Runtime name writer → missing-authority refusal
   preserving the exact opaque input graph, then successful supplied
   `shotSet` submission of the same `Renamed` input with no canonical or
   legacy mutation traffic. The parameterized settings half retains the prior
   raw graph/wire assertions unchanged.

## Evidence

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx
PASS — 6 files, 65 tests

node_modules/.bin/eslint src/tools/travel-between-images/pages/ShotEditorView.test.tsx --max-warnings 0
PASS

git diff --check
PASS
```

Not run: full suite, browser/e2e, localhost/live sockets, TypeScript,
installation, build, or shared dependency/cache writes.
