# Composition 0.0.14 — qualified immutable adoption handoff

Status: **qualified for package adoption** after the exact corrected
trust-environment1056 normal smoke passed. This handoff publishes one
write-once archive; it does not change any consumer source or lock.

## Exact release identity

- Package: `@banodoco/timeline-composition@0.0.14`
- Source commit: `df7b86308902fae90eda1dc3080d17d8fc30ea78`
- Source tree: `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`
- Archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz`
- Archive SHA-256: `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`
- Archive size/members: `72134` bytes / `80` regular members
- Archive mode: `0444`; adjacent checksum: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz.sha256`
- Package-smoke installed integrity: `sha512-Bgf9lHdk3CJCTsA3Jbd5WW9UYCHEZQTF3VFM1YO6dimZ+q8bQ8cX6CZ4FCfClBNgg10DQ1bozGMqFCpkGNXvvw==`

The archive was packed once by the 1042 producer and transported here with a
realpath-checked, write-once install. The 1042 independent source/packed-byte
review remains the source of the source delta and archive identity. The exact
archive bytes were not repacked or changed.

The old public13 identity is unchanged: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
`58477` bytes, `77` members. Its artifact remains the predecessor, not a
replacement or parity claim.

## Evidence and exact versions

The central prerequisite terminal record is
`vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-trust-prerequisite-1056-1021105527-6023`:
PASS, exit 0, 7s, composition runner tree
`c38450855972c8717f4633fa3e90635ba848af8e`. It recorded 11280015360 bytes
available against the 10737418240-byte floor, measured need 76239977, strict
TLS, the existing CA/proxy carriers, and exact metadata for:

```text
@remotion/layout-utils@4.0.509
@remotion/media@4.0.509
react@18.3.1
react-dom@18.3.1
remotion@4.0.509
typescript@5.9.3
@types/react@18.3.31
@types/react-dom@18.3.7
```

The corrected exact normal package-smoke terminal record is
`vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-exact-packed-package-smoke-1056-1021105601-32025`:
PASS, exit 0, 6s, same runner tree. Its existing command was:

```text
bash "$PWD/COMMAND"
```

and the command invoked the unchanged package script with Node `20.19.4`
and npm `10.8.2`:

```text
npm run test:package -- /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-public14-diagnosed-runner-pack-1042/release-output/banodoco-timeline-composition-0.0.14-public14-qualified-1042.tgz
```

It installed 18 packages and passed plain Node ESM, bundled render/SSR,
scoped host capability/override, shared theme and peer identity, strict
NodeNext typechecking, and installed-integrity checks; installed package files
were unchanged and the private stage/cache were removed. Development evidence
used Node `22.22.0`, npm `10.9.4`, TypeScript `5.9.3`, the existing registry
freshness check, `gen-registry:check`, `build`, `build:test`, and 9 focused
source tests (all passed); the existing Composition full was 85/0/0.

## Caller impact and updater commands

The package-wide source delta from immutable public13 (source tree
`13e375534fffd704305eced5686699d2c8c9c948`, release13 refs
`73bd62b1e`/`5a4e9b72f`) to approved14 `df7b86308` is compactly:

- **Scene/clip-look correction** (`c1f4c0b5e`): `scene-evaluation.ts` now
  evaluates the supported built-in entrance geometry and element crop, while
  `lib/clip-look.ts` and the `fade-up`/`scale-in` wrappers share the same
  clip-look calculation. The follow-on `7552213c6` compiles the pure
  Remotion spring/interpolate leaf used by that shared calculation.
- **Pure/default separation** (`e55654817`): generated animation defaults and
  metadata moved to `animation-metadata.generated.ts`; the React animation
  registry re-exports the same values and pure Scene evaluation consumes the
  metadata-only module.
- **Declaration-specifier repairs** (`c1f4c0b5e`, `7552213c6`): generated
  internal imports used by the public root/theme/audio/easing surfaces now
  carry `.js` specifiers where repaired, and the generated pure-primitives
  declaration points at the pinned Remotion types.
- **Duration signature** (`b3443897b`):
  `getTimelineDurationInFrames` accepts `T extends Pick<TimelineConfig,
  "clips">`; its duration body is unchanged, and full-config callers remain
  valid.

The source-backed product caller set for the duration export is Agent's
`remotion/src/Root.tsx` and rendering presenter test path, plus App's
`ShotTimelinePreview.tsx`, `CompactPreview.tsx`,
`VideoEditorAssetPanelSurface.tsx`, `TimelineEditorShellCore.tsx`,
`TimelineRenderer.tsx`, `useDerivedTimeline.ts`, `useRenderState.ts`, and
`lib/config-utils.ts`/the video-editor index re-exports. Runtime has no
Composition package caller in the scoped source trees. Agent and App consumer
managers own any coordinated manifest/lock update and their actual
route/journey tests; this handoff activates none of them. No Runtime source,
runtime guarantee, or consumer route change is implied.

InspectionMouth is **not in 0.0.14**, and media parity remains **OPEN**.

First, each consumer must use this exact source and verify it before any
manifest or lock write:

```sh
ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.14.tgz
SHA256=21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e
test "$(realpath -e "$ARCHIVE")" = "$ARCHIVE"
test "$(sha256sum "$ARCHIVE" | awk '{print $1}')" = "$SHA256"
test "$(tar -tzf "$ARCHIVE" | awk '!/\/$/{n++} END{print n+0}')" = 80
```

Agent updater, from `/home/user/work/agent/remotion`:

```sh
DEST="$PWD/artifacts/banodoco-timeline-composition-0.0.14.tgz"
test "$(realpath -e artifacts)" = "$PWD/artifacts"
if test -e "$DEST"; then cmp -s "$ARCHIVE" "$DEST"; else install -m 0444 -- "$ARCHIVE" "$DEST"; fi
test "$(sha256sum "$DEST" | awk '{print $1}')" = "$SHA256"
npm install --package-lock-only --ignore-scripts --no-audit --no-fund ./artifacts/banodoco-timeline-composition-0.0.14.tgz
```

App updater, from `/home/user/work/app`:

```sh
DEST="$PWD/vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz"
test "$(realpath -e vendor/artifacts)" = "$PWD/vendor/artifacts"
if test -e "$DEST"; then cmp -s "$ARCHIVE" "$DEST"; else install -m 0444 -- "$ARCHIVE" "$DEST"; fi
test "$(sha256sum "$DEST" | awk '{print $1}')" = "$SHA256"
npm install --package-lock-only --ignore-scripts --no-audit --no-fund ./vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz
```

These are manager-owned normal updater commands. They do not authorize
consumer route tests, shared-install mutation, or a replacement of the old13
artifact before the consumer manager has completed its own checks.

## Explicit limits and non-claims

- The inspectionMouth proposal is **not in 0.0.14**.
- Public13 physical request `15923` failed at staged `SceneSurface`; it is not
  media parity evidence and is not relabelled as parity.
- The default explicit-theme props proof is not final media evidence.
- No repeat source qualification, reviewer audit, browser/helper run, Runtime
  run, consumer install, dependency-graph copy, product edit, or full suite
  was performed for this handoff.
- Consumer managers still owe their coordinated Agent/App pins, lock review,
  installed-file identity checks, and actual route/journey tests. This note
  certifies the immutable package artifact and its exact normal package smoke,
  not whole-project M4 or owner-film readiness.

## Flat evidence paths

- 1042 review: `design/handoff-vw-release14-independent-archive-review.md`
- 1056 worker report: `design/handoff-vw-release14-trusted-smoke-report.md`
- 1056 central prerequisite: `design/handoff-vw-release14-trust-prerequisite-summary.txt`
- 1056 central smoke: `design/handoff-vw-release14-package-smoke-summary.txt`
