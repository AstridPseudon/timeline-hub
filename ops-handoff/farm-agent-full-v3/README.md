# Runtime farm-agent-full v3 source packet

This is a source-only, non-installing packet for the existing `agent full-farm`
row.  It selects the supported D21b normal-maker child route for the exact
tested Agent and Runtime sources.  It does not provision a child, initialize a
Store, mutate a registry, run a suite, or qualify Farm READY.

The v2 parent packet is deliberately unchanged.  v3 changes only the Python
authority used by the row: the authenticated D21b child interpreter.  Python
`-I` therefore imports the normal maker's non-editable Agent and Runtime
install from the child's site-packages; the row has no `PYTHONPATH` binding.

## Exact source and normal request

The tested identities are Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`,
tree `57f0231da0d7904ecd8778169973d6384e0ae141`, and Runtime
`1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree
`f56c396c4495547680b46e832565278d2c375e69`.  The declared Runtime lock and
canonical client hashes remain those in `runtime-source-selection.json`.

After independent checkout receipts are present, and only after the normal
maker's existing managed `agent-remotion-farm-v2-9cd` registration/template
preflight passes, Farm may issue this exact supported request through the
existing dispatcher:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
"$ORCH/bin/request-child-venv" \
  venv-agent-child-farm-v3-9cd \
  9cd3dbe865a941c052bda04ae0d61306d18f8f26 \
  remotion-env-nodes \
  agent-remotion-farm-v2-9cd \
  --source-carrier \
  /home/user/work/wt/agt-pin-9cd3dbe8 \
  /home/user/work/wt/rt-pin-1d9ddba5 \
  1d9ddba546f8fb1300f55ff62607ed492719cbaa
```

The request must not be sent when the D21b child receipt is absent.  The
receipt must identify the requested child name, Agent and Runtime SHAs, the
generated client tuple, the physical child path/interpreter, successful normal
maker status, retained source snapshots, installed import origins, and the
existing managed Remotion registration.  A request argument is not proof of
any of those facts.

The exact missing Farm inputs are: the current Store owner/index and registry
bytes; the existing `agent full` and single `agent full-farm` rows; the
managed `agent-remotion-farm-v2-9cd` entry and approved Node20/Remotion graph;
clean checkout receipts for both exact commits; and the successful D21b child
receipt for `venv-agent-child-farm-v3-9cd`.  Farm must stop on any missing,
partial, stale, dirty, drifted, or permission-denied input.

## Installation boundary

`FARM-CODEX-BRIEF.md` contains the guarded installer.  It opens the existing
Store, verifies the child receipt and source identity, renders literal paths,
backs up the current registry, and atomically replaces exactly one existing
`agent full-farm` row.  It preserves the `agent full` row and every byte
outside that row.  Rollback is allowed only while the registry still equals
this operation's post-image.  No owner/index, Store entry, child, source
checkout, shared venv, or Remotion asset is created or replaced.

The installed row retains the existing Node20/npm, Remotion project,
`ASTRID_TEST_NODE_MODULES`, schema/profile, source, and lease guards.  Its
Python command is the authenticated child interpreter with `-I`; it checks
actual child import origins and exact marker/receipt identity before the
pytest body.  The real child/import preflight, checkpoint, and Farm READY
decision remain Farm-owned after reviewed installation.

Private tests are synthetic fixture tests only.  They do not constitute an
actual Farm READY result or a checkpoint result.
