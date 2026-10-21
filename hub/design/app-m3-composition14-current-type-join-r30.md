# App Composition14 current type-join candidate

Status: **BLOCKED for the requested actual composed TypeScript program**.
The current-preserving four-path candidate is prepared; no integration adoption
is authorized or performed.

## Candidate identity and scope

- Worktree: `/home/user/work/wt/app-m3-composition14-current-type-join-r30`
- Base commit: `5f513665a` (`tl/integration`), containing r76 `d1374a363` and
  r77 `5f513665a`.
- Base tree: `1c28244f9de4399070bc31772aef2d1a6cfca128`.
- Candidate tree (computed from the working tree without writing the index or
  Git objects): `99490952d4d838baab15d55c1d68e8f7be198753`.
- A commit SHA is pending the harness commit; this worker did not commit.
- Current source repairs remain exactly the six existing r76/r77 paths:
  `commitOutbox.ts`, `commitSession.ts`, `occurrenceMediaCapture.test.ts`,
  `occurrenceMediaCapture.ts`, `sessionPlacement.ts`, and
  `VideoEditorProvider.tsx`.

Only these four donor paths were applied from r29/r28:

| path | donor blob |
| --- | --- |
| `package.json` | `95941009c04f5957f2550c9b5802b929cf090115` |
| `package-lock.json` | `f085ca5dd047f5a66027b904cd7d74c06d6277b9` |
| `config/vite/timelineCompositionPackage.test.mjs` | `93694fc1873e81d5430d5c1cca2df7d80b40e51d` |
| `vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz` | `c1e65c5aaa9ce95208f398d04328d77a55dc1543` |

Runtime 95, the `0.2.14` generated contract, the live
`initializeBootstrapTimeline`, and all current source outside those inherited
r76/r77 changes are unchanged. `clipScalarGesture.ts` was not changed; its
remaining App2 diagnostic is separately owned.

## Composition14 identity

- Package: `@banodoco/timeline-composition@0.0.14`.
- Archive: 72,134 bytes, 80 regular members.
- Archive SHA-256:
  `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`.
- Archive SHA-512:
  `0607fd947764dc22424ec03725b779596f546021c46504c5dd514cd583ba762999faaf1b43c717e826781427c2941360835d034356e8cc632a142a6418d5efbf`.
- Lock integrity:
  `sha512-Bgf9lHdk3CJCTsA3Jbd5WW9UYCHEZQTF3VFM1YO6dimZ+q8bQ8cX6CZ4FCfClBNgg10DQ1bozGMqFCpkGNXvvw==`.
- Root and lock both point to
  `file:vendor/artifacts/banodoco-timeline-composition-0.0.14.tgz`.
- Intended declaration origin is the archive’s installed package
  `node_modules/@banodoco/timeline-composition/dist/*.d.ts`, with the package
  manifest `types: ./dist/index.d.ts` and the declared public subpath types.
- r26’s private14 qualification previously proved all 80 installed files
  byte-identical to a fresh extraction and passed the unchanged Scene/clock/PCM
  controls. Those controls were reused as prior donor evidence, not rerun.

## TypeScript manifest and blocker

The original program is defined as:

```text
cwd: /home/user/work/wt/app-m3-composition14-current-type-join-r30
compiler: TypeScript 5.9.3
flags: --noEmit -p tsconfig.app.json
lock: flock -x /home/user/work/.app-tsc.lock
heap: NODE_OPTIONS=--max-old-space-size=4096
target/moduleResolution/module/jsx: ES2020 / Bundler / ESNext / ReactJSX
root files: 2558
```

The actual candidate program was **not invoked** (exit/errors: **N/A**). The
r26 private14 leaf was deleted after its qualification, and no real14 installed
leaf is accessible now. Available installs are shared 0.0.10 and private/shared
0.0.13 leaves; using either would make the result non-14 evidence. Creating,
installing, extracting, or overriding a private14 declaration leaf is forbidden
by this task, so this is a concrete blocker rather than a source diagnostic.

For context only, r26’s historical actual14 program on its older source tree
used the same original flags, exited 2, and reported nine errors: the one
separately-owned `clipScalarGesture` error plus eight HOME errors in
`commitSession`, `occurrenceMediaCapture`, `sessionPlacement`, and
`VideoEditorProvider`. That historical result is not relabeled as this
candidate’s result; the current r76/r77 source repairs were not requalified
here. The prior r26 run reported the seven old-duration diagnostics absent.

## Checks run

Passed:

```text
node --test --test-name-pattern='root and lock use the approved immutable public14 artifact' config/vite/timelineCompositionPackage.test.mjs
git diff --check
```

The package-boundary command passed its selected public14 root/lock/archive
identity check. The full package boundary suite was not run against the shared
install because it resolves shared Composition 0.0.10, not the candidate’s
0.0.14 leaf.

Not run: the actual TS5.9.3 composed program, install/build/new private graph,
browser, native, full, physical, Runtime pin, or integration adoption.

## Agent counterpart / gate

The exact committed normal14 Agent counterpart is present at commit
`255b6856cc1c96f4d40ddac05d4e3d98bb81051c`, tree
`aed2ccf7596add9118b272afad831c214ede11fe`, with the same approved archive.
The peer record says independent pin review1137 was active; the counterpart was
identified, but the peer/adoption gate is not claimed closed. No integration
adoption or publication was performed.
