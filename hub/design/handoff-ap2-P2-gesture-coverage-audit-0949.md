# Handoff: ap2-P2 gesture coverage audit

## Verdict

**FAIL for whole-tour coverage; PASS only for bounded source inventory.**

App base is `ff2d3c1d76c454f0402e48a42335d466a853cfe1`, tree
`84634e56df1aa205405e4a9301a8e6d3bd274f6f`. The existing P2 spec blob is
`45a8088fafd72a462409e444c0294e8a35682a0f`; discovery lists exactly three
selectors: parent move, transition-None single, and transition-None bulk.
Those are source-ready but no body execution was performed, so they are not
behavior credit and do not prove the complete gesture tour.

Real mounted/Runtime body sources exist for split, trim, move, and transitions.
Automatic placement has a real adjacent operation-proxy body but lacks the
full canonical `/commits` and Runtime old-route assertions. Popup add, popup
swap, selected-child popup editing, shared occurrence fork, element editing,
and registerAsset have only mocked/service/component coverage. The real
occurrence duplicate body is not a substitute for the promised fork-plus-media
popup path. P3 Gate-5 is a distinct move/doc.patch journey and must not be
double-counted as A3 family coverage.

## Exact evidence

The detailed matrix, exact existing test names, C0 boundary, concrete missing
case collection, limits, and commands are in the worker report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-gesture-coverage-audit-0949/report.md`

Key static results:

- P2 Playwright `--list`: **PASS**, exactly 3 selectors.
- Scoped ESLint over P1/P2/P3/core and A3 source/spec files: **PASS**.
- `git diff --check`: **PASS**.

## Required next collection

Run the three existing P2 bodies through the central service after owner
authorization, then collect real mounted popup ADD/SWAP, selected-child/fork,
element, and registerAsset bodies through the current save owner. Each must
retain exact v2 request/reply/history checks, intended canonical delta,
browser plus Runtime old-route proof, reload, and guarded inverse. Qualify or
strengthen the existing automatic-placement body for the same full contract.

## Limits

No browser, HTTP, Runtime/socket/service, build, full suite, or central
test-service run was made. No product, test, fixture, generated, pin, lock,
package, ops, or shared-install file was changed.
