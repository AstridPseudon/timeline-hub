# App native-None own-JSON final browser executor

Date: 2026-10-20

## Source under qualification

- App commit: `46c15aee5fd08aa71a49b0378eb694491f8482da`
- App tree: `93042fb19a46d121a9a843a75a9fe85b426fe67a`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime/producer: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- public12 Composition archive: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- tracked public source: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Chromium: `141.0.7390.37`, SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`

The App source change is the completed own-data/JSON-boundary fix: authored dynamic leaves use own enumerable data properties, and the read-only browser outbox helper returns JSON bytes before Node parses them. No further product or behavior-test changes were made here.

## Targeted evidence

```text
TMPDIR=/tmp/tl-none-local-93042 XDG_CACHE_HOME=/tmp/tl-none-local-93042-cache \
  npm exec vitest -- run --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/clipScalarCapture.test.ts \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx
```

Result: **3 files, 43 tests passed**. `git diff --check` passed. An initial attempt with `--configLoader=runner --no-cache` hit the repository config's existing `__dirname` incompatibility; the normal bundled Vitest loader then passed, with no shared-cache changes observed.

## Central browser qualification

The source-specific suite was registered in `ORCH/tests/suites.conf` as:

```text
e2e-native-none-own-json-final-v2-93042-agent8130-runtime2c4-public12-e2e-integration
```

The exact central request and wait were:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  app-m2-none-own-json-final-browser-executor \
  e2e-native-none-own-json-final-v2-93042-agent8130-runtime2c4-public12-e2e-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  app-m2-none-own-json-final-browser-executor-e2e-native-none-own-json-final-v2-93042-agent8130-runtime2c4-public12-e2e-integration-1020155632-24451
```

Final TestID:

```text
app-m2-none-own-json-final-browser-executor-e2e-native-none-own-json-final-v2-93042-agent8130-runtime2c4-public12-e2e-integration-1020155632-24451
```

Final result: **PASS, exit 0, 180 seconds, 2 passed**.

The central command ran the normal hosted build and the exact grep `M2 native None`. Discovery selected exactly two tests:

1. `three-products.spec.ts:1388` — single native `None`: raw absence, reload, lost ACK, Runtime restart, exact retry body/key/receipt, inverse, and zero legacy traffic.
2. `three-products.spec.ts:1464` — bulk native `None`: one atomic original-basis clear, unknown revision/opaque data preservation, retry, reload, inverse, real 409 conflict, retained draft, and zero legacy traffic.

Both passed. Preflight and postflight passed exact full-SHA/tree guards, Agent8130/Runtime2c4, all 75 Runtime artifacts, public12/all 77 archive files, React/Remotion peers, private cache isolation, Chrome141, source cleanliness, and unset `ASTRID_PUBLIC_CHECKOUT`/`ASTRID_APP_DIRECT_DIST`. The log also records 65 pinned Astrid source files and 155 vendor source files verified.

## Setup-only attempts

- TestID `app-m2-none-own-json-final-browser-executor-e2e-native-none-own-json-final-93042-agent8130-runtime2c4-public12-e2e-integration-1020155412-17296`: failed before build/browser because the generated runner initially placed `prepare-overlay.py` below its generated directory while the reused strict runner looked at the worker root.
- TestID `app-m2-none-own-json-final-browser-executor-e2e-native-none-own-json-final-93042-agent8130-runtime2c4-public12-e2e-integration-1020155455-5795`: same source-tree result was rerun before the cache identity was changed and failed with the same setup-only path error.

These attempts selected no browser case and are not product evidence. The runner was corrected, then the v2 literal suite was used because the central service caches an exact source-tree/suite result.

## Limits and next steps

No full suite, project TypeScript check, install, frame/PCM lane, or integration merge was run. The final two-case native-None browser gate is qualified on this exact source tuple; integration remains manager-owned and frozen for the Track Inspector port.
