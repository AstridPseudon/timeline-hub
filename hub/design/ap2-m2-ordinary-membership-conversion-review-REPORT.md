# AP2-M2 ordinary membership conversion review

## Verdict

**APPROVE the five-member ordinary journey expectation.** This is an
independent assertion-conversion review of the candidate based on `17655a570`
(`fix(app): route ordinary marker holds through generic capture`). It approves
the truthful native membership and retained assertions; it does **not** claim
that the App/Agent/Runtime browser gate has passed.

## Membership and order

The production action is `moveExistingShotsToMarkers()` in
`src/tools/video-editor/dev/scene-phase-markers/extension.ts`. It calls
`visualClips(snapshot)` without filtering. `visualClips()` walks visual tracks
in track order and filters `snapshot.clips` without reordering.

The canonical projection constructs `config.clips` as:

1. the two non-shot parent clips, in authored parent order;
2. each occurrence's child clips, in raw child order.

The ordinary seed therefore produces exactly these five display IDs, in this
order:

```text
f2-app-clip
f2-transition-clip
f2-occurrence:f2-plate
f2-occurrence:f2-agent-clip
f2-occurrence:f2-agent-clear-clip
```

The projected child IDs are represented in the actual selector form as:

```text
occurrence:f2-occurrence/clip:f2-plate
occurrence:f2-occurrence/clip:f2-agent-clip
occurrence:f2-occurrence/clip:f2-agent-clear-clip
```

The candidate expectation is consequently correct: ten commands, in five
move/hold pairs, with marker assignments `1, 6, 6, 6, 6` and holds `5, 3, 3,
3, 3`. The candidate regression test also directly checks the five-member
operation-target order.

## Capture, intent, and preservation

The generic port resolves projected child IDs through each clip's canonical
`clipRef`; it does not infer a parent owner from the display ID. The existing
authoring bundle/cohort contains the exact occurrence-qualified IDs,
occurrence ownership selection, shot/source mapping, source registry, and
owner-qualified selection proof needed by `captureClipMove()` and the scalar
hold capture. The child commands use the existing occurrence intent
(`ownership: occurrence`, fixed absolute position); parent moves retain the
existing fixed/absolute move intent, and scalar holds use the existing empty
intent.

The generic capture is sequential, so each hold is captured against the
preceding member's moved bundle. The move carrier writes the existing static
duration marker (`app.astrid.for`) and the hold carrier updates that marker
alongside `hold`. Neither operation reconstructs the clip row. Existing
transition, opaque app data, source registry data, and unrelated fields remain
in the bundle. This is covered by the neighboring generic/ordinary capture
tests and by the existing `recipe_m2_app_clip_scalar_fields.json` cohort,
including occurrence-qualified capture and opaque preservation.

## Boundary review

No intermediate move-before-hold correction is required:

- `f2-plate`: local move to `6`, original extent `12`, then hold `3` gives
  `[6,9)` inside the occurrence's `[0,12)` extent;
- `f2-agent-clip`: local move from `3` to `6`, hold `3`, gives `[6,9)`;
- `f2-agent-clear-clip`: local move from `6` to `6`, hold `3`, gives `[6,9)`.

The existing hold carrier is the minimal intent-preserving mechanism. No new
operation, inferred ownership, filtered subset, or weakened boundary assertion
is justified.

## Retained journey assertions

The candidate keeps the real assertions for the grouped ordinary batch,
disjoint Agent edit, newer local edit, lost acknowledgement, reload, Runtime
restart, byte-exact retry, rebased suffix, guarded undo order, opaque data,
immutable closure, and zero legacy traffic. The batch remains all-or-refuse at
generic capture; there is no filtered partial success or native-gate claim.

## Evidence and limits

Reused the recipe worker's exact evidence (no old source rerun):

```text
npm exec vitest run --no-cache --configLoader=runner \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
PASS — 1 file, 45 tests

npm exec eslint -- --max-warnings 0 \
  tests/e2e/local/three-products.spec.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
PASS — exit 0

git diff --check
PASS
```

No browser, localhost, live socket, Runtime-door, full suite, dependency,
schema, pin, or central ordinary run was performed. The stale retained App
`TimelineOps` adapter is the known prerequisite; the actual five-member native
acceptance remains unverified until that shared App fix is committed and one
central ordinary gate is run against the resulting source.

## Recommended next step

After the exact stale-adapter peer fix lands, run the one central ordinary
journey. If it reports a concrete native refusal for one of the five
owner-qualified members, preserve that refusal trace and review the actual
operation/fixture boundary; do not revert to a two-member or filtered batch.
