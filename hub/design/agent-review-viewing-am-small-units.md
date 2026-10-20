# Agent review: Viewing AM sprite and AM snap-plate units

Date: 2026-10-20

## Verdict

APPROVE the two narrow product/test/catalog units, with release held until the normal generated artifact manifest is refreshed. Merge separately and in order:

1. sprite tl/vw-m3-am-sprite-current-catalog-unit at 9d93e66e4e031b98fc042235334d1a4723006ebb;
2. plate tl/vw-m3-am-plate-fill-fixture-fix at 48f3eef4bfe876fe2481d950ae33fa370fd03c58, only after sprite is accepted.

This is not approval of a stale artifacts.json. After each landing, refresh and check the normal manifest in the combined current tree.

## Bases, scope, and conflicts

Reviewed Agent current tip: 6a6d92d3da9182378660ed1244124f569d8b4b0b (tl/integration and task HEAD). Both candidates share stale broad base cf7448ed6c1298b172d004914cfe2bb8c99048e7. Their full current-tip diffs contain 59 and 62 paths; those broad differences are not approved.

The exact owned scopes apply cleanly to current 6a6d92d with git apply --check --whitespace=error. Sprite scope is am-sprite/component.tsx, its direct test, and the normal generated catalog row. Plate scope is component.tsx, scene.ts, surface.ts, its registered scene test, the fill test, and the normal generated catalog row.

The plate candidate catalog contains the pre-sprite revision. Do not apply it wholesale after sprite lands; regenerate the normal catalog on the combined tree. No narrow source conflict remains after that composition.

## Sprite

Exact parent: bdd02bd3f753e24092b982772bd481afc84f49da. spriteAt is shared by draw and capability preparation. Known geometry is limited to a resolved source plus declared dimensions and undecorated bounds; alpha/decoding, decorated bounds, and unsupported outer geometry remain unknown. Hidden frames are absent. Direct geometry uses the draw clock and preserves the off-canvas/mixed-scale and immutable-input checks.

The handoff reports 33 targeted passes and 35/35 independent public SSR samples byte-equal to the parent, aggregate 963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b. My current-tip private composed archive ran 17 passed in 57.49s, including registered SSR cases.

## Plate

Exact parent: c35b317c1104dda20f5ecfa59c00f7f9a9edbeae. plateSurface is the single resolver used by draw and capability preparation. Assetless hex/token fill is positive, an image remains drawn, and explicit background takes precedence over fill. Empty/raw-invalid backing, non-opaque CSS, and public12 crop/entrance/exit geometry remain unknown. The old source-location fill assertions are replaced by registered public SSR assertions, not deleted behavior.

The handoff reports 108 targeted passes, 2 fill passes, 1 registered plate SSR pass, and 90/90 parent/candidate SSR samples byte-equal. My private sequential archive ran 2 fill tests passed in 0.18s and 14 registered plate capability/SSR tests passed in 29.96s.

## Catalog, manifest, and protected bytes

Normal scripts/gen_element_catalog.py --check passes in the sprite archive. After applying sprite, then plate source/tests and running the normal generator, the combined catalog is fresh and retains:

- sprite revision sha256:da9e894e6ad65f4503f60a9adf80596ad88ec1436302dcf57783d880496e1966;
- plate revision sha256:95e056c78f81e0455f49511dd8569438a5b9dc5975ea9672b8fa17bfe2cea296.

Current catalog SHA-256 is 265e363dfcc7196ebdeff011b63c830ca17847b160c3ec836c955ff3c22c2a8a and current artifacts.json SHA-256 is 2ef0f27f4b8a5d1029356861da0841e5f319485f259777c3f3d7d0080d5021a0. In private archives, artifacts.json --check reports the expected AM generated files as stale. The exact owner refresh is:

    python3 scripts/gen_element_catalog.py
    python3 scripts/artifact_manifest.py
    python3 scripts/gen_element_catalog.py --check
    python3 scripts/artifact_manifest.py --check

Sprite refresh needs am-sprite/component.tsx and catalog.ts. The combined plate refresh additionally needs am-snap-plate/component.tsx, scene.ts, and surface.ts. No package repack or pin change is authorized.

Protected current hashes, identical in both private archives:

    verified_source.py                         c0dcabd27230f9661be59b2461c9759716daad215e1b508c8f9e73bb96e326d8
    test_verified_source.py                    aa087e5840fbe84606ef8cdf85f971e5d9a17c8038c6cad23bd8513b6467b9c5
    published-sources.json                     1deac01582348b27a90455c27010622280178919ee2c3daed1e0c025b571dda6
    sdk/remote.py                              6d5c36420eeadc14e69f6414c843d8b5a17c5b893224b9ef364322907a2b175a
    sdk/timeline/commit.py                     524619491e5880b493f89175301098daa66cc37244e64572f8f00a93f0e3124e
    runtime.lock.json                          c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311
    visual-compile-contract.md                 94581609e327918152ee6779e8fb3915391c091167eba8758ecbe38a4200cbf4
    Composition 0.0.12 archive                 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
    remotion/package-lock.json                cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597

## Commands and limits

Private sequential archive: archived current 6a6d92d, applied only sprite scope, then applied only plate source/test scope while regenerating catalog normally. Shared node modules, runtimes, fixtures, and package bytes were read-only; pinned Node 20.19.4 and Remotion-0012 peers were used.

Candidate-specific results:

    git diff --binary cf7448ed6c1 9d93e66e4 -- sprite owned paths | git apply --check --whitespace=error    PASS
    git diff --binary cf7448ed6c1 48f3eef4b -- plate owned paths  | git apply --check --whitespace=error    PASS
    python3 scripts/gen_element_catalog.py --check                                                        PASS
    python3 scripts/artifact_manifest.py --check                                                          FAIL: AM generated files stale
    pytest ... tests/packs/rendering/test_sprite_scene_capability.py                                             17 passed
    pytest ... tests/packs/test_am_snap_plate_fill.py                                                        2 passed
    pytest ... tests/packs/rendering/test_am_snap_plate_scene_capability.py                                  14 passed

The named central composition12-owner-integration neighbor lane was requested once against the service snapshot. It returned 16 passed, 1 failed, 30 errors because the snapshot had no remotion/node_modules; presenter SSR fixtures errored at setup and generated-custom-elements failed with Node ERR_MODULE_NOT_FOUND. This is environment evidence only and does not qualify or disqualify either AM unit. Candidate-specific SSR used the private pinned peer set and passed.

No full suite, browser journey, live socket, physical pixel/audio parity, Runtime admission, artifact repack, D09 closure, or private-crop deletion was run or claimed.

## Final integration condition

Merge sprite first through the merge queue, refresh and check the normal manifest, then merge plate separately and repeat catalog and manifest generation/checks. Preserve presenter, source-certification, PCM, SDK, schema, lock, and public12 bytes. D09/private crop/parity remains held.
