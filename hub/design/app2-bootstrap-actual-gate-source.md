# App2 bootstrap actual consumer gate source

Status: source prepared, not qualified. This is one positive App three-products
test; no browser, socket, Runtime-door, or full-suite run was performed by this
worker.

## Exact source tuple

- App source under test: `dcf52eb3943dffb3554f616f6ecd738717e29d74`
  (`hub/timeline/app/tl/app-m2-bootstrap-prerequisite-source-refresh`; current
  worktree HEAD).
- Frozen Agent dependency: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.
- Frozen Runtime dependency: `7f6dd8920e1ceec41b137358df5e7fecc304888d`.
- Frozen native/provider evidence: central gate
  `app-bootstrap-frozen-pair-integration-1020152025-22537`, 12 passes for the
  exact Agent/Runtime pair. The separate four positive opaque-inverse vectors
  remain Agent-owned failures and are not xfailed here.
- App package/dependency pins: unchanged; no installed dependency, generated
  source, shared root, or pin was modified.

## Test source and limits

`tests/e2e/local/three-products.spec.ts` adds exactly one test:
`M2 bootstrap actual consumer: production initializer uses native create/init,
exact retry, restart and guarded undo`.

The test drives the production New Project flow through the hosted App and
authenticated Runtime door. It then checks, for one newly-created project:

1. Runtime `/v1` timeline create and commit requests occur.
2. The commit captures exactly `timeline.init` plus the two `track.create`
   commands, and the accepted history has one native bootstrap publication.
3. No `/timelines/:id/composition-revisions` request occurs.
4. A real track edit survives a lost acknowledgement, reload, Runtime restart,
   and exact persisted retry.
5. App Undo submits a guarded `timeline.inverse` and restores the original
   track label.

The test reuses the existing App fixture, door harness, outbox reader,
`faultFirstCommit`, `expectSameRealm`, and `TokenSniff`; it adds no fixture or
framework copy and does not alter the existing seven positive behaviors.

## Exact central-service proposal

After the production seam is wired and the named frozen pair is available to
the central runner, request the existing three-products suite once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-actual-gate-source full-e2e-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

This command is a proposal only and was not run for this task. The suite is
intentionally the existing `full-e2e-three-products` named suite because the
test is in `three-products.spec.ts`; no local browser/socket run or additional
full run is authorized here.

## Gate blockers

The current source cannot pass the new test honestly:

- `src/integrations/runtime/createDefaultTimeline.ts` still implements
  `publishEmptyTimeline` with `AstridRuntimeClient.publishParentComposition`,
  producing legacy snapshot traffic.
- `src/integrations/runtime/bootstrapInitialization.ts` contains
  `resumeBootstrapInitialization`, but no production caller reserves the
  create owner, invokes the initializer, or returns its verified basis to the
  editor.
- `src/integrations/runtime/generated.ts` has `WorkspaceClient.createTimeline`,
  but `AstridRuntimeClient` has no corresponding wrapper. The smallest
  production seam is the wrapper plus wiring the existing owner/outbox
  bootstrap into `createDefaultTimeline` and its first/additional timeline
  callers; deletion of the legacy publisher belongs in that qualified cutover.
- The Agent opaque-inverse hold remains independently open: the four original
  positive unrelated-parent-opaque undo vectors still fail with
  `inverse_dependency_changed`. This test does not weaken, skip, or encode
  that behavior as an expected failure.

Until those blockers are resolved, this source is a visible failing positive
gate, not a qualification or retirement claim.
