# After-anchor schema refusal test correction

Scope: App after-anchor recorder test only. No product, schema, normalization, wire, caller, or activation change.

## Change

Converted the two new impossible `it.fails.each(['missing', 'null'])` cases in
`src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts` into ordinary
passing assertions:

- missing hold: exact `clip.hold must be a finite positive number` refusal;
- null hold: exact `clip.hold must be a finite positive number` refusal;
- both assert the input bundle is unchanged after refusal;
- each has an equivalent positive numeric-hold case retaining the `from`/`to`
  window and incoming transition and asserting successful capture/replay.

No pre-existing positive assertion, full-record parity case, zero-hold refusal,
or sub-0.05 positive-floor case was changed. No `it.fails` marker remains in
the after-anchor test.

The Main-compatible missing/null-hold acceptance requirement remains explicitly
**OPEN**. Frozen Agent `3b3208c43903b770010de0649691cfa566447822` requires a
positive numeric hold in the authoritative birth schema before raw-window
derivation; this worker does not invent acceptance or bypass that boundary.

## Verification

All commands ran with shared dependencies read-only and Vitest cache/temp data
under `/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca`:

```sh
TMPDIR=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca PARENT_AFTER_PARITY_OUTPUT=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca/parity.json ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/commitSession.parentMedia.test.ts src/tools/video-editor/services/parentMediaCommands.test.ts
```

Passed: 4 files, 47 tests.

```sh
TMPDIR=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/media.test.ts
```

Passed: 2 files, 82 tests.

The embedded parity checker was run against a private archive of frozen Agent
commit `3b3208c43903b770010de0649691cfa566447822`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca/agent-exact TMPDIR=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca /home/user/work/venv-app2-native/bin/python - /tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca/parity.json <<'PY'
from pathlib import Path
exec(Path('src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts').read_text().split('PYTHON_AFTER_PARITY\n')[1].split('\nPYTHON_AFTER_PARITY')[0])
PY
```

Passed: 4 complete command/record/bundle and deterministic rebase matches, 6
matching refusals, and zero-duration floor check.

```sh
TMPDIR=/tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca ./node_modules/.bin/eslint src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts --max-warnings 0
./node_modules/.bin/tsc -p /tmp/ap2-m2-afteranchor-schema-refusal-test-correction-0407.nbd3ca/tsconfig.focused.json --noEmit --pretty false
git diff --check
```

All passed. No browser, HTTP, native Door, or full suite was run.

## Review and handoff

The independent assertion-conversion review verified that the only changed
source path is the after-anchor test, the two refusal cases are atomic and
schema-aligned, the paired positive cases preserve window/transition intent,
and no expected-failure marker or original positive behavior was weakened.
Recommended next step: resolve the Agent schema/raw-window discrepancy in a
separate successor before claiming missing/null-hold acceptance or activating
this dormant path.

