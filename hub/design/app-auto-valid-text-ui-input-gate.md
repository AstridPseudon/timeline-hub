# App automatic placement gate: valid text UI input

Status: implementation complete; the strict browser gate remains unqualified because the frozen cohort's real generation composer timed out before task admission.

## Scope and source tuple

This slice changes only `tests/e2e/local/auto-real-proxy.spec.ts` in App, based on the exact diagnosis that the prior gate selected By reference without a reference image and returned during validation before `prepare` / `taskEventsReady`. It keeps the existing single-case real operation-proxy gate and its downstream task, media, commit, reconnect, lost-ACK, reload, undo, and legacy-POST assertions.

The central runs used the settled frozen tuple:

- Agent `origin/codex/handover-timeline-r4-20261019-candidate-sdk` at `8130a401bf44a518d5a40ae274d398b8c560be55`.
- Runtime `origin/codex/handover-timeline-r4-20261019-candidate-runtime` at `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Composition public12 artifact from the R4 candidate.

No Agent, Runtime, Composition, or product code was changed. No cursor, poller, readiness, store, list-events adapter, or fake capability was added.

## Test setup correction

The test now uses a source-specific `chooseTextGeneration` wrapper that explicitly selects the production `Just text` radio and the registered text model, then fills the existing managed prompt with `a deterministic one-pixel test image`. The original approval checkbox assertion remains unchecked before check and checked afterward. The raw target uses the seeded occurrence's authored `V2` lane, not the parent occurrence's `S1` lane; the canonical readback assertion uses the same lane.

The existing temporary GenericPackHost fixture now advertises nonzero scratch/output estimates for its real one-pixel result. This satisfies the existing producer-admission guard without changing capability resolution or creating a fake capability.

## Verification

Direct targeted checks:

- `node node_modules/eslint/bin/eslint.js --no-cache playwright.auto-real-proxy.config.ts tests/e2e/local/auto-real-proxy.spec.ts` — passed.
- `git diff --check` — passed.
- `env -u ASTRID_CHECKOUT -u ASTRID_PUBLIC_CHECKOUT NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs NODE_COMPILE_CACHE=/tmp/app-m2-auto-valid-text-ui-input-gate-node-cache node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/operationHost.test.ts src/shared/components/ImageGenerationForm/hooks/useFormSubmission.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts` — 3 files, 73 tests passed.

Central strict gate runs, all on the frozen tuple:

| Run | Result | Terminal boundary |
| --- | --- | --- |
| `1020182125-10248` | failed | Invalid seeded lane `S1`; corrected to authored `V2`. |
| `1020182434-25305` | failed | Unregistered default model `qwen-image`; corrected to the registered text model. |
| `1020182747-3114` | failed | Missing nonzero storage estimates; corrected in the real pack fixture. |
| `1020183009-14016` | failed | Real `/api/astrid/generation/compose` timed out after 10 seconds before `/v1/tasks`. |

The final run reached the real compose POST and continued valid numeric-cursor event polling, but no task reservation or admission occurred. The remaining timeout is in the frozen App-side composer helper; bypassing it or stubbing its response would violate the strict real gate and the task scope.

Recommended next step: provide a healthy frozen-cohort composer/runtime setup or rerun this unchanged gate against the later current-root source when that source is authorized. Do not add a test bypass for `/api/astrid/generation/compose`.
