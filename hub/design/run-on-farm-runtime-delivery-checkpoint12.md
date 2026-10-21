Status: READY

# Runtime Gate 7 checkpoint 12:00 delivery rehearsal — farm request

Run exactly one current-tuple delivery dry-run on the test farm, after the farm
lead completes the preflight below. This is the changed-tree 12:00 checkpoint
rehearsal only. It is not final delivery, a final ZIP, or all-gates evidence.

## Source tuple

The four hub branch names and read-only source checkouts are:

| repository | hub branch name (remote-tracking ref) | checkout | commit | tree | origin/main | route |
| --- | --- | --- | --- | --- | --- | --- |
| Agent | `timeline/agent/tl/integration` (`hub/timeline/agent/tl/integration`) | `/home/user/work/agent` | `c9ac7c7b0e862ad32a919db33859c5fcbf58ad99` | `cab0a2aa34ba6dae880657eb484979039e206049` | `d4590b5f10699103f4ee6e6ff224727d698d8f59` | full bundle |
| Runtime | `timeline/runtime/tl/integration` (`hub/timeline/runtime/tl/integration`) | `/home/user/work/runtime` | `cc7410a1fa9bd5acc703abfd1b8fde0cf3d00365` | `1c8473c9e73fde02f9943b975eac171ac2757069` | `b535646faaad2f8ae7968dfe0f4fa3057f960264` | ranged |
| App | `timeline/app/tl/integration` (`hub/timeline/app/tl/integration`) | `/home/user/work/app` | `a8a3f23313e92c523359b3b37c3a63bd526dbb5e` | `79f5c76b96d4be75959d67a57197dee5f9546225` | `895e298cd06cc0392fec79be79fed763b39fb711` | full bundle |
| Composition | `timeline/composition/tl/integration` (`hub/timeline/composition/tl/integration`) | `/home/user/work/composition` | `df7b86308902fae90eda1dc3080d17d8fc30ea78` | `71d8e95edb1bb2d187c3193ef3462d4cfde277fa` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | ranged |

Agent, Runtime, and Composition match the completed blocked preflight. App
advanced before this packet from `5f513665a6961e3552cf47bf70303fe41f370ba3`
/ `1c28244f9de4399070bc31772aef2d1a6cfca128`; its new identity above was
rechecked at packet preparation. All four checkouts are clean and
object-complete. Do not substitute a private candidate, unpublished017/018,
or another source ref.

The consumer pin remains unchanged: Agent and App `runtime.lock.json` select
Runtime producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` and producer
artifact `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
Runtime `contract/artifacts.json` must still contain 76 entries with manifest
SHA-256 `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`.

## Exact existing delivery command

Use the existing `runtime delivery-owner-extras-dryrun` suite command exactly
as recorded in `ORCH/tests/suites.conf`; do not rewrite it, add retries, or
run the withdrawn actual-delivery entry:

```sh
env GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition" --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

The reviewed builder is the regular executable
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`,
SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.
The farm must expose that shared path read-only. If the farm cannot mount
`ORCH/bin`, that is a concrete missing prerequisite; do not invent or modify a
replacement carrier.

## Required shared inputs

The farm lead must verify these are regular, non-symlink files at the listed
shared paths before the one run:

- README input: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/README.template.md`, SHA-256 `79ec78539bf67ef03045a9fe9d6a11f85a36d8b056471c8ecb188a71189515c9`.
- Gate input: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/gate-results.md`, SHA-256 `23d3a529d8d210418553815d45a3b924d2ddb699d319cac415f48746ecebb852`. It is `DRAFT / BLOCKED`; Gate 7 is `OPEN`.
- Scanner extra source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip`, SHA-256 `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`; destination is `extras/owner_film_cliplook_scan-v1.0.8.zip`.
- Owner-instructions extra source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md`, SHA-256 `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`; destination is `extras/owner-film-differences.md`.

The delivery directory must contain no pre-existing final
`timeline-delivery-*.zip`. The farm must keep source checkouts and shared
dependencies read-only and run with its existing fixed 10 GiB disk-floor
policy. The local machine failed that floor at 7,889,068,032 bytes available
(shortfall 2,848,350,208 bytes); do not lower the floor or clean another
area's data.

## Farm preflight and result

Before execution, verify in one preflight that all four commit/tree pairs,
clean statuses, object completeness, origin/main refs, Runtime/App public014
pin and 76-entry artifact metadata, builder hash, both extra hashes, README,
gate input, tool paths, and the no-final-ZIP condition match this packet. A
farm-local fixed allowance must pass. Stop without executing if any check
fails, and report every failed prerequisite.

Run once only after that preflight. Preserve the dry-run's normal staging and
checksum log; it must not write a final ZIP. Return the farm result and its
full log to the orchestrator, including the captured four-repository tuple,
patch/bundle/applied-tree comparisons, staged extra identities, checksum
count, exit status, and duration. This packet claims no full suite, browser,
renderer, installed-launcher, owner-film, macOS, physical-parity, source/pin/
version, external-fetch, or final-ZIP evidence.
