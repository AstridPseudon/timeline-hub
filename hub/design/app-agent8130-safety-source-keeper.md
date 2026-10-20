# Agent current compatible safety source keeper

Result: **KEEP**. This is a read-only provenance record for the exact Agent
source selected for new App safety tests. It is not a new pin, schema,
dependency, package, or generated-file adoption.

## Agent source

| Field | Exact value |
| --- | --- |
| Worktree | `/home/user/work/wt/app-m3-agent8130-safety-source-keeper` |
| Branch | `tl/app-m3-agent8130-safety-source-keeper` |
| HEAD | `8130a401bf44a518d5a40ae274d398b8c560be55` |
| HEAD tree | `236c3e57e0265c52b81ba8085de3193026176bff` |
| Status | clean; `git diff --check HEAD` passed |

The source is the requested Base8130/tree236 source, distinct from the older
`d8749a9c` candidate. No product or generated-file changes were made.

## Normal Runtime/client/artifact tuple

`runtime.lock.json` is the normal committed lock (15 files; file SHA-256
`c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311`):

- Runtime source commit: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Published Runtime tree: `7ab412cc4bcbe517efcfa806e092336390312e18`
- Protocol/client: `workspace.v1` / `0.2.13`
- Schema digest: `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`
- Runtime artifact: `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Runtime `contract/artifacts.json`: 75 entries, file SHA-256
  `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`
- Runtime component manifest: `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`

The Runtime commit/tree and manifest were read from
`/home/user/banodoco/banodoco-workspace-runtime`; the documented retained
checkout `/home/user/work/wt/rt-m2-pin-2c4ac180` is absent in this sandbox, so
that checkout itself was not re-verified.

Agent's own `artifacts.json` is current: producer `astrid-agent`, 162 entries,
version `sha256:f8ca7aebd797e4fd59aad43c2d74e8702fc1038d33eb89dfaf1fd212426ab840`,
file SHA-256 `2ef0f27f4b8a5d1029356861da0841e5f319485f259777c3f3d7d0080d5021a`.

## Public command schema

Path: `astrid/core/timeline/schema/edit-command.schema.json`.

- SHA-256: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`
- `$defs`: 48
- `EditCommand.allOf`: 22 clauses
- Registered operations, in schema order: `clip.delete`, `track.set`,
  `shot.set`, `clip.set-params`, `clip.set-element`, `timeline.inverse`,
  `timeline.restore`, `clip.move`, `clip.add`, `occurrence.add-media`,
  `occurrence.swap-media`, `placement.move`, `placement.create`,
  `placement.unplace`, `shot.pool`, `track.create`, `clip.set`, `clip.trim`,
  `clip.split`, `occurrence.duplicate`, `occurrence.delete`, `producer.guard`.

The Runtime published artifact manifest independently records the same command
schema bytes as `contract/schemas/edit-command.json`.

## Composition 0.0.12 source and lock

The immutable Composition source origin is the Composition repository
`/home/user/peteromallet/timeline-composition`, release-preparation commit
`4b9f2eee4dda960dc3a38aeba8943368c0fed3d5`, merged/published as
`5e06f40146573a529896cc812229eb890c53c81a`; both point at source tree
`61d54da1d6a5b1f26132602cec49e84bded87805`.

The Agent consumer adoption is ancestor commit
`5f6c81309d96e7cd7abc2f22b32a377621c29092`, tree
`42d59104ef24fc745a56c55d81694a1cdb932f91`; its Composition bytes are
unchanged through this keeper HEAD.

| Field | Exact value |
| --- | --- |
| Archive | `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz` |
| Version / size / members | `0.0.12` / `58,444` bytes / `77` regular members |
| Archive SHA-256 | `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |
| Lock file | `remotion/package-lock.json`, SHA-256 `cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597` |
| Lock integrity | `sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==` |
| File resolution | `file:artifacts/banodoco-timeline-composition-0.0.12.tgz` |
| Peer/runtime tuple | React/React DOM `18.3.1`; Remotion, media, layout-utils `4.0.509` |
| Node/npm engines | `20.19.4` / `10.8.2` |

## Verification

Direct checks from the assigned worktree:

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

PYTHONDONTWRITEBYTECODE=1 python3 scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check HEAD
PASS
```

No tests, full suite, install, network, browser, TypeScript check, or build was
run, per the task brief. The source worktree remained clean after verification.
