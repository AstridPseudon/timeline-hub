# ap2-m2-selected-real-ui-journey-source

## Result

Blocked before source changes. The requested real hosted-App selected-PARAM journey cannot be seeded with a normal accepted P1 on the frozen Agent 8130 / Runtime 2c4 / App public13 tuple available to this worker.

The requested PLAN2/PLAN3/PLAN6 files were not present at the orchestrator scratchpad path; the available PLAN.md, selected handoffs, authority packet, brief, and latest App2 status were read instead.

The permitted files remain unchanged:

- `tests/e2e/local/three-products.spec.ts`
- `tests/e2e/local/support/harness.ts`

No synthetic Runtime document/object authority, test-injected capture port, native command mock, product change, pin change, or build flag was added.

## Exact prerequisite gap

1. The hosted App's static public13 catalog advertises `audio-reactive-colour` as `rendering/effect` revision `sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e` (`src/tools/video-editor/runtime/admitted-elements.ts` is explicit that hosted builds retain the compiled set and do not wait for runtime admission).
2. The normal Agent project-pack admission path in frozen Agent 8130 calls `element_definition_from_payload(... editable=True, priority=100 ...)` in `astrid/core/element/project_packs.py`. Computing the ordinary rendering source with the Agent catalog code gives revision `sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`, not public13's `sha256:2a9b...`.
3. Therefore a real project-pack snapshot accepted by the normal Agent admission path cannot be the exact descriptor the hosted PropertiesPanel needs. A hand-authored document claiming the public revision would be synthetic authority and would violate the task's explicit instruction to return the missing normal API/peer prerequisite.

The missing prerequisite is a normal published Agent/Runtime project-pack fixture (or a reviewed peer change that makes the published project-pack descriptor and public13 descriptor identical) for the selected P1. It must expose the exact accepted DocumentPin, snapshot object, descriptor revision, and current TS/native `clip.set-params` record inputs to the hosted App. No new App API or local validator should be introduced as a workaround.

## Checks run

- `node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts tests/e2e/local/support/harness.ts` — passed.
- `node_modules/.bin/playwright test tests/e2e/local/three-products.spec.ts --config=playwright.three-products.config.ts --list` — collected 9 existing tests; no browser, localhost, or socket run.
- `git diff --check` — passed; worktree has no source diff.
- `PYTHONPATH=/home/user/work/agent /usr/bin/python3 - <<'PY' ... load_element_definition(...); _element_revision(...) ... PY` — reproduced the normal Agent revisions: public-style `editable=False, priority=30` → `sha256:2a9...`; admission-style `editable=True, priority=100` → `sha256:8e3...`.

The targeted central suite was not requested because there is no commit-ready candidate and the required real P1 prerequisite is absent. No full, browser, localhost, live-socket, or uncommitted central suite was run.

## Decisions and next step

The settled plan's “do not synthesize authority” rule controls this outcome. Once Agent/Runtime publish a normal P1 fixture whose exact descriptor matches the frozen hosted catalog (or provide the reviewed published tuple), add the single minimal serial case to the two permitted files and request the exact central targeted three-products suite against the committed candidate.
