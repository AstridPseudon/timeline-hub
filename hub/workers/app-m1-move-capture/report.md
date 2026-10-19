Implemented the UI adapter handoff:

- Service moves and drag freeze the original host capture basis, then submit command claims with a thin TimelinePatch preview.
- Removed move fallbacks; unsupported moves refuse explicitly.
- Projection lookup retains raw clip IDs and occurrence owners.
- Exported `ops.clipMove: ClipMoveCapturePort` with `capture`, `finish`, and `submit`; documented the seam in shared coordination notes.

Final validation passed:

```bash
npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/{commands/semanticGestures.test.ts,hooks/useClipDrag{,.softtag}.test.tsx,data/shotComposition{,Adapter,Editor,Projection,.architecture}.test.ts,lib/timeline-patch.test.ts}
```

**409 tests passed across 9 files.**

```bash
npx eslint src/tools/video-editor/{commands/semanticGestures{,.test}.ts,hooks/useTimelineCommandsService.ts,hooks/useClipDrag{,.helpers}.ts,hooks/useClipDrag.test.tsx,hooks/useTimelineState.types.ts,data/shotCompositionProjection{,.test}.ts}
git diff --check
```

Both passed. No full suite or browser tests ran.

The manager assigned actual built-in capture and Python/TS parity to `app-m1-capture-parity`. Follow-clear/map/guard semantics remain unverified here; mocked refusal tests prove adapter propagation only. Next: integrate that implementation and install the port through session/outbox wiring. Missing capture intentionally refuses moves.

Commit message written to the requested `commit-msg` path. No manual git mutation.