# Shared D09 boundary — owner13:25

Agent owns separating EXPLICIT Scene checks from save-core validation in SDK publish/transaction/check callers. Saving MUST remain NoNode/renderer-independent; existing40guard tests and prototype24EMPTYpublicframes are in handoff-vw-m3-d09-sdk-source-join-REPORT.md.

Viewing worker vw-m3-root-prep-lifetime-extract owns run.py +newPRIVATEroot-preparation helper only. It extracts the EXISTING normal lifetime, preserving source/profile/registry/assets/server/temp/PCM/effect/finalprops/callback identity and cleanup. It will publish the exact private signature/yield type here after test-backed extraction; Agent must not invent a second Root preparer or a SourceFactory. No publicAPI/DTO/authorityfield is approved.

Explicit read-only queries reuse that exact prepared source lifetime without a fabricated successful capture or a renderer launch; normalrender caller behavior remains byte/semantically identical. Cache-row payload is a separately approved bounded change: successfulfresh callback only, exactkey/Rootsource/PNGhash, mismatchMISS; PNG-onlyfallback unchanged until ownqualification. D09 deletion stillwaitsbothseamsgreen ANDphysicalparity.

Current normal Root source/client pin is official013; originalsource/extent/PCMcaller alreadyownerintegrated. User CAPstored4000forrender, editor/read originals preserved; no renderConfig.


## Exact extracted seam — vw-m3-root-prep-lifetime-extract

Implemented in `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py`,
private `_prepared_remotion_root`; re-exported privately on `remotion.run` for the
existing backend seams. The 208 existing preparation/source/PCM/callback tests
passed before and after extraction. The expanded direct lane passed 225 tests;
11 direct context/fingerprint cases passed again after the type-only cast. Central
final-tree HTTP/phase/backend/lock lane passed 82 tests (1020133642-9871).

```python
_prepared_remotion_root(
    timeline_path: Path, assets_path: Path, staged_video: Path, *,
    provenance_out_path: Path, project_dir: Path, composition_id: str,
    theme_path: Path | None, min_free_gb: float | None,
    review: Mapping[str, Any] | None = None,
    materialized_root: Path | None = None,
    staging_parent: Path | None = None,
    materialized_objects: Mapping[str, str] | None = None,
    composition_clip_types: frozenset[str] = frozenset(),
    encode_aac_at_stitch: bool = False,
    frame_numbers: Sequence[int] | None = None,
    frame_output_dir: Path | None = None,
    on_scene_props: Callable[[Mapping[str, Any], Sequence[int]], None] | None = None,
    window: FrameWindow | None = None,
    composition_duration_frames: int | None = None,
)
```

It is a context manager, yielding the existing local values as a tuple (no new
DTO): `(merged_props, props_path, runtime_tools, theme_for_props, registry_state,
stage_summary, remotion_temp_root, remotion_port, render_hash, staged_public_root,
window_argument, alpha, frame_output_dir, pcm_aac_mp4, cli_video)`.
A query consumes `prepared[0]` as read-only final Root props **inside the with**;
`prepared[1]` is their already-written JSON path, `prepared[2]` the admitted runtime.
The remaining tuple values only continue the unchanged renderer launch.

The caller must own `remotion_lock.remotion_render_lock()` for the whole context;
the helper does not acquire or re-acquire it. It runs existing admission, registry,
source serialization, theme/profile, managed asset server, alpha, effect staging
and normal PCM preparation, in the existing order. For the existing frame-query
semantics pass the real requested `frame_numbers` and an invocation-private
`frame_output_dir`; these retain the current validation and skip video PCM work.
The output/stage/provenance paths are real invocation scratch paths, not a
successful capture. No frame/video, renderer process, capture label, or fresh
capture certification is produced by entering or leaving the context. The
existing capture callback runs at its original point before yield when supplied.

All assets, server URLs, effect staging, props JSON, temporary roots, and PCM WAVs
stay live until query/renderer completion or exception. Existing finally cleanup
removes props and effect assets first, then ExitStack closes PCM attempts, asset
server, materializer and runtime temp directory in their original reverse order.
Do not retain props for later URL consumption outside this lifetime.

Scope: no SDK publish/transaction edits, no pin change, no second preparer. This
worker's actual base pins Composition 0.0.12; the note above's “official013” is a
coordination target, not a claim that this worktree already adopted it. The one
cache-identity entry for the new helper is necessary so moving preparation does
not remove it from the existing frame source fingerprint.
