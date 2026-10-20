# App manual chooser: unique local option names

## Result

Fixed the reviewed keyboard-selection defect in the Runtime manual chooser. Each chooser-facing destination name now has a local ordinal prefix before the existing raw shot, occurrence, and child-track labels. The existing local `id` lookup and all frozen raw bindings remain unchanged; no canonical ID or field was added, and the name is never parsed back into authority.

Added normal-suite regressions for keyboard selection of duplicate child-track labels and duplicate cross-occurrence labels. Pointer selection and the intentionally unavailable native placement callback remain unchanged.

## Validation

All commands ran from `/home/user/work/wt/app-m2-manual-chooser-unique-bindings` with Vitest runner loading, `--no-cache`, private `/tmp` cache, `maxWorkers=1`, and file parallelism disabled.

- `./node_modules/.bin/vitest run ... RuntimeRecoveryChooser.test.tsx`: **32 passed**.
- Original targeted 19-file chooser/recovery set: **247 passed across 19 files** (the prior 245 plus two new regressions).
- `./node_modules/.bin/eslint src/features/tasks/components/TasksPane/utils/runtimeRecoveryDestinations.ts src/features/tasks/components/TasksPane/RuntimeRecoveryChooser.test.tsx`: **passed**.
- `git diff --check`: **passed**.
- `RuntimeTaskRecovery.test.tsx` rerun alone: **29 passed**. A combined four-file neighbor run had one cross-file callback failure (117/118); the isolated rerun passed, so no source change was made for it.

The retained review control file was also exercised unchanged: 6/8 passed, while its two failures were literal lookups for the pre-fix unprefixed display strings. The equivalent updated keyboard controls are now in the normal chooser suite and pass; the review artifact was not modified.

No full suite, build, browser, socket, install, or TypeScript run was requested or performed. No shared dependency, runtime, or cache files were modified. The native ADD callback remains intentionally absent and no placement acceptance is claimed.

## Decisions and next step

Used the review’s settled minimal fix: ordinal-prefix the selector’s existing name-valued option locally, preserving raw bindings and media pin immutability. No upstream refresh overlap was encountered in the owned chooser files.

Next step is independent qualification against the matched native ADD/command-service release, including canonical commit/undo and browser acceptance. The current change only proves chooser routing and keeps native placement honestly unavailable.
