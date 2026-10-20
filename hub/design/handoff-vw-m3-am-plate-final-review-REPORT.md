# REJECT exact commit for landing; bounded product implementation is sound

Reviewed `c35b317c1104dda20f5ecfa59c00f7f9a9edbeae` at identical clean HEAD in `/home/user/work/wt/vw-m3-am-plate-final-review`. Read PLAN, COMMON, current Viewing INBOX and repository AGENTS. No repository files changed. The review task is complete; this is not a D09 implementation blocker or completion claim.

## Required correction

**P2 — newly failing existing neighbor test.** The helper extraction at `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/component.tsx:83` moves `FILL_TOKENS` and `params.background ?? fill ?? COLOR.paper` to `surface.ts`, but `tests/packs/test_am_snap_plate_fill.py:25` and `:28` still require those strings inside the component. The actual suite gives **1 failed / 2 passed**. Running the unchanged test class with only its component read supplied from `git show c35b317c^:.../component.tsx` gives **3 passed**. This is a change-induced test-location regression, not a demonstrated drawing regression. Update that neighbor to follow the extraction while preserving its original fill/default/assetless behavior expectations. Do not skip, disable or encode lost behavior. Recheck this small unit after that correction.

## Qualified product assessment

The token table, source precedence, fill trimming and nullish background fallback are moved unchanged into one shared helper. Drawing still uses the original plateView, transforms, tint, wipe and mosaic code. The intrinsic capability describes the already painted AbsoluteFill backing; it proves opacity only for opaque 3/6-digit CSS hex colors. No media-alpha guess, copied geometry evaluator, clip-ID special case, public type/package change, source factory, DTO, renderer/save change or manufactured assetless fill.

Independent normal final-Root preparation uses the real projector, serialization, materializer, canonical profile and freshly generated owner maps; historical reads and runtime admission are explicit doubles, and the callback aborts before render. Normal and owner-qualified real AM dispatch produces COVERED/CONTENT image, COVERED/EMPTY explicit background, half-open GAP, fade DIP and translucent GAP; a managed fully transparent PNG still has the existing opaque backing. Pan/mosaic/tint/component wipe support is covered. Empty raw params and unproven CSS backing stay UNKNOWN.

The existing private crop, scale-in and fade-up positives are retained, including their original suites. Public12's outer geometry results remain explicitly UNKNOWN with unknown-animation-geometry. These unknown assertions do not replace the old positives. Clip outer animations are not qualified by component enter/exitWipe coverage. D09 callers and deletions remain held.

## Independent evidence

- Claimed targeted set reproduced: **108 passed in 36.41s** (14 new direct cases plus 94 neighbors).
- Additional existing fill neighbor: **1 failed, 2 passed in 0.15s**; parent-source control: **3 passed**.
- Parent versus exact-commit SSR, same public12 host: **1 passed in 4.52s**, all **10 variants × 9 frames** byte-equal, default theme equal, only capability registration added. The checked-in 90-sample hashes also pass.
- Targeted strict TypeScript: **exit 0**, strict/noEmit/Bundler, byte-equal copies of plate sources/direct dependencies in own disposable overlay. Ruff and patch whitespace: **exit 0**.
- Public12 artifact SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; its **77 installed files unchanged** across preparation fixtures. Real private scope directories, leaf-only peer links. Read-only clean peer HEAD `f8164bef73215272562c4d6974acadbd82c2898a`, React 18.3.1, Remotion 4.0.509, Node v20.19.4. No polluted shared graph used.

Exact commands and owned helper scripts: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-am-plate-final-review-commands.txt`.

## Normal generated-metadata handoff to Agent owner

Read-only `scripts/gen_element_catalog.py --check` exits **1 (stale)**. Descriptor comparison finds exactly one difference: AM plate revision, `sha256:9050dc21d2306b4f7c1741b3814e4b81ded364fa83b45baf0da1b168c018711c` → `sha256:95e056c78f81e0455f49511dd8569438a5b9dc5975ea9672b8fa17bfe2cea296`. Owner should run the normal catalog generator in the authorized landing worktree and commit that generated projection, then verify `--check`. Do not hand-edit metadata. The normal effect registry fingerprint is now `fb712a9116f95dae8cbd563e2e85c4016e3f37e3e969867d17a82d6e0a58e846`; regenerate normal host maps through the existing lifecycle, never inside installed Composition. This is routine metadata upkeep rather than grounds for any API/package invention.

## Limits and next step

No physical parity, decoded-image/image-loading proof, real Runtime admission, browser, audio, full-suite, current API, gate 6 or D09 completion claim. No shared dependencies/caches or git state written. Approval requires the small neighbor-test correction and normal Agent-owned generated metadata upkeep; then rerun only affected checks. Crop/outer-animation public positives and source-bound caller migration remain separate work.

Reviewed patch (not a proposed reviewer change): `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-am-plate-final-review-reviewed.patch`.
Reviewed absolute file list: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-am-plate-final-review-files.txt`.
