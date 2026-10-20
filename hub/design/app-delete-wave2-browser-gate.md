# App M2 committed wave2 parent-delete browser gate

## Result

**BLOCKED: the committed two-case browser gate did not qualify parent DELETE.**

Central TestID:
`app-m2-delete-wave2-committed-browser-gate-e2e-parent-delete-wave2-committed-tree92fd62-agent8130-runtime2c4-e2e-integration-1020172111-5045`

The source/public13/peer/cache guards passed, but the first browser case failed
before an accepted commit. The runner stopped on first product failure, so the
409 conflict case was not executed in this run.

## Exact source tuple

- App commit `00ac733de23fc896c434eff1965fc265542aaade`, tree
  `92fd62f4adecdb3f93acf92a5444bf035d6aa19e`.
- Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime and producer peer commit
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Composition public13 archive SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  exactly 77 regular files.
- Runtime manifest: 75 artifacts. Chromium: 141.0.7390.37, SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.

## Browser evidence

Command registered with the central service:

```text
e2e-parent-delete-wave2-committed-tree92fd62-agent8130-runtime2c4-e2e-integration
```

The dedicated runner reused the established two-case wrapper and ran only:

1. `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip`
2. `M2 current013 parent DELETE conflict: same-property Agent move wins while the original delete request is held and draft is retained`

Case 1 failed at `tests/e2e/local/clip-delete-command.spec.ts:211`:
`expect.poll(() => wire.posts.length).toBe(1)` received `0` after the test
asserted selection, focused the actual production `.clip-action` button, and
sent the real `Delete` key. The test uses no command injection or production
bypass. Case 2 was not run because the wrapper stops on the first failure.

The runner’s all-77 public13 archive/install, Agent/Runtime source and peer,
75-artifact, Chromium, and cache pre/post checks passed. Source postflight also
passed after the failed browser case.

The group behavior at `src/tools/video-editor/hooks/useClipEditing.test.ts:261`
is unchanged. No all-delete retirement claim is made. Raw deletion, opaque and
mirror preservation, reload/undo, lost-ACK restart/retry, exact key/body/receipt,
409 kept-draft/recovery, and zero-legacy qualification remain unproven because
the first UI request was never emitted.

## Local controls

```text
NODE_OPTIONS=--experimental-vm-modules node --test scripts/testing/current013-parent-delete.test.mjs scripts/testing/current013-integration.test.mjs
  PASS: 2 files, all subtests

node --check notes/parent-delete-public13-runner.mjs
bash -n notes/run-parent-delete-public13.sh
git diff --check
  PASS
```

No full suite, local browser/socket run, install, project typecheck, or product
source edit was performed.

## Next step

Resolve why the committed wave2 production path emits no Runtime commit after
the real focused Delete action, then rerun this exact two-case central suite on
the resulting committed tree. Do not relabel this failed run as a delete pass
or retire legacy writers from it.
