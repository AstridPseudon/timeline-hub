# a610 full-suite triage

Date: 2026-10-20 UTC. This is a classification report only; no product,
test, fixture, schema, pin, or generated artifact was changed.

## Result

Authoritative run: `agent-full-remotion-integration-1020015823-24749`, exact
tree `8f046de1844963feab3732cb4ffda7064c49f64e` (the full was not run on
current `4a75f68f`). Command and environment are recorded in
`notes/full-a610-classification.json`.

`11723 passed, 79 failed, 453 skipped, 30 errors, 563 subtests passed, 75
warnings, 2809.29s`.

The exact current non-passing set is 109 nodes: 62 persisted from the old
63-node baseline, plus 47 additional nodes. One old node is gone:
`tests/packs/runpod/test_worker_preparation.py::test_runtime_activation_checkpoints_restore_only_the_exact_process`.
The previous post-restore set had 67 nodes; its four consumer failures are
absent from a610 and remain counted as resolved, not silently forgotten:

- checked-in TypeScript element projection;
- `render_status` default;
- renderer-install journey wording;
- text-card visible markup.

The previous set also included the worker-preparation node, which is the one
old node absent from the current set. Therefore `previous\current = 5` and
`current\previous = 47`; the latter is the complete additional set.

## Additional 47-node classification

| cluster | nodes | classification | evidence |
|---|---:|---|---|
| pixel geometry/blink | 11 | valid supported-environment fixture problem | Every traceback is Node `ERR_UNKNOWN_FILE_EXTENSION` for direct `.ts` import. The exact pure probe gave Node `v20.19.4` plain import exit 1; Node `v22.22.0` imported the same module successfully. The shape source and pixel test blobs are identical between previous tree `36d86ed3` and a610 tree `8f046`. |
| RunPod owned host | 1 | UNKNOWN | The exact pinned-environment central targeted run reproduced `WorkerOwnerConflict: host did not acquire physical pod ownership`. `worker_process.py` and its test are unchanged across baseline `e475f212`, previous `36d86ed3`, and a610. The child is launched with stderr discarded, so the child exit cause and same-environment baseline result are not proven. |
| host bootstrap source identity | 16 | valid supported-environment fixture problem | Three fail because the fake inventory supplies `PosixPath` where discovery requires a record with `.pack_root`; thirteen fail with `RemotionValidationError: runtime validation refuses unsupported loader/interpreter overrides`. The host bootstrap/test blobs are unchanged from the previous full. The pinned full environment adds `ASTRID_REMOTION_PROJECT_DIR`, pinned Node, and installed schema variables; the previous full used the normal environment. |
| stage interpreter identity | 4 | valid supported-environment fixture problem | All four fail because a fake prior host has no launch-validation marker while the configured Remotion environment requires one. Test/bootstrap blobs are unchanged from the previous full. |
| host recovery | 14 errors | valid supported-environment fixture problem | Every setup error reaches the same `RemotionValidationError` for unsupported loader/interpreter overrides before the recovery assertion. Recovery tests and relevant host source are unchanged from the previous full. |
| admission recovery | 1 error | valid supported-environment fixture problem | The test dynamically loads the Runtime generated client under a synthetic module name; the current Runtime generated source imports `timeline_commit_types` relatively, producing `ImportError: attempted relative import with no known parent package` when `ASTRID_RUNTIME_CHECKOUT` is set. The Agent test source is unchanged. |

No additional node is proven to be a product regression. The RunPod owned-host
node remains UNKNOWN and keeps M1 HOLD. The proposed minimal corrections are
fixture/environment ownership work: run pixel assertions through the supported
TypeScript loader or a Node version that supports the repository's loader
contract; make fake host inventories real source-record-shaped objects and
provide a clean Remotion validation marker (or explicitly omit Remotion from
those fake-host tests); load the generated Runtime package with package
context; and capture child stderr in a narrowly scoped diagnostic probe before
deciding the RunPod owner. Preserve all existing assertions. Pixel changes
need Viewing ownership/grant; host/admission fixture changes need the owning
Agent/Runtime coordination. No fix was made here.

## Persisted 62-node classification

These are the old-baseline nodes still present, with their baseline causes
preserved:

| family | nodes | classification | traceback/source proof |
|---|---:|---|---|
| RunPod staging | 15 errors | strict preexisting external fixture/setup | `FileNotFoundError: /home/vibecomfy/vibecomfy`; same staging fixture failure as baseline. |
| H3 installed guard | 7 | strict preexisting dependency/source setup | isolated child `python -I` cannot import `astrid` from the dependency-only environment. |
| VibeComfy metadata | 1 | strict preexisting xdist/toolchain | `execnet.gateway_base.DumpError: can't serialize pathlib.PosixPath`. |
| RunPod actions path | 34 | strict preexisting main-path drift | Tests import `astrid.packs.runpod.executors`; current product path is `runpod/actions`. Product and test blobs are unchanged. |
| RunPod worker process import | 3 | strict preexisting test-code defect | `signal` is not imported by the test; the worker product source is unchanged. |
| generic host cleanup | 1 | strict preexisting contract mismatch | Baseline, previous, and a610 traces all raise `CommandCleanupUnresolved` after the test injects `CleanupUncertainError`; generic-host product blob is unchanged. |
| giant-file rationale | 1 | strict preexisting, with M1 metadata debt | The first assertion still reports unchanged `generic_host.py` 13,598-vs-13,798 drift. Separately, the a610-era `remotion_runtime.py` entry is also stale (1,247 recorded vs 1,353 actual) but is hidden by that first assertion. |

The complete node-by-node inventory, including every current node, status,
delta, classification, cluster, and prior-set status, is
[`full-a610-classification.json`](full-a610-classification.json). SHA-256:
`4ecca988d42f2ff302a47c68779d27402ba3b042c53104735e19686400ea360d`.

## Evidence commands and boundaries

Read-only source/set checks:

```text
git diff --name-only 36d86ed3 8f046
git diff --name-only e475f212 8f046
git rev-parse 8f046^{tree} 4a75f68f^{tree}
git rev-parse <tree>:<relevant-file>  # relevant source/test blob comparisons
```

The `36d86ed3..8f046` diff has 17 files and no pixel, host-bootstrap,
host-recovery, stage-interpreter, or RunPod worker-process source/test file.
The baseline-to-a610 diff does include the Remotion runtime/package/lock and
schema-environment changes, so unchanged-file reasoning was not used alone.

Central targeted process/socket run (not run directly in this sandbox):

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m1-full-a610-triage remotion-env-nodes --files "tests/packs/astrid_motion/test_pixel_shape_geometry.py tests/sdk/test_host_recovery.py tests/sdk/test_host_bootstrap_source_identity.py tests/stage1/test_pack_host_interpreter_identity.py tests/packs/runpod/test_worker_process.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-m1-full-a610-triage-remotion-env-nodes-1020025059-8756
```

Result: `35 failed, 112 passed, 2 skipped, 14 errors in 36.96s`, on worker
tree `d8ee74e07ad86e9f5ceb15546804c17be9aaaead`. Its relevant cluster blobs
match a610. A second central targeted command for
`tests/sdk/test_admission_recovery.py` reproduced its collection error in
`2.71s`: `1 error`, the same relative-import traceback. No full resubmission
was made. No direct socket or process-host test was run.

An exact same-environment baseline run is still UNKNOWN: the central service
snapshots the worker's current tree, and the requested new named
`a610-env-triage-integration` suite is not registered in the service allow-list.
The baseline identity and old node set are preserved in the JSON and prior
central artifacts; this report does not convert the normal-environment
previous full into same-environment proof.

M1 gate: **HOLD** pending the UNKNOWN RunPod ownership cause, the exact
same-environment baseline comparison, and owner-approved fixture corrections.
