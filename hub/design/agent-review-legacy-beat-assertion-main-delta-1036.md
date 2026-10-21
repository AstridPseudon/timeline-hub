# Legacy numeric-beat assertion conversion review

## Verdict

**NOT APPROVE** for current landing tree `e6168133f32e908ce984ee3855ebb690e838acfa` (`tl/agt-m2-legacy-beat-qualified-current-landing-1014`). The source implementation at `73613d322405d83a98560ce0577c5751103804b9` is otherwise bounded and preserves the requested Main numeric beat behavior, but the current landing's `e6168133f` delta introduces a Main/native parity regression for the retained `bars` downbeat carrier.

This is an assertion-conversion finding, not a product edit. No repository product files were changed in this review.

## One-to-one conversion ledger

| Old assertion / behavior | Current numeric-grid counterpart | Result |
| --- | --- | --- |
| `tests/sdk/test_timing_compiler.py::test_missing_anchors_and_unmigrated_evaluators_refuse_honestly`, old parameter `{"on": "beat 1 after \\"again\\""}` on a fixture with no beat carrier; unsupported beat refused and bundle remained unchanged | `test_main_numeric_beat_carrier_resolves_legacy_moment_without_mutating_neighbor` (lines 233–261): numeric `beats`, `downbeats`, and `bars` carriers resolve; untouched neighbor and authored bundle remain unchanged | Native compiler: pass; Main parity: incomplete for `bars` |
| Old unsupported beat refusal | `test_main_numeric_beat_carrier_missing_table_fails_closed` (lines 286–296): empty numeric grid refuses with `no beat` | Pass |
| Old unsupported beat refusal / malformed input safety | `test_main_numeric_beat_carrier_uses_child_speed_and_half_open_window` (lines 264–283): malformed string, bool, and null grid entries refuse | Pass |
| No silent replay of derived timing | `test_native_unrelated_move_recompiles_legacy_beat_and_guards_carrier_table` (lines 299–341): carrier, clip timing, placement start, and track kind changes refuse | Pass |
| Main/native numeric-beat parity | `test_main_context_beats_matches_native_compiler_on_real_fixture` (lines 344–355): `beats` carrier on `tiny_publishable.json` | Pass for ordinary `beats`; does not cover `bars` |

## Blocking counterexample

Current Main still resolves beat pools through `astrid/sdk/timeline/model.py:1129-1140`, which calls `timeline_intent.beat_sources`. The current landing's `astrid/sdk/timeline_intent.py:138-140` selects `downbeats` for a downbeat and no longer falls back to `bars`.

The native compiler independently retains the fallback at `astrid/sdk/timeline/_timing_evaluators.py:148-151`.

Source/Main fixture probe, using `tests/fixtures/timeline_editing/tiny_publishable.json`, set `a-rocket` to `downbeat 1 after c1` and `a-music.app.astrid.beats` to each carrier:

```text
{"downbeats": [0, 1, 2]} -> native 1, Main 1.0
{"bars": [0, 1, 2]}      -> native 1, Main TimelineEditError (refused)
{"beats": [0, .5, 1, 1.5, 2]} -> native 1/2, Main 0.5
```

This contradicts the retained source-736 success assertion for `bars` (the parameter at test line 238) and means the current landing does not preserve one-to-one Main behavior. The minimal manager follow-up is to restore Main's existing `downbeats`-or-`bars` selection, then rerun the bounded parity lane; do not broaden this into generic marker publication.

## Requested contract checks

- Main's pool is placed audio only: `_MomentContext.beats` iterates `tl.clips(audio=True)`; the native path requires a non-parent owner and `lookup._is_audio`.
- Source speed/window semantics are explicit in `_resolved_beats` (source start, playback rate, and half-open `[start, end)` filter) and `_legacy_words` (source-window correction under speed).
- Native replay guards capture carrier arrays, clip order/membership via `collection.clips`, clip timing/speed/track fields, placement timing fields, and referenced track kind (`native_word_anchor.py:208-231`).
- No schema, API, DTO, pin, authority, generic-marker, HTTP, renderer, browser, or full-suite work was performed.

## Evidence

Source/tree under review: `e6168133f32e908ce984ee3855ebb690e838acfa`; source implementation commits `60d95d69f81ccff1a113c5aec66b6be6d6bee876` and `73613d322405d83a98560ce0577c5751103804b9`.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timing_compiler.py -k 'beat or native'` — **7 passed, 40 deselected**.
- Same environment, `tests/sdk/test_timeline_checkout.py -k 'beat'` — **2 passed, 102 deselected**.
- Same environment, the `tiny_publishable.json` Main/native probe above — **ordinary beats and downbeats pass; bars-only parity fails as reported**.
- `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/_timing_evaluators.py astrid/sdk/timeline/native_word_anchor.py tests/sdk/test_timing_compiler.py` — **passed**.
- `git diff --check` — **passed**; worktree remained clean.

The 57-test timing/compiler lane was not rerun per the brief because the focused source/Main probe was sufficient. No full, native/HTTP, render, browser, or live suite was run.

## Recommended next step

Manager should reconcile the current `timeline_intent.beat_sources` `bars` fallback with the native compiler before approval, then rerun the 7+2 focused lanes plus a `bars` Main/native parity assertion. The current tree should remain **not approved** until that is green.
