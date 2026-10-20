# App2 M2 overlay strict-types final review

## Verdict

**APPROVE SOURCE** for `tl/ap2-m2-overlay-strict-types-repair` at
`6e592c1b1` (`fix(app): narrow overlay parent config`).

This approval is limited to the strict config-narrowing repair over the
already native-exact overlay helper. Selected authority, consumer wiring, and
whole-element-row gates remain **HOLD**.

## Source review

The candidate delta from `a08b9f56e` is one helper and five call-site changes in
`src/tools/video-editor/commands/elementOverlayCapture.ts`. `parentConfig`
reuses the existing `object(...)` guard and fails with the same source-pin
error when `parent.config` is absent or non-object. It only narrows the value
to the existing JSON-object shape; it does not add `any`, an unsafe cast, a
weaker guard, a new command field, or a tsconfig change. `git diff --check`
passes and the worktree is clean.

## Evidence

Focused tests:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/runner.test.ts
```

**6 files, 245 tests passed.**

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/elementOverlayCapture.ts src/tools/video-editor/commands/elementOverlayCapture.test.ts --report-unused-disable-directives --max-warnings 0
```

**Passed.**

Actual strict ES2020 project check:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

It exits 2 with 11 unrelated existing errors: one in
`src/tools/video-editor/commands/elementCapture.ts` and the remainder in the
Composition integration (`PreviewPanel/RemotionPreview.tsx`,
`TimelineRenderer.tsx`, `VisualClip.tsx`, and `playerEvaluation.ts`). There are
zero errors in `elementOverlayCapture.ts`; the eight candidate-local
nullable/general-JSON config errors from the prior review are gone.

Fresh current-TS to Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` probe:

```text
node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/current-overlay-types-final-probe.mts
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AG" /home/user/work/venv-app2-native/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/current-overlay-types-final-compare.py \
  /tmp/current-overlay-types-final-probe.json
```

The temporary probe covered an existing visual output track and an absent
destination track. Both produced commands were accepted by Agent; both
`track.create` + `clip.add` and `clip.add` cases, followed by `clip.delete`,
had exact full command/record/bundle parity. Guarded inverse and deterministic
replay matched in both cases, including the final round trips:

```text
existing_track: validate=accepted create_exact=True delete_exact=True inverse=True replay=True roundtrip=True
new_track: validate=accepted create_exact=True delete_exact=True inverse=True replay=True roundtrip=True
```

The temporary probe files and output were removed after the run.

## Limits and next steps

No full, browser, localhost/live-socket, Runtime, dependency, shared-install,
pin, generated-file, source, test, Git, or ledger mutation was run or made by
this review. The selected-pack authority seam, consumer integration, and
whole-row qualification still require their separately assigned gates before
any overlay producer is approved end to end.
