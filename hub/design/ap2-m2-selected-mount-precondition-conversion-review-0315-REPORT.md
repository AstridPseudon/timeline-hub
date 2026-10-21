# M2 selected DEV mount-precondition conversion review

## Verdict

APPROVE the exact source commit `b9a5ecd91d0235a9958af258e2cd5b1504687332` with
tree `ec5791f3c0d05d3a6934d72a77f03da5a49ea94f`.

This is within the requested test-conversion scope. It changes only
`tests/e2e/local/three-products.selected-param-dev.spec.ts`.

## Review findings

- The original `expectConnected(page)` startup waits were at three positions:
  immediately after `page.goto()`, after the first existing reload following
  P2/source removal, and after the second existing reload before draft
  recovery. The source replaces those exact three calls with
  `expectAppMounted(page)`.
- `expectAppMounted` waits only for the first child of the existing empty
  `#root` to attach, using `STARTUP = { timeout: 20_000 }`. The original
  `expectConnected` helper uses the same 20-second timeout. No timeout budget
  was increased.
- This is a real startup/mount precondition, not a semantic-failure
  workaround. `index.html` starts with an empty `#root`; `src/app/main.tsx`
  renders into it only after existing startup work; and `src/app/bootLayer.ts`
  already observes non-empty root content as part of its first-frame readiness.
  The retained `openSeededTimeline` and selected assertions remain responsible
  for workspace and data readiness.
- Same-origin DEV does not render the status pill: the existing
  `RuntimeConnectionProvider` sets `gated` false when there is no runtime
  origin, and `RuntimeConnectionGate` returns its children directly in that
  case. The hosted `expectConnected` helper and its other callers are
  unchanged.
- The mount helper is not used as timeline, clip, parameter, or P1 authority.
  The source retains the exact selected timeline, clip, params, P1 schema-pin,
  P2/removal, refusal, draft, lost-ACK, restart/reload, request body and key,
  undo, and zero-legacy assertions. It retains the original two
  `page.reload()` calls. The added timeline/clip/params checks at the final
  reload close the previously identified readiness gap before recovery.
- No new DOM hook, readiness flag, navigation, reload, retry, recovery action,
  or product/bootstrap/route/shared-harness change was introduced.

## Exact baseline mapping

| Original boundary | Original precondition | Reviewed source |
| --- | --- | --- |
| Initial startup | `page.goto()` then `expectConnected(page)` | same `page.goto()` then `expectAppMounted(page)` at line 53 |
| P2/source removal | existing first `page.reload()` then `expectConnected(page)` | same reload then `expectAppMounted(page)` at line 74 |
| Lost-ACK restart | existing second `page.reload()` then `expectConnected(page)` | same reload then `expectAppMounted(page)` at line 106 |

The pre-conversion source was `7db1752ca`; the immediate source parent is the
approved readiness tree `a0a73dae3`. `git diff a0a73dae3..b9a5ecd91` reports one
changed path only, with the three connection calls replaced and the final
reload's retained selected-surface assertions restored.

## Checks run

All checks were read-only and used an isolated export of the exact source tree;
shared `node_modules` remained read-only.

- `git diff --check a0a73dae3 tl/ap2-m2-selected-existing-mount-precondition-source-0311` — passed.
- `npm exec -- eslint --no-cache tests/e2e/local/three-products.selected-param-dev.spec.ts` — passed.
- `npm exec -- playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — passed; exactly 1 test in 1 file.

Not run: browser execution, localhost/live sockets, central actual gate, or
any full suite, per the task. The source report also records that no dedicated
Vite child stderr artifact is available; retained diagnostics are the driver
stderr, trace ZIP, and error context. Actual selected-case qualification is
therefore still pending the central test service.

## Decision / next step

No defect found and no source correction requested. The orchestrator may use
this exact commit/tree for the one authorized central selected DEV run. If it
fails before `#root` mounts, diagnose the cold DEV bootstrap/module graph; do
not increase this fixture timeout or add recovery behavior.
