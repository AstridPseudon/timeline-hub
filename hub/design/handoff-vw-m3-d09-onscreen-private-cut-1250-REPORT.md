# D09 onscreen private transition branch cut

## Result

Removed one duplicated live evaluator branch from `astrid/core/timeline/onscreen.py`:

- deleted the private same-track transition-window scan (`starts_by_track`);
- deleted its recognized-ID/default-duration fallback (`FADE_TRANSITION_IDS`,
  `DEFAULT_TRANSITION_FRAMES`, and the `clip.transition` DIP append).

The installed public Composition Scene query already owns transition resolution
and is exercised by the direct public transition cases. Independent clip fade
ramps, entrance/exit timing, static roles, and pixel geometry remain in the
private adapter as required. No blanket unavailable result was added.

The direct Scene transport test now uses the frozen Composition 0.0.13 archive:

`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

## Function disposition map

| `onscreen.py` surface | Disposition |
| --- | --- |
| `element_coverage`, `role_of`, and compatibility patchpoints | Intentional static-role adapter; retained. |
| `_frames`, `_animation_frames`, `clip_start_frame`, `clip_end_frame` use | Timing seam; retained. |
| `layout_bounds`, `_covers_canvas`, `_is_cropped`, `_intersects_canvas` | Pixel/geometry lane; deferred and retained. |
| `_build` transition-window branch | Duplicated visibility/coverage math; removed in this cut. |
| `_build` fade/entrance/exit ramps, `_opacity`, `_visible`, `visible_at` | Remaining private fallback/label behavior; retained. |
| `_classify`, `_change_points`, `coverage` | SDK fallback and RLE behavior; retained pending source-bound public replacement. |
| `scene_answers.frames_at` / `host_frames_at` | Existing public Scene transport/thin host adapter; unchanged. |

The existing assertion map remains authoritative for the 14 legacy on-screen
tests: all remain present and passing. Its six missing/partial geometry,
`none`, audio, and exact-RLE rows were not relabelled or replaced here. The
public13 current-source packet and assertion map were independently reviewed
as source evidence; this cut does not claim whole-module retirement, public14
adoption, pixel parity, or audio parity.

## Tests

All commands used the worker tree plus the read-only Runtime source at
`/home/user/work/runtime`; no shared dependency was changed.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
-p no:cacheprovider tests/packs/rendering/test_scene_answers.py \
tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py \
tests/sdk/test_coverage_empty_cut.py tests/sdk/test_scene_public_summary_rle.py \
tests/sdk/test_scene_summary_projection.py
56 passed in 3.48s
```

The public Scene tests ran against Node `v20.19.4` and the frozen 0.0.13
archive above. The legacy on-screen and SDK coverage neighbors passed without
renderer access beyond the public Scene test file.

```text
/home/user/work/venv-agent/bin/ruff check --no-cache \
astrid/core/timeline/onscreen.py tests/packs/rendering/test_scene_answers.py
All checks passed!
git diff --check
passed
```

No full, browser, localhost/socket, physical render, package install, or
public14 qualification was run. An initial pytest collection without the
read-only Runtime `PYTHONPATH` failed before collection with missing
`runtime_protocol`; the corrected command above is the qualifying result.

## Commit handoff

The harness should commit the worktree using the worker `commit-msg` file.
