# Agent AM-sprite current port

Status: ready for one PR/source-unit review and merge.

## Provenance and boundary

- Current base: 8e3107853d17453758a933d1f47215cc1c002660
- Approved original donor: 9d93e66e4e031b98fc042235334d1a4723006ebb
- Donor product parent: bdd02bd3f753e24092b982772bd481afc84f49da
- Ported the approved AM-sprite unit onto current content; did not merge or
  overwrite stale donor ancestry.
- AM-snap-plate 48f3eef4b was not ported; it remains a separate later unit.

Exact source delta:

- astrid/packs/astrid_motion/rendering/elements/effects/am-sprite/component.tsx
  — capability preparation registered on the real component; spriteAt is
  shared by draw and capability evaluation.
- tests/packs/rendering/test_sprite_scene_capability.py — 283-line direct
  capability/SSR regression lane.
- astrid/packs/rendering/elements/catalog.ts — normal generator revision only:
  f88ce18c... to da9e894e....

The component and direct test are byte-identical to the approved donor:

| Path | SHA-256 |
|---|---|
| sprite component | fc79cee164d9d7aeb2a008d9d924e7b41710856b0b630bbc91137ff504b5172e |
| direct sprite test | b150fab9792d35429128994a38a1ef2f11c22b8e51473955eaa730d505764cfa |
| generated catalog | 542ea5db49f7b88c931bd476aa509a7f531dc16c4b67b1102e1330e8d28a94b2 |

There is no AM-sprite scene.ts in the approved unit. No plate files, presenter
or theme/public12 files, pin/Root/source/save-core files, artifact package, or
handwritten digest were changed.

The implementation keeps declared frame geometry and actual draw geometry
consistent. Known bounds require a resolved source and declared dimensions;
alpha/decoding/opaque coverage, hidden frames, missing or raw-invalid
dimensions, and decorated bounds remain unknown/absent honestly. Unsupported
outer crop/entrance/exit geometry remains public UNKNOWN. No private crop or
statistics path and no D09 claim was added.

## Protected current bytes

These current-base files were checked after the port and retain the approved
current SHA-256 values:

| Path | SHA-256 |
|---|---|
| astrid/core/rendering/verified_source.py | c0dcabd27230f9661be59b2461c9759716daad215e1b508c8f9e73bb96e326d8 |
| tests/packs/rendering/test_verified_source.py | aa087e5840fbe84606ef8cdf85f971e5d9a17c8038c6cad23bd8513b6467b9c5 |
| tests/fixtures/current-union-command-schemas/published-sources.json | 1deac01582348b27a90455c27010622280178919ee2c3daed1e0c025b571dda6 |
| astrid/sdk/remote.py | 6d5c36420eeadc14e69f6414c843d8b5a17c5b893224b9ef364322907a2b175a |
| astrid/sdk/timeline/commit.py | 524619491e5880b493f89175301098daa66cc37244e64572f8f00a93f0e3124e |
| runtime.lock.json | c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311 |
| docs/design/visual-compile-contract.md | 94581609e327918152ee6779e8fb3915391c091167eba875ecbe38a4200cbf4 |

## Evidence

All commands used the shared Remotion-0012 dependency tree read-only, the pinned
Node 20.19.4 executable, private pytest basetemp directories, and disabled
pytest/Vitest-style caches.

- PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/gen_element_catalog.py astrid/packs/rendering/elements/catalog.ts — pass; only the AM-sprite revision changed.
- PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/gen_element_catalog.py --check — pass.
- Direct changed lane: tests/packs/rendering/test_sprite_scene_capability.py — 17 passed in 55.39s.
- Approved neighbor replay: tests/packs/rendering/test_sprite_scene_capability.py tests/packs/rendering/test_scene_host.py tests/sdk/test_timeline_checkout.py::test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address — 33 passed in 86.57s.
- tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current — 1 passed in 5.66s.
- python -m ruff check --no-cache tests/packs/rendering/test_sprite_scene_capability.py — pass.
- git diff --check — pass.

No full suite, render/export, browser journey, live socket, physical
pixel/audio parity, Runtime admission, or artifact repack was run or claimed.

Artifact-manifest refresh was not needed for this source/catalog unit. An
initial scripts/artifact_manifest.py --help probe wrote a repository-wide
artifacts.json; that unrelated change was restored and is absent from the
final worktree.
