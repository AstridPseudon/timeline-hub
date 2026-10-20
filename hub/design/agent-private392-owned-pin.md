# Agent private392 normal owned pin

Status: prepared on the Agent worker for manager review. This is one normal
private owned pin only; it is not an integration or public-release adoption.

## Exact identities

| Item | Exact value |
| --- | --- |
| Agent frozen base committed SHA | `e010e6a3868e963471244491bb6672c3e4a5135e` |
| Agent frozen base tree | `70414cf6875d2c97c45f33e0a5158c80bd7391d9` |
| Runtime producer committed SHA (`source_commit`) | `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414` |
| Runtime producer tree | `8be43e13acb436120f8a63b1a178d64c49422461` |
| Runtime producer identity | `astrid-runtime` |
| Runtime protocol | `workspace.v1` |
| Runtime contract/package version (read from producer files) | `0.2.13` |
| Release declaration | `generators/release.json: contract_version 0.2.13` |
| Component manifest digest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Frozen Agent command schema digest | `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` |
| Frozen Agent command schema shape | `56 definitions, 30 operations, schema v2` |

## Distinct producer digests

These are different identities and must not be substituted for one another:

| Meaning | Exact digest |
| --- | --- |
| Runtime health/schema digest (`SCHEMA_DIGEST`) | `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042` |
| Raw timeline commit bundle schema (`runtime_protocol/schemas/timeline-commit-bundle.json`) | `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3` |
| Producer artifact manifest version (`contract/artifacts.json`) | `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d` |
| Producer artifact count | `75` |

The consumer lock contains the normal 15 copied paths. The producer manifest
contains 75 artifacts; these counts refer to different layers and are both
intentional.

## Allowed scope

- Update the Agent `runtime.lock.json` through `python scripts/vendor_lock.py
  update runtime.lock.json --producer /home/user/work/wt/rt-pin-f8da4b6d`.
- Carry the previously approved `909bfad8` `_source_closure` canonical-image
  conversion when absent. It projects raw Runtime revision envelopes onto the
  existing canonical image fieldsets while preserving raw rows and authored
  payload, pins, order, and identity.
- Run generated-client parity, vendor-lock, schema-floor, and small
  project-data source-neighbor checks.

## Explicit exclusions and limits

- Private-only: no `tl/integration` adoption, public release, or fake override.
- No native pair in this pin; the manager must independently review this pin
  before one bounded new392 + existing-lifecycle pair.
- No new source semantics, fields, schema changes, or image normalization.
- Do not include future group, word, audio, provenance, transition, or opacity
  work.
- Leave old952, 613, a0, and public013 paths untouched.
- The next lifecycle step is not an old44 replay.
