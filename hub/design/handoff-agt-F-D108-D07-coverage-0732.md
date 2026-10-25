# F-D108 D07 faithful current coverage — source-only handoff

Candidate is based on `tl/integration` `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, with the only repository change in `tests/editing_conformance/test_recipe_m2_clip_trim.py`. Candidate blob is `1b34745fca1dcc21f15267f744711eb16d4b5700`; parent blob is `62384aad61494c67a614ad1a7122fee4119e0829`. The candidate adds three tests, 94 lines, and deletes nothing.

The three tests are source-qualified candidates held for independent protected review. They are not normal-merged by this worker; the orchestrator should land them only after the core terminal/MAIN decision.

## Exact original-to-current predicate map

### D07-1 — track-scoped ripple, audio isolation, parent extension

Old selector: `tests/test_timeline_editing_helpers.py::test_ripple_is_track_scoped_and_never_moves_audio` from `c456b328`, lines 93–111, body SHA-256 `2fa51658762c0efbbb6ba9384067d293729c7ec5abd779f1a4a425eb6c1435d3`.

New selector: `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_preserves_exact_track_scoped_ripple_timing_and_audio`, lines 133–158, body SHA-256 `a7b2497917104be830e6a1fcc0105c20b1b01d11a56f67ac98d63e33032c8e5b`.

The new source uses only current `capture_clip_trim`, `capture_move`, `execute`, and `document_from_bundle`. It preserves the original positive literals and asserts:

- input first visual `(at, from, to) == (0, 0, 1)`;
- first visual grows to `(0, 0, 1.5)`, i.e. playback `[0,1)` → `[0,1.5)`;
- later same-track visual moves to `at=1.5` while retaining source `[0,1)`;
- unrelated audio remains `(at, from, to) == (0, 0, 2)`;
- compiled parent duration is exactly `2.5`, from the original `2`-second placement.

The old audio-target ripple and `parent_duration="preserve"` refusal calls are not revived. They remain `approved_interface_retirement`; no exact current refusal replacement was invented.

### D07-2 — source trim, speed, move, endpoint length, quantization

Old selector: `tests/test_timeline_editing_helpers.py::test_canonical_source_trim_speed_move_and_retime_intervals` from `c456b328`, lines 114–131, body SHA-256 `7c2a1ce6e8a400421422a6cd93aef8b8c06cee1f501c96213516af64690b3f74`.

New selector: `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_speed_two_preserves_source_window_move_and_endpoint_length`, lines 161–191, body SHA-256 `8c971cd5f011d28ffec6b33cfb607eb44ef7683466cab69ccc08db4bd4488a2a6`.

The new source preserves the exact positive source/playback fields:

- speed-2 clip at `at=4`, source `[2,4]`, canonical `from`/`to` fields, and no `source_start`/`source_end` aliases;
- half-open frame interval `(120,150)` at 30 fps;
- a current canonical inconsistent placement/duration is refused before mutation and the input remains unchanged;
- current `capture_move` to `10` preserves source `[2,4]` and speed `2`;
- a second current `capture_move` to `20` still preserves source `[2,4]` and speed `2`;
- current source-time trim to `out_s=5` at `at=20` produces source `[2,5]`, speed `2`, and playback endpoint `20 + (5-2)/2 == 21.5`.

The retired `place_media`/detached `move`/`retime` construction path is not restored. The current refusal is an analogue through the registered `clip.move` duration/window guard, not a claim that the retired call signature still exists. No extra ABA or inverse obligation was added because it was absent from the original selector.

### D07-3 — shifted canonical source window and audio isolation

Old selector: `tests/test_timeline_editing_helpers.py::test_ripple_shifts_canonical_intervals_without_touching_audio` from `c456b328`, lines 145–155, body SHA-256 `b825f19f314baa5561afdac2f82c6bab8577d0fecd4543cbaa2818775271a2b0`.

New selector: `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_preserves_shifted_source_window_and_audio_bytes`, lines 194–224, body SHA-256 `958988f8e601107d89d856b1251037c6ca11e3e4bda617eb50ba4fc9633d83a6`.

The new source uses the supported current trim-plus-move sequence and asserts:

- first visual grows from playback `[0,1)` to `[0,1.5)`;
- later visual moves to `at=1.5` and retains the exact source window `[8,9]`;
- unrelated audio row is byte-for-byte equal to its deep-copied pre-edit row;
- compiled parent duration remains exactly `2.5`.

This is separately mapped as a live approval gap; it is not cleared by the existing grouped candidate or by D07-1 coverage.

## Existing source preservation and caller support

An AST parse plus in-memory `compile()` passed for parent and candidate. An AST source-slice/hash comparison passed for every pre-existing function: all existing bodies, arguments, assertions, and markers are byte-conserved. Only the three new selectors above exist in the candidate.

The supported production path is present in the current source: `_trim_commands.py:95` (`capture_clip_trim`), `capture.py:252` (`capture_move`), `commands.py:84,106` (registered `clip.move` and `clip.trim`), `commands.py:201` (`execute`), and `commit.py:302` (`document_from_bundle`). No retired writer, helper alias, product guard/schema/client/pin, fixture helper, or other source file was changed.

## Static verification

- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_recipe_m2_clip_trim.py`: PASS, `All checks passed!`.
- Parent snapshot with the same Ruff check: PASS, `All checks passed!`.
- `/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir=/dev/null tests/editing_conformance/test_recipe_m2_clip_trim.py`: PASS, `Success: no issues found in 1 source file`.
- Parent snapshot with the same mypy check: PASS, `Success: no issues found in 1 source file`.
- `git diff --check`: PASS.
- No pytest, import/collection, helper/fixture/function execution, probe/service, browser/render, install, or full suite was run, per the D108 family-body pause.

Evidence log: `workers/agt-F-D108-D07-coverage-0732/evidence/static-source.md`.

## Decision and next step

No incompatible authored positive input was found. The only deliberate translation is D07-2's retired inconsistent `place_media(start=0,end=3,source_start=2,source_end=4,speed=2)` refusal into the current canonical `clip.move` duration/window guard; this is reported as a current guard analogue while the old interface remains retired. Independent protected review should decide whether that analogue is sufficient for the exact refusal predicate before MAIN landing. No behavior was weakened and no old API was resurrected.
