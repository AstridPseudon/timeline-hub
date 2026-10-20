# Corrected parent-delete browser execution

Date: 2026-10-20

This records the required browser execution for the corrected two-case parent-delete source. It is an execution report, not a qualification or mergeretirement claim.

## Exact source tuple

- App final branch: `tl/app-m2-delete-corrected-two-case-browser-executor`
- App SHA: `40d73c1de77fd12e30b477de88fc411f3febf072`
- App tree: `d378ea776bf25d5a120df9a2eecb067eb8bc8ece`
- Agent SHA: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime SHA: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Public Composition: `0.0.12`, 77 files, `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- Runtime artifact count: 75
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`
- Launcher: `scripts/testing/current013-parent-delete.mjs`
- Cache identity: `parent-delete-treed378ea776bf25d5a120df9a2eecb067eb8bc8ece-agent8130a401bf44a518d5a40ae274d398b8c560be55-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnera71c71b3613f34d4b382a73959bf798271c7d646c380c011f1725a217e399bc7-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901`

## Central browser execution

Registered suite: `e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration`

Test ID: `app-m2-delete-corrected-two-case-browser-executor-e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration-1020154110-20541`

Exact central result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-delete-corrected-two-case-browser-executor-e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration-1020154110-20541/`

Result: exit 1 after 189 seconds; `1 passed`, `1 failed`.

The hosted bundle built successfully. Playwright collected and ran exactly the two parent-delete tests:

1. `M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip` — **failed**.
2. `M2 current013 parent DELETE conflict: same-property Agent move wins while the original delete request is held and draft is retained` — **passed** in 10.6s.

## Concrete product failure

The first case stopped at `tests/e2e/local/clip-delete-command.spec.ts:261`:

```text
expect((owner.intents[0].payload as { commands: unknown }).commands)
  .toEqual(request.commands)
```

The received owner intent omitted own `__proto__` keys that were present in the original request. The missing keys included:

- `parent/clip:f2-app-clip::value.__proto__.raw`
- `parent/clip:f2-app-clip::value.app.canonical.__proto__.literal`
- the corresponding nested `state.value` keys

The central log shows the exact deep-equality diff and failure:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-delete-corrected-two-case-browser-executor-e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration-1020154110-20541/log.txt`

The runner also emitted this Playwright trace location for the failed case:

`test-results/clip-delete/clip-delete-command-M2-cur-9193a-rse-restore-raw-opaque-clip/trace.zip`

Because the failure occurred before the independent Agent publication, lost-ACK recovery, Runtime restart, exact retry, and inverse restore assertions, those later first-case behaviors are unverified in this execution. The second case reached a passing result for the held same-property conflict and retained draft path.

No assertion was weakened, no command was injected, and no product fix was attempted after the concrete product failure.

## Commands

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-delete-corrected-two-case-browser-executor e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m2-delete-corrected-two-case-browser-executor-e2e-parent-delete-corrected-tree-d378ea7-agent8130-runtime2c4-e2e-integration-1020154110-20541
```

The authorized lane was registered with the final App SHA/tree and the frozen Agent/Runtime/public pins. No stale parent-delete suite was reused.
