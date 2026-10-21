# Gate7 current four-repo integration dry run

Date: 2026-10-21

## Disposition

The single central `delivery-dryrun` run completed with exit 0 and passed
linearized patch and bundle tree equality for all four current integration
refs. It is **not accepted as the requested Gate7 dry run**, because the
central runner captured the request before the two required `--extra` carrier
arguments were added. The recorded command and staging contain no extras.
No automatic retry was made.

## Source tuple

The packer read these unchanged integration refs:

| repo | `tl/integration` commit | tree |
|---|---|---|
| Agent | `57d6635616f2982b814cfcc059b670ea1a7c9f2c` | `0174fd49bd175a726a44542d1d6e31bca13c0f02` |
| Runtime | `9d1c43c647301da48a6e86ad82e466b501bd2418` | `50e74e3243c5da4cf77b6e6cc76605fae8aeb649` |
| App | `780c502368cb6eb379cf3848af7009067c7cd744` | `8eed52bb7f8555c7765a8b485e00920bbf906639` |
| Composition | `e7ef7a0729a2d7dad3c0ae60da9e6bb8f844d332` | `408633d6b73dde63f683eaf9d13a132bb34a3bd7` |

Installed carrier: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build`, SHA-256
`3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`.

The required frozen payloads were present and independently re-hashed:

- scanner ZIP: `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
- owner instructions: `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`

## Storage and command

Before queueing, free space was 10,620,284 KiB (10.13 GiB), meeting the real
10 GiB safety floor. The exact intended command was:

```bash
GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1 \
TIMELINE_DELIVERY_SCRIPT_SHA=3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990 \
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build \
  --dry-run --repos "agent runtime app composition" \
  --extra "extras/owner_film_cliplook_scan-v1.0.8.zip=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip" \
  --extra "extras/owner-film-differences.md=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md"
```

The central request was `runtime-delivery-dryrun-1021004301-18070`. Its
recorded command was missing both extras, and its staging directory had 10
files (README, checksums, four bundles, four patches), rather than the 12
files required with the carrier. This is a test-service request-capture race,
not a packer/source-repository failure.

## Actual result

Central service result: **PASS, exit 0, 99 seconds**.

| repo | patch/bundle/applied tree result |
|---|---|
| Agent | `0174fd49bd17 / 0174fd49bd17 / 0174fd49bd17` PASS |
| Runtime | `50e74e3243c5 / 50e74e3243c5 / 50e74e3243c5` PASS |
| App | `8eed52bb7f85 / 8eed52bb7f85 / 8eed52bb7f85` PASS |
| Composition | `408633d6b73d / 408633d6b73d / 408633d6b73d` PASS |

Staging was `build-20261021T004311Z`, 334.0 MiB uncompressed; no ZIP was
written. The App shallow source was handled through the installed private
source view. Source refs remained unchanged after the run.

## Limits

This proves only the four-repo patch/bundle source-tree equality for the
current tuple. It does not prove extra-carrier staging, a final delivery ZIP,
the owner film scan, hard-stop approval, macOS, physical parity, or any other
Gate7 gate. The required extra-bearing run remains unverified and is held
without retry under the no-automatic-retry instruction.
