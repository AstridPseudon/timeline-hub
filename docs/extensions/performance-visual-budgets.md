# Extension performance and visual budgets

These are release gates, not aspirational targets. The fixed browser fixture catalog
(`src/test/editorExtensionFixtureCatalog.ts`: scene phase markers, the transcript lane, the Runaway
timeline lane and a test-only overlay-layers extension) is what the browser gates run against; it is a
test inventory, not the shipped catalog (production loads only the live-scenes and transcript
extensions).

The former single browser performance gate (`extension-performance-budget.spec.ts`, startup,
activation, command-search, heap and aborted-bridge budgets) is retired. It measured that fixture
inventory with wall-clock budgets (30 s ready, 3 s manager) too loose to catch a regression, and its
aborted-bridge case exercised a DEV-only Runaway bridge loader that no longer exists. Each signal it
checked now has one owner:

| Signal | Owner |
| --- | --- |
| Mounted data-lane items stay at most 128 on every animation frame of real wheel input | `tests/e2e/timeline/data-lane-viewport.spec.ts` (566 seeded persisted Runaway items; sparse-window contract) |
| Mounted controls and DOM nodes stay bounded at 500, 5,000 and 50,000 source intervals | `npm run test:extension-scale` (`largeLaneScale.test.tsx`) |
| Extension command listed by label in the command palette | `tests/e2e/timeline/extension-overlays.spec.ts` (B key / palette case) |
| Horizontal document overflow caused by extension chrome (status-bar slot, marker pager) | `tests/e2e/timeline/shell-responsive-overflow.spec.ts` at desktop, tablet-portrait and phone |

Neither Runaway source rows nor transcript rows travel over a host bridge any more: they are persisted
bundle source items (`sourceItemsBySchemaRef`), so there is no request-coalescing budget to hold.

The deterministic large-lane scale gate runs with:

```sh
npm run test:extension-scale
```

It exercises 500, 5,000, and 50,000 source intervals through the Runaway parser and the typed
`DataLaneRow`. Each size must retain the source count, mount at most 128 selectable transition
controls, stay below 5,000 live DOM nodes, expose an 11-region density summary, and keep Home/End
navigation pinned to the first and last source interval. Boundedness is proven structurally (rendered
items and DOM nodes at their budgets at every scale), not by wall-clock or heap readings, which vary
with machine load and GC timing.

Visual regression uses three complementary gates:

- `tests/e2e/timeline/layout-geometry.spec.ts` compares committed desktop,
  phone, tablet portrait, and tablet landscape geometry within an 8 px
  tolerance. Counts and structural flags are exact.
- `npm run test:e2e:extension-visual` compares focused, committed Chromium
  pixel baselines for the timeline with the four fixture extensions active:
  the transcript lane, the 566-transition Runaway lane, and the composed marker
  layers at desktop, tablet, and phone sizes. The gate fixes locale,
  timezone, colour scheme, reduced motion, device scale, animations, scroll
  position, and bundled-font readiness; it intentionally does not claim human
  typography or real-footage acceptance. The composed cases also assert that
  the host density label does not cover selectable Runaway transition chips.
- The cross-browser/accessibility suites retain screenshots for composed marker
  layers, transcript/Runaway lanes, responsive controls, 200% content zoom, and
  reduced motion. The caption render matrix validates both caption rows on
  every encoded frame at seven frame rates and asserts that the render emits no
  font-stretch warnings; signed human acceptance still owns typography, shaping,
  and legibility judgment over real footage.

Budget changes require a release-note rationale and updated frozen-candidate
evidence; they must not be relaxed merely to make a regression pass.
