# F-D108 D07 source disposition

Source-only disposition against `tl/integration` `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` (base named by the task; captured root `d6294843286c18e57af3c1874cf1996be42212d2`). No product or test file was changed.

## Important path correction

The three D07 predicates are not in `tests/timeline/test_inverses.py`. That path is the separate D05 inverse-test deletion (`deletion-ledger.agent.md:51`); it is absent at the D108 base. The three exact D07 bodies are in the reviewed source-rehearsal tree `c456b3281497653cecf44f61acd6fa30565d83c8`, `tests/test_timeline_editing_helpers.py`, file blob `6a483b5aa36d53d853d882cd3782c8517db4d476`. The current/captured D108 tree has that path at blob `0bd2bf1bf9688ab05acb84a39192672c65d976e6`, with the three bodies removed. This is a source-location discrepancy in the task wording, not a reason to map D05 inverse tests onto D07 timing behavior.

## Disposition

All three finite rows remain individually accounted for as `RESTORE_NEEDED_APPROVAL_GAP` under the exact D108 crosswalk. The D07 ledger’s approved interface retirement is real: detached `retime`/`retime_with_ripple` and the old `place_media`/`move`/`retime` recipe are not to be revived. It does not, by itself, clear the specific D07 review requirement to preserve the live timing/audio/window predicates. The current grouped native test is real source and is a strong positive candidate, but it is not an approved one-to-one mapping in the D108 crosswalk and lacks some old predicates (notably inverse/no-write or retired-policy refusal assertions).

Approval used for every row: `agent-review-d07-current.md:18-37` plus `deletion-ledger.agent.md:53`; the latter’s broad D07 retirement is explicitly subordinate to the former’s current review. D69 requires restore-needed bodies to retain the old assertions; D72 permits retirement only for the approved retired interface, not silent loss of live behavior.

### D07-1 — track-scoped ripple, audio isolation, parent extension

Old selector: `tests/test_timeline_editing_helpers.py::test_ripple_is_track_scoped_and_never_moves_audio`

Old exact source: `c456b328:93-111`; file blob `6a483b5aa36d53d853d882cd3782c8517db4d476`; body SHA-256 `2fa51658762c0efbbb6ba9384067d293729c7ec5abd779f1a4a425eb6c1435d3`.

Old predicates: visual `first` changes from `[0,1)` to `[0,1.5)`; later visual `second` shifts to `at=1.5` while retaining source window `[0,1)`; unrelated audio remains `(at,from,to)=(0,0,2)`; parent duration extends `2→2.5`; the old audio-target ripple and `parent_duration="preserve"` calls raise the named `TimelineEditError` messages.

Current source trace:

- `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_replaces_track_ripple_and_compiles_parent_extension`, lines 97-130, file blob `62384aad61494c67a614ad1a7122fee4119e0829`, body SHA-256 `f00b333665e159afc1bfa17f500e16343b39b15465d37b533834bd267517014c`. It uses current `capture_clip_trim` + `capture_move` + `execute`; it asserts visual playback intervals `[0,1.5)` and `[1.5,2.5)`, later source `[8,9)`, audio `[0,2)`, and compiled parent `2.5`. This is the closest actual current source and proves the positive native/compiler shape, but it does not assert the old literal first source window `[0,1.5)`, inverse/redo, or the two retired-policy refusal cases.
- Crosswalk partial candidates, exact current blobs/bodies: `tests/packs/timeline/test_cli_edit_flags.py::test_insert_time_moves_everything_after_it_later` lines 356-361, file `81ff077be92f6de6bc012bd607e18f7044030ce1`, body `3a01d8932dcdcc2ac6052e5570b8001dde0b5df0fe58de02048dab0ef4a3c833` (global insertion/duration only); `tests/sdk/test_timeline_checkout.py::test_close_gap_before_a_word_ripples_everything_after` lines 211-218, file `75a9fae98485d8b0e71261039664c4bdcaf9f7a5`, body `65299912c5edaea637439dd84fcebf02d37867893ab2e0c6ed62c3c690a1da84` (later word/clip timing only).

Disposition: `live_missing_coverage` for the old positive composite predicate and current inverse/no-write proof; `approved_interface_retirement` for the obsolete audio-target/parent-preserve `retime_with_ripple` policy calls. No genuine semantic uncertainty was found. The row is not cleared because the specific review requires the positive state to remain named and asserted.

Bounded proposal, no implementation here: extend the existing `test_recipe_m2_clip_trim.py` native grouped test, using only its current callers `capture_clip_trim`, `capture_move`, `execute`, `document_from_bundle`, and `timeline_duration_seconds`, to assert the old literal visual/audio tuples and exact `2.5` duration, then use the existing conformance `inverse` helper for exact undo/redo and unchanged audio. Do not add a ripple flag, revive `retime_with_ripple`, or invent a parent-preserve contract. Keep the retired-policy cases ledgered as interface retirement unless an already registered current command has an exact refusal semantics; none was found.

### D07-2 — source trim, speed, move, endpoint-length change, quantization

Old selector: `tests/test_timeline_editing_helpers.py::test_canonical_source_trim_speed_move_and_retime_intervals`

Old exact source: `c456b328:114-131`; file blob `6a483b5aa36d53d853d882cd3782c8517db4d476`; body SHA-256 `7c2a1ce6e8a400421422a6cd93aef8b8c06cee1f501c96213516af64690b3f74`.

Old predicates: create a speed-2 clip at `at=4` with source `[2,4]`; canonical fields remain and helper aliases are absent; the half-open quantized interval is frames `(120,150)`; inconsistent placement is refused; move to `10` preserves `[2,4]` and speed; retime start to `20` preserves the source window; endpoint `21.5` changes source `to` to `5`, retaining speed 2.

Current source trace:

- `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_trim_hold_is_source_time_and_playback_duration_applies_speed`, lines 84-94, file `62384aad61494c67a614ad1a7122fee4119e0829`, body `832c3327ca00455eba181f14a8e124a27beea008e514a64312fe641d449e16ae`: current `clip.trim` preserves source-time hold and playback duration for parametrized speeds, with `[1,5]` source assertions and inverse covered by its neighboring trim tests, but not move/endpoint-length together.
- `tests/editing_conformance/test_recipe_m1_commands.py::test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation`, lines 147-162, file `e70ad97b413c224d5471c065237ec9ca8f52254a`, body `796c81e844ab0401a1ebe98a2020beb3d5ab31442e9fe465e4e2142072477078`: current `capture_move` preserves `[2,6]`, speed 2, sibling isolation, inverse, and compilation, but is an occurrence move rather than the old combined parent trim/move sequence.
- `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_rational_fps_source_contact_and_half_open_intervals_are_not_requantized`, lines 165-178, file `62384aad61494c67a614ad1a7122fee4119e0829`, body `f3d8eea47e045f192284dff4fe8c70b87bf39fed877433040839a68cc284b7ac`: current rational-FPS contact, half-open frame boundary, duration, and no-unwanted-output-read predicates.
- The current grouped native candidate above is lines 97-130, same file blob `62384aad...`, body `f00b333665e159afc1bfa17f500e16343b39b15465d37b533834bd267517014c`; it combines trim endpoint change and move, but uses speed 1 and has no inverse or frame assertion.

Disposition: `live_missing_coverage` for one current-API test preserving the old combined speed-2 trim/move/endpoint/quantization sequence and the exact inconsistent-input atomic no-write purpose. `approved_interface_retirement` for the detached `retime` calls and the old `place_media` construction path. No genuine semantic uncertainty was found.

Bounded proposal, no implementation here: add one conformance case beside the existing trim case in `tests/editing_conformance/test_recipe_m2_clip_trim.py`. Build the existing `bundle` with source `[2,4]`, `speed=2`, and `at=4`; create sequential current commands with `capture_move` and `capture_clip_trim`, asserting the exact old values after each command, frames `(120,150)`, and `inverse`/redo equality. Reuse the existing current invalid-trim atomic case for no mutation. Allowed production callers remain only `astrid/sdk/timeline/_trim_commands.py:capture_clip_trim`, `astrid/sdk/timeline/capture.py:capture_move`, and the registered `clip.trim`/`clip.move` operations; do not add a replacement `retime` API.

### D07-3 — ripple shifts canonical source windows without touching audio

Old selector: `tests/test_timeline_editing_helpers.py::test_ripple_shifts_canonical_intervals_without_touching_audio`

Old exact source: `c456b328:145-155`; file blob `6a483b5aa36d53d853d882cd3782c8517db4d476`; body SHA-256 `b825f19f314baa5561afdac2f82c6bab8577d0fecd4543cbaa2818775271a2b0`.

Old predicates: first visual grows from one second to `1.5`; later visual shifts to `at=1.5` while retaining literal source window `[8,9]`; unrelated audio remains byte-for-byte unchanged.

Current source trace:

- `tests/editing_conformance/test_recipe_m2_clip_trim.py::test_native_group_replaces_track_ripple_and_compiles_parent_extension`, lines 97-130, file `62384aad61494c67a614ad1a7122fee4119e0829`, body `f00b333665e159afc1bfa17f500e16343b39b15465d37b533834bd267517014c`: actual current grouped trim/move asserts later `[1.5,2.5)` with source `[8,9]` and unchanged audio `[0,2]`, plus parent extension. This is an exact positive source-window/audio match for the central predicate, but lacks the old test’s original first-source values and an inverse/no-write assertion.
- `tests/sdk/test_timeline_media_verbs.py::test_trim_slip_and_move_keep_the_window_equal_to_the_hold`, lines 152-159, file `3cf3ea92225113204835ba6a74f796aed0eadbaf`, body `3cd35f2ab38f5daa40f4101401dc45bcddbd6fd54c937d97d8ded733c9c1e1b5`: single-clip source-window/hold invariant through trim, slip, and nudge; not track ripple or audio isolation.
- `tests/editing_conformance/test_recipe_m1_commands.py::test_trimmed_positive_speed_nonzero_occurrence_and_sibling_isolation`, lines 147-162, file `e70ad97b413c224d5471c065237ec9ca8f52254a`, body `796c81e844ab0401a1ebe98a2020beb3d5ab31442e9fe465e4e2142072477078`: sibling/source-window/inverse coverage, but no unrelated audio row or grouped parent extension.

Disposition: `approval_gap` on the existing grouped native candidate, not a retired-interface clearance. The current source visibly has the intended positive behavior; the specific current review/crosswalk still has no approved one-to-one mapping for this old predicate. No genuine semantic uncertainty was found.

Bounded proposal, no implementation here: protected review of the existing grouped test in `test_recipe_m2_clip_trim.py`, with a minimal assertion extension only if the reviewer requires the old literal first/source tuple and exact inverse/no-write check. Keep current callers `capture_clip_trim`, `capture_move`, and `execute`; do not introduce a ripple command or touch audio through a retired writer. If the existing body is accepted as exact positive coverage, record that approval against this selector individually; do not clear D07-1 or D07-2 by aggregate/operator count.

## Static source facts and limits

- `astrid/sdk/timeline/_trim_commands.py:15-92` is the current `clip.trim` implementation; `:95-101` captures it through `execute`.
- `astrid/sdk/timeline/capture.py:252-255` captures current `clip.move`.
- `astrid/sdk/timeline/commands.py:29-39,84,106` registers `clip.move` and `clip.trim`; `commands.py:201-255` executes the registered commands atomically and records claims.
- The current `Checkout.insert_time`, `close_gap`, and `ripple_delete` callers are separate public reflow APIs; none is an exact replacement for the old detached parent-media ripple helper.
- The current source has no `retime` or `retime_with_ripple` production caller. No retired writer was revived, and no new contract/auth/history/pin behavior was proposed.

## Verification

Source-only checks performed:

- `python3` AST parse plus in-memory `compile()` of the traced current test/source files: PASS.
- JSON parse and unique old-selector mapping check on the companion handoff JSON: PASS.
- `git diff --check`: PASS (clean tree; no product/test diff).

No pytest, import, collection, helper execution, fixture/service/probe, browser/render, install, or full suite was run, per the task’s source-only restriction.
