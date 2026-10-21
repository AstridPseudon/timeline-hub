# Agent AM-footage current-resource adoption

## Scope

Adopted the exact AM-footage source behavior from Viewing revision
`2e9fb6e260778e0ae6dc4a39a498d0f36a837ef` onto Agent `4467c1c1a`:

- added `helper.ts` and `scene.ts` byte-for-byte from the exact revision;
- declared both files as normal `astrid_motion` resources;
- regenerated the normal element catalog and artifact manifest;
- did not port `scene.test.mjs`, oldRoot/compositionpackage/pins,
  disablestrictness, private geometry/physical claims, or any wire/DTO/authority
  surface.

The scene behavior retains full-field support for blank and own-entry-undefined
media slots, transparent inset bounds, admitted-media geometry, and unknown
alpha when media facts are incomplete. Catalog/custom-owner descriptors and
immutable admission data were otherwise unchanged.

## Qualification

- Pack validation passed in a private staging checkout.
- Normal Remotion generation passed in private staging with the public13
  Composition dependency and Node 20.19.4. Generated types and element
  registries were not copied into the product worktree.
- Normal generated Root typecheck passed:
  `tsc --noEmit --pretty false -p <private-stage>/remotion/tsconfig.json`.
- Five direct scene controls passed: admitted full-frame media, transparent
  inset, own-entry-undefined media, blank slot, and unresolved transparent
  inset.
- Five volume controls passed from
  `remotion/tests/am-footage-volume.test.cjs`.
- Targeted Agent tests passed: `25 passed in 20.63s` with staging dependency
  environment:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
    ASTRID_REMOTION_PROJECT_DIR="$STAGE/remotion" \
    ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
    /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
    tests/packs/astrid_motion/test_astrid_motion_pack.py \
    tests/packs/rendering/test_remotion_element_generation.py \
    tests/test_artifact_manifest.py \
    tests/core/test_editor_element_catalog.py \
    tests/core/test_element_catalog_cutover.py
  ```

The first targeted invocation without staging dependencies had 22 passes and
3 environment-only failures because this worktree intentionally has no local
`remotion/node_modules`; the staging-backed rerun passed all 25.

No full suite, browser, render, socket, install, activation, runtime-payload,
private-code, or managed-replay check was run.
