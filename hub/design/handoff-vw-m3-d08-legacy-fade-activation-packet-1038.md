# D08 legacy-fade / public14 App packet

Status: **UNAPPLIED — archive qualification is a prerequisite.** This packet is
based on App `hub/tl/integration` and contains no product, package pin, lockfile,
or vendored-artifact change.

## Decision

There is no remaining physical App duplicate to delete for the approved
Composition 0.0.14 clip-look rule.

The former private opacity workaround was already removed before this packet:

- The historical `preparePlayerClipOpacity` scene shim created a synthetic
  `app-native-opacity` component and mutated a `DrawPlan` to
  `Number.MAX_SAFE_INTEGER` (historical App `78d7224de`).
- Current `src/tools/video-editor/compositions/playerEvaluation.ts:27-31`
  adapts the host clock once and calls the public
  `evaluation.clipOpacity` export. No synthetic component, scene query, or
  duration mutation remains in the current tree.

The remaining `DrawPlan`/fade code is a compatibility adapter and must stay:

- `playerEvaluation.ts:68-143` uses a compiled public plan only for an
  explicitly canonical, all-native track. Its fallback keeps host timing for
  gaps, overlaps, oversized transitions, invalid/unsupported declarations,
  and mixed chains.
- `playerEvaluation.ts:38-44,95-106` admits the App incoming-only image
  boundary only for a silent native-image pair. Video and injected effects
  stay host-timed so their playing/audio subtree is not frozen.
- `VisualClip.tsx:564-594` resolves the live transition catalog, preserves
  contributed renderer parameters and static CSS renderers, and emits the
  existing missing-transition diagnostic instead of substituting a fade.
- `VisualClip.tsx:636-645,649-747` applies public `queryDrawFrame` only to
  an admitted plan and keeps the host Sequence path otherwise.
- `TimelineRenderer.tsx:1297-1312` gates the public plan on actual host
  capability/owner identity, live bindings, generated modules, and registered
  clip types. A native-looking clip name cannot override a custom owner.

Composition 0.0.14's approved source (`f57d9601c`, final source tree
`202692df`) changes public Scene answers for known clip-look geometry: crop,
`fade-up`, and `scale-in` report known bounds/opacity using the existing
renderer-aligned math; unsupported custom modifiers, unsupported entrances,
exit animation, and unknown component internals remain unknown. It does not
replace the App transition renderer, media/audio clock, owner gate, or missing
diagnostic path. Therefore activating 0.0.14 alone supplies no safe App source
deletion.

## Exact unapplied file packet

Current tree: App `5ff11809e8100a6670acdb55eb19588ea168a80c`, equal to
`hub/tl/integration`.

| file | packet action after archive qualification |
|---|---|
| `vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz` | Add the newly qualified immutable archive supplied by the release owner; do not invent or copy a hash. |
| `package.json` | Generated updater change from the future archive path to `file:vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz`. |
| `package-lock.json` | Generated together with `package.json` by the normal updater. |
| `src/tools/video-editor/compositions/playerEvaluation.ts` | **No deletion/change.** Public scalar opacity is already active; host transition compatibility remains required. |
| `src/tools/video-editor/compositions/VisualClip.tsx` | **No deletion/change.** DrawPlan, host transition renderers, custom-owner handling, and unknown diagnostics remain required. |
| `src/tools/video-editor/compositions/TimelineRenderer.tsx` | **No deletion/change.** Existing capability/owner gate remains required. |

The source patch is intentionally empty. Do not manufacture a deletion for
`DrawPlan`, `preparePlayerTrack`, `wrapWithClipEffects`, or the host transition
renderer: public14 does not provide an equivalent App render/audio contract.

## Future normal updater invocation

Run only after the immutable public14 archive has passed its independent packed-
byte review and is available at the release-owned path. `ARCHIVE` is an input,
not a guessed hash or a replacement for the archive:

```bash
ARCHIVE=/absolute/path/to/banodoco-timeline-composition-0.0.14.tgz
test -f "$ARCHIVE"
test "$(basename "$ARCHIVE")" = banodoco-timeline-composition-0.0.14.tgz
realpath "$ARCHIVE"
test "$(realpath vendor/artifacts)" = "$PWD/vendor/artifacts"
cp --no-clobber "$ARCHIVE" vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz
npm install --package-lock-only --ignore-scripts --no-audit --no-fund \
  ./vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz
```

The command is deliberately not run in this packet. Before HOME review, verify
the generated diff changes only the package dependency metadata and lock entry;
the archive hash, member manifest, and source/tree identity come from the
qualified release handoff.

## Qualification and closure map

The current public13 control archive is retained unchanged:

- `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- 77 regular members, 58,477 bytes
- SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

After the future updater, rerun the existing focused App lane (with the actual
0.0.14 archive in the package graph):

```bash
ASTRID_CHECKOUT=/home/user/work/agent \
  node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/compositions/playerEvaluation.test.ts \
  src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx
node_modules/.bin/eslint \
  src/tools/video-editor/compositions/playerEvaluation.ts \
  src/tools/video-editor/compositions/VisualClip.tsx \
  src/tools/video-editor/compositions/TimelineRenderer.tsx --max-warnings 0
git diff --check
```

Required one-to-one retained behavior nodes for HOME review:

| behavior | existing test node | disposition |
|---|---|---|
| Native authored/object/array fades use the public scalar evaluator on the host content clock | `playerEvaluation.test.ts::evaluates authored opacity and object/array fades on the native content clock` | Retained replacement for the removed synthetic opacity scene; no assertion removal. |
| Legacy image fade keeps incoming-only appearance and host clock | `VisualClip.evaluation.test.tsx::preserves the mounted image fade pair with outgoing opacity one and the legacy incoming clock` | Retained; public DIP is not a replacement for this legacy film behavior. |
| Video transition keeps the playing media/audio clock | `VisualClip.evaluation.test.tsx::retains the host path for video transitions without freezing or extracting its audio` | Retained; no DrawPlan deletion. |
| Contributed and static transition renderers preserve params/identity | `VisualClip.test.tsx::passes transition progress and params to contributed renderer`; `::handles object-style renderer (static CSSProperties)` | Retained host ABI. |
| Custom owner and unknown internals stay visible/diagnostic | `TimelineRenderer.sequence.test.tsx::retains host bounds and neighboring timing when an injected component overrides a compiled media name`; `playerEvaluation.test.ts::keeps undeclared custom and typed component internals unknown and present` | Retained owner/unknown guards. |
| Canonical public plans remain equivalent at the admitted seam | `VisualClip.evaluation.test.tsx::canonical 0.0.9 compiled preview and public draw`; `TimelineRenderer.sequence.test.tsx::passes the compiled incoming fade and occurrence cap through the actual renderer without host reclamping` | Rerun against qualified 0.0.14; rename wording only if HOME chooses, with assertions preserved. |

The Composition-side public14 source tests are the proof of the new clip-look
Scene rule. App activation does not convert these host tests into refusal tests,
remove old pixels, rerun MAIN6, rerun browser/MP4 work, or close physical Gate6.
MAIN6 intended-DIP, incoming-COVERED, and owner-film scanner evidence remain
retained as separate evidence.

## Limits

No public14 archive, hash, install, pin/lock update, source deletion, browser,
helper, Runtime, socket, full suite, current browser/MP4, or repeated MAIN6
capture is claimed by this packet. No assertions were removed, weakened, or
converted.
