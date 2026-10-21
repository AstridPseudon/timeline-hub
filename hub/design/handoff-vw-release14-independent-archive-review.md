# Public14 actual archive review

## Verdict

**REQUEST CHANGES — do not approve the release yet.** The actual immutable
public14 bytes exist and pass this review's independent identity, member,
export, declaration, purity, syntax, and direct pure-ESM checks. The normal
packed-byte consumer smoke did not reach its assertions: Node20.19.4's
existing `scripts/smoke-package.mjs` stopped at `spawnSync('tar') EPERM` in
the pack worker sandbox. Therefore SSR, peer identity, installed-package
integrity, and strict NodeNext consumer evidence are still unverified.

## Artifact and provenance

- Archive:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-public14-diagnosed-runner-pack-1042/release-output/banodoco-timeline-composition-0.0.14-public14-qualified-1042.tgz`
- Size: 72,134 bytes; 80 members; archive and sidecars are single-link,
  read-only owned files.
- SHA-256:
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`
- Sidecar: adjacent `.sha256`, matches `sha256sum -c`.
- Source commit/tree: `df7b86308902fae90eda1dc3080d17d8fc30ea78` /
  `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`.
- Approved source delta from `7bb54bbd6` is exactly
  `typescript/src/lib/duration.ts` plus
  `typescript/tests/duration.test.ts`; the duration implementation body is
  unchanged apart from the generic `clips`-only parameter declaration.
- Package metadata is `@banodoco/timeline-composition` `0.0.14`, ESM, with
  the expected `main`, `types`, nine public exports, and retained CHANGELOG
  entry.
- Immutable public13 guard remains 58,477 bytes, 77 members, SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Independent packed-byte checks

Passed:

- `sha256sum -c <public14>.tgz.sha256`, archive size/member count, sidecar
  identity, and public13 size/member/SHA guards.
- Export targets and declaration targets resolve inside `dist`; import and
  default targets agree; archive member scope is limited to package metadata
  plus `dist` JavaScript/declarations.
- Node20.19.4 `--check` on every packed top-level ESM file.
- Node20.19.4 direct import of packed `dist/evaluation.js`, with a clip/scene
  witness. `prepareScene`, `querySceneFrame`, `querySceneOcclusion`,
  `clipOpacity`, and `encodedEnvelopeSource` are callable.
- Static transitive graph check: evaluator imports no external runtime peer;
  internal ESM imports are extension-complete and remain inside `dist`.
- Packed `lib/duration.d.ts` contains
  `getTimelineDurationInFrames: <T extends Pick<TimelineConfig, "clips">>`;
  the packed duration implementation still only reads `timeline.clips` and
  has no `timeline.tracks` access.
- Packed root/evaluation surfaces retain the approved Scene/clip-look and
  `encodedEnvelopeSource` exports. Source Scene evaluation remains explicitly
  pure and reports undeclared component internals as unknown.

Reviewed prerequisite evidence (not rerun because source is unchanged):

- Central registry freshness witness: 1 passed, 0 failed.
- Development `gen-registry:check`, `build`, and `build:test`: passed.
- Focused source tests: 9 passed, 0 failed, 0 skipped.
- Existing unchanged development full: 85 passed, 0 failed, 0 skipped.

## Missing evidence / exact next step

The pack worker ran exactly one pack and then invoked:

`/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm run test:package -- <public14 archive>`

It stopped before smoke assertions at `scripts/smoke-package.mjs:13` with
`spawnSync tar EPERM`; no retry, install, repack, source change, or consumer
adoption occurred. Run that existing smoke once, outside the nested-process
restriction, against this exact archive and SHA using Node20.19.4/npm10.8.2.
Only after its ESM/SSR/peer/strict-NodeNext assertions pass should this review
be upgraded to APPROVE.

No source, archive, pin, dependency, or worktree changes were made by this
review worker. Temporary review extraction was cleaned.
