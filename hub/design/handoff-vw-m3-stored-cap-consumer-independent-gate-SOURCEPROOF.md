# Source proof

## Public Composition path

- `typescript/src/evaluation.ts`: public exports include `prepareScene`,
  `querySceneFrame`, and `clipOpacity`.
- `typescript/src/scene-evaluation.ts`: `prepareScene` converts the admitted
  occurrence duration to an end cap at the public preparation boundary.
- `typescript/src/lib/transition-spans.ts`: the prepared plan keeps the
  half-open draw interval and excludes its endpoint.

The command file records the direct 12-leaf run against these source modules.

## App still path at b1ef

- `src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx`
  (`TimelineFramePreview`): `inputProps` is `{ config: output, ... }`; its
  `Thumbnail` receives no `compiledTransitions` prop.
- `src/tools/video-editor/compositions/TimelineRenderer.tsx`
  (`TimelineRendererBody`): `compiledTransitions` is optional. With it absent,
  the render config uses `boundCanonicalConfigClips` and the native adapter;
  only the supplied vector activates the public compiled path.
- `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx`:
  the Player input already forwards `delivery.compiledTransitions`.

These are read-only source observations; no App source was copied or changed.
