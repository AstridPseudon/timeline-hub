## App M0 loopback validation

Completed the authorized Linux socket/process rerun. No tracked repo changes; HEAD remains `850763dfc269a34edf8dcdf38c630033c26ecdd8`.

Probes passed:

- Local HTTP bind and round-trip: HTTP 200, `loopback-ok`.
- `execFileSync("node", ["--version"])`: `v22.22.0`.
- `execFileSync("git", ["--version"])`: `git version 2.43.0`.

Logs: [probes.log](/tmp/app-m0-loopback/probes.log), [vitest-targeted.log](/tmp/app-m0-loopback/vitest-targeted.log).

Command:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/runtime/processes/astridAcpBridge.test.ts src/integrations/paired/pairedTransport.test.ts src/tools/video-editor/examples/extensions/__tests__/process-runtime-canary.integration.test.tsx src/tools/video-editor/runtime/processes/ProcessManager.integration.test.ts src/integrations/runtime/vendorLock.test.ts src/tools/video-editor/runtime/processes/processFixture.test.ts src/tools/video-editor/data/astridBridgeProxyPolicy.test.ts src/tools/video-editor/runtime/project-element-selection.test.ts src/integrations/paired/objectCachePolicy.test.ts src/integrations/astrid/transport.test.ts src/tools/video-editor/runtime/element-admission-build.test.ts
```

Selected exactly:

- `src/tools/video-editor/runtime/processes/astridAcpBridge.test.ts`
- `src/integrations/paired/pairedTransport.test.ts`
- `src/tools/video-editor/examples/extensions/__tests__/process-runtime-canary.integration.test.tsx`
- `src/tools/video-editor/runtime/processes/ProcessManager.integration.test.ts`
- `src/integrations/runtime/vendorLock.test.ts`
- `src/tools/video-editor/runtime/processes/processFixture.test.ts`
- `src/tools/video-editor/data/astridBridgeProxyPolicy.test.ts`
- `src/tools/video-editor/runtime/project-element-selection.test.ts`
- `src/integrations/paired/objectCachePolicy.test.ts`
- `src/integrations/astrid/transport.test.ts`
- `src/tools/video-editor/runtime/element-admission-build.test.ts`

Result: exit `0`; 11/11 files passed; 115/115 tests passed; 0 skipped; 0 unhandled errors; Vitest duration `18.33s`.

The original restricted full baseline remains not green: `17,954 passed / 56 failed / 24 errors` in 1,447 files, `2,384.29s`, exit `1`. The frozen 50 socket/IPC/process failures all pass with socket access. Six unrelated assertion failures remain unaddressed. macOS and the three-products e2e journey were not run.

Updated [app-baseline.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-baseline.md) and wrote the required commit message. Recommended next step: manager may merge the original listener-fix branch; separately triage the six unrelated baseline failures.