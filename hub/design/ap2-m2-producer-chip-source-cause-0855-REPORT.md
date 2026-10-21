# Producer initial-chip source-cause report — 0855

## Result

The retained `19080` failure is an obsolete test marker, not a missing
transcript occurrence and not a producer/product rendering defect. The route
mounted the production vendored transcript renderer, which rendered exactly
the two protected transcript occurrence buttons. The test still queried the
marker used by the retired dev renderer.

Prepared the smallest justified correction in:

`tests/e2e/local/producer-ownership-current-pin.spec.ts:94`

```diff
- await expect(page.getByTestId('transcript-lane-chip')).toHaveCount(2);
+ await expect(page.getByTestId('transcript-lane-occurrence')).toHaveCount(2);
```

The correction is test-only. It retains the exact count of two and leaves the
stable occurrence IDs, labels, protected foreign/user row assertions, source
identity checks, producer commands, later state checks, retry checks, and undo
assertions unchanged.

## Exact evidence and source cause

- Retained packet: `failure-1792572330-28858`, verified by the prior report and
  packet `SHA256SUMS`.
- Browser snapshot: lane `astrid.transcript` was visible and contained exactly
  two buttons with the expected labels and source IDs:
  `transcript-source:current-pin-speech:segment:foreign` and
  `transcript-source:current-pin-speech:segment:user`. The stale source item
  was absent from the mounted `[0,4]` carrier projection as intended.
- Failure: `tests/e2e/local/producer-ownership-current-pin.spec.ts:92`
  queried `getByTestId('transcript-lane-chip')` and received `0`.
- Mounted production source:
  `vendor/astrid-browser/astrid/packs/rendering/ui/transcript-lane/TranscriptLane.tsx:256`
  emits `data-testid="transcript-lane-occurrence"`; line 265 emits the same
  `Transcript segment: ... asset ..., source ..., start to end` label shape
  captured in the retained DOM.
- Registration path:
  `vendor/astrid-browser/astrid/packs/rendering/ui/transcript/extension.tsx:10`
  imports that renderer, and lines 52–56 register it for
  `astrid.transcript`. The generated catalog admits the extension at
  `vendor/astrid-browser/astrid/packs/rendering/editor/catalog.ts:8,16–22`;
  `src/tools/video-editor/dev/localExtensions.ts:9,14–16` supplies the catalog
  to the editor.
- The old marker remains only in the non-mounted dev example at
  `src/tools/video-editor/dev/transcript-lane/TranscriptLaneView.ts:131`.
- Host fallback is not causal: `src/tools/video-editor/components/TimelineEditor/DataLaneRow.tsx:980–1029`
  uses extent bars only for opaque lanes or lanes without a registered
  renderer. The retained lane was registered and rendered occurrence buttons.

Therefore the old/new mapping is:

| Assertion intent | Old marker | Mounted marker |
| --- | --- | --- |
| Count the two in-window transcript occurrences before producer action | `transcript-lane-chip` (retired dev renderer) | `transcript-lane-occurrence` (production pack renderer) |

No evidence supports changing the product renderer, source projection,
fixture seed, IDs, labels, timeout, or any producer behavior. The observed ACP
503 and Runtime history 409 remain secondary/unestablished and were not used
to infer causality.

## Verification and execution boundaries

- `git diff --check` — PASS.
- No browser, build, daemon, socket, actual producer run, retention replay,
  central test submission, full suite, install, or broad test was run, per the
  task boundary. The retained actual remains `19080` FAIL; historical `23671`
  and `17481` remain FAIL/UNKNOWN. Producer execution and all later protected
  row/commit/retry/undo assertions remain unreached by the retained actual.

## Handoff

No product patch or peer-owned HOME/shared/preview patch is proposed. The
prepared App-owned test correction is ready for review; a future actual may
reuse the retained packet but should be run only under the orchestrator's
ordinary-batch/central-snapshot decision.
