# H7 migration: what visibly changes if shots become nested layers

Read-only. Scripts: /private/tmp/claude-501/-Users-hannahomalley/290c846c-a08d-435e-aec6-9213ca83a716/scratchpad/shots/h7_migration_analyze.py (run with `python3 -I`), and /private/tmp/claude-501/-Users-hannahomalley/290c846c-a08d-435e-aec6-9213ca83a716/scratchpad/shots/h7_realm_fetch.py (SDK read, `open_bundle` per timeline, sourced from live-door/env.sh).
Outputs: .../shots/h7_film_analysis.txt (film), .../shots/h7-realm/ (18 bundles + _index.json), .../shots/h7-realm-analysis/*.txt (per-timeline analysis).
Data: Runtime head fcb41cecdb (same as tl-23s); browser drafts not included.

Semantics used. TODAY = flattened: visual clips sorted by parent track index (picture 0 top). NESTED = each shot is one layer on `picture` (idx 0), so it is above all loose visuals; inside it, its own track order. LOW = each shot is one layer on `plate` (idx 5), so loose clips on picture/chrome/type/fx/sprite draw above it. Shot layers are assumed opaque where they have an active visual child, and black where empty (see caveats).

## 1. Film timeline (almost-ready-no-first-second-v2, 7 shots)

Track order: picture 0, chrome 1, type 2, fx 3, sprite 4, plate 5, then audio (vo, music, sfx).

Loose top-level visual clips (only 2):
- clip-0: track type (idx 2), 23.867-28.867 s, hold image a1336a48-2721-4cd0-b0c1-81b71fc1ecb9. Overlaps shot 02 THE VISION (9.133-28.667) and shot 04 BACK TO WORK (28.667-42.333) for 0.2 s.
- clip-1: track type (idx 2), 196.567-201.567 s, image a09025f7. Starts at the timeline end (196.567); the shot 08 end is the same instant, so no overlap. Its 5 s run goes past the 196.567 s duration.

Pairwise stacking (overlap windows):
| loose | shot child | window | today | nested | low (plate) |
|---|---|---|---|---|---|
| clip-0 | c05-00 am-footage (plate) | 23.867-24.367 | clip-0 on top | shot on top | clip-0 on top |
| clip-0 | c05v1-00 softserve (plate) | 24.367-28.667 | clip-0 on top | shot on top | clip-0 on top |
| clip-0 | c17-00 am-footage (plate) | 28.667-28.867 | clip-0 on top | shot on top | clip-0 on top |
| clip-0 | c17-40 am-flap (fx) | 28.667-28.867 | clip-0 on top | shot on top | clip-0 on top |
| clip-0 | c17-39 am-type (type) | 28.667-28.867 | SAME TRACK, unresolved | shot on top | clip-0 on top |

Look at 23 s (what the owner sees): today the image clip-0 is drawn over the speaker footage. Under NESTED, clip-0 is hidden for its whole overlap (23.867-28.867 s), so the image is gone and the speaker footage shows. Under LOW (plate), the look is unchanged except for the same-track pair c17-39, which depends on the tie-break (unknown).

Hidden under nested: clip-0 (23.867-28.867 s). Shot children whose order flips relative to clip-0: c05-00, c05v1-00, c17-00 and c17-40 (all currently under clip-0 and would move over it). Tie: c17-39.

Shot internals (section 4 of the script output): all 7 shots list their tracks as an order-preserving subset of the parent's order, with no shot-only tracks and no clip on an undeclared track. Nested or low, inner stacking among a shot's own clips is unchanged. The only changes are the cross-layer ones above.

## 2. Other timelines in the realm (4 projects, 18 timelines, read-only)

Timelines with at least one shot placement: 9 of 18.
Timelines with a loose visual clip overlapping a shot: 4 of 18.
- 811a657.../01M4GGKMHZ3J8V402C8CWSCE95 ("Almost Ready — chapters"): 8 shots, 5 loose visual clips, 10 overlapping pairs, 5 loose clips hidden under nested.
- 811a657.../01M53A4F6WYGNQAD3XHS6MKNY0 ("chapters (04/05 fixed)"): same counts as above.
- 811a657.../almost-ready-no-first-second-v2 (the film): 7 shots, 2 loose, 2 overlapping pairs (clip-0 only).
- 20859a30.../01M4G8W9VERXYSNEQC3J6HK987 ("Render smoke"): 1 shot ("Opening", on track `picture`, but this timeline has no `picture` track; its tracks are V1-V4), 4 loose text clips, 2 overlapping pairs. Odd, not analysed in depth.
Shot-only timelines with no loose overlaps: 01M4GFCX (8 shots, 0 loose), almost-ready-one-shot-original (1 shot), v9-vision-trial (1 shot), 01M4GBH85 (1 shot), r3s-import-trial (1 shot). Pure-loose timelines: the rest.

The chapter timelines matter more than the film. Chapter 05 THE YEAR (58.133-90.8 s) and chapter 06 ASTRID (90.8-96.2 s) have loose sprites:
- am-sprite-09, am-sprite-10, am-sprite-11 (CRATE-WRENCH, CRATE-BROOM, CRATE-CLAW), plus c29-06 MYSTERY, are on track `sprite` (idx 4), 85.667-93.3 s.
- Today these sprites sit under shot 05's type-track clips c29-02..05 (type, idx 2) and show above shot 06's plate. Today the shot 06 chrome/sprite clips c30-03/04 are also under them at 92.8-93.3 s.
- NESTED: all four sprites are hidden under shots 05 and 06 for their whole overlap. At 90.8-92.8 s, shot 06's plate footage (c30-00) would replace the sprite that is visible today.
- LOW (plate): the sprites would sit above shot 05's type clips from 85.667 s, and every window from 85.667 to 93.3 s changes against today.
- A tie: c17-05 (plate, loose, 57.967-58.167 s) against the plate child of shots 04/05. Under LOW this is also a plate/plate tie.

## 3. Low-slot, the question asked

For the film: yes. Placing shots at plate keeps clip-0 above every shot child it overlaps, so today's look survives there, except the c17-39 tie.
For the chapter timelines: no. Loose sprites on track idx 4 sit above plate, so placing shots at plate puts the sprites over shot 05's type clips, which today are on top. Low-slot is not a single answer for all timelines.

## 4. Caveats (facts and assumptions)

- Same-track ties: when a loose clip and a shot child are both on one track and overlap (clip-0 vs c17-39 on type; c17-05 vs plate children), the flattened order is not in any file I read. The analysis sorts by (idx, start), which is a guess. Needs a renderer check (TimelineRenderer.tsx, shotCompositionProjection) before any decision.
- Opacity: the nested result assumes shot children are opaque where active. If a shot's type/fx clip is transparent, clip-0 shows through it. Opacity was not checked per clip.
- Empty shot area: nested is hidden where the shot is active but empty only if the shot layer paints black. TimelineRenderer.tsx:1727 uses an AbsoluteFill with backgroundColor black, and ShotClipSequence (TimelineRenderer.tsx:212-276, call at :1416) is the nested legacy path. I did not verify which layer the nested renderer uses for the empty case. The film results don't depend on this, since the shot's children cover clip-0's span.
- Duration of hold clips is taken as `hold` seconds. Media clips with no `hold` use to-from.
- The analysis only sees timeline records. Preview and render paths were not run.

## 5. Opinion (label: opinion, not measured): what a migration has to do

1. Don't pick one slot. The film needs the shot above the image (or the image moved into the shot), and the chapter timelines need the sprites above the shot. No single shot track gives both looks, so the migration must choose per overlay: move loose overlays that belong over a shot onto a track above `picture`, or fold them into the shot as children. A rule like "loose clips stay put, shots move" will change looks.
2. For the film, the simplest look-preserving option is probably to re-home clip-0 as a child of shot 02 or 04 (or a loose clip on a layer above picture), and make the 0.2 s tail into shot 04 explicit. Either way the owner should see the image where it is today.
3. Resolve same-track ties in the new model before migrating: state which of clip-0 and c17-39 wins at 28.667-28.867 s, and make the migration keep that winner.
4. Verify with a before/after frame diff at the windows above: film 23.9, 24.5, 26, 28.7, 28.85 s; chapters 85.7, 87, 89.5, 91, 92.9 s and 58.1 s. A mismatch at any of these is a visible change.
5. Clean up the odd `Render smoke` Opening shot (track `picture` absent from its parent) before any shot-semantics change, since it is a test case the migration would touch.
