# App2 M2 overlay native source review

## Verdict

**REQUEST CHANGES — source.** Consumer qualification and the whole overlay row
remain **HOLD**, as required by the brief.

The native behavior probe is clean, but the candidate does not pass the
required strict app typecheck: `elementOverlayCapture.ts` has eight new
candidate-local errors at lines 69, 86, 139, and 148 because `parent.config`
is still typed as nullable/general JSON after `assertParentBundle`. The same
run also reports unrelated existing errors in `elementCapture.ts` and the
Composition integration. Repair the candidate's config narrowing, then rerun
the app typecheck; no source edits were made in this review.

## Scope and source checks

- Reviewed exactly `a08b9f56e` over `01f891ab6`: 423 lines of
  `elementOverlayCapture.ts` and 85 lines of its focused test.
- Reuses `AuthoredState` and `MoveRecording`; it emits only the existing
  `track.create`, `clip.add`, and `clip.delete` operations.
- Existing-track creation preserves authored `at`, `hold`, `track`, complete
  element reference, params, opaque fields, sibling order, and mirrored clips.
- Absent destination creation reserves the supplied track/clip IDs once and
  stages `track.create` then `clip.add` atomically on a copied bundle.
- Selected project-pack refs fail closed before mutation with the explicit
  authenticated-Agent-authority error; literal refs remain positive. No
  existing producer or legacy path was gated by this source-only change.
- Delete is parent-scoped, guards collection membership/order, target row and
  declared dependency fields, and preserves unrelated data. Native inverse and
  replay were exercised below.

## Native parity evidence

Against frozen Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, using the
read-only private source and `/home/user/work/venv-app2-native`, actual
TypeScript-produced commands were submitted to Agent validation/execution.

Both existing-track and new-track cases returned:

```text
validate: accepted
execute: accepted
create_command_record_bundle_exact: true
delete_command_record_bundle_exact: true
inverse_exact: true
replay_exact: true
roundtrip: true
```

This compares the full command claims, records (including writes, reads,
selections, bindings, created IDs and derived writes), raw bundle, guarded
inverse, and replay—not reconstructed expected JSON.

## Tests and static checks

Passed:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/runner.test.ts
```

Result: **6 files, 245 tests passed**.

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/elementOverlayCapture.ts \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  --report-unused-disable-directives --max-warnings 0
```

Result: passed.

Failed, requiring repair before source approval:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

Candidate-local failures are TS18047/TS7053/TS2339 in
`elementOverlayCapture.ts` (nullable/general-JSON `config` use). The same run
also has pre-existing/non-candidate failures in `elementCapture.ts` and the
Composition files (`PreviewPanel/RemotionPreview.tsx`, `TimelineRenderer.tsx`,
`VisualClip.tsx`, and `playerEvaluation.ts`).

No full, browser, localhost, live-socket, dependency, shared-worktree, pin,
generated, Git, ledger, or source/test edits were made.
