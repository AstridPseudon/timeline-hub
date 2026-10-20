# App cap six-export environment triage

## Result

The six missing Composition exports were an environment mismatch in the
shared dependency installation, not a public13 package defect and not an App
source defect. The assigned source tree remains unchanged.

The prior cap report identified 10 project TypeScript diagnostics: six missing
exports from `@banodoco/timeline-composition/evaluation` and four separately
owned shot-name diagnostics. The six export references are:

- `AudioTrack.tsx`: `computeMediaTrim`, `encodedEnvelopeSource`, and
  `EncodedEnvelopeSource`.
- `compiledAudioSourceClock.ts`: `computeMediaTrim` and
  `getSanitizedPlaybackRate`.
- `config-utils.ts`: the `computeMediaTrim` re-export.

## Identity and resolution evidence

- Source HEAD: `c84028f7f71ced31ebd5636068469860cb8ab5f0`.
- Source tree: `c404c633472c56413547e03f3378afafe4c61cf2`.
- `package.json` and `package-lock.json` both require the local
  `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`.
- The archive SHA-256 is
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
  It contains 77 regular members.
- The owned private13 package was compared member-by-member with the archive:
  77 compared, 0 mismatches. Its package version is `0.0.13`.
- The assigned worktree's `node_modules` is a symlink to the shared App
  install. TypeScript resolved the Composition evaluation declaration there
  as `/home/user/work/app/node_modules/@banodoco/timeline-composition/dist/evaluation.d.ts`,
  package version `0.0.10`.
- The private13 resolution instead reached the owned overlay's
  `dist/evaluation.d.ts`, package version `0.0.13`.
- React and ReactDOM are `18.3.1`; Remotion, media, player, and layout-utils
  are all `4.0.509`; TypeScript is `5.9.3`. These versions match the public13
  peer declarations and the App package requirements.
- `tsconfig.app.json` uses ES2020, bundler module resolution, and only the
  existing `@/*`, `@astrid/editor-sdk`, and timeline-schema path mappings. No
  path mapping masks or redirects the Composition package.

The shared 0.0.10 declaration lacks the six evaluation exports. The verified
0.0.13 declaration contains all of them. Therefore no public artifact,
package, lockfile, peer pin, or product import path was changed.

## Verification check

I created a private clean leaf outside the source worktree from the exact HEAD
and pointed its `node_modules` at the already-owned private13 overlay. No
install, cache write, shared dependency mutation, or source edit was done.

One actual project typecheck was run after that environment correction:

```sh
flock -x /home/user/work/.app-tsc.lock \
  env NODE_OPTIONS=--max-old-space-size=4096 \
  node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/typescript/bin/tsc \
  --noEmit -p tsconfig.app.json
```

Result: exit 2, with no Composition export diagnostics. The remaining four
diagnostics are the separately owned source errors:

```text
src/tools/video-editor/commands/shotSetCapture.ts(61,18): error TS18047: 'bundle.source_mapping' is possibly 'null'.
src/tools/video-editor/commands/shotSetCapture.ts(61,40): error TS2339: Property 'shots' does not exist on type 'string | number | boolean | JSON[] | { [key: string]: JSON; }'.
  Property 'shots' does not exist on type 'string'.
src/tools/video-editor/commands/shotSetCapture.ts(145,19): error TS2322: Type 'string | null' is not assignable to type 'string'.
  Type 'null' is not assignable to type 'string'.
src/tools/video-editor/commands/shotSetCapture.ts(195,35): error TS2345: Argument of type 'JSON' is not assignable to parameter of type 'object'.
  Type 'null' is not assignable to type 'object'.
```

No full suite, install, browser, render, parity, or new test was run. The
Viewing derived-cap fallback review remains HOLD as directed.

## Recommendation

Repair or refresh the shared App dependency environment so the worktree's
normal `node_modules` resolves the declared public13 archive. The package
owner does not need a public13 mutation request: the archive is authoritative
and internally consistent. Separately owned shot-name fixes should address the
four remaining `shotSetCapture.ts` diagnostics.
