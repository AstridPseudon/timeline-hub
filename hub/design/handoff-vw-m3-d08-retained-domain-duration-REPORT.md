# vw-m3-d08-per-clip-duration-authority

## Result

No App source patch is safe. The remaining per-clip helpers are legitimate
App/domain and host adapters, not deletable duplicates through the current
Composition 0.0.13 public API.

## Source comparison

- App `config-utils.ts:35-41` delegates `getClipSourceDuration` and
  `getClipTimelineDuration` to `timeline-domain.ts:807-840`. That domain policy
  admits only finite non-negative hold values, requires finite `to > from` for
  non-hold trims, and normalizes non-positive/non-finite speed to `1`.
- App `config-utils.ts:79-83` applies the final `Math.max(1, round(seconds *
  fps))` frame policy through `lib/time-grid.ts`. It is used by the many App
  Sequence/placeholder/audio/visual callers in `TimelineRenderer.tsx` and
  neighboring composition components (for example lines 219, 343, 376, 418,
  459, 953, 1045, and 1184).
- Composition's internal `typescript/src/lib/duration.ts:3-18,30-32` has the
  same arithmetic only for already-canonical values: raw `hold` when its type
  is number, otherwise raw `(to ?? 0) - (from ?? 0)`, and `speed ?? 1`; then
  `Math.max(1, round(...))`. It does not implement App's invalid-input/domain
  admission semantics.
- `playerEvaluation.ts:20-25` is an adapter. It sanitizes the public
  Composition playback rate and rewrites the App clip into the Composition
  evaluator's expected raw `hold` + `speed` representation while preserving
  the App-authored clip. Removing its App duration input would change the
  evaluator input for malformed/legacy clips.
- Composition package root exports only `getTimelineDurationInFrames` from
  `typescript/src/index.ts:41-42`; `package.json:9-20` exposes root and
  `./evaluation`, but neither exposes a per-clip duration helper. The root
  query also includes `round(clip.at * fps)`, so it is not a per-clip
  replacement unless the caller normalizes `at` (explicitly out of scope).

## Pure vector probe

`duration-equivalence-probe.mjs` transcribes the two source implementations,
calls only the existing public root duration query, and does not deep-import or
activate private Composition modules. Results:

| vector | App seconds/frames | Composition private seconds/frames | public root query |
|---|---:|---:|---:|
| valid hold (`hold=.5,speed=1`, 30 fps) | `.5 / 15` | `.5 / 15` | `15` at `at=0` |
| valid trim slow (`2..3,speed=.5`) | `2 / 60` | `2 / 60` | `60` at `at=0` |
| sub-frame hold (`hold=.017,speed=2`) | `.0085 / 1` | `.0085 / 1` | `1` at `at=0` |
| non-zero start (`at=.125,hold=.5`) | `.5 / 15` | `.5 / 15` | `19` (adds start frame) |
| malformed trim (`from=1,to=NaN`) | `0 / 1` | `NaN / NaN` | `NaN` |
| reversed trim (`from=4,to=3`) | `0 / 1` | `-1 / 1` | `1` at `at=0` |
| hold clip with missing hold (`clipType=hold,from=1,to=2`) | `0 / 1` | `1 / 30` | `30` at `at=0` |
| zero speed (`hold=2,speed=0`) | `2 / 60` | `Infinity / Infinity` | `Infinity` |
| NaN speed (`hold=2,speed=NaN`) | `2 / 60` | `NaN / NaN` | `NaN` |
| negative speed (`hold=2,speed=-1`) | `2 / 60` | `-2 / 1` | `1` at `at=0` |

The first three vectors establish equivalence for valid canonical input and
frame rounding. The remaining vectors establish that the formulas are not
semantically interchangeable at the App boundary.

## Smallest deletion prerequisite

There is no deletion to export under the stated constraints. A future deletion
would first require Composition public13 (or a later explicitly approved
package) to publish a per-clip duration API whose contract exactly matches the
App canonical domain policy, including malformed trim/hold-kind and invalid
speed behavior, plus frame clamping. A root whole-timeline query or private
deep import is insufficient. No package version, public export, renderConfig,
or product change was made.

## Verification

- `node duration-equivalence-probe.mjs` — passed; produced the vectors above.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/lib/config-utils.test.ts src/tools/video-editor/compositions/playerEvaluation.test.ts --pool=forks --maxWorkers=1 --no-file-parallelism --reporter=dot` — passed, 2 files / 64 tests.
- An initial `./node_modules/.bin/vitest run --no-cache --configLoader=runner
  --config config/testing/vitest.config.ts
  src/tools/video-editor/lib/config-utils.test.ts
  src/tools/video-editor/compositions/playerEvaluation.test.ts --pool=forks
  --maxWorkers=1 --no-file-parallelism --reporter=dot` attempt was not usable
  because the existing config references CommonJS `__dirname`; the successful
  rerun used the normal config loader with `--no-cache` and did not write shared
  caches.
- `git diff --check` — passed. App worktree remains clean; no source files
  changed.

Not run: browser, full suite, install, render, live sockets, or physical
audio/video parity.
