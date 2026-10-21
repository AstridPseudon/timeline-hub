# Gate 7 current-descendants delivery rehearsal

Date: 2026-10-21 UTC

## Result

Exactly one current four-repository delivery rehearsal passed. This is a
dry-run staging proof, not a final ZIP or a Gate 7 completion claim.

The settled adoption decision treats Agent `091aa23e…` and App `3be3c116…`
as the published cohort. It does not require the canonical integration refs to
be rewound. The rehearsal therefore used the current clean integration
descendants that retain those pins. No ref, source checkout, delivery carrier,
or Runtime product source was changed.

## Inputs pinned before request

| repository | live `tl/integration` commit | live tree | adopted/published pin | relation |
| --- | --- | --- | --- | --- |
| Agent | `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e` | `075339b2c6d5e57c1b0e76754457d053b51edf2c` | `091aa23ec83ea05ffd3b0115a640230d51c8c429` / `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` | pin ancestor |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` | same commit/tree | exact |
| App | `1557c312b999ddc0a21c1728acbc64052ef6491f` | `cf94daef960fe1426f6f50e4000b00c0fc42867e` | `3be3c116610c4ffdf019cba447464280fd7b8e06` / `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a` | pin ancestor |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` | same commit/tree | exact |

All four integration worktrees were clean before the request. `merge-base
--is-ancestor` passed for both adopted pins. The exact live tuple was checked
again after the run and every commit/tree pair remained unchanged.

The immutable Runtime publication facts were also checked before the request:

- producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- artifact producer `astrid-runtime`, version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
- `contract/artifacts.json` manifest SHA-256
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.

These are retained publication/compatibility facts, not a new pin or release.

## Preflight and command

The existing `delivery-owner-extras-actual` suite was not used because its
command does not include `--dry-run`. The existing Runtime-owned
`delivery-owner-extras-dryrun` suite was used; it contains the exact reviewed
carrier, `--dry-run`, and both required extras.

Preflight passed:

- carrier SHA-256:
  `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`;
- scanner extra SHA-256:
  `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`;
- owner-instructions extra SHA-256:
  `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`;
- carrier and both extras were regular, non-symlink files;
- `delivery-build --help` exposed `--dry-run`;
- no final `timeline-delivery-*.zip` existed before the request;
- free space was 8.27 GiB, above the central named-run 5 GiB light-suite
  floor.

The one submitted command was:

```text
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition" --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

## Central result

Request: `runtime-delivery-owner-extras-dryrun-1021040405-30942`

Result: **PASS, exit 0, 97 seconds**. Staging was
`ORCH/delivery/build-20261021T040409Z`, with 12 files and 22.3 MiB
uncompressed. The carrier reported fresh-main patch application, bundle
verification, and applied-tree/bundle-tree/source-tree equality:

| repository | patch tree | bundle tree | applied tree | result |
| --- | --- | --- | --- | --- |
| Agent | `075339b2c6d5e` | `075339b2c6d5e` | `075339b2c6d5e` | PASS |
| Runtime | `6abc2f117391` | `6abc2f117391` | `6abc2f117391` | PASS |
| App | `cf94daef960f` | `cf94daef960f` | `cf94daef960f` | PASS |
| Composition | `20467712e66d` | `20467712e66d` | `20467712e66d` | PASS |

`sha256sum -c ORCH/delivery/build-20261021T040409Z/SHA256SUMS` passed for all
11 non-self members. The exact retained checksum entries were:

```text
1ce066fdc4f4f47c4aca0ca74672dbafd33c9d603b2bb16faa30cc1e18d1d66f  patches/agent/0001-Squash-tl-integration-of-agent-onto-origin-main.patch
204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee  extras/owner_film_cliplook_scan-v1.0.8.zip
7671a4641ee3bb489c00b0c86a54a8e8a3b7cb5733de10ce3c933488f17ccca0  bundles/app.bundle
779e7945d7dcf02903f1cab96293fe4fcea6bfb2c70621a856ca3718f329577f  bundles/composition.bundle
858cdb1912cd4f9d08db1392c4d3cc03b72093d26b4252f2d0aaddeb75691d0b  bundles/agent.bundle
95979e1051404545132d3cda3986d82021e3377acd82955695f6c21ef3aaade1  patches/composition/0001-Squash-tl-integration-of-composition-onto-origin-mai.patch
969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220  extras/owner-film-differences.md
b66c54883f5549c1edfa8b2e289091ca0c1a781e13121c54c52c7a9b70743aae  bundles/runtime.bundle
cb88f6f5d82f9e8adbdbb4d05aebd70b81b3eb1b94816ddf011d3e20949478bc  README.md
e7212613dc3ecbb1f8cdc0a9b8cf4e60ff2d06460cd25134dcad95e6ade703ee  patches/app/0001-Squash-tl-integration-of-app-onto-origin-main.patch
ec5ac754f3e9c9c0a2fa173d3664d4347fb030fe4d9c7a0d0ef222b2c937cbd5  patches/runtime/0001-Squash-tl-integration-of-runtime-onto-origin-main.patch
```

The builder ended with `dry run: ZIP not written`; no final ZIP existed after
the run. The generated README is truthful for this rehearsal: it says
`M4 gate results — current inputs (DRAFT / BLOCKED)`, keeps Gate 7 **OPEN**,
and explicitly makes no final ZIP, owner-film, macOS, physical-parity, or
all-gates-green claim. It also preserves the distinction between the Runtime
producer `95bd…`, compatible server `b92…`, and the current descendant source.

## Scope limits

This is the one current descendant dry-run evidence record. The prior proper
run `10810` remains historical evidence for its older tuple and is not
relabeled. The withdrawn non-dry-run `delivery-owner-extras-actual` result is
not reused. No full suite, Runtime product test, render, browser, install,
owner-film scan/viewing, macOS check, physical parity check, source/code/
packer change, pin rewrite, or final ZIP was performed or claimed.
