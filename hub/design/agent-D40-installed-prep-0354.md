## Result

Installed D40 positive qualification remains unqualified. No existing environment matches current Agent `252cf33d…` + Runtime D40 producer `f3208b26…`.

Exact original node:

```text
tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack
```

Census cause: admitted-child `runtime_protocol` import failure; this is environment/custody evidence, not product-pass evidence.

## Current custody path

Runtime `f3208b26…` must:

1. Configure private owner grants in Runtime support state.
2. Validate repository, checkout, revision, subpath, tree, exact file hashes, and selected definitions.
3. Capture source bytes into `OwnerSourceCapture`.
4. Bind the capture to the retained preparation/profile.
5. Consume the private `_RuntimeExternalSources` handle before Agent discovery.
6. Let Agent `generic_host` select only the captured bytes.
7. Execute those bytes through the existing captured-source loaders.

Caller grants cannot fabricate custody, and digest-only authorization is insufficient. Runtime `36760ee0…` remains reference-only; no unrelated pin adoption or D39 regeneration was made.

Relevant current tuple:

- Agent: `252cf33d02184abcba4664634802291cfc791ca3`
- Runtime D40: `f3208b26b53c4d7053e5464eaa7c5e15b1505812`
- Runtime client identity:
  - `__init__.py`: `d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2`
  - `contract_metadata.py`: `a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae`
  - `generated.py`: `9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904`
  - `timeline_commit_types.py`: `88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616`
- Node: `v20.19.4`
- Remotion/profile archive: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
- Remotion lock: `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`

## Existing environments

The managed c886 environment is real but stale:

- Agent `c36ca8c9…`
- Runtime `abd47e68…`
- Client tuple is the older recorded tuple.
- Receipt: `status=passed`
- Origins are private site-packages paths.
- Direct URLs point to old `.child-venv-source-*` snapshots.
- Requirements lock hash: `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`

The f1012 environment also exists but is not a current qualified child:

- Wheel hashes:
  - Agent: `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`
  - Runtime: `aac07960e997c8881a594d6d9a3e18eccfef6828dc15cab9fc0f3fd25f941c49`
  - Client: `f0cb9f222c5d2697eb8c1d912cccfce30fa058530a1471b8441b54b4546497a4`
- Origins are private.
- Final audit reports no pin mismatches.
- It lacks current `.astrid-source-commit`, `.astrid-runtime-source-commit`, client identity, and provision receipt.

Neither environment may be relabeled as current D40 evidence.

## Supported later request

After the disk threshold is satisfied, the supported request shape is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv \
  venv-agent-child-d40-original-252cf-f320 \
  252cf33d02184abcba4664634802291cfc791ca3 \
  --source-carrier \
  /home/user/work/wt/agt-F-D40-installed-prep-0354 \
  /home/user/work/wt/rt-pin-f3208b26 \
  f3208b26b53c4d7053e5464eaa7c5e15b1505812
```

This was not executed. No installation, provisioning, benchmark, body run, source overlay, or `PYTHONPATH` qualification was performed.

## Test-only seam proposal

The original fixture creates an untrusted temporary external root and directly constructs `GenericPackHost`. The smallest faithful later seam is setup-only:

- retain all existing fixture contents, assertions, positive/negative predicates, and `host.admit`/`host.invoke_capability` invocation;
- place the temporary fixture under a test-only Git-backed checkout with origin, revision, tree, and exact file inventory;
- configure the private Runtime owner grant through the existing in-process owner setup;
- create retained preparation/profile data with matching selected root/files;
- launch through `RuntimeHostLaunchVerifier -> generic_host`, so capture is consumed before discovery.

Do not use a forged grant, profile assertion, digest-only trust, or old installed source with new arguments.

## Evidence and tests

Existing evidence reviewed:

- Agent D40 focused tests: `32 passed`.
- Neighbor controls: `56 passed, 2 failed` because installed VibeComfy/child Runtime environment was unavailable.
- Runtime integrated service: `317 passed, 2 deselected`.
- Raw full census: `17159 passed, 262 failed, 5 errors, 4 skipped`.
- Installed env86 cohort: `69 passed, 17 failed`.

No tests were run in this readonly preparation task. The worktree remains clean; only the required commit-message and `DONE` markers were written.