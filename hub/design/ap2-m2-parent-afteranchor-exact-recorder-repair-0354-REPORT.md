# Dormant after-anchor recorder repair

HOLD: the recorder repair is ready for review, but the entire requested raw-window contract cannot be satisfied against the frozen Agent reference. Missing/null video hold is refused by that Agent's command schema. Two new positive requirements remain explicit expected failures; this is not complete qualification or permission to activate.

Base: App `5ad9f184b70cb22c0b01d3bbf9bb22ba3cc8b4bb`, tree `6fefbe0850d72e0f5facf1c87cf44b1e4e55899e`. Reference: Agent `3b3208c43903b770010de0649691cfa566447822`, tree `84120e176540fbc2281dcff4b7186ec8ae413274`. Agent was read with git show and exported once into my own TMPDIR; no reference checkout or metadata write.

Read PLAN, app2 STATUS/INBOX/BRIEF and the 0344 review. No standalone HOME.md was present in the provided checkout; HOME's current pin/activation directions were read in STATUS/INBOX. Scope remains M2.

## Changes

Only `parentAfterAnchorCapture.ts`, its test, and the existing `parentClipAddCapture.ts` seam changed. Live callers changed: **none**. Existing append/swap/session tests were not edited.

Deleted append-then-decorate and the synthetic replacement of derived_writes. The dormant path now uses the existing MoveRecording execution seam: validate media/rate/raw row, select/read the anchor and ordered peers, write same-track peer timing, compile the mirror before creation, insert at the recorded boundary, and finish compilation. The append caller keeps its original path. No new engine or wire carrier.

Removed at_ms strip/restore: a cloned source at_ms refuses, while a later peer's supported raw at_ms timing write is retained. Preserved incoming transition and opaque fields. Explicit null effect IDs remain null; explicitly null track/asset overrides refuse. Duration calculation permits zero and floors at 0.05, while the authoritative birth schema still refuses a zero-hold row.

The focused regression checks the COMPLETE record, including command, reads, selections, bindings, writes, created IDs, dependencies and both mirror states. An embedded reproducible Python checker additionally compares the exported App outputs with actual Agent capture/execute/rebase replay. It does not substitute final-bundle equality for recorder parity.

## Evidence that corrects the review

1. Actual Agent produces **two** derived mirror writes for a nonzero same-track ripple: the handler's pre-create `compile_mirrors()` and `commands.execute()`'s final `compile_mirrors()`. The review's assertion of one write is incorrect. The repair records both naturally at those points, without rewriting recorded history.
2. Agent's raw `_clip(raw_window=True)` supports deriving a missing/null hold, but the authoritative `execute()` rejects the command before reaching it. `ClipAddMediaArgs.row` references `ClipAddArgs.properties.row`, which requires hold and defines it as a number with exclusive minimum zero. Actual results:
   - missing hold: `invalid_edit_command: 'hold' is a required property`
   - null hold: `invalid_edit_command: None is not of type 'number'`
   - zero hold: `invalid_edit_command: 0 is less than or equal to the minimum of 0`
   - source at_ms: `unsupported_timing: media edit does not support at_ms`

Therefore accepting missing/null hold here would repeat the App-only acceptance problem. The App refuses these rows and keeps two new positive transition/missing-hold requirements as `it.fails`, with the precise Agent schema prerequisite named. A positive sub-0.05 duration proves the floor. The Python checker also verifies that Agent's capture-row helper computes the zero-duration floor before the schema refuses the resulting row.

## Tests

All tests used existing dependencies read-only. TMPDIR was `/tmp/w-d5d5a74fca`. A private copy of `config/testing/vitest.config.ts` preserved its root, aliases, plugins, setup and tests; imports were made absolute, and cacheDir pointed inside TMPDIR. Its config bundle was also emitted under TMPDIR, never the shared node_modules.

The final capture run was:

```sh
TMPDIR=/tmp/w-d5d5a74fca PARENT_AFTER_PARITY_OUTPUT=/tmp/w-d5d5a74fca/parity.json ./node_modules/.bin/vitest run --config /tmp/w-d5d5a74fca/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/commitSession.parentMedia.test.ts src/tools/video-editor/services/parentMediaCommands.test.ts
```

Result: **4 files, 45 passed, 2 expected failures (47 total)**. The last two supplied filters name nonexistent files and matched nothing; they are not counted as coverage. The real session/media neighbors were then run by their actual paths:

```sh
TMPDIR=/tmp/w-d5d5a74fca ./node_modules/.bin/vitest run --config /tmp/w-d5d5a74fca/vitest.config.ts --no-cache src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/media.test.ts
```

Result: **2 files, 82 passed**. The session fixture uses its injected in-memory transport; no listener, network request, browser or native Door was used. This is neighbor regression coverage, not session/HTTP acceptance evidence.

Exact Agent parity command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-d5d5a74fca/agent TMPDIR=/tmp/w-d5d5a74fca /home/user/work/venv-app2-native/bin/python - /tmp/w-d5d5a74fca/parity.json <<'PY'
from pathlib import Path
exec(Path('src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts').read_text().split('PYTHON_AFTER_PARITY\n')[1].split('\nPYTHON_AFTER_PARITY')[0])
PY
```

Result: **4 complete commands/records/bundles and deterministic rebase replays matched; 6 refusals matched; zero-duration floor matched**. Cases include ordinary rate-aware ripple, incoming transition, explicit null effect IDs and the positive small-hold floor. Initial parity testing exposed the schema mismatch above; it was not discarded or bypassed.

```sh
TMPDIR=/tmp/w-d5d5a74fca ./node_modules/.bin/eslint src/tools/video-editor/commands/parentAfterAnchorCapture.ts src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.ts --max-warnings 0
TMPDIR=/tmp/w-d5d5a74fca ./node_modules/.bin/tsc -p /tmp/w-d5d5a74fca/tsconfig.json --noEmit --pretty false
git diff --check
```

All **passed**. The private TypeScript config extends the repo's tsconfig.app.json, includes the three touched files including the test, clears its test exclusion, sets incremental=false, and uses the existing node types through an absolute typeRoots path. This is a focused typecheck, not repository-wide types.

An initial `--configLoader=runner` invocation failed before tests with the existing config's `__dirname is not defined`; the private config resolved this without product/config edits. An initial private type config lacked Node type resolution; adding its existing absolute typeRoots resolved that harness issue. Neither startup attempt is counted as a test pass.

No full suite, UI/browser/native HTTP qualification, activation, pin, generated contract, Provider or session source change. All temporary copies/configs/exports were removed after checks. No shared dependency or cache was changed. Worktree contains only the three intended source/test modifications.

## Handoff

Review the bounded recorder repair independently. Keep it dormant and HOLD the missing/null-hold acceptance requirement: Agent ownership must resolve its schema/handler disagreement before that behavior can be delivered. No App-only normalization or invented carrier is justified. BLOCKED records this exact remaining requirement; DONE is intentionally absent.
