# Complete stored-cap current-join independent review

Decision: **HOLD** the exact candidate `6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214` / tree `32dc0de053ffb98d718077a111994181ae03ea15`.

## Verified scope

- Current-root diff `0d5009e18bee8e29f894dabf5db501a0fcea750f..6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214` is exactly the 30-file union of the 22 producer and 11 corrected consumer files; overlap is the three shared surface/bounds files.
- The producer computes `canonicalTiming.storedOccurrenceDurationMs` from the original occurrence in `shotCompositionProjection`, and the graph/session paths cover bootstrap, local preview, recovery and accepted-command projection. Popup bootstrap/recovery/save paths retain the verified raw composition and use identity-based raw counterparts.
- The scalar is not present in Runtime/command/timeline-data source fields. Graph-aware draft/publication exits use the retained verified raw counterpart, remove only the new scalar, restore raw same-name `canonical`/`canonicalTiming` collisions, preserve null/opaque/`__proto__`/ordering data, and visibly refuse when that derived exit lacks a verified basis. The generic no-basis serializer path is the blocking exception below.
- The consumer uses the existing private bounded config copy. The selected config/fact provenance, compiled transition vector and duration extent reach Player, still/`TimelineFramePreview`, and client render together. Per-clip malformed/missing/negative/non-finite caps fall back to effective bounds; editor/read geometry remains unchanged.

## Evidence

- Private13 focused cap lane: **2 files, 13/13 tests passed**.
- Producer-omission negative control (only scalar emission removed): expected failure, **2/2 tests failed** with `expected 5 to be 4` for paused and playing delivery; this confirms the consumer does not manufacture the cap.
- Serializer/session/graph neighbors: **8 files, 225/225 tests passed**.
- Proportional combined lane: **26 files, 585 tests; 577 passed, 8 failed**. The eight are the known MAIN574 lifecycle label assertions in `useVideoEditorPreviewSurface.lifecycle.test.tsx`; the diffs only add resolved clip labels. No cap assertion failed. These remain under separate fix `5404` and were not skipped, weakened, or imported.
- Scoped ESLint on all 29 TypeScript/TSX cap files: **exit 0**. `git diff --check`: **exit 0**.
- Static manifest check: producer 22 + consumer 11 = union 30; actual current-root diff 30; no missing or extra paths.

## Blocking finding

`serializeForDisk(resolved)` still takes its legacy raw-authored path when
`rawComposition` is omitted. A direct private13 probe using the actual
projected graph config showed that it persists
`storedOccurrenceDurationMs` in every projected clip. The same omission is
reachable through `serializeResolvedTimelineEdit`, whose existing command
and mutation callers pass no raw composition. This violates the settled rule
that the derived scalar is never authored, sent or stored. It is not the
known MAIN574 label failure or the ten App2 diagnostics.

Required bounded repair: ensure every derived serializer caller supplies the
retained verified raw basis, or make the no-basis derived exit refuse visibly
without guessing/scrubbing raw same-name metadata. Add a permanent regression
for the no-basis `serializeForDisk`/resolved-edit call shape before approval.

## Not claimed

No product files were changed by this review. No parity, pixel/audio, full-suite, project typecheck, build, install, browser, socket, or live-service claim is made. The ten existing App2 TypeScript diagnostics remain separate and are not evidence against this cap join.

Recommended next step: repair and independently re-review the serializer
boundary, then handle the separate 5404 label reconciliation and App2
diagnostics before central qualification.
