# ap2-m2-selected-seam-race-repair

## Result

Repaired the shared selected-PARAM seam proposal on current App root `0034cc30e`.

- The hook now forwards the complete accepted `canonicalDocument` and existing `graph` to the approved resolver, so occurrence ownership can be checked against the existing materialization.
- The hook publishes a retained basis only after its head/project/timeline fence passes, clears it before loading and on failure/teardown, and requires the pre-read head to remain unchanged before accepting an async poll result.
- Runtime retained document/object reads preserve the original pin, client, session slot, and negotiated identity across the async read.
- Runtime history pagination validates every page head before dereferencing it, freezes the first head, rejects cursor cycles/head drift, and raises the existing visible schema-incompatibility error for malformed heads.
- Added focused malformed-first/later-page refusal controls and a graph-only occurrence positive. No original-pin policy, DTO/store/cache/browser validator, source refresh, or production PropertiesPanel activation was added.

## Evidence

- `TMPDIR=/tmp/ap2-m2-selected-seam-race-repair-tmp node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/selectedParamAuthority.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/integrations/runtime/client.test.ts src/tools/video-editor/data/DataProvider.test.ts` — **149 passed**.
- `/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider /home/user/work/agent/tests/sdk/test_timeline_selected_param_authority.py` — **27 passed** (read-only native integration tree; HEAD `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1`).
- `npm run typecheck:strict-islands -- --pretty false` — **passed**.
- `node node_modules/eslint/bin/eslint.js --max-warnings 0 src/integrations/runtime/client.ts src/integrations/runtime/dataProvider.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/data/DataProvider.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/commands/selectedParamAuthority.ts` — **passed**.
- Forward `git apply --check --whitespace=error-all` against an archived clean `HEAD` tree — **passed**; `git diff --check` — **passed**.

The packet's separate 181/19 combined selected-session lanes are not present on this assigned current-root base, so they were not claimed or recreated here. No full, browser, localhost, live-socket, or e2e suite was run.

## Handoff

Flat patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-seam-race-repair.patch`

The shared DataProvider/provider changes remain a private proposal for the App final join. PropertiesPanel/production PARAM wiring remains unclaimed; native PARAM production proof is not implied by prop or resolver wiring.
