# Verification commands

Run from the current App worker worktree with the retained Node20 executable:

```sh
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
"$NODE" --version
sha256sum "$NODE"
"$NODE" --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
"$NODE" --test scripts/testing/current013-integration.test.mjs
"$NODE" --import tsx --test tests/e2e/timeline/viewing-parity/source-tuple.test.ts
"$NODE" tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --discover "$PWD"
"$NODE" node_modules/@playwright/test/cli.js test --config playwright.viewing-parity.native-codec.config.ts --list
```

Observed: Node `v20.19.4` with SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`;
controller, integration, and source-tuple tests pass; discovery finds exactly
five cases; Playwright lists 5 tests in 1 file. The Runtime owner evidence is
the referenced 143-pass compatibility audit.
