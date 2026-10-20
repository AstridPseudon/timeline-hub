# AP2-M2 bootstrap scoped-audit central gate

## Result

**NOT QUALIFIED — the one central bootstrap run failed at the first created-project scope assertion.**

The committed helper is `252da0590a0806839c790328e50b210030baab0e` (tree
`0ec60cc85b444520b19a2963ff56347b3d2ad1b5`). The request used target
`ap2-m2-bootstrap-explicit-scope-helper-fix` exactly:

```text
ap2-m2-bootstrap-explicit-scope-helper-fix-ap2-m2-bootstrap-scoped-audit-central-gate-1020215432-17076
```

The private normal014 driver selected exactly one test before building, built
the hosted App successfully, and ran only:

```text
tests/e2e/local/three-products.spec.ts
  --grep "bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo"
```

The first failure was:

```text
tests/e2e/local/three-products.spec.ts:1176
the UI-selected timeline must belong to the created project
received selectedTimeline: undefined
```

The browser reached the created-project URL and selected-timeline URL checks,
but the selected timeline ID was absent from the created project's Runtime
`/v1/projects/{project}/timelines` response. The central log retains the first
failure stack and trace reference in result directory
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-explicit-scope-helper-fix-ap2-m2-bootstrap-scoped-audit-central-gate-1020215432-17076/log.txt`.

## Evidence

Central command/result:

```text
request-test ap2-m2-bootstrap-explicit-scope-helper-fix ap2-m2-bootstrap-scoped-audit-central-gate
wait-test ap2-m2-bootstrap-explicit-scope-helper-fix-ap2-m2-bootstrap-scoped-audit-central-gate-1020215432-17076
status=fail exit=1 duration=118s
```

The private driver passed these pre-browser checks:

- Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`.
- Runtime `202074110717146fc7f08af2306a8dd7f695b0b1` with producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`.
- Artifact `f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`; schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`; 75 artifact bytes verified.
- Locked Composition `0.0.13`; archive, lock, 425 symlinks, 0 broken symlinks, 77 regular Composition files, and read-only graph guards passed.
- Pre-build Playwright list selected exactly one bootstrap test.
- `npm run build:hosted` passed; private caches, node graph, Python environment, and run root used `TMPDIR`/EXIT cleanup.

The prior owner wrapper result `...22557` remains correctly classified: its
ordinary probe and graph guards passed, while its overall wrapper failed on
unrelated existing App `tsc` diagnostics. This bootstrap driver did not run
that wrapper or call its typecheck condition.

## Boundary and next step

No qualification claim is made for door-audit create/init order, history,
lost-ack retry, reload/restart, undo, opaque values, or zero legacy traffic;
the first scope assertion stopped the test before those assertions. No source,
API, schema, pin, dependency, adoption, or shared installation was changed.
No full suite or local browser/socket/driver run was performed, and the single
central result was not retried.

The next action belongs to the App owner: diagnose why the UI-selected timeline
is absent from the created-project list on this exact candidate, then request a
new central run only after an approved source or fixture correction.
