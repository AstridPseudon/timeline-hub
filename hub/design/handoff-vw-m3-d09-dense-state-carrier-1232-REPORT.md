# vw-m3-d09-dense-state-carrier-1232

## Source-backed join

The existing source-backed producer path is:

1. `build_filmstrip_pack` selects the motion window and calls the retained `RemotionFrameProvider`.
2. `RemotionFrameProvider.capture` invokes the existing renderer callback with its frame list.
3. `RemotionFrameProvider._observe_scene(props, frames)` validates the frozen source and prepares `CaptureSceneLabels`.
4. `CaptureSceneLabels.observe` calls existing `host_frames_at(props, basis, frames)` exactly once.
5. `CaptureSceneLabels.retain` retains those exact rows after the successful capture.
6. `motion.sheet.build_context` reads those rows through the existing `scene_for_frame` / `_frame_facts` carrier into `ctx.shared["public_scene"]`.

The producer now joins the existing motion window's padded sample frame list
to the card frame list before step 2. The requested list is deduplicated and
sorted once; card frames are refreshed whenever semantic frames are requested
so the existing one-mode fresh/cache rule cannot silently combine evidence.
Semantic rows are carried in memory only and are not minted as new cache
entries.

## Scope and overlap

Applied files are only:

- `astrid/packs/rendering/actions/timeline_visualize/motion/sheet.py`
- `astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py`
- `astrid/packs/rendering/actions/timeline_visualize/composed_frame.py`
- `tests/packs/rendering/test_scene_source_carry.py`

The parallel `fast_lane.py`, `_filmstrip_cache.py`, `labels.py`, and
`builtin.py` lanes were not modified. The real unapplied patch is
`handoff-vw-m3-d09-dense-state-carrier-1232.patch`; it contains only the
existing curve-consumer default-motion admission and direct aggregate tests.
Apply it after the parallel `builtin.py` decision, in this order:

`producer join -> builtin consumer patch -> focused aggregate tests`.

## Evidence

The applied targeted tests passed as listed in the worker report. The source
transport regression proves exact frame/source retention and wrong-source
refusal. No full/browser/helper/native/socket/install suite was run. Full Ruff
also exposes an unchanged pre-existing E731 at
`filmstrip_cards.py:490`; lint passes with only that known finding ignored.

