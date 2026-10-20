# Gate 6 current-cohort frame readiness audit

Verdict: **HOLD for launch preparation; the existing `--ready` refusal is correct.**
This is a source/readiness audit only. No product source, branch, dependency, cache,
browser, socket, grant, install, render, or full suite was changed or run.

## One-screen launch handoff

Reviewed held cohort (do not merge wholesale):

- App review candidate `e26079c440d09d7712588581e369204b3e035db9`, tree
  `e523fc0dc76eeff03a68f3cdb59e78a8b6b55798`; parent/source cohort
  `cc9c77b1f235d831200e629fe7ad253c084faf4f`, tree
  `23775814910b625e8e274c1cff320792261faf13`. Discovery is exactly five
  `native-codec-chrome155` cases; the reviewed record covers the four actual
  normal-MP4 cases plus the tab case.
- Held controller Node: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`,
  `v20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Current source identities inspected read-only:
  - App integration `9d518546df880ec515f2f424c55073193f2a2e64`, tree
    `9b3a0a813e9731a60493d94e66e63da7a68ce4d2`.
  - App public13 owner unit `d08e969b07f01ea013585fe8ed746e92b6b8a9a9`, tree
    `be033455c82b47e47d2786f40aa5ade38a1223aa`.
  - App stored-cap correction `3a4350f9d9a578f817568d5fe348c5d750595129`, tree
    `24b051ff0f580f0d6b84950ba03a9fb8d11afe47` — **pending; do not assume landed**.
  - Native fixture source unit `e4c7a3792e879d22eada87a8cd3b7e9550c4a470`, tree
    `e43c4c34107bb474beb5e86e669cb4d75d961e7a`; the same files are in held
    `e26079c44`.
  - Agent integration `30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`, tree
    `50925d6df67ce717653e3ce7ac12803f8865da93`, using Composition public12.
  - Runtime integration `/home/user/work/runtime`, `a51af885ea631c695a857985239c7fe7bf2e871f`,
    tree `7c6ab6700307309a7942e64eb4d0c6c7cc42b681`, contract `0.2.13`.
  - Composition public13 release: source `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`,
    tree `13e375534fffd704305eced5686699d2c8c9c948`, archive SHA-256
    `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
    Agent30fc's normal public12 artifact remains SHA-256
    `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

Minimal clean launch input is a new private App snapshot containing the current
9d518 base plus public13 `d08e969b0`, the pending cap correction once landed,
the reviewed native-fixture unit (`e4c7a3792` files below), and the held
controller/test leaf from `e26079c44`. Keep all shared App dependencies read-only;
use the existing clean private App12 dependency graph at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules`
and the retained Node above. `/home/user/work/app` is not a launch root: it is
currently `590c19795111fd1891bbd50a5f8d48bef3505a26` and has untracked vendor
entries.

Required App source/config surface is already present in the current owner source
for normal Render and frame capture: `tests/e2e/timeline/player-export-frame-parity.spec.ts`,
`tests/e2e/timeline/viewing-parity/cases.ts` (blob `af897e57…`),
`tests/e2e/timeline/viewing-parity/frames.ts` (blob `97675623…`),
`tests/e2e/timeline/viewing-parity/fixture.ts`, `harness.ts`,
`tests/e2e/local/support/harness.ts`, and
`playwright.viewing-parity.native-codec.config.ts`. The current source includes
the normal `App Render action` case, `capturePlayerFrame`/`decodeExportFrame`,
the `Rendered film` dialog, and the `Play last render` restoration path. The
native fixture is specifically `tests/e2e/timeline/viewing-parity/native-fixture-helper.py`
plus `native-fixture.integration.test.ts` from `e4c7a3792`; those two files are
not in 9d518/d08e until the owner port lands. No old 320-era helper was imported
or blind-ported.

For the eventual central launcher, bind these exact absolute inputs in its literal
command/cache identity (paths below are the existing current integration roots;
the App root must be the new clean snapshot):

```text
ASTRID_CHECKOUT=/home/user/work/agent
ASTRID_PUBLIC_CHECKOUT=/home/user/work/agent
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
TIMELINE_BUNDLE_AGENT_HEAD=30fc8dd154015a7c58cf4ce7b065ccc46f470ee8
TIMELINE_BUNDLE_RUNTIME_HEAD=a51af885ea631c695a857985239c7fe7bf2e871f
ASTRID_REMOTION_PROJECT_DIR=<private Agent public12 Remotion graph>
ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
VIEWING_FRAME_SOURCE_TUPLE=<fresh tuple for this exact App/Agent/Runtime/Composition set>
TIMELINE_COMPOSITION_CHECKOUT=<source root named by that tuple>
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/google/chrome/chrome
```

The standing guards remain: App/Agent/Runtime source cleanliness and exact trees;
private physical dependency graphs; all 77 Composition members; pinned Node and
Chrome executable/tree identities; five-case offline discovery; the 10 GiB disk
floor; owned short `/tmp` and flock/resource guards; source pre/post identity;
and a fresh grant plus one-shot marker. App13 adoption must be explicit first;
Agent13 adoption remains second and is not automatic.

Exact retained environment guard values are Node `v20.19.4` / SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490` and Chrome
`155.0.8059.84` at `/opt/google/chrome/chrome`, executable SHA-256
`cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`, full-tree
SHA-256 `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`,
255 files. The central lane must serialize with
`flock -w 600 /home/user/work/.app-m1-browser.lock`; the controller's standing
free-disk floor is `10 * 1024**3` bytes.

## True blockers vs stale holds

True launch blockers:

1. The cap correction `3a4350f9d` is still pending.
2. The native fixture e4c source unit is not in current App 9d518/d08e; its
   owner port must land in the clean App snapshot.
3. The current Agent is public12 (`30fc…`), while the held controller expects a
   different Agent13/Runtime13 tuple. The manager must freeze a new exact current
   tuple and source-tuple file; no existing grant can be reused.
4. `/home/user/work/app` is not a clean 9d518 launch root. Create/retain a clean
   private snapshot after the owner units land.

Stale/non-blocking holds:

- The held controller's `APP13.status = pending-consumer-adoption` and its
  `--ready` refusal are intentional sequencing, not a controller defect.
- The prior d874/public-source build failure is evidence for that old frozen pair
  only; it is not a normal-render failure claim for current Agent30fc.
- The reviewed `e260/sourcecc9` cohort remains a test-only qualification
  candidate, not an adoption or merge source.

No normal Render, native fixture HTTP, browser, PCM, or failure claim was made by
this audit. The manager may launch the next central qualification only after the
four true blockers are resolved and the literal tuple/guard file is refreshed.

## Pure evidence

- `node --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs` — exit 0.
- `node --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs` — exit 0; TAP pass.
- Held `--ready <App> /home/user/work/agent /home/user/work/runtime` — exit 1 at
  `App13 consumer adoption is pending; --ready remains refused`, before graph,
  Chrome, discovery, preflight, or grant checks.
- Offline `--discover` from a private archived App snapshot with the clean App12
  dependency graph — exit 0, `discovered exactly five native-codec-chrome155 parity cases`.
- Read-only `git show`/tree and source-content checks — passed for every identity
  and source path listed above.

Not run: browser/render/capture/PCM, localhost or live sockets, install/network,
full/central suite, grant, or automatic adoption.
