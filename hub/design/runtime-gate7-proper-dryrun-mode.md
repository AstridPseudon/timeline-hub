# Runtime Gate 7 proper dry-run mode

Date: 2026-10-21 UTC

## Result

Added the Runtime-owned `delivery-owner-extras-dryrun` suite entry in
`ORCH/tests/suites.conf`. The withdrawn historical
`delivery-owner-extras-actual` entry was left unchanged. The new entry uses
the reviewed carrier unchanged (`delivery-build` SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`), passes
`--dry-run`, and retains the existing scanner and owner-instructions extras.

The cheap preflight passed: `delivery-build --help` exposes `--dry-run`; both
extra sources are regular non-symlink files; their hashes are
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee` and
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`; all four
integration worktrees were clean; and no final ZIP existed before the run.

Exactly one central suite was requested:

`rt-m4-gate7-proper-dryrun-mode-0336-delivery-owner-extras-dryrun-1021033645-10810`

The service reported **PASS, exit 0, 73 seconds**. Its command was:

```text
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition" --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

## Source tuple and verification

The four current integration sources were unchanged during the run:

| repository | `tl/integration` commit | source tree | `origin/main` |
| --- | --- | --- | --- |
| Agent | `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e` | `075339b2c6d5e57c1b0e76754457d053b51edf2c` | `497714c73531f164082555ec81b61ca5bc8b6554` |
| Runtime | `30413e3c3e6db027f450e864ea9cb4a07446475b` | `2c5a5088c90cddfb38fba6dadcad899b28fb2c59` | `b535646faaad2f8ae7968dfe0f4fa3057f960264` |
| App | `3be3c116610c4ffdf019cba447464280fd7b8e06` | `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a` | `860d43b331fb4422b16bc0dbd7b08666a0c766a0` |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` |

Each repository passed the packer's fresh-main patch application, bundle
verification/fetch, and exact applied-tree/bundle-tree/source-tree equality:

```text
agent:       075339b2c6d5 / 075339b2c6d5 / 075339b2c6d5
runtime:     2c5a5088c90c / 2c5a5088c90c / 2c5a5088c90c
app:         d030e4b8b41a / d030e4b8b41a / d030e4b8b41a
composition: 20467712e66d / 20467712e66d / 20467712e66d
```

The immutable published014 producer was read-only at Runtime
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`; the documented `all76` artifacts
were not changed. This dry run does not requalify those producer artifacts.

## Retained checksum evidence

The existing dry-run mode retained staging at
`ORCH/delivery/build-20261021T033649Z`, containing 12 files and 22.2 MiB
uncompressed. Its `SHA256SUMS` retained exactly these entries:

```text
0a2ed18327721850772042fce60f2dfd9ab1feb91749eb2cd3638358e59d54fb  bundles/agent.bundle
0c802aa52684ca2395fc9a5f0e8e78ca36eb8ddfaee5540343a1f53be68977fd  bundles/runtime.bundle
204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee  extras/owner_film_cliplook_scan-v1.0.8.zip
3748fe26d8b875ce297c28797167768246a9af3ac8ae0f01ea93dd4cadbc0707  patches/agent/0001-Squash-tl-integration-of-agent-onto-origin-main.patch
75c0b5a8f5f941014dd5a1d6b400cca7fde35ec3d54b02ee06e18fe23eb7866e  patches/composition/0001-Squash-tl-integration-of-composition-onto-origin-mai.patch
779e7945d7dcf02903f1cab96293fe4fcea6bfb2c70621a856ca3718f329577f  bundles/composition.bundle
80ab42f9eb6d3d43d6e287c67094c1c655f1ef1b538e99f8c8e719befba8ac34  README.md
895026341b621cdca8d60394e9627e0fe49dab32b52ee51bd02c97da1d695ede  bundles/app.bundle
969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220  extras/owner-film-differences.md
a34533db73dfecd7f768c05a0ca15b0a23b6342366c0e6f4e4f402fedaa70b7b  patches/app/0001-Squash-tl-integration-of-app-onto-origin-main.patch
b5f313bbac2757cdc0434d482ea0770ef0e03bf27eefcc4eb65e31aefc3b686b  patches/runtime/0001-Squash-tl-integration-of-runtime-onto-origin-main.patch
```

The service log records the two extras, four bundles, four patches, README,
and checksum file. The extra destinations were accepted through the existing
traversal/collision/regular-file custody checks; the reviewed packer was not
edited or rehashed.

Storage available was 9,015,877,632 bytes before and 8,999,604,224 bytes
after the run. No final ZIP existed before or after it. The log explicitly
ends with `dry run: ZIP not written`.

## Scope and limits

This is private delivery preparation evidence only. It is not a final ZIP,
all-gates result, owner-film viewing, renderer/browser result, physical parity
result, macOS result, or claim that the README's incomplete gate inputs are
green. The prior non-dry-run owner-extras run remains historical and withdrawn;
it receives no pass credit from this record. No Runtime product code,
`bin/delivery-build`, producer, artifact, source ref, or shared dependency was
changed.
