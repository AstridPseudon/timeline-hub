# Agent published Main014/Main497 final review

## Decision: APPROVE

Reviewed the exact committed candidate, not `d7a`/`old6ef` or an uncommitted
worktree:

- candidate `tl/agt-m2-main014-published-landing-compose`:
  `68dc081cb563e99cf38d7926dd6f3ed840514682`, tree
  `c04a3d3a52af275988026959f370c53cb212f44d`;
  parents `d7a5e46362559d12e4a912fcc8656f2664624427` and
  `04fdd64205b4a2365e50455bd3ac81b027c617f3`;
- eventual current integration input:
  `8b9d5eea3aebfbd6b70b8b476b8d33792bfd1c58`, tree
  `e9025917838f313e7d81f0ece573bc2b11228f54`;
- current integration's only post-`04fdd` commit is
  `b5ab828ef`: deletion of `_clip_row` (20 lines) from
  `astrid/sdk/timeline_sheet.py`.

The candidate delta from `d7a5e4636` is the intended nine-path, `+524/-6`
AM-footage/Scene-summary unit. The candidate is Main497-descended (`497714c73531f164082555ec81b61ca5bc8b6554` is an ancestor). The current-parent merge resolution has only `artifacts.json` as a combined-diff path; the eight current source/test paths are byte-identical to `04fdd6420`.

## Pins and source preservation

- `runtime.lock.json` SHA-256:
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`.
- Runtime source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`; producer version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  Independent comparison against the immutable Runtime commit found all
  `15/15` locked consumer files byte-identical to both producer files and
  producer manifest entries.
- Agent ordinary schema hash:
  `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  shape is `55` definitions / `29` `EditCommand` branches.
- Composition 0.0.13 archive hash is
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with
  `77` archive entries.
- Target `artifacts.json` is self-consistent: all `157/157` target-tree
  entries hash to the committed manifest.
- No private15 or proposed-source marker/file was introduced. No new schema
  was added by the candidate delta.

The current `04fdd` AM-footage/helper, AM-footage/scene, pack registration,
catalog registration, Scene-check logic, and three Scene tests are exact in
the candidate. Existing live-scene path moves are content-preserving renames;
the generated artifact manifest follows the target paths. The worker's
affected-current matrix also covered Scene, CLI, cache, draft, safety, and
assertion neighbors.

## Dormant initializer caller audit

No production caller activates `timeline.init`. The only target-tree hits are:

- `astrid/sdk/timeline/commands.py:39,62` — dormant provider registration;
- `astrid/sdk/timeline/native_initialize.py:25-33` — capture/helper definition;
- `astrid/sdk/timeline/commit.py:921` — validation/guard inspection;
- `tests/editing_conformance/test_pristine_initialize.py` and schema/fixture
  declarations — test support only.

The simulated clean merge of `8b9d5eea` with `68dc081c` produced tree
`e9ec3166bd9071afbb4504ac7b036f2eb0dcffe4`; its `timeline_sheet.py` has no
`_clip_row`, so the current deletion survives the eventual adoption.

## Tests and evidence

Reused authorized exact-target evidence from the Main014 worker:

```text
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-main95bd/node_modules \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_scene_public_summary_rle.py \
  tests/sdk/test_scene_real_public_summary_rle.py \
  tests/sdk/test_scene_summary_projection.py \
  tests/core/timeline/test_scene_roles.py tests/core/timeline/test_onscreen.py \
  tests/core/timeline/test_onscreen_more.py \
  tests/packs/rendering/test_scene_only_executor.py \
  tests/packs/timeline/test_cli_native.py tests/packs/timeline/test_cli_commit_move.py \
  tests/sdk/test_timeline_reflow_golden.py tests/sdk/test_timeline_reflow_keep.py \
  tests/packs/rendering/test_effect_registry_target.py \
  tests/packs/test_composition_elements.py tests/timeline/test_effects_catalog.py \
  tests/core/gateway/test_doctor_bundle.py
110 passed in 41.96s
```

Also recorded from that exact target tree: CLI surface check passed, artifact
manifest check passed, `vendor_lock.py check ... --producer` passed, and
`git diff --check` passed. The real-scene test required the read-only pinned
Node 20/Remotion environment and then passed as part of the 110.

Independent checks in this review passed:

- exact Runtime lock/client/manifest byte comparison: `15/15`;
- target artifact manifest: `157/157`;
- ordinary schema shape and Composition archive checksum/count;
- Main497 ancestry and current-source blob identity;
- clean simulated eventual merge with the dead-row deletion retained.

No product files, pins, schema, generated files, or integration refs were
changed. No browser, render/export, live-socket, or full suite was run or
requested. App native-bootstrap qualification is intentionally outside this
approval, per the owner ruling; the publication/source adoption does not wait
for that gate.
