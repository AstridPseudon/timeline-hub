# Composition release14 exact smoke1050 peer handoff

## Result

**BLOCKED — no adoption packet is published.** The one existing central
`smoke1050` run is terminal and failed before any packed-package smoke
assertion. This handoff records the immutable artifact and all retained
evidence, but it does not authorize Agent/App pins, updater recipes, or
consumer adoption.

The precise missing requirement is a successful ordinary consumer install of
the exact archive, with the declared peer `@remotion/layout-utils@4.0.509`
resolving, followed by the existing ESM, SSR, installed-integrity, and strict
NodeNext assertions. The central run instead recorded npm
`SELF_SIGNED_CERT_IN_CHAIN` registry failures and then `ERESOLVE`:
`@remotion/layout-utils@undefined` was found while the root requested
`4.0.509`; the package's peer requirement is also `4.0.509`.

## Immutable artifact identity

The existing write-once artifact was not changed or repacked:

- filename: `banodoco-timeline-composition-0.0.14-public14-qualified-1042.tgz`
- path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-public14-diagnosed-runner-pack-1042/release-output/banodoco-timeline-composition-0.0.14-public14-qualified-1042.tgz`
- SHA-256: `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`
- bytes: `72134`
- tar members: `80`
- package: `@banodoco/timeline-composition@0.0.14`
- source commit: `df7b86308902fae90eda1dc3080d17d8fc30ea78`
- source tree: `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`

The archive and sidecars remain single-link, read-only files. Public13 remains
immutable at 58,477 bytes, 77 members, SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Exact central result

- suite: `composition integration-public14-exact-packed-package-smoke-1050`
- test ID: `vw-m4-public14-exact-packed-central-smoke-1050-integration-public14-exact-packed-package-smoke-1050-1021104659-425`
- result: `fail`, exit `1`, duration `141s`
- counts: `0 smoke assertions reached; npm install failed before assertions`
- log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m4-public14-exact-packed-central-smoke-1050-integration-public14-exact-packed-package-smoke-1050-1021104659-425/log.txt`

The existing command was the normal package script, with no assertion or
dependency relaxation:

```text
env -i HOME="$STAGE/home" LANG=C.UTF-8 \
  PATH="/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin" \
  NODE_PATH='' TMPDIR="$STAGE/tmp" NPM_CONFIG_CACHE="$STAGE/npm-cache" \
  NPM_CONFIG_USERCONFIG="$STAGE/npmrc" \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm \
  run test:package -- <exact archive>
```

The central preflight verified the archive hash, size, member count, realpaths,
Node `v20.19.4`, and npm `10.8.2`. The temporary stage was owned and removed
after the failed run. There was no retry, `--force`, `--legacy-peer-deps`,
repack, source change, shared dependency write, or local smoke replay.

## Retained evidence

The existing independent source/byte review is consumed as existing evidence;
no review of that review was commissioned. It independently passed:

- archive SHA/sidecar, size/member count, export and declaration target scope;
- Node20 syntax checks for packed top-level ESM and a direct packed ESM import;
- internal extension-complete graph and no external runtime import from the
  evaluator;
- Scene/clip-look exports and packed evaluator witness;
- source registry freshness (`1 passed`), `gen-registry:check`, `build`, and
  `build:test`;
- nine focused source tests (`9 passed, 0 failed, 0 skipped`); and
- the unchanged development full result (`85 passed, 0 failed, 0 skipped`).

The source qualification used Node `v22.22.0` / npm `10.9.4`. The packed
consumer smoke used Node `v20.19.4` / npm `10.8.2`; these are separate
toolchains and are reported separately.

The duration implementation body is unchanged and still reads only
`timeline.clips`. The corrected packed declaration is:

```ts
export declare const getTimelineDurationInFrames:
  <T extends Pick<TimelineConfig, "clips">>(timeline: T, fps: number) => number;
```

## Gates and withheld actions

- ESM, SSR, installed-package integrity, peer identity, and strict NodeNext
  consumer evidence: **not proven** because install failed first.
- Physical same-film/public13 parity: **not proven**. Retained physical
  request `15923` reached the real task and failed on `SceneSurface`; it made
  no parity, MP4, PNG, frame, or PCM claim. No browser, helper, Runtime, or
  physical launch was performed here.
- Agent/App coordinated actual pins and normal updater recipes: **withheld**;
  no adoption packet exists.
- Runtime bundling: the window has elapsed; no delay or speculative private
  cohort is introduced.
- D09 `inspectionMouth`: **not in this archive** and remains pending peer
  agreement.

Next action belongs to the release owner: restore a registry environment in
which the existing script can resolve the declared peers, then obtain a
separate authorized smoke decision against these exact immutable bytes. Do not
alter this archive, its source/pin/version identity, or publish consumer
adoption from this failed result.
