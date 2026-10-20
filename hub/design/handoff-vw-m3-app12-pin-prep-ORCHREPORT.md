# App 0.0.12 pin-prep handoff

Status: exact patch prepared, unapplied to the App product worktree.

## Selected source cohort

Use AppSTATUS's selected minimal source cohort:

- App `9d9101fef15470c813d060ed0169676fa7206c2e` (`hub/tl/app-m3-current-minimal-safety-typecheck`)
- This is the minimal public10 / official client028 source reference.
- The source carries the existing official Runtime client 0.2.8 dependency. Its Runtime lock producer is recorded by the release-readiness design as `1ad39f5c4bf834736bb2ee04b031eebbcdb11ce0` (artifact `sha256:4010d93be2…`). Do not change that pin in this handoff.
- AppSTATUS still requires the one-current-tuple sequence: Runtime publishes `design/runtime-current-tuple.md`, Agent publishes the matching public10 consumer pin, then App adopts the same tuple. Those are current release prerequisites, not reasons to broaden this patch.

The current App integration tip is not the patch base: AppSTATUS explicitly selects the minimal `9d9101f…` source reference for this release preparation. The patch therefore preserves the full root/lock/guard semantics of that cohort, including package path, opaque package exports, history labels, and current-consumer resolution.

## Four-file owner patch

Apply [handoff-vw-m3-app12-pin-prep.patch](./handoff-vw-m3-app12-pin-prep.patch) to the selected App cohort, then place [handoff-vw-m3-app12-pin-prep-artifact.tgz](./handoff-vw-m3-app12-pin-prep-artifact.tgz) at:

```text
vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
```

The resulting four-file change is exactly:

1. `package.json`: Composition file dependency `0.0.10` -> `0.0.12`.
2. `package-lock.json`: root file dependency, package version/resolved path, and integrity only.
3. `config/vite/timelineCompositionPackage.test.mjs`: public12 artifact path, byte/hash assertions, installed version, and manifest version. The existing resolver/export/shared-peer checks are unchanged.
4. `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`: the immutable release12 bytes. The old 0.0.10 artifact remains untouched.

No official client/runtime pin, generated metadata, provider, DTO, source, or root bundler configuration is part of this patch. The package remains opaque to App; package exports and consumer-root semantics come from the tarball and are not rewritten here.

## Immutable artifact identity

The copied artifact is the Composition release12 artifact from the release handoff (`5e06f401`, Composition full69PASS plus Agent theme equality):

```text
sha256: 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3
bytes:  58444
tar members: 77
sha512 integrity: sha512-490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==
```

The SHA-512 value above was derived from the artifact bytes, not copied from a lockfile. The release artifact's package manifest is `0.0.12`, ESM with `import`/`default` exports, and retains the existing peer tuple: React/React DOM 18.3.1 and Remotion 4.0.509 (including layout-utils/media).

## Default-theme test decision

The original implicit fallback assertion in `src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx` must be updated as an ordinary final expectation: no `it.fails`, xfail, or skip. [handoff-vw-m3-app12-implicit-default-tests.patch](./handoff-vw-m3-app12-implicit-default-tests.patch) updates both package-theme mocks and the fallback assertion to the new public default:

```text
id banodoco-default; fg #FAFAFA; bg #050814; accent #67E8F9
heading/body Arial; mono monospace; base/small/large 32/22/84
normal/bold 400/600; lineHeight 1.2; fadeMs 450; canvas 1920x1080@30
```

The existing explicit `2rp` assertions remain unchanged, so authored/explicit themes stay preserved. Other `theme: 'default'` tests found in the cohort do not assert the fallback palette; they do not need a decision update for this pin.

## Offline validation performed

- `git apply --check` and actual apply of the pin patch against a temporary archive of App `9d9101f…`: PASS.
- Semantic JSON/guard assertions on that temporary patched snapshot: PASS.
- `git apply --check` and actual apply of the implicit-default test patch against a temporary archive of the sequence test: PASS.
- Artifact SHA-256, derived SHA-512, byte count, and tar member count: PASS (`0a7b6152…`, `490yQt…`, `58444`, `77`).
- Product worktree status: clean.

No install, network, shared `node_modules` mutation, browser, socket, or full suite was used. Isolated Composition release12 ESM/SSR/strict-NodeNext/direct-default evidence remains the Composition release handoff's evidence; this App prep does not claim a fresh App dependency-graph run. After the owner applies the four-file change in a supported existing App install, run the targeted bundler guard and the sequence test; the owner may then perform the already-approved isolated packed-package checks without changing the shared install.
