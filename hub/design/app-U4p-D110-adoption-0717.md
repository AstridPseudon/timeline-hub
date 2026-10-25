# App U4p D110 adoption

## Result

Adopted the qualified Agent D110 release through the normal App provenance tools.
The only final App change is `public/install-manifest.json`, updating `agent.sha` to
`070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`. `runtime.lock.json` was re-synced
against the normal Runtime checkout and remained byte-identical because it already
identified Runtime `c91626f5e905f9336b51aae0486a071d83f0bac7`.

The production installer and generated Runtime client therefore target:

- Agent release: `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, tree `6056414359ae9fce08d999d54cbecf719fda33c3`
- Runtime producer: `c91626f5e905f9336b51aae0486a071d83f0bac7`, tree `16264479ae18fbb05ec5356ce5b5ab6f69dea9aa`
- Runtime product base: `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree `a522511414947e48e317a5e5c2103483b121a750`
- Schema: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

## Source qualification

The normal Agent tree exactly equals the named D110 capture tree and the independently
reviewed candidate tree `6056414359ae9fce08d999d54cbecf719fda33c3`. The normal Agent
release commit changes only `astrid/sdk/timeline/inverse.py` and adds
`tests/sdk/test_inverse_removed_shot_owners_runtime.py` relative to its release parent.
The D110 release handoff and independent review both record PASS; no additional source
or security review was required.

Runtime `c91626f5e905f9336b51aae0486a071d83f0bac7` differs from product `1daca` only
in the reviewed release-check inventory: `README.md`, `scripts/check-before-push`, and
`tests/test_release_native_smoke.py`. The Runtime lock retains the canonical 14
artifact mappings, producer version, and schema digest.

## Verification

Passed:

- `/opt/node20/bin/node scripts/sync-runtime-client.mjs /home/user/work/runtime`
- `/opt/node20/bin/node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --plan`
- `/opt/node20/bin/node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --write`
- `/opt/node20/bin/node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime`
- `/opt/node20/bin/node scripts/installer/manifest.test.mjs`: 2/2
- `/opt/node20/bin/node scripts/runtime-schema-guard.test.mjs`: 2/2
- Central targeted Vitest: `installManifestSkew.test.ts` 2/2 and `vendorLock.test.ts` 15/15, 17/17 total
- Runtime artifact check and `tests/test_artifact_manifest.py`: 3/3
- Node 20 syntax checks: 3/3
- Node 20 scoped ESLint: 0 warnings/errors
- JSON syntax, exact producer mappings 14/14, protected/canonical bytes 14/14, producer/schema retention, and `git diff --check`

The direct updater test command `/opt/node20/bin/node scripts/installer/update-manifest.test.mjs`
was attempted and both tests were blocked by the sandbox with `spawnSync git EPERM` while
creating its temporary fixture repository. The central generic targeted Vitest runner did
not execute `.mjs` arguments, so this remains unverified here; no test or production code
was changed to bypass it.

No full suite, browser, service body, build, package install, generator repair, or P1/P2/P3
body was run. D111 was not awaited or substituted. The final App diff is scoped to the
owned installer manifest.
