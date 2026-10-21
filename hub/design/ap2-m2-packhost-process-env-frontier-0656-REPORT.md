# App2 Remotion pack-host environment audit

## Result

**App2-owned active runners: not applicable.** The named App2 runners do not
start a Remotion pack-host, so no App2 process-local unset patch or planted
child-environment check is justified. No App product, shared harness, package,
pin, assertion, argv, budget, or graph files were changed.

The directive is applicable to the separate HOME/Viewing pack-host seam noted
below.

## Concrete process evidence

### Parent normal014 driver and source-common

- `design/normal014-parent-media-central.sh:17-22` verifies sources, the
  locked graph, and a private Python environment. Its only test child is
  `normal014-parent-media-central.sh:51-52`, the Runtime checkout's single
  pytest node.
- The same driver exports only `ASTRID_CHECKOUT`,
  `ASTRID_RUNTIME_CHECKOUT`, `PYTHONPATH`, Python bytecode/user-site and pip
  settings at `:44-50`; it does not invoke a pack-host helper.
- `design/normal014-source-common.sh:216-220` uses Node only for the locked
  Composition `computeMediaTrim` probe. `:323-352` uses Python imports,
  `astrid --help`, and pytest collection. There is no `remotion_runtime.py`,
  `probe_context`, pack-host, or Remotion host launch in this path.
- Therefore inherited `NODE_OPTIONS`/`NODE_PATH` are not inputs to a Remotion
  pack-host child in this runner. The runner's retained parent failure is not
  evidence of a pack-host refusal.

### Selected durable runner

The retained runner is
`workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh`.

- `:104-127` launches `python -m astrid_runtime workspace create/inspect`.
- `:136-145` builds the private Node graph and App overlay.
- `:165-171` launches Playwright collection, `npm run build:hosted`, and the
  selected three-products test under `flock`.
- `:162` sets `NODE_OPTIONS` and there is no `NODE_PATH` sanitization, but this
  runner does not launch a pack-host. The selected spec calls
  `harness.startSelectedParamDevServer()` at
  `tests/e2e/local/three-products.selected-param-dev.spec.ts:25-26`; its
  harness starts the direct Runtime (`tests/e2e/local/support/harness.ts:501-505`)
  and the dev/proxy processes, not `startRealPackHost`. The Runtime command has
  no `--worker-profile`/service declaration (`/home/user/work/runtime/runtime_protocol/cli.py:57-60`),
  so its normal `start` path does not configure a local Worker/pack-host
  composition (`:363-394`). The selected path has no Remotion
  render/pack-host operation.
- The retained selected-run failure is explicitly pre-collection/setup
  (`workers/ap2-m2-selected-draft-p1-review-gate/report.md:5`), not a
  `probe_context` packet. Its historical cause remains unknown.

### Producer startup artifacts

The STATUS-named startup artifacts are the 0647 custody/startup gates and
`producer-startup-only-probe.mts`.

- `producer-startup-custody-gate.sh:86-92` invokes the source preflight and
  format-only `tsx` probe; `:91-92` delegates startup/list/run to the existing
  gates.
- `producer-startup-only-gate.sh:56-86` creates private Agent/Runtime roots,
  exports the normal checkout/Python/cache/TMPDIR variables, sets
  `NODE_OPTIONS`, and invokes `tsx` with the probe.
- The probe's only process work is the existing `DirectHarness` Runtime
  startup/health check at `producer-startup-only-probe.mts:28-73`; it does not
  import or spawn the Remotion pack-host helper. The 0647 report also records
  the intended source/module preflight and that no producer body or startup
  qualification occurred.
- Thus these artifacts also have no App2-owned pack-host child requiring the
  new unsets.

## HOME seam request

The exact Remotion pack-host launch is Viewing-owned:
`tests/e2e/timeline/viewing-parity/bootstrap.ts:106-126` clones the supplied
environment, adds Python settings/PYTHONPATH, and passes that environment to
the Python helper at `:122-126`. Before that spawn, HOME should make the
smallest process-local change:

```ts
delete env.NODE_OPTIONS;
delete env.NODE_PATH;
```

The existing clone (`const env = { ...(options.env ?? process.env), ... }`) keeps
the parent environment unchanged. HOME should add its planted check in the
existing bootstrap unit seam: capture the `env` argument in the injected
`spawn` callback, assert both keys are absent in that exact child environment,
and assert the parent sentinel values remain unchanged. This is a HOME change;
no App2 file was edited concurrently.

## Retained failure evidence and limits

The named App2 retained failure reports do not contain a packet naming both
`NODE_OPTIONS` and `NODE_PATH` together with `pack-host`/`probe_context`.
Accordingly, no causal match is claimed for the parent, selected, or producer
failures. Historical unknown remains unknown without that evidence. No
Remotion launch, browser/render/startup/actual replay, installation, full
suite, or Runtime/provider work was run.

## Checks

- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-custody-gate.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-startup-shell-contract-repair-0647/artifacts/producer-startup-only-gate.sh` — PASS.
- `git diff --check` — PASS; no worktree changes.
- No App test suite was run because no App2-owned pack-host launch or code
  change was found, and the task forbids browser/render/startup/actual replay.
