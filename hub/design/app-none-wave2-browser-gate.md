# App D01 Native None wave2 committed browser gate

## Result

The committed joined App candidate passed the central two-case browser gate:
**2/2**, exit 0, 173 seconds. This is the D01 transition-None serialization
retirement gate only; it is not whole-writer completion.

Exact source tuple:

- App: commit `b14bfda0db43e1225394b3e6a7f60ab0dd48cd58`, tree `c6e0d13cd7631b714a069790de9a930a554f8c03`.
- Agent: commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- App Composition: public13 archive `banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular files.
- Agent Composition: public12 archive `banodoco-timeline-composition-0.0.12.tgz`, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular files.
- Runtime producer: all 75 manifest artifacts matched the pinned Runtime2c4 manifest `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`.
- Public source attribution: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.

## Central evidence

Requested test ID:

`app-m2-none-wave2-committed-browser-gate-e2e-native-none-wave2-committed-b14bfda0-treec6e0d13c-agent8130-runtime2c4-public13-e2e-integration-1020172044-22648`

Suite:

`e2e-native-none-wave2-committed-b14bfda0-treec6e0d13c-agent8130-runtime2c4-public13-e2e-integration`

Commands:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  app-m2-none-wave2-committed-browser-gate \
  e2e-native-none-wave2-committed-b14bfda0-treec6e0d13c-agent8130-runtime2c4-public13-e2e-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  app-m2-none-wave2-committed-browser-gate-e2e-native-none-wave2-committed-b14bfda0-treec6e0d13c-agent8130-runtime2c4-public13-e2e-integration-1020172044-22648
```

Discovery selected exactly these two real UI cases in
`tests/e2e/local/three-products.spec.ts`:

1. Single clear: raw transition absence, reload, lost acknowledgement,
   Runtime restart, exact retry bytes/key/receipt, inverse, and zero legacy
   traffic.
2. Atomic bulk clear: one original-basis request, opaque/unknown revision
   preservation, retry/reload/inverse, real 409 conflict with the complete
   draft retained, and zero legacy traffic.

The strict runner passed the preflight and postflight guards for exact source
identities, App public13/9412 and Agent public12 archives/all77, Runtime all75,
peer versions, 65 pinned Astrid source files, 155 vendor source files, 20
public imports, private public13 overlay/cache isolation, Chromium 141, unset
direct-source overrides, and unchanged source/cache state after the run.

## Implementation boundary

The App worktree product source and two-case assertions were not changed. The
ORCH wrapper retargeted the established MAIN574/public13 strict runner only to
the joined App SHA/tree, its short private TMPDIR, and its own runner path.
No fixture injection, bypass, wire-shape change, stored state, skipped test,
weakened assertion, or expected-failure marker was added.

No full suite, project TSC, install, local browser/socket run, or frame/PCM
lane was run. The central named browser lane performed its normal hosted build.
Remaining SET/parameter/reset transition handlers are outside this None-clear
gate and remain separate work; this result does not claim their retirement.
