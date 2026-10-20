# AP2-M2 bootstrap approved-scope real gate

## Result

Blocked: the single authorized central bootstrap-only integration run failed before project creation was observed. No retry was submitted.

## Changes

- Ported only the ce47 bootstrap scope-race repair onto current HOME:
  - exact normal `POST /v1/projects` response matching by submitted name, status 201, response project ID/name, and exact URL wait;
  - retained strict `{ realmId, projectId, timelineId }` equality and added the created-project URL assertion;
  - added the approved scope helper and three-case regression;
  - added the approved wrapper unchanged.
- Preserved later ordinary/trim/selected rows and assertions. No generic/trim file was copied and no e2e spec was replaced wholesale.
- The three repaired source files and wrapper are byte-identical to the approved ce47 source. Hashes:
  - `three-products.spec.ts`: `fda4df2030ff09d8c6606611c84f5ed761ca4cf7836190903348c579d95a08f6`
  - `timeline-scope.ts`: `a2965d220628de15bb169baff96dd1db020248d3df727ea6e2d83640b17346ab`
  - `timeline-scope.test.ts`: `71e73fd4fc59ae5079144518d1aa0d0be5fa1818e3b9c9e7c529b037527175ee`

## Checks

Passed:

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — 3 subtests passed.
- Playwright list with the bootstrap grep — exactly 1 test in 1 file.
- ESLint on the three repaired TypeScript files.
- `npm run typecheck:strict-islands`.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit`.
- `sh -n tests/e2e/local/support/bootstrap-wrapper-selector-source-fix.sh`.
- `git diff --check`.
- Reused unchanged custody evidence: 128 App + 12 native tests passed, as recorded by the approved custody report; not rerun.

Central run (exact private Agent3c4/Runtime202/a0/f021/6ba/Composition13 tuple):

`ap2-m2-bootstrap-wrapper-selector-source-fix-integration` — failed, exit 1, one test.

The wrapper passed source identity, artifact/lock checks, private graph setup, exact one-test selection, and hosted build. The browser test then timed out after 90 seconds at `page.waitForResponse` for the normal named `POST /v1/projects` response (`three-products.spec.ts:1354`). Retained sanitized evidence contains only `beforeCreate`; no `projectCreate`, reservation, selected scope, retry, restart, inverse, or cleanup evidence was produced.

Retained evidence: `scratchpad/orch/workers/ap2-m2-bootstrap-project-scope-causal-repair/scope-evidence/bootstrap-scope.json`.

## Decisions / blockers

The failure is not silently retried and no assertion or process change was made. The real gate is unverified; therefore no dead-writer cut and no public014 adoption claim were prepared.

Recommended next step: investigate why this exact normal project-create response is absent in the locked central harness, then obtain review before any process or assertion change and schedule a fresh authorized gate.
