# App → Viewing: duration type-contract handoff

Date: 2026-10-21

Status: unapplied Composition-owned type correction. This worker made no App
source, package, build, version, or pin change.

## Decision

The seven retained current13 diagnostics are one public-boundary mismatch, not
seven App value problems. App passes a `ResolvedTimelineConfig` to the public
Composition duration evaluator. App's resolved config has an optional theme
and resolved-only fields; public Composition 0.0.13 declares a whole
`TimelineConfig` with required `theme: string`.

The smallest accurate correction is in Composition's duration declaration:

```ts
export const getTimelineDurationInFrames = (
  timeline: Pick<TimelineConfig, 'clips'>,
  fps: number,
): number => {
  // existing implementation unchanged
};
```

The source implementation and arithmetic remain unchanged. The normal
Composition type-artifact generation should expose that narrower declaration;
this handoff does not promise a release, version, or pin. The existing App
imports and calls can remain unchanged. No App cast, synthetic theme/default,
deep import, or seven-site wrapper is warranted.

## Why this input type is exact

Current App declarations (`src/tools/video-editor/types/index.ts`):

```ts
type TimelineConfig = {
  output: TimelineOutput;
  clips: TimelineClip[];
  // ...
  theme?: string;
  // ...
};

type ResolvedTimelineConfig = {
  output: TimelineOutput;
  tracks: TrackDefinition[];
  clips: ResolvedTimelineClip[];
  registry: Record<string, ResolvedAssetRegistryEntry>;
  theme?: string;
  // ...
};

type ResolvedTimelineClip = TimelineClip & {
  assetEntry?: ResolvedAssetRegistryEntry;
};
```

The App helper in `src/tools/video-editor/lib/config-utils.ts` does not wrap or
alter the public evaluator; it imports and re-exports
`getTimelineDurationInFrames`. Thus the current effective call signature is
the public package signature, with `ResolvedTimelineConfig` at each callsite.

The retained public13 declaration in
`vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` is:

```ts
export type TimelineConfig = {
  theme: string;
  tracks?: TrackDefinition[];
  clips: TimelineClip[];
  output?: unknown;
  pinnedShotGroups?: unknown;
  theme_overrides?: unknown;
};

export declare const getTimelineDurationInFrames: (
  timeline: TimelineConfig,
  fps: number,
) => number;
```

`ResolvedTimelineConfig` is structurally suitable for the proposed
`Pick<TimelineConfig, 'clips'>`: its `ResolvedTimelineClip[]` is an array of
the App `TimelineClip` plus an optional resolved asset entry. The required
public `theme` is the only incompatible top-level member reported by the
qualified compiler capture; the extra resolved fields are irrelevant once
the function asks only for `clips`.

## Fields the duration body actually reads

The public13 body in `dist/chunk-SE4TPVLW.js` is equivalent to:

```ts
const getTimelineDurationInFrames = (timeline, fps) => Math.max(
  1,
  ...timeline.clips.map((clip) =>
    secondsToFrames(clip.at, fps) + getClipDurationInFrames(clip, fps),
  ),
);
```

Its called helpers read only these values:

- `timeline.clips`;
- for each clip, `at`, `hold`, `to`, `from`, and `speed`;
- the `fps` argument.

`getClipSourceDuration` uses numeric `hold` when present, otherwise
`(to ?? 0) - (from ?? 0)`. `getClipTimelineDuration` divides by
`speed ?? 1`; `getClipDurationInFrames` rounds with `Math.round` and clamps
each clip to at least one frame. The outer function also clamps the timeline
result to at least one frame. It does not read `theme`, `output`, `tracks`,
`registry`, `assetEntry`, or any other resolved field. No authored value is
manufactured by the proposed type correction.

## All seven exact diagnostic sites

The retained qualified r8 compiler output reports the same `TS2345` at every
site: `ResolvedTimelineConfig` is not assignable to public `TimelineConfig`
because `theme` is `string | undefined` locally but `string` publicly.

| Exact diagnostic site | Current argument expression | FPS argument/value carried |
| --- | --- | --- |
| `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:232:40` | `activeConfig` (mounted shot-local resolved config) | `activeConfig.output.fps` |
| `src/tools/video-editor/components/CompactPreview.tsx:46:40` | `projectOutputTimelineConfig(previewConfig).config` (projected output config) | `previewConfig.output.fps` |
| `src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx:47:40` | `output` (projection of `previewComposition.config`) | `output.output.fps` |
| `src/tools/video-editor/components/TimelineEditorShellCore.tsx:578:40` | `outputConfig` (projection of `editorData.resolvedConfig`) | `outputConfig.output.fps` |
| `src/tools/video-editor/compositions/TimelineRenderer.tsx:1625:75` | `renderConfig` (selected render projection) | local `fps`, from `renderConfig.output.fps` |
| `src/tools/video-editor/hooks/useDerivedTimeline.ts:71:9` | `projectOutputTimelineConfig(resolvedConfig).config` | local `fps`, from `resolvedConfig.output.fps` |
| `src/tools/video-editor/hooks/useRenderState.ts:596:53` | `projectOutputTimelineConfig(renderConfig).config` | local `fps`, from `renderConfig.output.fps` |

The exact repeated diagnostic text is:

```text
error TS2345: Argument of type 'ResolvedTimelineConfig' is not assignable to parameter of type 'TimelineConfig'.
  Types of property 'theme' are incompatible.
    Type 'string | undefined' is not assignable to type 'string'.
      Type 'undefined' is not assignable to type 'string'.
```

No `clips`, `at`, `hold`, `from`, `to`, `speed`, output projection, or FPS
value changes are proposed.

## Runtime and domain behavior that must remain unchanged

This boundary correction must not replace the retained per-clip App domain
adapters. In `src/tools/video-editor/lib/config-utils.ts`:

- `getClipSourceDuration` delegates to
  `getConfigTimelineClipSourceDuration` in `timeline-domain.ts`;
- `getClipTimelineDuration` delegates to
  `getConfigTimelineClipDuration`, preserving App's hold-kind, finite-trim,
  and invalid-speed rules;
- `getClipDurationInFrames` keeps the App `Math.max(1, ...)` frame clamp and
  shared frame rounding.

The public whole-timeline duration query is not a substitute for those
per-clip adapters. In particular, malformed hold/trim/speed inputs and
non-zero starts must not be normalized, clamped differently, or made valid by
adding a theme. The proposal changes only the static input requirement for a
function whose body already reads the clip timing data above; runtime output,
rounding, defaults, and threshold behavior stay the same.

## Retained evidence and test classification

The original correct13 r8 capture is retained at these concrete paths:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/report.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/notes/compiler-context.txt`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/notes/tsc.stdout`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-type-selflink-private-overlay-one-check-r8/notes/diagnostic-file-code-counts.txt`

That capture records source commit `1a54d30521945c7ea1ab7148e840011c8893c78d`,
source tree `941ff4c78ea72a48f6e83f310e54a4258f45e24b`, one qualified
`tsc -p tsconfig.app.json --noEmit` invocation, package 0.0.13 origins,
`TS2688=0`, Composition `TS2305=0`, and 63 current App diagnostics. The
duration boundary is exactly seven of those 63 diagnostics; the other 56 are
outside this handoff.

The retained r12 focused pass was:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/lib/config-utils.test.ts src/tools/video-editor/components/TimelineEditor/TimelineDurationGuide.test.tsx --pool=forks --maxWorkers=1 --no-file-parallelism --testNamePattern='matches shared visible-time vector|renderer-owned independent start/duration rounding|re-exports the public timeline duration evaluator' --reporter=dot
```

It passed 8 duration/config assertions. No test or compiler was rerun for this
handoff.

The retained neighboring config run recorded 25 passed and 22 failed. Those
22 failures all raised `TypeError: getSanitizedMediaTrimProps is not a
function` in `config-utils.test.ts`; none was a duration assertion. They are
classified here as an effective shared8 export environment, not as proven
product failures: the retained r12 log records `realpath node_modules` and
the package path under the shared `/home/user/work/app/node_modules` graph,
while the inspected shared package is 0.0.10 and its `dist/evaluation.js`
does not export `computeMediaTrim`. In contrast, the committed public13
artifact above exports `computeMediaTrim` from `dist/evaluation.js`, and the
qualified r8 compiler context resolves the package from the protected
0.0.13 graph and records the runtime symbol as present. The 22 failures
therefore establish an export-graph/environment mismatch; they do not prove a
product defect or a public13 failure.

The retained r12 lint and `git diff --check` passed. This worker did not run
tests, TypeScript, builds, browsers/live sockets, installs, or graph changes.

## Next action for Viewing

Apply the one Composition-owned input-type correction above, regenerate the
ordinary declaration artifact through the existing Composition workflow, and
then re-run the seven-site typecheck and focused duration tests under a
qualified public13 graph. Keep the App callsites, per-clip adapters, test
assertions, runtime arithmetic, package version/pin state, and all unrelated
diagnostics unchanged.
