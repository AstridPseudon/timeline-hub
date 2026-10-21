# Timeline delivery, {{UTC}}

This ZIP packages the integration branch `tl/integration` of each Timeline repository (agent, runtime, app, composition). Each repository ships two ways: a git bundle of its integration history, and one linearized binary-capable patch series on the pinned `origin/main` shown below. Both are meant to apply to a fresh checkout containing that exact pinned commit. Nothing here has been pushed. This document is not evidence that a remote `main` is fresh; an owner-controlled refresh and rerun is required before release.

The patch series is based on the pinned `origin/main` commit and has the `tl/integration` tree. Its commit message lists the merged commits, one per line. Per-commit history is only in the bundle.

The patch route is intentionally linearized: `git am` creates a new synthetic
commit, so its commit ID is not the source integration commit and must not be
reported as one. The tree ID is the delivery identity. For published014, this
also means that the Runtime patch commit is not the immutable published
producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; compare the resulting tree
and the published artifact bytes instead.

At build time the patch series was applied with `git am` to a fresh repository holding only the pinned `origin/main`, and the resulting tree was compared with the immutable `tl/integration` tree. Every bundle was checked with `git bundle verify`, fetched, and compared to that same tree. The results are in the per-repository sections below; a later refresh must repeat these checks.

## Contents

- `README.md`: this file.
- `bundles/<repo>.bundle`: git bundles of `tl/integration`. A *ranged* bundle holds only the commits after `origin/main` and needs `origin/main` present. A *full* bundle holds all history and clones on its own.
- `patches/<repo>/*.patch`: the binary-capable linearized patch series from the pinned `origin/main` tree to `tl/integration`.
- `SHA256SUMS`: checksums of every other file in this ZIP.

## Summary

{{REPO_SUMMARY}}

Line counts come from `git diff --numstat --no-renames origin/main tl/integration`. A file counts as a test when a path segment is `tests`, `test`, `__tests__`, `e2e` or `spec`, or its name is `test_*`, `*_test.py`, `*.test.*` or `*.spec.*`. Everything else counts as non-test/product for this diff summary, including generated data and unrelated infrastructure. These are not the authored Timeline-core census; the area census documents use the narrower PLAN boundary.

## Applying

Start from a fresh clone or checkout whose local `origin/main` is exactly the commit listed in that repository’s section. Do not substitute a newer remote commit in this draft. Verify the pin before applying:

```sh
test "$(git rev-parse origin/main)" = "<pinned origin/main from this README>"
```

The per-repository sections are authoritative for the build that produced this
README: they supply the pinned IDs, whether the bundle is ranged or full, the
patch count, and the expected integration tree. The angle-bracket values above
and in the commands below are intentionally filled by `delivery-build`; do not
replace them with values from another build.

Use exactly one of these two equivalent routes for each repository:

- **Patches:** `git switch -c tl/integration origin/main`, then `git am /path/to/patches/<repo>/*.patch`. Verify that `git rev-parse HEAD^{tree}` equals the `tl/integration` tree listed in the repository section. The result has the same tree as `tl/integration`, but linearized history.
- **Bundle:** for a ranged bundle, run `git bundle verify /path/to/bundles/<repo>.bundle`, then `git fetch /path/to/bundles/<repo>.bundle tl/integration` and `git switch -c tl/integration FETCH_HEAD`; verify the fetched commit/tree against the section. For a full bundle, run `git bundle verify /path/to/bundles/<repo>.bundle` and `git clone -b tl/integration /path/to/bundles/<repo>.bundle <dir>`.

Replace `/path/to/` with the folder this ZIP was unpacked into.

Do not combine the routes on one checkout or force either route onto a newer
base. If a pin, bundle verification, patch application, commit, or tree check
fails, stop and retain the failure for the next source refresh.

### Published014 Runtime and consumer source authority

For the published014 tuple, keep these identities distinct:

- immutable Runtime producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, contract/client `0.2.14`,
  and the published `all76` artifact set;
- compatible Runtime server source: `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
  tree `6abc2f117391de8e7e35c0283f575a002199894d`, a descendant of the
  producer and not a new publication;
- normal consumers: Agent `091aa23ec83ea05ffd3b0115a640230d51c8c429`, App
  `3be3c116610c4ffdf019cba447464280fd7b8e06`, and Composition13
  `7bb54bbd64107e5090643ecca1e4d33164173e85`.

### Current bounded evidence inputs

The current Runtime server is `b92d3e7a` / tree `6abc2f1`. Its full run
`runtime-full-retained-owned-temp-integration-1021035028-28646` passed with
`6002 passed, 26 skipped, 15 xfailed`; the current TypeScript run
`rt-m2-gate4-main014-ts-evidence-0407-ts-client-check-1021040813-12394`
passed all 61 tests. The installed launcher proof
`rt-m2-wc10-sdk-envelope-fixture-one-proof-0322-wc10-installed-launcher-integration-1021032335-4406`
passed one test. Exact commands and limits are recorded in the Runtime design
reports named in `gate-results.md`.

App native initializer activation `1557` / `real7782` and current mixed
neighbor `4657` are bounded successful evidence; the whole mixed run was
withdrawn. They do not prove all-writer retirement, physical parity, or the
complete consumer journey. Private016/da77 is superseded immutable evidence and
was never adopted. Private017 is the sole open private line: Runtime candidate
`42a7203f49bb89f299ec854cfbf2b1444e815a7c` / tree
`1f220b3d3a27e8eb061b15c944bad784c8fdb82e`, package `0.2.17`, is approved for
exact artifact identity only. Agent reciprocal approval, normal private pin,
native execution, RT03 proof, and HTTP qualification remain pending. It is not
published, pinned, adopted, merged, or activated; no private017 actual HTTP
proof is claimed. Private015 / C3d / 3e6c and older 392 / 952 are superseded
immutable historical evidence and were never adopted. The current Agent full
failure remains visible with its exact source scope in `gate-results.md`.

The historical rehearsal
`runtime-delivery-owner-extras-dryrun-1021040405-30942` remains scoped only to
its old Agent `7ab6cbae`, Runtime `b92d3e7a`, App `1557c312`, and Composition
`7bb54bbd`; it is not current-tuple evidence. Its successor request
`runtime-delivery-owner-extras-dryrun-1021070626-26457` was withdrawn after a
wrong-tuple cache hit and is no pass. The authorized current rehearsal
`runtime-delivery-owner-extras-integration-dryrun-1021070937-11141` passed
freshly in 84 seconds with exit 0 on exact Agent
`b79fec587dc7bab3fcb0624785d38faa519b3c93`, Runtime
`b92d3e7a05eec65c142294ef4873edd059e9b31d`, App
`42b0c6c8434e2c491f8dbdf00a210ed755e41a95`, and Composition
`7bb54bbd64107e5090643ecca1e4d33164173e85`. Fresh-main patch, bundle, and
source tree equality passed for all four repositories: Agent tree
`02c9f56468f676bbc53a548c9295cf5e3a31ea89`, Runtime tree
`6abc2f117391de8e7e35c0283f575a002199894d`, App tree
`fa887b5689d7ad44957021080f74d13a9d0c4e30`, and Composition tree
`20467712e66dbadff4d562c0d5baae22b8c077a7`. It used the added
integration-scoped suite with the reviewed builder and both extras unchanged;
the scanner ZIP hash is `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
and owner-instructions hash is
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
This is rehearsal evidence only: no macOS check, owner-film viewing, physical
parity check, final ZIP, or all-gates result has been run.

The Runtime bundle is the source-history carrier. If it contains the
published producer, verify that object without changing the checked-out patch
branch:

```sh
git bundle verify bundles/runtime.bundle
git fetch bundles/runtime.bundle \
  refs/heads/tl/integration:refs/delivery/runtime-history
git cat-file -e 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c^{commit}
git merge-base --is-ancestor \
  95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c refs/delivery/runtime-history
```

The existing producer-checkout route is equally valid: run the normal
consumer byte check against a clean checkout of `95bd…` (for example the
provided `rt-pin-95bd3c5f` checkout), using the repository's existing
`vendor_lock.py check` or `vendor-lock.mjs check` command. Do not rewrite
`runtime.lock.json`, copy generated files by hand, or use the synthetic patch
commit as the producer identity. A compatible `b92…` server may execute the
same bytes, but it does not change the lock's source authority.

### Runtime launch paths

The tested normal product path uses one private, non-editable environment
containing the Runtime package, generated Runtime client `0.2.14`, and the
matching Agent package. Its existing profile command is:

```sh
astrid-runtime up --profile astrid --data-root <support-root> --json
```

The installed carrier and its package/source identities must be checked before
launch; the current installed proof `...-4406` is launcher evidence only and
does not close the cross-product journey or delivery gates. Keep this path
separate from the generic neutral Runtime path, which intentionally has no
Agent provider:

```sh
python -m runtime_protocol doctor --root .runtime --json
python -m runtime_protocol create --root .runtime
python -m runtime_protocol start --root .runtime
```

Neutral startup must remain neutral and must not be made to fall back to the
Agent provider. Neither path changes registry publication, authentication,
vendor locks, or the selected source tuple.

Runtime historical-fixture prerequisite: before applying the linearized Runtime patch,
import the supplied Runtime bundle into a side ref so the accepted-replay fixture's
pre-retirement commit remains available. This does not change the final patch branch:

```sh
git bundle verify bundles/runtime.bundle
git fetch bundles/runtime.bundle \
  refs/heads/tl/integration:refs/delivery/runtime-history
git cat-file -e a020a1c77a07aa657efb60b0442450209e55e470^{commit}
git merge-base --is-ancestor a020a1c77a07aa657efb60b0442450209e55e470 \
  refs/delivery/runtime-history
git switch -c tl/integration origin/main
git am patches/runtime/*.patch
```

The `refs/delivery/runtime-history` side ref is intentional: it preserves the original
Runtime history for upgrade/replay fixtures while the patch route still leaves the
linearized `tl/integration` tree as the checked-out branch. Keep the bundle and patch
forms together; the patch alone does not carry historical commit objects.

## Per repository

{{REPO_SECTIONS}}

## Gate results

{{GATE_RESULTS}}
