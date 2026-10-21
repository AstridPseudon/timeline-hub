# App D01 settings.prompt native proof source (r43)

Status: source staged only. Do not activate or claim the browser proof until the
exact safety review and the actual same-fixture run both complete.

## Exact source

- `tests/e2e/local/shot-name-command.spec.ts`
- New case: `M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime`
- Existing `SettingsAutoDisable` case and all of its assertions remain unchanged.
- The case reuses `settingsSeed`, `openParent`, `openEmbeddedCanonicalShot`,
  `rawSettingsShot`, `observeTraffic`, `waitForPost`, `commandOutboxes`, and the
  existing Runtime restart/recovery controls. It adds no fixture/schema copy,
  writer, Provider mock, state carrier, or test hook.

## Intended assertions

The mounted prompt edit must emit one occurrence-owned native `shot.set` with
`settings.prompt`, the exact base head/publication, and no legacy save. The raw
shot readback must retain `negativePrompt: null`, the present opaque
`x_settings_opaque` object, and the rest of the raw shot closure. After reload,
the second prompt acceptance is held after Runtime acceptance, then its exact
request body and idempotency key must survive outbox recovery and Runtime
restart. The Runtime inverse must restore the first accepted prompt while
retaining the same raw null/presence/opaque fields.

The normal GUI does not currently expose a distinct clear control in canonical
embedded mode (`canonicalOnly` omits the generation/settings form). No control
or semantics is invented here: explicit null/absent/clear remains covered by
the existing direct native capture tests, while this source case is limited to
the real mounted prompt callback and string edit.

Source-only checks run for this staging change:

```sh
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/shot-name-command.spec.ts
git diff --check
```

Both passed. The browser case, localhost/live-socket journey, build, install,
graph, and full suite were not run by this task.

## Same-fixture Main command proposal (not run here)

Run exactly one browser case against the frozen published014 Agent/Runtime
tuple, with the existing settings fixture and private dependency graph:

```sh
TIMELINE_MAIN95_PROMPT_RUN=1 \
TIMELINE_MAIN95_PROMPT_APP_TREE=<exact-source-tree> \
TIMELINE_MAIN95_PROMPT_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
TIMELINE_MAIN95_PROMPT_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
TIMELINE_MAIN95_PROMPT_RUNNER_SHA256=<exact-runner-sha256> \
ASTRID_CHECKOUT=/home/user/peteromallet/astrid-agent \
ASTRID_RUNTIME_CHECKOUT=/home/user/banodoco/banodoco-workspace-runtime \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
TIMELINE_MAIN95_PROMPT_VENDOR_CHECKOUT=/home/user/work/app \
TIMELINE_MAIN95_PROMPT_RUNTIME_PRODUCER_CHECKOUT=/home/user/banodoco/banodoco-workspace-runtime \
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
TIMELINE_MAIN95_PROMPT_PRIVATE13_NODE_MODULES=<private-13-node-modules> \
TIMELINE_MAIN95_PROMPT_PRIVATE13_READY=<private-13-ready-file> \
./node_modules/.bin/playwright test --config playwright.shot-name.config.ts \
  --grep "M2 real embedded settings prompt: native shot.set preserves exact raw settings, retries after restart, and undoes through Runtime"
```

The command is a concrete proposal only; replace placeholders with the exact
central snapshot values and run through the orchestrator test service. Do not
claim activation, approval, or accepted browser evidence from this source-only
stage.
