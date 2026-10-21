# Gate7 current rehearsal after owner storage release

Date: 2026-10-21 UTC

## Disposition

The complete current preflight passed and the one authorized named service
request was submitted. The service returned a cache hit for the unchanged
Runtime tree instead of executing a new four-repository build. Therefore this
task has no fresh current delivery proof. The cached PASS is preserved as
historical and is not relabelled as the current tuple.

The worker is **BLOCKED on central test-service cache behavior** after exactly
one request. No second request, source mutation, cleanup, or ZIP was made.

## Storage floor

The mandatory floor is `10,737,418,240` bytes. The final preflight measured
`10,905,231,360` bytes free; the immediate pre-submit check measured
`10,905,104,384` bytes free, a margin of `167,686,144` bytes. Both passed.

## Current preflight tuple

All four integration worktrees were clean, each current ref was descended from
its `origin/main`, and `git rev-list --objects --missing=print` found no
missing objects:

| repository | current commit | current tree | `origin/main` | required adoption ancestry |
| --- | --- | --- | --- | --- |
| Agent | `b79fec587dc7bab3fcb0624785d38faa519b3c93` | `02c9f56468f676bbc53a548c9295cf5e3a31ea89` | `497714c73531f164082555ec81b61ca5bc8b6554` | `091aa23e…` ancestor: PASS |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d` | `6abc2f117391de8e7e35c0283f575a002199894d` | `b535646faaad2f8ae7968dfe0f4fa3057f960264` | base Runtime ref: PASS |
| App | `42b0c6c8434e2c491f8dbdf00a210ed755e41a95` | `fa887b5689d7ad44957021080f74d13a9d0c4e30` | `860d43b331fb4422b16bc0dbd7b08666a0c766a0` | `3be3c116…` ancestor: PASS |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | Composition13: PASS |

The Runtime public producer `95bd3c5f…` is an ancestor of current Runtime;
private016 Runtime `da77e2dd…` and Agent `10226a7f…` are not ancestors. Runtime
`contract/artifacts.json` has exactly 76 entries: every current blob is
byte-equal to producer95 and matches its manifest, with manifest digest
`a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.
The public014 tuple checks passed: Runtime/Agent edit-command schema
`6ba7b51e…`, Runtime schema digest
`sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
client version `0.2.14`, contract manifest
`75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14`,
component manifest `1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`,
and Agent lock source producer95/version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

The reviewed executable builder matched SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`. The
scanner and owner-instructions inputs were regular non-symlink files with
SHA-256 `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
and `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
README and gate-results inputs existed; gate-results remained DRAFT/BLOCKED
with OPEN statuses and no final ZIP existed. The suite line had the reviewed
builder guard, `--dry-run`, both exact `--extra` arguments, and the existing
request/wait/output/owned-temp paths. No source, release, or private016
artifact was mixed in.

## One requested service run

Request command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime delivery-owner-extras-dryrun
```

| field | value |
| --- | --- |
| requested run ID | `runtime-delivery-owner-extras-dryrun-1021070626-26457` |
| request time | `2026-10-21T07:06:26Z` |
| status / exit | `pass` / `0`, cache resolution at `2026-10-21T07:06:29Z` |
| service disposition | `CACHE HIT ... not re-run` |
| cached source run | `runtime-delivery-owner-extras-dryrun-1021040405-30942`, requested `2026-10-21T04:04:05Z`, PASS/exit 0, 97 seconds, completed `2026-10-21T04:05:46Z` |

The cached command captured the exact ext tuple:

```text
extras/owner_film_cliplook_scan-v1.0.8.zip
  -> handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip
  sha256=204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee
extras/owner-film-differences.md
  -> handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md
  sha256=969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220
```

The retained cached stage is
`ORCH/delivery/build-20261021T040409Z`. It contains 12 members: README,
four bundles, four patches, two extras, and `SHA256SUMS`; the checksum file
contains 11 non-self entries. The cached builder reported fresh-main patch
application, bundle verification/fetch, and full tree equality for all four
cached sources:

```text
agent       075339b2c6d5 / 075339b2c6d5 / 075339b2c6d5 PASS
runtime     6abc2f117391 / 6abc2f117391 / 6abc2f117391 PASS
app         cf94daef960f / cf94daef960f / cf94daef960f PASS
composition 20467712e66d / 20467712e66d / 20467712e66d PASS
```

Those are cached historical results (Agent `7ab6cbae…`, Runtime `b92d3e7a…`,
App `1557c312…`, Composition `7bb54bb…`), not the current preflight sources
above. The cached log ends `dry run: ZIP not written`; no final ZIP was
created. No current Agent/App patch application, bundle check, checksum
generation, or fresh tree equality was executed.

## Not run and next step

No new delivery builder process, final ZIP, renderer/browser/install/full
suite, owner-film scan/viewing, macOS check, physical parity check, or source
cleanup was run. Product files, integration refs, shared dependencies, and
the reviewed builder/suite were not modified.

The next step requires central test-service cache invalidation or an explicit
cache-bypass mechanism keyed to all four source trees, followed by one newly
authorized current dry-run. Do not count or relabel the cached PASS as current
Gate7 evidence.
