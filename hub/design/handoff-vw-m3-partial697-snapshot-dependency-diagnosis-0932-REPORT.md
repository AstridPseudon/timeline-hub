# Partial697 snapshot Composition dependency diagnosis

## Result

The exact cause is an attachment mismatch in the central test snapshot, not a bad archive or collection result.

The 0923 result
vw-m3-partial697-retained-one-physical-0923-e2e-viewing-partial697-retained-one-physical-0923-1021092730-22788
collected both tests, then failed during presenter_query setup before physical capture:

    ValueError: cannot verify missing rendering components: installed public Composition package is missing at
    /home/user/work/wt/.test-vw-m3-partial697-retained-one-physical-0923-e2e-viewing-partial697-retained-one-physical-0923-1021092730-22788/remotion/node_modules/@banodoco/timeline-composition/package.json

The fixture has two dependency paths which were incorrectly treated as one:

1. tests/packs/rendering/test_presenter_scene_capability.py:26-31 reads the immutable artifact and optional ASTRID_COMPOSITION_TEST_NODE_MODULES peer graph. In the 0923 command that graph was the approved public13 runtime graph /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules.
2. test_presenter_scene_capability.py:43-48 extracts the public13 package into the private temporary project and leaf-links peer packages from that graph. This is the path used by the crop helper.
3. scripts/gen_effect_registry.py:146-155 independently resolves ASTRID_REMOTION_PROJECT_DIR or defaults to ROOT/remotion, then opens ROOT/remotion/node_modules/@banodoco/timeline-composition/package.json. The 0923 command did not set ASTRID_REMOTION_PROJECT_DIR, and its snapshot had no remotion/node_modules, so registry discovery failed before capture.

The physical path then would have continued through tests/packs/rendering/presenter_crop_capture.py:35-44, which copies the geometry, entry, and capture helpers and starts Node. presenter_crop_capture.mjs:5-8 opens @remotion/bundler and @remotion/renderer; presenter_crop_geometry.mjs:3-5 opens Composition root/evaluation and generated query.mjs; presenter_scene_capability.mjs:8-39 opens esbuild, React, React DOM, Remotion, Composition root/evaluation, and host registries.

The service already has the normal carrier. Its agent snapshot logic at
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run:40-42
links the source checkout's remotion/node_modules into the snapshot when it exists.
The smallest repair is the one authorized read-only, untracked source symlink:

    /home/user/work/wt/vw-m3-partial697-snapshot-dependency-diagnosis-0932/remotion/node_modules
      -> /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules

No package path, assertion, crop, threshold, denominator, renderer, or source authority was changed. The symlink is for a later manager-authorized test-service snapshot; invoking the 0923 command directly in this live worker would trip its clean-tree guard because the carrier is intentionally untracked.

## Full physical dependency path manifest

For snapshot root S and approved graph G, the physical test needs these roots/files:

    S/remotion/package.json
    S/remotion/node_modules
    S/remotion/node_modules/@banodoco/timeline-composition/package.json
    S/astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/*
    S/astrid/packs/astrid_motion/rendering/elements/_shared/{am.tsx,mosaic.tsx}
    S/astrid/packs/rendering/shared/element_contracts.ts
    S/remotion/{package.json,webpack-alias.mjs,src/host-registries.ts}
    S/remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz
    S/tests/packs/rendering/{presenter_crop_capture.py,presenter_crop_capture.mjs,presenter_crop_entry.mjs,presenter_crop_geometry.mjs,presenter_scene_capability.mjs,test_presenter_crop_equivalence.py,test_presenter_scene_capability.py,_helpers.py}

    G/@banodoco/timeline-composition/package.json
    G/@banodoco/timeline-composition/dist/{index.js,evaluation.js,registries.js,theme-api.js}
    G/@remotion/bundler/package.json and dist/index.js
    G/@remotion/renderer/package.json and dist/esm/index.mjs
    G/@remotion/media/package.json and dist/esm/index.mjs
    G/@remotion/layout-utils/package.json and dist/esm/index.mjs
    G/esbuild/package.json and lib/main.js
    G/react/package.json and index.js
    G/react-dom/package.json and index.js
    G/remotion/package.json and dist/esm/index.mjs
    G/.package-lock.json and transitive files reached by those package entries

    /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/artifacts/banodoco-timeline-composition-0.0.13.tgz
    /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node

In the actual 0923 command, ASTRID_COMPOSITION_TEST_ARTIFACT overrides the
snapshot artifact with the runtime artifact above; the source artifact path is
the default fallback and is retained in the manifest for completeness.

The fixture's private temp project is T under pytest's temp root:

    T/remotion/node_modules                         # private real directory
    T/remotion/node_modules/@banodoco/timeline-composition  # extracted 77 files
    T/remotion/node_modules/<all non-@banodoco peer leaves> # symlinks into G
    T/remotion/{package.json,webpack-alias.mjs,query.mjs,builtin-default-theme.json}
    T/remotion/src/{host-registries.ts,effects.generated.ts,animations.generated.ts,transitions.generated.ts}

The staging helper explicitly protects this topology at
tests/packs/rendering/_helpers.py:21-25,35-48,57-82: the private destination
and scope parents are real directories, Composition is extracted privately,
and only peer leaves point read-only into G.

## Identity and readiness evidence

The target was checked before attachment: real graph root, real @banodoco scope
parent, real Composition package directory, no pre-existing destination or
foreign ancestor. The approved identities are:

- Runtime graph G: 4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c, 21455 entries.
- Composition 0.0.13 archive: SHA-256 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, 77 regular members, no archive links; installed package bytes matched all 77.
- Node: v20.19.4, SHA-256 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490.

The reusable static/in-process control is:

    /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-partial697-snapshot-dependency-diagnosis-0932-READINESS.py

It checks the exact symlink target and real scope parents, all 77 archive
bytes, Node identity, Composition registry discovery, and direct resolution of
package root/evaluation/registries/theme-api plus Remotion bundler, renderer,
media, layout-utils, esbuild, React, React DOM, and Remotion. It does not start
a host, browser, server, renderer, or capture.

Absent attachment control, run before creating the symlink:

    env -u ASTRID_REMOTION_PROJECT_DIR \
      ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
      PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=S /home/user/work/venv-agent/bin/python \
      -c 'from scripts import gen_effect_registry; gen_effect_registry._public_registry_ids()'

Result: exit 1 with the exact missing-manifest error above.

Qualified attachment control:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-partial697-snapshot-dependency-diagnosis-0932-READINESS.py \
      --root /home/user/work/wt/vw-m3-partial697-snapshot-dependency-diagnosis-0932 \
      --graph /home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
      --artifact /home/user/work/wt/vw-m3-partial697-snapshot-dependency-diagnosis-0932/remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz \
      --node /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node

Result: exit 0; registry IDs effects=1, animations=6, transitions=2; all direct
imports resolved inside G; archive 77/77 matched 9412; target realpath and
scope checks passed. The control syntax/JSON validation also passed via
python3 -B -c ast.parse(...) and python3 -m json.tool.

## Scope and limits

- No source test change was applied. The worker source has only the authorized
  untracked remotion/node_modules symlink; no shared graph file was written.
- No central request, browser, helper, Runtime, socket, render, full suite,
  install, copy, hardlink, or graph mutation was performed.
- The previous 0923 failure is preserved. The prior 32349 explicit physical
  result and private697/public799 statistics remain unqualified for this
  partial input and were not replayed or relabelled.
- Next step: manager review, then one normal test-service snapshot/run with this
  carrier and the existing unchanged command. A later physical pass would
  qualify only that requested partial case; it would not change retained
  assertions or previously unqualified statistics.

