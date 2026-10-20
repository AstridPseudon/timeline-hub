# App-owner application instructions

Run from the selected App `9d9101fef15470c813d060ed0169676fa7206c2e` worktree. These commands are instructions for the App owner; this worker did not run them in the product worktree.

```bash
cp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app12-pin-prep-artifact.tgz \
  vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
git apply /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-app12-pin-prep.patch
git diff --check
sha256sum vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz
openssl dgst -sha512 -binary vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz | base64 -w0
tar -tzf vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz | wc -l
node --test config/vite/timelineCompositionPackage.test.mjs
```

Expected artifact outputs are, respectively, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, SHA-512 base64 `490yQtC4k3cuBQJ4Aee5qEqOPNrlQrXPQkE0p6R8UDACAcT8amHe8EjCRI4vE+HtvXwUiy8zBjm7RcW7aTv9eA==`, and member count `77`.

Apply the separate [implicit-default test patch](./handoff-vw-m3-app12-implicit-default-tests.patch) in the same App source update. With the supported existing App dependency graph available, run the focused sequence test using the repo's normal Vitest command/config. Do not regenerate the lockfile or replace the tarball: the lock entry and artifact bytes are already exact.

The package-level ESM/SSR/strict-NodeNext/direct-default checks belong to the Composition release handoff and should be repeated only in the owner's supported isolated package context. No shared install, network install, browser, socket, or full suite is part of this handoff.
