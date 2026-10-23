# DB-composition-dry FIRST RETURN report

## Result

**Qualified PASS for the requested controlled dry run.** The exact 635f source was rebuilt once in a private extracted tree with recorded inputs, packed once with `npm pack --ignore-scripts`, and compared against the reviewed immutable archive. The generated archive is byte-identical to that archive, and all 80 extracted payload members are byte-identical. No product source, build script, pin, lockfile, consumer archive, branch, release, or shared dependency was changed.

Statuses are intentionally separate:

| Area | Status | Evidence |
| --- | --- | --- |
| Source delivery | PASS (with preserved prior failure) | The first authorized delivery run exited 1 because `orch/delivery/README.template.md` was missing. The authorized retry after template0749 exited 0; applied, bundle, and source trees were all `5ab5191a296980a0a6bcd1178ab6902d6478a148`. |
| Safe build/type/meta | PASS | Registry check, production no-emit typecheck, no-cleanup production compile/bundle, private test compile, opaque-meta loader test, and private packed export/type smoke passed. |
| Production pins/callers | PASS (read-only verification) | Current Agent and App manifests/locks point to the commit-named archive, with matching SRI, bytes, hash, and production caller linkage. |
| Controlled reproducibility | PASS for this recorded input set | Private packed archive and reviewed immutable archive: 73,451 bytes, SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, 80 members, `cmp` exit 0; extracted member list and every member byte compare equal. |

This is not a new release or repinning decision. H9 V4cut remains unchanged. No rendering parity or H3 journey claim is made.

## Identity, delivery, and prior evidence

- Live `git ls-remote origin refs/heads/main`: `67b8aa3d0d6831d3e3504a340ff583c3da253707`, exit 0.
- `git merge-base --is-ancestor 67b8aa3d0d6831d3e3504a340ff583c3da253707 635f4de06fda22a85fc2e4cfc764d0153a4c9f40`: exit 0.
- Exact Composition source commit: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- Exact Composition source tree: `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- `origin/main` tree recorded by the delivery retry: `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`.
- Authorized command: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos composition`.
- Initial 0746 delivery command: core tree verification passed, then the overall command exited 1 at `render_readme()` with `FileNotFoundError` for `orch/delivery/README.template.md`; staging was `build-20261023T074630Z`.
- The initial failure was not relabeled. Its retained log records the scratch package as 73,406 bytes, SHA-256 `1b263a6e3098509cbd832a621b4ce97336d7a5e49d4c60df06dad086c2b5f281`, with 64 equal members, 7 differing common bundled-JS files, and 9 changed chunk names.
- Template0749 supplied the authorized missing delivery input. The exact retry command exited 0; staging was `build-20261023T074841Z`, and applied/bundle/source trees were all `5ab5191a296980a0a6bcd1178ab6902d6478a148`. No ZIP was written. The retry reused the successful delivery proof and did not repeat a squash outside the authorized tool.

The earlier author claim that `npm run build:test` passed is corrected: the retained 0751 review records that command exiting 1 because plain Node could not resolve extensionless imports. Only the loader-based metadata test passed. The controlled run below does not claim `npm run build:test`; it uses the required private outDir equivalent.

## Controlled input record

The source was created with `git archive --format=tar 635f4de06fda22a85fc2e4cfc764d0153a4c9f40` into the owned private directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-DB-composition-first-return-0757/controlled-rebuild-635f-20261023`

The only dependency link was a private-tree symlink whose `realpath` was `/home/user/work/composition/node_modules`; no file in that shared install was written.

Tool versions read from that read-only install:

- Node `v22.22.0`.
- npm `10.9.4`.
- TypeScript `5.9.3`.
- esbuild `0.27.7`.
- tsx `4.23.15`.
- Remotion `4.0.509`.
- React and React DOM `18.3.1`.
- `@remotion/media` and `@remotion/layout-utils` `4.0.509`.

Source/package/build hashes:

- `package.json`: `a2435c315fe2235c63d32551f3c38ec85e049f2fc950f3ab556686fd7dab40f7`.
- `package-lock.json`: `b0c1a911648538219cdded4eeb4f76544af85e09366168966240246e54f8d1dd`.
- Source tree: `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- `scripts/build.mjs`: `111871dea911771cd69c8c25116165e4ae87e01368addb75bf96cbe01572492a`.
- `scripts/build-typescript.mjs`: `544e995ca60cd060ceed7858571613d213523f11a6c8936e3533cb7a24b8a5bf4`.
- `scripts/build-remotion-primitives.mjs`: `8cc1351a8f3c35c39ba2d14abd089e42b133daa9ba6ed61ada8980275d07f4e6`.

The original bundler options and entry order were preserved:

```text
entryPoints: index, evaluation, theme-api, registries, registry.generated,
             effects.generated, animations.generated, transitions.generated
outdir: dist
bundle: true; splitting: true; format: esm; platform: neutral
target: es2022; jsx: automatic
external: react, react/*, react-dom, react-dom/*, remotion,
          @remotion/media, @remotion/layout-utils
```

Before the production bundle, the no-cleanup equivalent primitive compiler produced:

- `typescript/src/lib/remotion-primitives.generated.js`: `903f9a2f2d322814ccc6f912ac167e902b4ecee7037ad38503a88bd811fab21d`.
- `typescript/src/lib/remotion-primitives.generated.d.ts`: `e5120365986908f9d18ce43216f75bff87092af88f63716d108e40a3ec035627`.
- Remotion primitive output was self-contained, with no external imports; the version guard was `4.0.509`.

The immutable archive does not retain a complete historical tool/input manifest. The retained V3/review records report the same current Node/npm/esbuild/TypeScript/tsx/Remotion versions and the same source/package identity, but that is not proof of the immutable archive's original generated-input provenance. The present result is therefore qualified to the explicitly recorded controlled input set.

## Exact commands and results

Acceptance and build commands were run with shell status propagation and each result was recorded:

1. `npm run gen-registry:check` in the extracted source: **exit 0**.
2. Equivalent primitive build using the original Remotion stdin, self-contained dependency guards, esbuild options, and output path, omitting only cleanup in the empty private output: **exit 0**.
3. `node node_modules/typescript/bin/tsc -p typescript/tsconfig.json --noEmit`: **exit 0**.
4. `node node_modules/typescript/bin/tsc -p typescript/tsconfig.json`: **exit 0**.
5. Equivalent declaration copy and original declaration-extension fix: **exit 0**.
6. Equivalent production esbuild bundle with the original options and entry order: **exit 0**.
7. `node node_modules/typescript/bin/tsc -p typescript/tsconfig.test.json --outDir <owned>/controlled-test-dist-635f-20261023`, followed by copying the original generated primitive JS into `<owned>/src/lib`: compiler **exit 0**, copy **exit 0**.
8. The first requested opaque-meta loader invocation lacked a peer-resolution link in the outDir and exited 1 with `ERR_MODULE_NOT_FOUND: react`. This was an environment setup failure, not a test assertion; no result was called PASS.
9. After adding a private symlink to the qualified read-only shared peer install, the exact requested command `node --import ./typescript/tests/register-extensionless.mjs --test --test-name-pattern='opaque meta does not change scene timing, asset selection, or rendered output' <owned>/tests/registries.test.js` passed 1/1, **exit 0**.
10. `npm_config_cache=<owned cache> npm pack --ignore-scripts --pack-destination <owned pack dir>`: **exit 0**, exactly one generated archive, 73,451 bytes, 80 files.
11. `sha256sum` of the generated archive and reviewed immutable archive: both `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; `cmp -s`: **exit 0**.
12. `tar -xzf` into separate owned generated/reference directories; member counts: **80 / 80**; member-list `diff`: no output; per-member `cmp`: no differing members; per-member hash comparison: no differing members.
13. Private packed export imports for `.`, `evaluation`, `theme-api`, `registries`, `effects.generated`, `animations.generated`, `transitions.generated`, and `registry.generated`: **exit 0**.
14. Private packed strict NodeNext type smoke using the retained consumer assertions: **exit 0**.
15. `git diff --check` in the Composition worktree: **exit 0**; tracked worktree remains clean.

There were five malformed setup invocations during this worker's execution, all corrected before the corresponding acceptance command: three omitted the `workers/...` component in the scratch path (registry, primitive, and esbuild attempts, exit 1), one declaration-fix command allowed shell backtick expansion and exited 1, and one first loader test lacked the private peer link (listed above). None wrote product or shared files; all corrected commands have their actual exits recorded above.

No lint script exists in `package.json`; lint is **N/A**, not skipped. No full, browser, render, journey, install, repack, cleanup, or release operation was run.

## Production consumers and pin integrity

Read-only checks observed:

- Agent HEAD `e49a6e76b3ab363e312c55b313714af1f845f54b`, tree `6ba7770dac3843b4d24d933521893277139d5ba1`.
- App HEAD `890b9561666c3619f69335dd747b15e042b3a9a3`, tree `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`.
- Agent `remotion/package.json` and lock use `file:artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`.
- App `package.json` and lock use `file:vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`.
- Both tracked consumer archives are 73,451 bytes and SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Both lock SRI values are `sha512-Ajl7lyCbJqbbOpHKEr2xlhFw85hWyirlTU1Dq63BNNUdHYfqgzLXljmudP359uKH6yBxSBMPTDoHLxgiDt65oQ==`.
- App’s `.sha256` sidecar agrees with the same hash. Both archives have 80 members.
- Agent production linkage includes `remotion/src/Root.tsx`, `ThreeTimelineComposition.tsx`, `src/host-scene.ts`, and evaluation callers importing the package. App linkage includes `TimelineRenderer.tsx`, `compileSequenceComponent.tsx`, and registry/runtime callers.
- Agent was clean when checked. App had pre-existing untracked `vendor/timeline-ops/timeline-ops`, `vendor/timeline-schema/timeline-schema`, and `vendor/timeline-theme-2rp/timeline-theme-2rp`; these were not touched. No consumer pin/archive/source writes were made.

## Decision and handoff

The earlier 0751 mismatch was a qualified finding based on a 73,406-byte scratch package versus the 73,451-byte immutable archive. This controlled run proves that exact source, the recorded current dependency graph, the recorded generated primitive bytes, the unchanged compiler/bundler logic, and the private no-cleanup build produce the reviewed bytes exactly. It does not invent or retroactively certify the historical provenance of the immutable archive. The existing archive and consumer pins remain authoritative and untouched.

Recommended next step: retain this report as the bounded delivery-build evidence, have the orchestrator's independent review consume the exact hashes and commands, and make any release/pin decision separately. No source fix or artifact repair is indicated by this run.
