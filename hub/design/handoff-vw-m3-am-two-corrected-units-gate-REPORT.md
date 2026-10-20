# APPROVE — both exact corrected Agent units, independently

Reviewed the two requested final Agent commits separately against their exact
parents and against the current Agent `tl/integration` base. No product edits,
merges, checkouts, installs, browser/render/socket runs, network access, or
shared dependency/cache writes were performed.

## Sprite — APPROVE

Exact branch/commit: `tl/vw-m3-am-sprite-current-catalog-unit` /
`9d93e66e4e031b98fc042235334d1a4723006ebb`

Parent/product commit: `bdd02bd3f753e24092b982772bd481afc84f49da`.
The follow-up commit is catalog-only; the AM-sprite component and its direct
capability test are byte-identical to `bdd02bd3`.

Full delta from current-base parent `cf7448ed6c1298b172d004914cfe2bb8c99048e7`:

- `astrid/packs/astrid_motion/rendering/elements/effects/am-sprite/component.tsx`
- `tests/packs/rendering/test_sprite_scene_capability.py`
- `astrid/packs/rendering/elements/catalog.ts`

The component registers `prepareSceneCapability` on the real exported
component, and its capability and draw path both use the same private
`spriteAt` helper. The public Composition SSR test uses real
`TimelineComposition`, `resolveHostRegistries`, and the existing host
serialization/projector fixtures. No private evaluator math, public type/new
type, clock, source factory, DTO, save path, or renderer path was added.
Missing source/dimensions, decorated bounds, alpha/opacity/opaque coverage,
off-canvas content, and unsupported outer geometry remain conservative
`unknown`; hidden frames remain absent. Existing drawing behavior is retained.

Evidence on the exact corrected unit:

- Targeted Agent lane: **33 passed** (17 new sprite cases, host neighbors, and
  the existing SDK address diagnostic).
- Parent/candidate registered SSR comparison: **35/35 samples byte-equal**;
  aggregate `963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b`.
- Normal `scripts/gen_element_catalog.py --check`: **pass**; only the normal
  AM-sprite catalog revision changed.
- Ruff and `git diff --check`: **pass**.

## Plate — APPROVE

Exact branch/commit: `tl/vw-m3-am-plate-fill-fixture-fix` /
`48f3eef4bfe876fe2481d950ae33fa370fd03c58`

Parent/product commit: `c35b317c1104dda20f5ecfa59c00f7f9a9edbeae`.
The correction leaves the three product files byte-identical to `c35b317c` and
adds only the registered SSR fill/draw assertions, removes the stale
source-location neighbor assertions, and refreshes the normal catalog.

Full delta from current-base parent `cf7448ed6c1298b172d004914cfe2bb8c99048e7`:

- `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/component.tsx`
- `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/scene.ts`
- `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/surface.ts`
- `tests/packs/rendering/test_am_snap_plate_scene_capability.py`
- `tests/packs/test_am_snap_plate_fill.py`
- `astrid/packs/rendering/elements/catalog.ts`

`component.tsx` and `scene.ts` share the same `plateSurface` resolver, and the
component registers `prepareSceneCapability` on the real exported component.
The registered SSR test runs the real public `TimelineComposition` through
`resolveHostRegistries`; it now proves assetless fill drawing, image drawing,
and explicit `background`-over-`fill` precedence while retaining the existing
10-variant × 9-frame hash set. The stale fill neighbor no longer looks for
private source locations. Empty/unproven backing and non-opaque CSS remain
`UNKNOWN`; the public outer crop/entrance/exit geometry hold remains intact.
No private math/new types/clock, public package/schema/DTO, source factory,
save, renderer, or D09 deletion was added.

Evidence on the exact corrected unit:

- Corrected fill neighbor: **2 passed** (the previous 1-failure regression is
  gone without weakening the behavior proof).
- Claimed targeted suite: **108 passed in 31.60s**.
- Registered plate SSR: **1 passed in 3.99s**, 10 variants × 9 frames;
  existing hashes unchanged and added fill/draw assertions passed.
- Independent parent/candidate SSR identity from the prior final review:
  **90/90 samples byte-equal** (10 × 9), default theme equal.
- Normal `scripts/gen_element_catalog.py --check`: **pass**; only the normal
  AM-plate catalog revision changed.
- Strict TypeScript, Ruff, and `git diff --check`: **pass**.

## Current-base and artifact boundaries

Both complete branch patches apply cleanly with `git apply --check` against the
current Agent `tl/integration` worktree, whose shared merge-base is
`cf7448ed6c1298b172d004914cfe2bb8c99048e7`. The Agent worktree was clean before
and after these read-only checks.

The corrected units do not change the root Composition artifact. The current
Composition worktree remains on the pinned `@banodoco/timeline-composition`
`0.0.12`; any normal owner-controlled generated-artifact refresh is a separate
follow-up. This review grants no package/artifact broadening and does not
repack `0.0.12` or claim the planned `0.0.13` change.

The exact command/evidence ledger is in
`handoff-vw-m3-am-two-corrected-units-gate-commands.txt`.

## Limits and next steps

These are bounded Agent-unit approvals only. They do not qualify current API
completeness, Runtime admission, physical pixel/audio parity, browser behavior,
outer animation/crop capability, D09 source joins, or legacy caller deletion.
Owner may land each exact branch independently, then handle the ordinary
generated-artifact lifecycle and downstream integration gates.
