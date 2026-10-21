# Producer0333 public13 execution-environment repair

## Result

Producer0333 failed before its body because the central suite ran directly against the shared App `node_modules` attachment. That attachment resolved `@banodoco/timeline-composition` 0.0.8, whose `/evaluation` module does not export `getSanitizedPlaybackRate`. This is an execution-environment binding failure, not a missing export in the approved public13 artifact.

The durable correction is to run the existing public13 build wrapper and its existing protected graph, using the build-only suite:

```text
request-test ap2-m2-producer-effective-public13-build-cause-0342 public13-effective-build-preflight
```

The authoritative run was `ap2-m2-producer-effective-public13-build-cause-0342-public13-effective-build-preflight-1021034145-2103`. It used the existing wrapper (SHA-256 `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`) with:

```text
env PUBLIC13_BUILD_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh "$PWD" ordinary
```

Result: exit 0 in 58 seconds. The hosted Vite/Rollup build transformed 5,584 modules and completed in 52.26 seconds. No browser, localhost, Runtime door, producer test body, or actual journey ran.

## Source and cohort

The tested App snapshot is the exact stage0320 source:

- App commit `4ef89267f00d193273441ff6dbb955f30d27d708`, tree `8c7393050ded32854503dfb7719a102b5dec94eb`.
- Approved producer body commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree `d908845dbc8e5ebf96698d08621557e904f20c52`.
- Producer selector config SHA-256 `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Immutable public13 Composition tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The protected graph was read-only at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph`.

Its Composition package hash is `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`; its `dist/evaluation.js` hash is `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`.

## Exact cause evidence

The wrong effective package was tested negatively before attachment:

```text
manifest=/home/user/work/app/node_modules/@banodoco/timeline-composition/package.json
evaluation=/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/evaluation.js
version=0.0.8
evaluation_sha256=0ee058ca8657a6bbdbe8c127359297f856c5a7b1cb68258bd3bdc20846d98b96
getSanitizedPlaybackRate=undefined
```

With the protected graph attached only through the worker's own temporary `node_modules` symlink, the actual Node and Vite resolver both selected:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/node_modules/@banodoco/timeline-composition/dist/evaluation.js
sha256=e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155
version=0.0.13
getSanitizedPlaybackRate=function
clipOpacity=function
```

The Node `createRequire` probe and Vite build resolver returned the same realpath and hash. The protected graph's 77 regular Composition files were compared against `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`: 77 archive members, 77 graph files, and 0 differing members.

The central wrapper repeated these controls before build: frozen Agent/Runtime commit and tree checks, protected graph/archive hash checks, Composition version/package/evaluation hashes, App and Agent `createRequire` resolution, App and SDK Vite resolution, and the public13 export probe. It used private run/cache/TMPDIR paths and restored the original App `node_modules` symlink.

## Scope and callers

No product import, fallback, package pin, lockfile, repack, shared dependency, or graph file changed. No tracked App file changed in this repair. The live producer callers remain unchanged:

- `src/tools/video-editor/dev/transcript-lane/extension.ts` (`transcriptLaneExtension` / `buildTranscriptCaptionPatch`)
- `src/tools/video-editor/dev/scene-phase-markers/extension.ts` (`scenePhaseMarkersExtension` / `moveExistingShotsToMarkers`)
- `src/tools/video-editor/dev/localExtensions.ts` registration

The original producer suite's argv, environment/source identities, immediate child return-code behavior, and `NoTestsFound` guard were not changed. The corrected command is build-only and is not authorization to run the actual producer journey.

## Tests

- Negative shared-package Node probe: PASS; confirmed 0.0.8 and missing `getSanitizedPlaybackRate`.
- Protected graph vs public13 tarball all77 byte comparison: PASS; 0 differing members.
- Protected graph Node + Vite resolver probe: PASS; identical realpath/hash and required exports.
- Central `public13-effective-build-preflight` result above: PASS, exit 0; hosted build passed.
- `git diff --check`: PASS.

Not run: producer browser journey, actual case, localhost/socket tests, or any full suite. The source worktree is clean and no build output remains in it.
