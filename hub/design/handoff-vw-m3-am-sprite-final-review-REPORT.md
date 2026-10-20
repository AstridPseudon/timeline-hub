# APPROVE — exact narrow Agent AMsprite capability unit

Reviewed **bdd02bd3f753e24092b982772bd481afc84f49da** against parent **cf7448ed6c1298b172d004914cfe2bb8c99048e7**. HEAD is exactly the requested commit. Read PLAN, COMMON, current Viewing INBOX and the worktree AGENTS.md. No source changes made. No blocking component/test finding.

Only `astrid/packs/astrid_motion/rendering/elements/effects/am-sprite/component.tsx` (+46/-17) and `tests/packs/rendering/test_sprite_scene_capability.py` (+283) change. This approval covers that bounded Agent-owned unit, not an integrated caller or retirement gate.

## Findings

- The component's existing stepped pose, scale clamp, logical positions, entrances, blink/strip clock, flip, silhouette, outline and shadow calculations are preserved. A single private `spriteAt` now supplies both drawing and capability geometry. `LOGICAL_PX` stays 6; screen dimensions stay art dimensions times scale. No second geometry implementation or exported helper.
- Normal generated owner dispatch forwards `prepareSceneCapability`, through `resolveHostRegistries` to the unchanged public12 `prepareCompositionScene`. Tests use real `project_shot_composition` output and renderer `_serialize_timeline`, explicit tracks/theme/assets and existing owner references. Wrong owner refuses; selected registry source wins over params.src. No package, public type/schema, DTO, source factory, save or renderer path changes. The existing public evaluation types are only imported.
- Raw stored x4212/y20 at scale8 gives x25272/y120 and 128x128, preserving the existing drawing units. Normal editor conversion stores x702/y3 and draws x4212/y18. Mixed scale8/6 gives widths128/96; runner x-900 becomes -5400 and later x300 becomes1800; normal compiled source joins preserve the occurrence and .70/.56 asset provenance. These provenance values are preserved data, not new public damaged-art diagnostics.
- No source/dimensions, unrelated fallback dimensions, outline/shadow expansion and unsupported outer crop/animations remain unknown. Bare authored width/height cannot invent bounds. Normal compilation rejects an invalid strip width; a deliberately raw host probe for invalid dimensions stays unknown. Source absence and stamp/blink hiding remain known absent.
- Declared layout bounds never establish decoded image presence, alpha, opacity or opaque coverage. Even an offcanvas rectangle retains unknown visible/coverage where alpha is unproved; authored alpha/opaque flags do not promote it. No source-authority claim is added.
- Independently substituted the actual parent component into the same generated registered SSR path: **35/35 markup samples byte-equal** to candidate. Recomputed parent aggregate SHA256 `963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b`, matching the new regression assertion. This establishes these SSR samples, not physical pixel parity.

## Independent checks

Exact commands are in the companion commands file. All run from the assigned worktree, dependencies read-only, private test stages and real scope directories.

- Targeted pytest: **33 passed in 29.57s**, comprising all **17 new** sprite cases, 15 existing host cases and the unchanged existing SDK address diagnostic. Includes strict TypeScript noEmit against actual public12 declarations, units/offcanvas/mixedscale/strip/absence/unknown-alpha/owner/source/SSR checks.
- Independent review probe: **exit0**, parent SSR comparison, four raw dimension probes, normal invalid-strip schema refusal and in-memory baseline/candidate metadata comparison.
- Ruff on new direct test: **All checks passed**. Exact commit `git diff --check`: **exit0**.
- After tests and independent probes, **all77 installed public12 members still byte/hash-equal to the pinned tar**, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Private stage @banodoco/@remotion are real directories. Exact HEAD verified; worktree clean.

Two supplementary probe setup failures were retained: the first omitted the existing fixture's removal of inherited loader/interpreter override variables; the next attempted an invalid strip through normal schema admission and was correctly refused. The final probe explicitly handles that refusal and separately tests raw host data. Neither is a product failure or a weakened repository test. Logs: `review-probe-initial.log`, `review-probe-schema-refusal.log`, `review-probe.log` in this worker directory.

## Generated metadata — owner follow-up only

The normal element catalog freshness check **exits1** on this exact candidate. Its checked-in bytes match generated parent output exactly. Candidate generation changes only AMsprite's revision in `astrid/packs/rendering/elements/catalog.ts`:

- Parent: `sha256:f88ce18c3486aca0cf5a844420b822c554ff3b3eb396ab4c1ea54430a43be5b3`
- Candidate: `sha256:da9e894e6ad65f4503f60a9adf80596ad88ec1436302dcf57783d880496e1966`

Generated host-effects import query/fingerprint also correctly changes from `f26441ae79b7...` to `a89157a6a62c...`. Host maps are generated normally, not a tracked source addition. Tool catalog generation is unchanged and still matches the checked-in catalog. Component/helper resources remain within the already declared pack closure. Metadata diffs are recorded in this worker directory; **no metadata was edited**. Agent owner must regenerate the normal element catalog and rerun its freshness check when integrating; this is not an all-checks-green claim.

## Boundaries and next step

Approve the exact narrow capability unit for Agent ownership review/integration, with the normal generated-catalog follow-up above. Keep D09 caller/cache/mouth/private geometry in place until their qualified source join and existing positive behaviors pass. This capability is not a deletion and the retained SDK test's passing private path does not qualify its public replacement.

Nothing blocked the assigned review. No install, network, browser, physical render, socket, full suite, central request, git mutation or shared dependency/cache write. No production source-admission, native environment qualification, current API compatibility or frame/audio parity claim. Worktree remains unchanged.
