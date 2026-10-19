# @banodoco/timeline-composition

Version 0.0.8 ships built ESM and declarations for the timeline evaluator,
Remotion composition, theme API and default registries. Plain Node can import
`@banodoco/timeline-composition/evaluation` without React, Remotion or a TypeScript
loader. The renderer uses host peers React/React DOM 18.3.1 and
Remotion/media/layout-utils 4.0.509; those runtimes are never bundled.

The package owns text-card (including the `text` alias), six animations, two
transitions and four 2rp effects relocated from App. The bundled 2rp source is
**0.1.0**; equivalence to the separately referenced 0.1.1 theme is unverified.
Fonts, media and project pack admission remain host responsibilities.

## Scoped host elements

`TimelineComposition` accepts an optional `registries` prop. The same input is
the final argument of `prepareCompositionScene`. Effects and aliases, animations
and their defaults/meta, and transitions and their defaults/meta use the public
`CompositionRegistries` contract from the root or `./registries` export.
Every supplied member is the host's **complete resolved map** for that category;
omitted members use bundled defaults. `resolveElementRegistries(theme, input)`
returns these maps, admitting core effects plus effects for the selected runtime
theme. Hosts resolve pack/theme precedence before passing the maps.

```tsx
import {
  TimelineComposition, resolveElementRegistries,
  type EffectProps, type RuntimeTheme,
} from '@banodoco/timeline-composition';

const Title = ({params}: EffectProps<{title: string}>) => <h1>{params.title}</h1>;
const registriesFor = (theme: RuntimeTheme) => ({
  effects: {...resolveElementRegistries(theme).effects, 'project-title': Title},
});
// <TimelineComposition {...input} registries={registriesFor(runtimeTheme)} />
```

Pass the same maps to scene preparation and rendering. A component's existing
`prepareSceneCapability` hook is used for both packaged and host effects;
undeclared internals, alpha and geometry remain unknown. Registry inputs never
assign module globals or modify installed files. Packaged effects' internal
animations and clip entrance/exit animations read the instance's scope. Hosts
mounting packaged components themselves can wrap them in `ElementRegistryProvider`
(and the shared `ThemeProvider`) from `./theme-api`. Pure animation helpers take
an optional registry input (`composeAnimations` takes it in its input object;
`normalizeAnimationReferences` and `resolveAnimationReferences` take it last).
Unknown animation/transition IDs and invalid animation phases still throw.

Animation metadata declares `supportsEasing: true` when the registered component
consumes explicit easing. The composer passes canonical `easing` and clamped,
eased `progress` over `elapsedFrames / durationFrames`, under any registered ID.
Components can use `easing` with their own timing window; bundled type-on owns
its `startFrame` / `durationFraction` reveal window. With no authored easing,
both props are undefined and bundled components retain their normal motion.
Omitted or false support refuses explicit easing. Supply the matching metadata
and defaults when overriding a registration; names confer no private behavior.
This declaration does not establish scene geometry, alpha or visibility.

```tsx
import type {AnimationRegistries, WrapperAnimationProps} from '@banodoco/timeline-composition/theme-api';

const Sweep = ({children, progress}: WrapperAnimationProps) => (
  <div style={{opacity: progress ?? 1}}>{children}</div>
);
const animations = {
  animations: {'project-sweep': Sweep},
  animationMeta: {'project-sweep': {kind: 'wrapper', phase: 'entrance', supportsEasing: true}},
  animationDefaults: {'project-sweep': {durationFrames: 20}},
} satisfies AnimationRegistries;
// composeAnimations({...input, refs: {id: 'project-sweep', easing: 'ease-in'}, registries: animations})
```

## Transitions

A clip's `transition` (on the clip that starts the boundary, i.e. the outgoing clip) joins it to the next clip on the same track. The next clip must start within one frame of the outgoing clip's end (or exactly at it); otherwise the transition is ignored and the boundary is a cut. A transition longer than either clip is also ignored.

- **Placement** is set by `align` on the transition object. `'end'` (the default, upstream's placement) puts the overlap window in the `T` frames before the boundary, so the incoming clip starts inside it. `'start'` puts it in the `T` frames after the boundary, and `'center'` centres it on the boundary.
- **Dissolve** (any id other than `fade`, e.g. `cross-fade`): the incoming clip ramps 0 to 1 over the window while the outgoing clip stays fully opaque underneath, so there is no hole in the frame.
- **Dip** (`fade`): the outgoing clip ramps 1 to 0 over the first half of the window, then the incoming clip ramps 0 to 1 over the second half. The background shows through at the midpoint, on purpose.
- **Extension frames**: a clip that is pulled into a window beyond its own span is drawn over the extra frames but shows itself frozen at its boundary frame, so its own timing never shifts. The outgoing clip is extended past its end; the incoming clip is extended back before its start.
- **Chains** (A to B to C): each boundary is planned independently. B is extended back for the A to B window and, if its own boundary to C runs past B's end, forward too. Each clip is drawn in track order, so later clips sit on top.

The planning is pure and lives in `typescript/src/lib/transition-spans.ts`.

## Pure planner API

Import `@banodoco/timeline-composition/evaluation` to prepare one visual track
and query individual frames without loading React, Remotion, theme components
or generated registries:

```ts
import {prepareTrack, queryTrackFrame} from '@banodoco/timeline-composition/evaluation';

const track = prepareTrack(
  [{start: 0, duration: 30}, {start: 30, duration: 30}],
  [{T: 10, kind: 'dissolve', align: 'end'}],
);
const at25 = queryTrackFrame(track, 25);
// {frame: 25, layers: [
//   {clipIndex: 0, drawLocalFrame: 25, ownFrame: 25, opacity: 1},
//   {clipIndex: 1, drawLocalFrame: 5, ownFrame: 0, opacity: 0.5},
// ]}
```

`prepareTrack(spans, transitions)` delegates to the existing `planTrack`. Inputs
are frame spans in track/painter order, with already resolved transition specs;
`transitions[i]` joins clip `i` to clip `i + 1`, and a missing/null entry is a cut.
The caller owns clip sorting, seconds-to-frames conversion, duration calculation
and theme transition resolution, as `TimelineComposition` does today. Prepare
again when these inputs change. The returned `plans` snapshot can be reused;
treat it and its nested plans as read-only.

`queryTrackFrame(track, frame)` accepts one finite track-absolute frame (including
fractional frames) and returns mounted layers in input order. Each layer retains
its input `clipIndex`. Mount intervals are `[drawStart, drawStart + drawDuration)`;
gaps and empty tracks return no layers. Mounted zero-opacity layers remain in
the answer. The result contains only the requested frame, with no film-length
enumeration or serialization. Preparation and each query scale with clip count,
not film duration; no cache is installed by this API.

`queryDrawFrame(plan, drawLocalFrame)` returns the same `drawLocalFrame`, clamped
`ownFrame`, and transition `opacity` for a single plan. It does not filter by
mount interval: its caller supplies a frame inside the clip's draw Sequence.
`TransitionLayer` uses this query for its Freeze frame and opacity;
`TimelineComposition` uses `prepareTrack` for its Sequences. Both paths delegate
to the original `ownFrame` / `layerOpacity` implementation. The subpath also
exports the planner input/output types, including `ClipSpan`, `TransitionSpec`
and `DrawPlan`.

This API describes transition mounting and timing. Its opacity excludes
track opacity, clip fades, component opacity, transforms, bounds, pixel coverage
and occlusion. It does not establish rendered visibility. Component internals
and coverage remain unknown here. Renderer-owner/Python caching and consumers,
coverage findings, and App Player integration are separate work.

## Transition authoring admission

The evaluation subpath also exports `declareAppTransition` and
`prepareDeclaredTrack`. These are explicit authoring admission calls; existing
renderer callers continue to use `prepareTrack` with legacy semantics.

```ts
import {declareAppTransition, prepareDeclaredTrack} from '@banodoco/timeline-composition/evaluation';

const host = 'timeline-composition';
const declaration = declareAppTransition(
  'visual', 'a', {type: 'crossfade', duration: 0.3, params: {easing: 'linear'}}, 30, host,
);
const admitted = prepareDeclaredTrack('visual', [
  {id: 'a', start: 0, duration: 30},
  {id: 'b', start: 30, duration: 30},
], [declaration], host);
```

A declaration names one outgoing clip on one track, the supported host and
implementation, resolved frame spec, and preserved App params. App duration is
in seconds and rounds once to frames. `crossfade` maps to `cross-fade`
(dissolve); `fade` maps to dip. Other implementations or hosts throw
`TransitionAdmissionError` with a `code` and actionable `nextStep`.

Admission requires ordered, non-overlapping own clip spans; gaps are valid.
Duplicate owners, cross-track owners and owners without a successor are refused.
Admission never sorts, moves, trims or repairs clips. After validation it calls
the existing planner, including its cut behavior for gaps and transition lengths
that do not fit. Planner draw extensions may overlap by design. Params are
preserved as declaration data; this pure API does not execute custom components.
This API does not wire the App editor or change legacy rendering automatically.

## Speed

`clip.speed` is a playback rate, and the clip's length is its hold divided by `speed` (speed 2 halves the length).

- **Media clips** (`VisualClip`, `AudioTrack`) apply `speed` as `playbackRate` on the media itself, so the footage plays faster or slower.
- **Element clips** do not use `playbackRate`. The element sees `useCurrentFrame() = floor(local × speed)`, so speed 2 plays its animation twice as fast in half the length, and speed 0.5 plays it at half speed over twice the length. The entrance and exit windows stay in timeline frames, as before.
- A footage element (`am-footage`) reads the current frame for its video, so it plays at the clip's speed with no element change. An element must not set `playbackRate` itself, or the speed would apply twice.
- Invalid speeds (not a finite number above 0) act as 1.

The element remap is a `<Freeze>` around the element content, applied in `ClipLook.tsx`. The sanitising and frame math is pure and lives in `typescript/src/lib/clip-look.ts` (`clipSpeed`, `remappedFrame`).

## Build, package and verify

Node.js 20 or newer is required (validated with Node.js 22.22.0). Install from
the lockfile, then build and pack:

```sh
npm ci
npm run gen-registry:check
npm run build
npm pack
npm run test:package -- "$PWD/banodoco-timeline-composition-0.0.8.tgz"
```

Use a writable `npm_config_cache` if the environment's default npm cache is
read-only. `npm run build` cleans `dist`, checks all four generated registries,
strictly checks the complete source/declarations with TypeScript 5.9.3, and
builds shared ESM chunks with esbuild 0.27.7. Compiler and generator errors fail
the build. `npm run build:ts` checks/emits declarations separately. `npm pack`
runs the build again; the tarball contains only built runtime/declarations,
package metadata and this README. Consumers install the tarball bytes and
normal peers; they need no source aliases, source checkout or code generation.

`npm run test:package -- /absolute/path/to/artifact.tgz` installs that actual
artifact and exact peers in a fresh temporary consumer. It checks plain Node
imports of every public entry, the evaluator's peer-free import graph, bundled
resource-card rendering, scoped host registration/capabilities, shared
ThemeProvider and React/Remotion identity, NodeNext declaration consumption,
installed-file immutability and dependency deduplication. It removes its temporary
consumer on exit. The declaration probe uses `skipLibCheck` for upstream Remotion
4 declarations (which reference the legacy global `Timer`); the package source
itself receives the strict build check using the existing Timer compatibility
interface. This smoke does not prove browser pixels, Player audio or film parity.

Registry generation uses only `scripts/builtin-inputs.json` and the listed local
components/defaults/meta under `typescript/src/builtins`. `npm run gen-registry`
updates checked-in generated source; `gen-registry:check` refuses drift in any of
the four files. Installed themes and neighboring workspaces cannot affect this
output. Optional host discovery/generation stays in the host and supplies maps
through the same scoped input.

The public ESM/declaration exports are `.`, `./evaluation`, `./theme-api`,
`./registries`, `./registry.generated`, `./effects.generated`,
`./animations.generated`, `./transitions.generated` and `./package.json`.
There are no source/deep-path or CommonJS exports and no npm schema or separately
installed theme dependency.

Focused checks for the packaging/registry change:

```sh
npm run build:test
node --import ./typescript/tests/register-extensionless.mjs --test \
  typescript/test-dist/tests/registries.test.js \
  typescript/test-dist/tests/animations.test.js \
  typescript/test-dist/tests/scene-evaluation.test.js scripts/gen-registry.test.mjs
```

`npm test` runs the repository suite; orchestration workers request full suites
through the central test service. Do not regenerate or edit an installed package.
Consumer migrations, existing-film comparison and real Player/export frame/audio
parity remain separate integration gates.

## Keyframe origin

`clip.keyframeOrigin` is key-time zero in **seconds relative to the clip's
start on the timeline**. Zero means clip start. It is independent of media
`from`/`to` and playback `speed`; trimming changes source sampling, never this
origin or authored keys. Keys retain their payload units (App seconds, sprite
frames). For a declared origin `o`, App key time at timeline second `t` is
`t - (clip.at + o)`; sprite key frame at own local frame `f` is `f - o * fps`.
The sprite then applies its existing step quantization and held-pose selection.
Transition extensions still use the evaluator's existing clamped own frame.

The pure `./evaluation` and component `./theme-api` subpaths expose
`timelineKeyframeTime`, `spriteKeyframeFrame` and `declareKeyframeOrigin`.
`declareKeyframeOrigin(clip, 'app-seconds')` stamps legacy origin `-clip.at`;
`'sprite-frames'` stamps zero. Both preserve keys without conversion, rounding or
mutation, and preserve an already declared origin. Missing origins keep each
legacy consumer's existing domain. New clip-local seconds keys use origin zero.
A later timeline move carries a declared origin with its clip. An undeclared App
clip retains the old absolute-timeline behavior. This contract is available to
component consumers; it introduces no easing, loops or modifiers.
