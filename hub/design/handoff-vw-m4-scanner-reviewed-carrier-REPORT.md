# vw-m4-delivery-owner-film-scanner-carrier-note

## Result

Prepared `README-PAYLOAD.md` and `COMMAND` for the Runtime owner. No product
repository or shared delivery input was modified. The handoff reuses the
approved scanner 1.0.8, the reviewed carrier, and the current Composition e7
delivery evidence.

Changed worker-output paths: `README-PAYLOAD.md`, `COMMAND`, `REPORT.md`,
`commit-msg`, and `DONE`.

## Verified inputs

- Composition source: `e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332`, tree
  `408633d6b73dde63f683eaf9d13a132bb34a3bd7`.
- Composition `origin/main`: `67b8aa3d0d6831d3e3504a340ff583c3da253707`, tree
  `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`.
- Carrier `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`:
  SHA-256 `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.
- Scanner ZIP: 12,221 bytes, SHA-256
  `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`;
  members exactly `README.md` and `owner_film_cliplook_scan.py`.
- Owner instructions: 10,519 bytes, SHA-256
  `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
- Existing e7 patch: 467,845 bytes, SHA-256
  `12f8361a3f4d6f1c1edcf684600bc5e0fcf2276f5136a27c4b93d0095c71a440`.
- Existing e7 bundle: 221,307 bytes, SHA-256
  `46de26e1082485028a915d8693ec0484326e78c13a67c6d1ee03fb22702b8af3`.
- Existing e7 proof: exact 113/113 fresh-main equality, bundle and diff checks,
  and central Composition `npm test` 78 passed / 0 failed / 0 skipped.

## Commands and results

- Read-only `sha256sum` checks for the carrier, scanner, owner instructions,
  e7 patch, and e7 bundle: PASS; exact values are recorded above.
- Read-only `unzip -Z1` scanner member check: PASS; two expected members.
- Read-only manifest parse: PASS; e7 source/main identities, sizes, hashes,
  and bundle prerequisite/head agree with the handoff.
- Read-only Composition ref check: PASS; `/home/user/work/composition`
  `tl/integration` is e7 and `origin/main` is 67b8.
- Worktree check: clean on `tl/vw-m4-delivery-owner-film-scanner-carrier-note`.

## Decision and blocker

The one documented builder invocation uses the reviewed `--extra` carrier,
all four repos, the exact scanner and instructions, and the existing e7
patch/bundle/manifest/report as traceability extras. This is the smallest
honest handoff that preserves the approved inputs without rebuilding them.

The builder currently has no `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/`
directory, so its required `README.template.md` is absent. The gate-results
input is absent as well. Runtime must supply/refresh those owner-controlled
inputs before executing `COMMAND`; they were not fabricated here.

## Not run / not claimed

No scanner test replay, owner-film scan, final four-repo ZIP build, macOS run,
browser/render run, or full suite was run. No owner-film result, clean claim,
or final M4/Gate 7 completion claim follows from this handoff.
