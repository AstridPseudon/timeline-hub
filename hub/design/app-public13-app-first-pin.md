# App-first Composition public13 pin

## Source and release identity

- App source base: `b1ef4b9b9` (`tl/app-m3-label-live-policy-remount-fix`); the
  worktree was clean before this unit.
- Approved Composition source: `af98594dce80c0350a1fc21dfc44839b2279edf1`.
- Composition release commit: `73bd62b1e1b710a730545c862bd2da76e324ca46`.
- Integration source observed in `/home/user/work/composition`: `5a4e9b7`.
- Release handoff: `design/handoff-vw-m3-release13-admission-only-REPORT.md` and
  `design/handoff-vw-m3-release13-final-gate-REPORT.md`.
- Release sidecar: `design/handoff-vw-m3-release13-banodoco-timeline-composition-0.0.13.sha256`.
- Release handoff CHANGELOG source: Composition `CHANGELOG.md` records
  `0.0.13` as the existing `encodedEnvelopeSource` public evaluation export.
- Supplied App artifact:
  `artifacts/banodoco-timeline-composition-0.0.13.tgz`.
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Size: 58,477 bytes; 77 regular members.
- Lock integrity: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.

The supplied sidecar, release handoff, final-gate report, member manifest, and
CHANGELOG source agree. I found no separate registry/publication confirmation;
none is claimed or inferred. No registry fetch, install, or repack was used.

## Changes

- Updated the App dependency in `package.json` and the root dependency plus
  resolved/version/integrity entry in `package-lock.json` from public12 to
  public13.
- Added the approved archive at
  `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`.
- Updated the existing `config/vite/timelineCompositionPackage.test.mjs` identity
  control to public13 and asserted the announced public
  `evaluation.encodedEnvelopeSource` export.
- Runtime013, MAIN17, root `b1ef4b9b9`, public12 archive, peers, and unrelated
  App files were not changed.

Archive comparison against `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`
found exactly these four changed members: `package.json`, `README.md`,
`dist/evaluation.js`, and `dist/evaluation.d.ts`. The remaining 73 members are
byte-identical. This is an identity/pin unit only; it does not qualify the App
continuous-PCM consumer or physical frame/audio parity.

## Tests and checks

Targeted command, using a private hard-linked dependency overlay with the
public13 package extracted from the approved archive (shared dependencies were
not modified):

```sh
node config/vite/timelineCompositionPackage.test.mjs
```

Result: **PASS, 9/9**. This covered root/lock/archive identity, seven Vite or
Vitest config aliases, shared peer resolution, and SSR imports including the
new public evaluation export.

Also run:

```sh
git diff --check
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz
```

Both passed; the checksum matched the approved value. No full suite,
project-wide TypeScript, browser, build, network, install, or PCM consumer
qualification was run. The latest Viewing handoff still leaves consumer
activation and physical parity qualification open.
