# D08 stored-cap consumer: preserved boundaries

Status: corrected, unapplied consumer and tests patches returned.

## Corrections

1. The missing carrier was the existing internal seam from
   `VideoEditorAssetPanelSurface` to `TimelineFramePreview`/`Thumbnail`:
   the panel previously supplied only `config`. The patch carries the already
   compiled `compiledTransitions`, bounded `durationInFrames`, and the
   private `pairedConfig`/`projectionFact` identity through that seam. The
   still forwards the vector to `TimelineRenderer`; it does not compile a
   second vector. `PanelFrameAnchor` is unchanged, and no public API, DTO,
   store, renderConfig, or serialized field was added.

2. `storedOccurrenceDurationMs` is selected only when it is a finite,
   nonnegative number. In stored mode each clip independently falls back to
   its existing effective `occurrenceDurationMs` when metadata is missing,
   negative, nonnumeric, NaN, or infinite. Malformed values are never
   clamped to zero. Valid zero remains on the existing zero-length semantics.

The private stored-cap copy preserves the source/editor config and uses only
the approved `canonicalTiming.storedOccurrenceDurationMs` scalar. The clean
b1ef App extract accepts both patches with `git apply --check`.

## Evidence

- Mounted targeted Vitest lane: 6 files, 115 tests passed, exit 0.
- Scoped ESLint: all touched consumer/test neighbours passed with
  `--report-unused-disable-directives --max-warnings 0`.
- Scoped TypeScript: `tsconfig.worker.json` passed with the private current
  Composition build overlay.
- No App producer, producer types, session/pin, `TimelineData` field,
  Composition source, shared dependency, branch, or ref was modified.

The App producer recomputation and wire/storage stripping remain App-owned and
unverified. Controlled fixtures qualify consumer behavior only; they do not
qualify the producer. No full suite, browser, render, network, install,
socket, or live-service run was performed.

