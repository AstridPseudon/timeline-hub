# D96 report — GLOBAL SCOPE FAIL

No product changes applied. The exact shared `12→14` harness patch is blocked by:

- `tests/e2e/local/three-products.p2-popup.spec.ts:280` (`native-none`) places a copied occurrence at `on: 12`.
- `occurrence.place-shared` copies `duration_ms`, producing old adjacent intervals `[0,12)` + `[12,24)`.
- With the proposed seed, this becomes overlapping `[0,14)` + `[12,26)` on `S1`.

Required follow-up: placement-only host-window parameter, default `12`, or a dedicated popup fixture. No narrower patch authored.

Direct caller inventory: 17 callers (18 `rg` matches including the helper definition).

| Caller | Mode / usage |
|---|---|
| `scripts/testing/d66-plain-stack.mjs:749` | Seed receipt/history smoke; no timing assertions. |
| `tests/e2e/local/auto-real-proxy.spec.ts:27` | Production child image placement; intended host-boundary consumer. |
| `tests/e2e/local/clip-delete-command.spec.ts:21` | Parent delete and closure membership; relational timing only. |
| `tests/e2e/local/parent-split-command.spec.ts:17` | Uses isolated split fixture; independent registry duration `12` at `:29`. |
| `tests/e2e/local/parent-trim-command.spec.ts:28` | Parent source-window trim; no occurrence extent. |
| `tests/e2e/local/public-trim-mounted-fixture.spec.ts:15` | Mounted parent trim; no occurrence extent. |
| `tests/e2e/local/shot-name-command.spec.ts:45` | Shot name/settings persistence; no timing. |
| `tests/e2e/local/three-products.live-edit-smoke.spec.ts:21` | Parent drag/Agent label; no occurrence extent. |
| `tests/e2e/local/three-products.mounted-readiness.spec.ts:97` | Readiness setup; no timing snapshot. |
| `tests/e2e/local/three-products.p2-elements-assets.spec.ts:46` | Production child drop snapped to `9`, hold `5`; intended consumer. |
| `tests/e2e/local/three-products.p2-popup.spec.ts:255` | Blocking `on:12` shared-occurrence adjacency dependency. |
| `tests/e2e/local/three-products.p2-tour.spec.ts:33` | Parent gestures/transitions; no occurrence extent. |
| `tests/e2e/local/three-products.spec.ts:60` | Main suite child drop; intended consumer; duplicate duration checked relationally. |
| `tests/e2e/local/three-products.spec.ts:2844` | Native transition-clear worker; no occurrence extent. |
| `tests/e2e/local/track-label-command.spec.ts:53` | Parent move/label/retry/undo; no timing. |
| `tests/integration/runtimeRestore.test.ts:47` | Restore-history integration; no extent. |
| `tests/integration/runtimeRestore.test.ts:122` | `referenceAt=3`; shot settings, not old 12-second extent. |

Evidence map: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-D96-caller-audit-apply-0403/evidence/map/caller-map.md`

Checks:

- Patch SHA: `6378b5b4…e4a`
- Base harness SHA: `92f1261b…956`
- Private scratch application reproduced proposed SHA: `84563009…6809`
- `git apply --check --whitespace=error`: passed
- `git apply --numstat`: `5 5`
- `git diff --check`, `git diff --exit-code`: passed
- Worktree remains clean.
- Node, TypeScript, ESLint, and focused tests not run because the conditional application route failed global scope.

`BLOCKED` and commit message files were created; no `DONE` marker.