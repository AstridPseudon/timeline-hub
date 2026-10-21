# D09 bound coverage adapter independent review

## Verdict

**Blocked: no safe product patch.** The completed candidate worktree is
byte-identical to `tl/integration` (`a086cc6db`): no new
`onscreen`/`scene_answers` adapter, retirement, or original-positive
conversion is present to qualify.

The precise missing carrier is between the old caller and public Scene:

- `astrid/sdk/timeline/check.py::_CheckMixin._on_screen()` constructs a new
  `{tracks, clips}` render-config projection and calls
  `astrid.core.timeline.onscreen.coverage()`.
- `astrid/core/rendering/scene_answers.py::host_frames_at()` requires the
  retained Root `props` (including exact timeline/assets/theme) and `basis`;
  `_prepared_host_frames_at()` additionally requires the retained source
  paths, prepared-root lifetime, project/pin and materialization arguments.
- The old caller supplies none of those source-bound values. It cannot be
  routed through the public Scene adapter by changing only the allowed
  `onscreen.py`/`scene_answers.py` surface without inventing a source carrier
  or changing the caller-owned SDK path.

Therefore retiring the transition/fallback coverage math now would lose the
old caller's successful DIP behavior. Keep the current transition branch and
private pixel/crop/statistics behavior. Do not convert this no-source path to a
guessed public answer; preserve the existing explicit unavailable behavior on
already source-bound managed Scene failures.

## Evidence

Static source trace:

- `check.py:93-119`: old caller builds only `tracks`, `clips`, `fps`, canvas
  and element declarations, then invokes `onscreen.coverage()`.
- `check.py:246-281`: only an explicitly connected checkout uses the separate
  managed Scene path; detached/save checkouts fall back to `_on_screen()`.
- `scene_answers.py:99-124`: public host adapter rejects missing exact Root
  timeline/assets/theme inputs; `scene_answers.py:127-204` requires the
  retained source and prepared Root context.
- `onscreen.py:211-277`: current private implementation still derives
  transition DIP windows; no public Scene call exists there.

Runtime tripwire: patched all three public Scene answer entry points
(`frames_at`, `host_frames_at`, `_prepared_host_frames_at`) to fail, then ran
the original `Checkout._on_screen()` caller. It passed and returned
`[(0, 120, COVERED), (120, 135, DIP), (135, 240, COVERED)]`, proving that
the caller did not reach public Scene.

## Tests

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/sdk/test_coverage_empty_cut.py::test_a_declared_fade_in_is_a_dip_not_a_gap \
  tests/core/timeline/test_onscreen_more.py::test_a_cross_fade_of_two_full_plates_is_covered_not_dip \
  tests/sdk/test_scene_caller_preservation.py::test_private_scene_only_missing_managed_source_binding_is_unavailable \
  tests/packs/rendering/test_scene_answers.py::test_invalid_runtime_context_never_becomes_empty_answer
```

Result: **4 passed in 0.62s**.

The runtime tripwire command also passed after correcting the expected frame
range; it reported: `old caller used private onscreen coverage; public Scene
adapter was not reached`.

No full, browser, localhost/socket, install, shared-dependency write, or
renderer run was performed. No files in the product worktree were changed.

## Recommended next step

Provide an existing source-bound carrier at the old caller (or assign the
caller-owned SDK change that retains the prepared Root/source context), then
route exactly one original `Checkout._on_screen()` positive through public
Scene and add a one-to-one unavailable control. Only after that proof should
the transition fallback be retired; preserve static roles,
`_timing_evaluators`, pixel crop/statistics, `saveNoNode`, and current pins.
