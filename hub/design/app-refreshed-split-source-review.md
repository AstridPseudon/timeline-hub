# Refreshed split source review

## Verdict

**PASS, limited source review; no blocking findings in the approved scope.**

Reviewed frozen candidate `f665d5308cc018bc89eff73a5cff21dc8a3bf1b3` against its direct base `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`. The candidate is exactly the approved 18-path delta (`+4,486/-39`), including the two approved CORS paths; `git diff --check` is clean. No product files were changed in this review worktree.

This verdict is limited to the reviewed native single-parent source split primitive, its supported UI/SDK ingress, shared collection/mirror preflight, and the existing in-process command/outbox behavior. It is not a safe Runtime/App deployment qualification or a browser/e2e/Gate 5/Gate 6 closure.

## Line findings

No blocking findings.

- `src/tools/video-editor/commands/clipSplitCapture.ts:57-76,199-200` uses the shared `parentClipSplitRows` reader for both native capture and session eligibility. It rejects divergent parent/config mirrors, null or invalid collections, and duplicate/missing IDs without normalizing either mirror.
- `src/tools/video-editor/commands/commitSession.ts:324-384` binds the supported operation to the raw `parent/clip:<id>` identity, ignores opaque `app.canonical` ownership metadata, reserves and carries one caller-supplied right ID, re-executes the original guarded command after ACKs, and requires the exact prepared preview before enqueueing.
- `src/tools/video-editor/commands/clipSplitGesture.ts:50-93` fences capture/finish/submit and rejects duplicate completion; `src/tools/video-editor/commands/clipSplitCapture.ts:169-187,321-327` validates the closed command envelope and all captured claims on replay.
- `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts:22-42,48-80` and `src/tools/video-editor/hooks/useTimelineCommandsService.ts:768-840` route supported single-parent inputs through the shared port while retaining the established writer for group, multi-clip, occurrence, unsupported, and ordinary non-native paths. There is no fallback after native capture has started.
- `src/tools/video-editor/commands/commitSession.ts:124-203,226-242` keeps an unknown acknowledgement pending, appends dependent split/move suffixes durably behind it, and uses `pump(false)` so append completion does not implicitly retry the uncertain request. Explicit retry/recovery is still required.
- `src/shared/lib/media/mediaCrossOrigin.ts` and its test are byte-identical to refreshed root `7bb885b638838588a0dff81b64b7c34960ac07f3`; no auth/provider behavior was added.

## Verification

Commands run by this review:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-split-source-port/notes/runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/shared/lib/media/mediaCrossOrigin.test.ts
PASS: 1 file, 21 tests, exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python <read-only parity probe using git show f665d5308:.../recipe_m2_clip_split.json>
PASS: 1/1 native split command; complete record, authored output, inverse and redo verified, exit 0

git diff --check 85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c f665d5308
PASS: no output, exit 0
```

The source-port worker’s recorded bounded qualification remains relevant but was not repeated here: 38 files / 1,551 tests passed, native parity passed, changed-file lint passed, original callback preservation passed, and the known-failure guard passed. This review deliberately did not rerun that whole targeted selection.

## Open qualification limits

The following remain open and are not claimed by this review: actual safe Runtime pairing, browser gestures, real reload/restart, guarded undo against publication history, live socket/localhost behavior, observed zero legacy HTTP traffic, full suite, build, project typecheck, install, and decoded audiovisual pixel/audio parity. The candidate’s own in-process tests cover mounted recovery and guarded publication-inverse request construction, but do not close those real-environment checks.

No KEEP marker was created. No commit, checkout, merge, rebase, push, integration mutation, shared dependency/cache mutation, or build output was produced.
