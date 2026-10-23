# DB-composition-dry independent FIRST-RETURN review

## Result

**PASS, qualified to the recorded controlled environment.** The corrected
first-return evidence is independently supported: exact source commit `635f4de`
and its source tree match, the private controlled archive is byte-identical to
both normal Agent/App archives, all 80 payload members compare equal, current
consumer pins still name the reviewed archive, and the required targeted checks
pass. This is not rendering parity, H3, or a final delivery-gate claim.

The prior failures remain failures and are not relabeled:

- The initial delivery run exited 1 because `README.template.md` was missing.
- The earlier scratch package was 73,406 bytes with SHA-256
  `1b263a6e3098509cbd832a621b4ce97336d7a5e49d4c60df06dad086c2b5f281` and
  diverged from the reviewed archive. This review does not infer or claim a
  historical cause was eliminated.
- The old author claim that `npm run build:test` passed was false; the retained
  evidence records exit 1 from extensionless Node resolution. This review did
  not run or claim that command passed.

## Independent evidence

### Delivery staging and source identity

I inspected both existing delivery stagings without rerunning the delivery
tool. The retry staging `build-20261023T074841Z` contains the generated README,
SHA256SUMS, patch, and bundle. Its README records applied/bundle/source tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`; the bundle hash was stable across
the two stagings, while the generated patch hash changed with the staging
timestamp. `git bundle verify` independently passed and
reported tip `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` requiring upstream
`67b8aa3d0d6831d3e3504a340ff583c3da253707`. The repaired template has all four
placeholders. The inherited exact tool command was
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos composition`:
the initial run exited 1 for the missing template and the authorized retry
exited 0. No ZIP was produced.

The extracted controlled source was checked against every regular file in
commit `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`: 120 checked, 0 missing,
0 mismatched. The commit tree is
`5ab5191a296980a0a6bcd1178ab6902d6478a148`.

### Build correspondence and generated inputs

The source helper hashes match the recorded values:

| Input | SHA-256 |
| --- | --- |
| `package.json` | `a2435c315fe2235c63d32551f3c38ec85e049f2fc950f3ab556686fd7dab40f7` |
| `package-lock.json` | `b0c1a911648538219cdded4eeb4f76544af85e09366168966240246e54f8d1dd` |
| `scripts/build.mjs` | `111871dea911771cd69c8c25116165e4ae87e01368addb75bf96cbe01572492a` |
| `scripts/build-typescript.mjs` | `544e995ca60cd060ceed7858571613d213523f11a6c8936e3533cb7a24b8a5bf4` |
| `scripts/build-remotion-primitives.mjs` | `8cc1351a8f3c35c39ba2d14abd089e42b133daa9ba6ed61ada8980275d07f4e6` |

The recorded environment was independently read from the qualified private
dependency link: Node `22.22.0`, npm `10.9.4`, TypeScript `5.9.3`, esbuild
`0.27.7`, tsx `4.23.15`, Remotion `4.0.509`, React/React DOM `18.3.1`, and
`@remotion/media`/`@remotion/layout-utils` `4.0.509`.

I inspected the original source helpers. The controlled commands preserve the
primitive stdin, Remotion-version guard, self-contained dependency check, and
the production esbuild entry order:
`index`, `evaluation`, `theme-api`, `registries`, `registry.generated`,
`effects.generated`, `animations.generated`, `transitions.generated`, with
bundle/splitting/ESM/neutral/es2022/automatic-JSX and the original externals.
The only omitted behavior was cleanup in an initially empty private output;
the forbidden cleanup scripts were not invoked.

Generated primitive hashes independently match:

- JS `903f9a2f2d322814ccc6f912ac167e902b4ecee7037ad38503a88bd811fab21d`;
- declaration `e5120365986908f9d18ce43216f75bff87092af88f63716d108e40a3ec035627`.

### Archive and normal consumers

The new scratch archive is 73,451 bytes and SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
`cmp` passed against both the tracked Agent and App archives; per-member `cmp`
passed for all 80 members against each archive. The computed SRI is
`sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`.

Read-only consumer checks show both manifests and locks still reference the
commit-named reviewed archive and both locks contain that exact SRI. App's
`.sha256` sidecar matches. No consumer source/config references the scratch
`0.0.14.tgz`. Production callers remain present in Agent Remotion entrypoints
and App video-editor registry/theme/rendering modules. Consumer worktrees have
no tracked changes; App's three pre-existing untracked vendor entries were
left untouched.

The first-return packed export/type smoke is inherited evidence, not rerun:
the exact same archive bytes were independently proven, and no repack or
autorepacking smoke was performed.

## Targeted commands executed

All three requested checks were run against the extracted source and existing
candidate test output; all exited 0:

```text
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-DB-composition-first-return-0757/controlled-rebuild-635f-20261023
npm run gen-registry:check                         # exit 0
node node_modules/typescript/bin/tsc -p typescript/tsconfig.json --noEmit  # exit 0
node --import /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-DB-composition-first-return-0757/controlled-rebuild-635f-20261023/typescript/tests/register-extensionless.mjs --test \
  --test-name-pattern='opaque meta does not change scene timing, asset selection, or rendered output' \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-DB-composition-first-return-0757/controlled-test-dist-635f-20261023/tests/registries.test.js  # exit 0
```

The last command reported 1 test, 1 pass, 0 fail, 0 skipped, 0 cancelled, and
exit 0. `git diff --check` passes in this review worktree and in both consumer
worktrees. Composition has no lint script, so lint is N/A.

No full/browser/journey/render/install run, cleanup script, `npm pack`, product
edit, pin/lock/archive edit, or shared dependency write was performed by this
review. H9 V4 remains cut. No source fix or artifact repair is indicated.
