## Completed

- Narrowed `timeline.init`’s recorded reads to authored fields while preserving the exact pristine-parent guard.
- Added four original opaque-field reload → inverse → redo cases.
- Updated the golden fixture’s actual read footprint.
- Published ORCH/App2 reports, commit message, and `DONE`.

## Tests

- Focused initializer/provider tests: **31 passed**
- Actual Runtime `a0dca169` init/retry test: **1 passed**
- Actual Runtime init/birth neighbor tests: **2 passed**
- `git diff --check`: passed

No full suite, App activation, schema/wire/pin, release, or shared dependency changes.