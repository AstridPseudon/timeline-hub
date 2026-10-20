# App unused fallback shims — qualified deletion

## Result

Deleted exactly four App fallback-only modules from current App source. No
active loader, package alias, mock, test, renderer path, installed-theme source,
vendor source, package pin, lockfile, or supported unknown-element diagnostic
was changed.

Worker-visible source SHA before the harness commit: `cc4dff86b845432acc38dd9407ccb079a6a5a677`.
The harness commit SHA is pending because this worker does not run git commit.

## Product patch / file list

Only deletions, 4 files, 246 physical lines / 229 nonblank lines:

- `src/tools/video-editor/compositions/fallback/registry.generated.tsx`
- `src/tools/video-editor/compositions/fallback/theme-api.tsx`
- `src/tools/video-editor/lib/theme-api.fallback.tsx`
- `src/tools/video-editor/lib/registry.generated.fallback.ts`

Final `git diff --check`: PASS. No build output or temporary files remain in
the worktree.

## Qualification evidence

- Exact candidate-name/path search over tracked current source found no
  consumer outside the first candidate's self-import of the fallback theme
  type. The self-import disappeared with the deletion.
- Active renderer and sequence paths import package exports:
  `@banodoco/timeline-composition/theme-api` and
  `@banodoco/timeline-composition/registry.generated`.
- `config/vite/vite.config.ts` aliases the installed package and retains only
  the unrelated timeline-schema fallback. Vitest configs likewise resolve the
  package and dedupe it; no candidate fallback alias exists.
- `examples/embed-demo/vite.config.ts` has its own committed
  `examples/embed-demo/stubs/timeline-composition/*` fallback for a missing
  package. Those stubs are distinct files and were preserved.
- Installed package exports and the vendored source resolve the active theme
  API and generated registry. The package tarball and `vendor/timeline-theme-2rp`
  source remain untouched.
- `TimelineRenderer` still dispatches unknown/unavailable registry entries to
  loud `UnknownClipPlaceholderSequence` diagnostics; no refusal behavior was
  removed or rewritten.

## Tests and checks

```text
git diff --check
PASS

npx vitest run --config config/testing/vitest.config.ts \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts
PASS — 5 files, 65 tests, 0 failures

npx eslint --max-warnings 0 \
  src/tools/video-editor/compositions/TimelineRenderer.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx \
  src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts \
  src/tools/video-editor/compositions/TimelineRenderer.tsx \
  src/tools/video-editor/compositions/installed-themes.ts \
  src/tools/video-editor/sequences/registry.ts
PASS — exit 0

npx tsc -p tsconfig.app.json --noEmit
EXIT 2 — existing unrelated baseline errors:
  src/integrations/runtime/RuntimeConnectionProvider.tsx:90:53 TS7053
    string cannot index RuntimeRefusalCode map
  src/tools/video-editor/components/AgentChat/AgentChatNewChatButton.tsx:80:23 TS2550
    String.replaceAll unavailable under the configured lib target
```

Not run: full suite, browser, localhost/socket/service tests, install,
network, or central test service. No new tests were needed because the
existing current-source renderer/alias tests provide the replacement proof.
