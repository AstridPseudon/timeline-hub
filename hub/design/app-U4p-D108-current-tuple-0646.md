# U4p D108 current tuple adoption

**PASS** — normal App provenance now targets the qualified integrated heads.

## Tuple

- App base: `51239c79e26ff743623218b9c09fdce1629ec90c`
- Runtime: `c91626f5e905f9336b51aae0486a071d83f0bac7`, tree `16264479ae18fbb05ec5356ce5b5ab6f69dea9aa`
- Agent: `d6294843286c18e57af3c1874cf1996be42212d2`, tree `6aeae30f0892a424104a4348bca6fd74ba1315d6`
- Runtime product parent: `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree `a522511414947e48e317a5e5c2103483b121a750`
- Schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- Runtime contract: `0.2.14`; producer version and 14 artifact mappings preserved.

## Source verification

The Runtime first-parent diff from product release `1daca` to `c916` is exactly:
`README.md`, `scripts/check-before-push`, and `tests/test_release_native_smoke.py`.
The Agent first-parent diff from `5554fe792bba5ed17c90e0a1ccf46f4d5df19601` to
`d629` is exactly its `runtime.lock.json` adoption. This verifies the board
statement that `c916` adds reviewed release checks while retaining the `1daca`
product bytes; no unqualified product substitution or additional source/security
review was introduced.

Existing source evidence consulted: `runtime-D102c-release-0615.json` and
`rt-R-release-smoke-home-0630-report.md`. The latter records the current Runtime
release smoke as two genuine provider tests passed and the exact authored paths.

## Changes

Only the normal tooling changed:

- `runtime.lock.json`: `source_commit` `1daca` → `c916`.
- `public/install-manifest.json`: Agent `8c88` → `d629`; Runtime `1daca` → `c916`.

Schema digest, manifest schema, producer version, canonical generated/schema
bytes, protected six, D105a placement controls, D96 source blobs, and retention
product/control bytes remained unchanged.

## Verification

- `/opt/node20/bin/node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime`: passed.
- `/opt/node20/bin/node scripts/installer/update-manifest.test.mjs`: 2/2 passed.
- `/opt/node20/bin/node scripts/installer/manifest.test.mjs`: 2/2 passed.
- `/opt/node20/bin/node scripts/runtime-schema-guard.test.mjs`: 2/2 passed.
- Vitest `installManifestSkew.test.ts` + `vendorLock.test.ts` with isolated temp config/cache: 17/17 passed (2/2 + 15/15).
- Runtime artifact manifest check: current; `tests/test_artifact_manifest.py`: 3/3 passed.
- Node syntax checks: 3/3; scoped ESLint: 0 warnings/errors.
- JSON syntax, exact producer mappings: 14/14, protected/canonical bytes: 14/14, and `git diff --check`: passed.

No full suite, browser, service, build, package installation, generator repair,
or P1/P2/P3 body was run. The existing known stale generator baseline remains
untouched and unclaimed as new evidence. The current `/opt/node20/bin/node`
reports `v20.20.0`; the commands were run through that supported Node 20 path.
