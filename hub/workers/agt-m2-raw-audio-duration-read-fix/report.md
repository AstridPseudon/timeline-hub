## Completed

- Recorded raw-audio `duration_seconds` reads via existing `Recording` claims.
- Replay/accept now rejects changed duration metadata before writes.
- Preserved exact media pins, trim guards, speed/source units, opaque data, inverse behavior, and zero-write refusal.
- Added regression for the 8→7 replay counterexample plus same-value/inverse coverage.
- Wrote design/report/commit-message artifacts and `DONE`.

## Tests

- `test_recipe_m2_clip_trim.py` — **122 passed**
- CLI/provider neighbors — **126 passed**
- Parent-media neighbor — **25 passed**
- `py_compile` — passed
- `git diff --check` — passed

No full suite, Runtime suite, or actual Agent/Runtime legacy pair was run. Pairing remains held pending committed and independently approved corrected Runtime single-FD counterpart; rejected `ab4c` was not consumed.