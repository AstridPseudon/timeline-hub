# Runtime Gate7 corrected cross-product cache dry-run

Date: 2026-10-21 UTC

## Result

The one authorized current delivery dry-run passed as a fresh central-service
execution. The integration-scoped suite name keyed the external Agent, App,
and Composition refs; the service did not return a historical cache result.
This is delivery evidence only. Gate7 remains subject to the open limits in
the gate-results input, and no final ZIP or adoption is claimed.

## Withdrawal and authorization

The predecessor request `runtime-delivery-owner-extras-dryrun-1021070626-26457`
was terminally withdrawn at `2026-10-21T07:08:14Z`; its `WITHDRAWN` record says
the cache hit used older Agent/App sources. Historical run
`runtime-delivery-owner-extras-dryrun-1021040405-30942` remains scoped only to
its original Agent `7ab6cbae`, Runtime `b92d3e7a`, App `1557c312`, and
Composition `7bb54bbd` tuple. No old proof was replayed.

The corrected suite was already present in `tests/suites.conf`:
`runtime delivery-owner-extras-integration-dryrun`. Its command is identical
to `delivery-owner-extras-dryrun` except for the suite name. The reviewed
builder remains unmodified.

## Complete preflight

All checks below passed before the request.

| Check | Evidence |
|---|---|
| Storage | `df -PB1 /home/user/work`: `10,893,426,688` bytes free before request; floor `10,737,418,240` bytes. |
| Agent | `b79fec587dc7bab3fcb0624785d38faa519b3c93`, tree `02c9f56468f676bbc53a548c9295cf5e3a31ea89`; clean; descends `origin/main` `497714c73531f164082555ec81b61ca5bc8b6554`; adopted `091aa23e…` is an ancestor; no missing objects. |
| Runtime | `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`; clean; descends `origin/main` `b535646faaad2f8ae7968dfe0f4fa3057f960264`; no missing objects. |
| App | `42b0c6c8434e2c491f8dbdf00a210ed755e41a95`, tree `fa887b5689d7ad44957021080f74d13a9d0c4e30`; clean; descends `origin/main` `860d43b331fb4422b16bc0dbd7b08666a0c766a0`; adopted `3be3c116…` is an ancestor; no missing objects. |
| Composition | `7bb54bbd64107e5090643ecca1e4d33164173e85`, tree `20467712e66dbadff4d562c0d5baae22b8c077a7`; clean; descends `origin/main` `67b8aa3d0d6831d3e3504a340ff583c3da253707`; no missing objects. |
| Published Runtime cohort | Producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` is an ancestor; `contract/artifacts.json` has exactly 76 entries, zero missing/mismatched blobs, and zero byte differences from producer95; manifest SHA-256 `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`. |
| Ordinary schema | Runtime and Agent edit-command schemas both SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`. |
| C13 | Retained `agent-remotion-0013` project, its `node_modules`, and pinned Node20 executable exist. No C13 execution was attempted or claimed. |
| Reviewed builder | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`, SHA-256 `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`; executable and `--help` checks passed. |
| Inputs and honesty | Scanner extra is regular/non-symlink, SHA-256 `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`; owner instructions are regular/non-symlink, SHA-256 `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`. README and gate-results inputs exist; gate-results remains DRAFT/BLOCKED/OPEN and no final ZIP exists. |

The exact suite argv was checked against the old named suite: after replacing
the suite token, the lines compare equal. It retains `GIT_CONFIG_GLOBAL=/dev/null`,
`PYTHONDONTWRITEBYTECODE=1`, the reviewed builder guard, `--dry-run`, all four
repos, both exact `--extra` destinations/sources, and the existing service
request/result, output, and builder-owned temporary paths. No product source,
shared dependency, private016 artifact, builder, existing suite, or test tool
was modified.

## One service request

Request command:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime delivery-owner-extras-integration-dryrun
```

| Field | Value |
|---|---|
| Request ID | `runtime-delivery-owner-extras-integration-dryrun-1021070937-11141` |
| Request time | `2026-10-21T07:09:37Z` |
| Result | `pass`, exit `0`, 84 seconds; terminal `2026-10-21T07:11:11Z` |
| Cache marker | No `cached_from` file; service log contains actual per-repo builder results and staging. |
| Captured external refs | Agent `b79fec587dc7bab3fcb0624785d38faa519b3c93`; App `42b0c6c8434e2c491f8dbdf00a210ed755e41a95`; Composition `7bb54bbd64107e5090643ecca1e4d33164173e85`. Runtime is the requested target `b92d3e7a05eec65c142294ef4873edd059e9b31d`. |

Captured command:

```text
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition" --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

## Fresh builder evidence

The service log records actual fresh-main patch application, bundle
verification/fetch, and complete tree equality for every current source:

| Repo | Patch / bundle / source tree | Result |
|---|---|---|
| Agent | `02c9f56468f6` / `02c9f56468f6` / `02c9f56468f6` | PASS, 19s |
| Runtime | `6abc2f117391` / `6abc2f117391` / `6abc2f117391` | PASS, 3s |
| App | `fa887b5689d7` / `fa887b5689d7` / `fa887b5689d7` | PASS, 61s |
| Composition | `20467712e66d` / `20467712e66d` / `20467712e66d` | PASS, 1s |

The retained stage is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/build-20261021T070948Z`.
It contains 12 files: README, four bundles, four patches, two extras, and
`SHA256SUMS`; the checksum file contains 11 non-self entries and
`sha256sum -c SHA256SUMS` passed. The extras are present at the exact reviewed
destinations and retain hashes `204a7aac…c93ee` and `969fe303…da220`.
The builder ended `dry run: ZIP not written`; no final ZIP or adoption was
performed.

## Not run

No Runtime full/pytest suite, browser, renderer, install, generation, C13
execution, owner-film scan/viewing, macOS check, physical parity check, final
ZIP creation, source refresh, adoption, or old proof replay was run. No
additional service request or workaround was made.
