# Corrected Agent-review proposal: preserve known mouth facts

## Result

`proposal.patch` is a revised, unapplied proposal against clean base
`751dd75e2866712a661edce20c4c50b6ac89d7c7` (`751dd75e2`). It changes only:

- `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts`
- `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/scene.ts`
- `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/element.yaml`

The patch adds `mouthInspectionRect(raw)`, derived from the existing
`mouthAnchor(raw)` and `mouthEraseRect(anchor)`, then expands that same actual
drawing geometry by one logical pixel horizontally and two vertically. The
scene uses the same `presenterAt` view and `pixelGeometry` transform. The
public diagnostic remains a known inspection area for the existing normalized
default, partial, fractional, and raw-invalid inputs; it does not become
unknown merely because a private legacy crop would have skipped or interpreted
those inputs differently.

Mosaic remains unknown, and unsupported outer geometry remains subject to the
existing public sanitizer. Presence, alpha, plate support, and occupied-pixel
claims are unchanged. The component drawing body, motion/codebook behavior,
and existing 286 SSR expectations are not changed by this proposal.

This is a review artifact only. No product source was applied or committed.
Agent review is required before any source scope change or consumer migration.

## Consumer boundary retained

The public ROI is an inspection area, not proof of occupancy or statistical
equivalence to the old private `mouth_box` crop. The legacy consumer must keep
its current private crop and fallback until a separately reviewed qualification
completes:

- An absent mouth keeps the original legacy skip. The public normalized default
  must not be narrowed to unknown to reproduce that private skip.
- Only an explicit complete numeric anchor whose integer values equal the
  component's normalized `mouthAnchor` values is eligible for a compatibility
  comparison. Omitted, partial, fractional/non-integer, non-finite, and
  clamped/raw-invalid inputs remain unqualified for equivalence; their private
  legacy geometry may differ from the actual normalized draw and must not be
  described as statistically equivalent.
- Until qualification, retain private crop/fallback and existing statistics.
  Do not add a caller flag, public type, private clock, or copied timing/
  geometry formula.
- The existing actual public query policy remains: use the same prepared Root,
  resolve the exact compiled clip/occurrence and owner, obtain component frame
  zero through the public query API, retain that component-zero ROI for the
  selected series, and reject missing/ambiguous/stale/foreign identity as
  unknown. The already-qualified five-case clock prototype is sufficient for
  this proposal; it is not rerun here.

## Precise post-approval test update plan

These tests are a later Agent-reviewed change, not part of this unapplied
artifact:

1. Update intentional geometry expectations from the erase rectangle to the
   padded compatibility ROI, using the literal existing pixel conversion at
   1920x1080, 640x360, 641x361, and 720x405. For the explicit
   `{x:151,y:104,w:19}` zoom-1 frame-0 640x360 case, retain the exact padded
   crop `(298,202,345,219)` and area `799`; retain the erase control
   `(300,206,343,215)` and area `387` separately.
2. Keep passing known-region tests as known for defaults, custom anchors,
   partial/fractional/raw-invalid normalization, zoom/focus clamps, push,
   punch, bob, rational fps, speed, preroll, and occurrence identity. These
   tests must not be rewritten to expect refusal and must not be made strict
   XFAILs. Keep mosaic and unsupported-outer-geometry unknown tests, the
   source-bound owner/identity controls, all 286 SSR hashes, and legacy
   neighbors.
3. Add or retain consumer controls without changing the public fact: absent
   mouth skips privately; partial/raw-invalid private inputs are explicitly
   unqualified; explicit complete normalized integer anchors alone can enter a
   compatibility comparison. The test must assert no claim of equivalence for
   unqualified inputs and no per-PNG moving-ROI selection.
4. After approval, prepare exactly four registered `renderStill` calls at
   frames `[0,3,4,5]`, 1920x1080, fps30, duration60, scale `1/3`, explicit
   mouth `151/104/19`, words `[[.1,.4]]`, chrome none, `blinkEvery:0`, seed7.
   Prepare one Root, obtain component-zero compatibility ROI once, and retain
   it for all four PNGs. Do not run this capture in this task.
5. On unchanged PNG copies, require old crop == compatibility crop ==
   `(298,202,345,219)` with 799 pixels and zero identity differences on every
   unaltered image. Keep natural adjacent-pair fractions and strict `>2%`
   decisions identical, including a natural positive above 2%.
6. Keep planted-copy controls: 8 changed pixels gives `8/799` below 2% for
   old/compatibility and `8/387` above 2% for erase; 20 changed pixels is
   detected by all three; 15/16 boundary controls preserve
   `15/799 <= .02 < 16/799`; and 16 pixels placed only in compatibility
   padding are detected by old/compatibility but missed by erase. Copies only;
   do not alter the threshold, normalize images, or weaken positives.

## Verification

Commands run from this worktree:

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-proposal-preserve-known/proposal.patch
git apply --numstat /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-proposal-preserve-known/proposal.patch
git status --short --branch
```

Results: patch check passed; numstat is `10/1` for `motion.ts`, `3/3` for
`scene.ts`, and `9/2` for `element.yaml`; the product worktree remains clean
at `751dd75e2`. No prototype, browser, install, network, source-pack pin,
full suite, or product behavior test was run. The existing five-case clock
prototype is already qualified by the completed proposal report, and no new
clock behavior is introduced here.

## Decision / next step

The held proposal's strict public-input narrowing and new refusal/XFAIL path
were removed because they would falsify existing known/default/raw-normalized
public facts. Forward this corrected patch to the Agent manager for required
review. Keep the old proposal held; do not apply this one or schedule the
four-still controls until approval.
