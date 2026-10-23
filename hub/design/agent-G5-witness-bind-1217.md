# G5 witness bind — 1217

## Result

The bounded source-fixed continuation was dispatched exactly once through the central test service. It executed one test body and failed in the Agent emitter after setup. This is a draft-only **NO-GO** result; no integration or product repair was attempted.

Service: `agt-G5-witness-bind-1217-g5-emitter-current-runtime-nodes-1023121605-11640`

Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G5-witness-bind-1217-g5-emitter-current-runtime-nodes-1023121605-11640/`

Exact request:

```text
agt-G5-witness-bind-1217 g5-emitter-current-runtime-nodes --files tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated
```

The service recorded `tree=3ed568fbd57a7732712bdd3558edc6f5ba008282`, `exit=1`, and `1 failed in 4.07s`. It was not a cache hit, skip, zero-test run, or guard failure.

## Source and guard custody

- Snapshot parent: `6120c25492574353ac12279f184b2355b53c4828`.
- Snapshot tree: `3ed568fbd57a7732712bdd3558edc6f5ba008282`.
- Runtime: commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean.
- Normal producer: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Frozen edit-command schema: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Frozen Composition artifact: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Corrected test SHA-256: `28ca8b12f2ca21c84d74c6601ae3887fc4873e90ffa1f35c20a56177272df72e`.
- New wrapper SHA-256: `d720fba3ab285078c7f10d0ca20836f1405cd19d10ba95d3817748a80da57d40`.
- Preserved 1201 wrapper SHA-256: `530335aa45ff50bc164411b22927798544826ecca2b0c312b8b45940e707b489`.

The existing `g5-emitter-current-runtime-nodes` row was updated only to point to the new worker-local wrapper and to assert its literal SHA-256. The new wrapper is copied from 1201's inline origin-witness runner, with the snapshot parent/tree and corrected test-integrity guard updated. It retains the Runtime, producer, schema, Composition, origin, `-m integration`, exact-node, and one-argument guards. The suite command adds `bash -n`, required-file, and offline exact-node collection checks before the body. The old 1201 script and evidence were not modified. No product, test, Runtime, pin, generated, contract, dependency, daemon, or shared-install files were changed.

Pre-dispatch checks:

```text
git rev-parse HEAD                 = 6120c25492574353ac12279f184b2355b53c4828
git rev-parse HEAD^                = b4a5b3b7ef524049e569c9694aa730b9368f8ad0
git rev-parse HEAD^{tree}          = 3ed568fbd57a7732712bdd3558edc6f5ba008282
bash -n new wrapper                PASS
offline pytest --collect-only      1 test collected in 1.74s
```

## Failure classification

The central origin witness reported Agent and generated client modules from the synthetic snapshot and Runtime protocol from the exact pinned Runtime at `before`, `session-start`, `session-finish`, and `after`.

The first body failure is in the corrected test's emitter exercise. The exact error is:

```text
astrid.sdk.timeline.emitter.DocumentPatchError:
cannot emit a source-bound doc.patch: closure root
'internal-revision:emitter-ed13442089bc4946998a7fcc5e9b3007-internal-revision'
has contradictory authoring aliases; use a semantic command
```

It is raised from `astrid/sdk/timeline/emitter.py:293`, with the underlying alias contradiction at `emitter.py:205`. The service did not reach the later Runtime refusal/history/accepted roundtrip assertions. This is a new durable source classification against the current corrected Agent tree, not evidence to waive or weaken the test. Stop here as instructed; the dedicated R1 atomic-scope worker owns any separate atomic dependency-union issue.

## Evidence and next step

The full central log is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G5-witness-bind-1217-g5-emitter-current-runtime-nodes-1023121605-11640/log.txt`

Do not rerun this node, use `--no-cache`, run all 19 nodes, or repair the emitter in this task. The next owner should classify/fix the contradictory authoring-alias source contract, then request a new bounded central witness from the resulting source.
