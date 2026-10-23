# G5 witness review — agt-G5-test-runtime-witness-1201

## Verdict

The worker’s central-service witness is a genuine **FAIL**, not a PASS, skip, or zero-test result. The harness and custody checks are sufficient to classify the failure. The one meaningful execution ran the requested node once and failed in 4.07 seconds before the Runtime refusal/history assertions.

The failure is an existing public-bundle/source-boundary mismatch: the authenticated public Runtime bundle does not contain `source_mapping["_runtime_document"]`, while the current Agent emitter’s `document_from_bundle()` path requires it. This review does not add a private-cache workaround, alter the test, or rerun the body.

## Custody and registration

- Agent source: `HEAD^`/source commit `b4a5b3b7ef524049e569c9694aa730b9368f8ad0`; central synthetic snapshot tree `0f15546b263450058f6d4a26ce0ad7ff901ed57d`.
- Runtime: `/home/user/work/wt/rt-pin-3b926efa`, commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean.
- Normal Agent producer pin: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Frozen schema SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Frozen Composition artifact SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- The allow-list has exactly one new row for `agent g5-emitter-current-runtime-nodes`; the worker’s recorded diff shows no changes to the other suite rows.
- The row’s `*-nodes` suite is guarded by `request-test`’s explicit `--files` requirement. The wrapper also requires exactly one argument and exact equality with the requested node.

The wrapper checks the Agent parent and synthetic snapshot tree, exact Runtime commit/tree and cleanliness, normal producer lock, frozen schema file, and Composition hash. It separately checks the generated client schema digest (`sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`); this separation corrected the first preflight mistake without changing product files.

The wrapper invokes pytest with `-m integration`, `-o addopts=`, and `-p no:cacheprovider`. Its same-process origin witness reported Agent and generated client modules from the central synthetic snapshot and `runtime_protocol` from the pinned Runtime before, at session start/finish, and after the case. The service result contains one failed test and no skip or zero-test condition. The central runner independently rejects zero-test output as failure.

## Service evidence

Meaningful result:

```text
service: agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910
command: bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-test-runtime-witness-1201/run-g5-emitter-current-runtime-nodes.sh tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated
result: exit 1 — 1 failed in 4.07s
```

The result directory is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910/`.

The first registration (`...1023120116-22440`) failed in preflight with no test log because the wrapper incorrectly equated the normal client `SCHEMA_DIGEST` with the frozen schema-file SHA. The second (`...1023120217-7687`) was a cache hit of that old preflight failure and did not execute the node. A subsequent no-cache registration (`...1023120254-8937`) also exited in about one second with an empty test log and is not counted as a test execution. Only `...1023120356-29910` is the meaningful witness.

## Failure classification

Setup passed through `loaded.ok`, accepted revision/head equality, and the authenticated `voiceover` source binding. The first failing operation was line 284 of `tests/editing_conformance/test_native_sheet_current_runtime.py`:

```python
invalid_commands = emit_document_commands(before, unsupported)
```

The production path raised:

```text
DocumentPatchError: cannot emit a source-bound doc.patch: '_runtime_document'
KeyError: '_runtime_document' at astrid/sdk/timeline/commit.py:308
```

The stack reached `astrid/sdk/timeline/emitter.py:179`/`265`. The bundle returned by the current public Runtime route has the public `source_mapping["shots"]` provenance but no private/in-memory `source_mapping["_runtime_document"]`. The emitter therefore cannot construct the expected invalid `doc.patch`; the Runtime refusal, unchanged-head/history, accepted roundtrip, reload, undo and redo assertions did not run.

This is the deliberate existing G2/P4 public-cache boundary, not a seed/setup failure and not an origin mismatch. It is recorded as source classification only. No direct HTTP body was captured or edited, and no private-cache or fake-acceptance workaround was introduced.

The production caller and full-v2 request/reply route were not changed by this review. The existing shapes remain the base pair, commands, label, steps, patch, reads, ordinals, merge, key, dry-run, source, rationale, group ID, and data/receipt/full-canonical/records/deps/effects/history/undo-steps/preview plus required would-status/conflict-head-reason/invalid code/path/hint/command fields. The worker’s Agent commit is test-only; Sol1208’s test boundary repair was not duplicated.

## Cache-key caveat

The final wrapper bytes are stable at SHA-256 `530335aa45ff50bc164411b22927798544826ecca2b0c312b8b45940e707b489`. The test-service cache key is computed from repository, source tree, suite, files, and the literal suite command. The suite command currently contains only the wrapper path, not its bytes. Therefore changing the wrapper at that path during preflight did not invalidate the old cache key; the observed cache hit reused the old preflight failure.

Before any cached reuse, registration should embed a literal final wrapper hash (preferably as a shell assertion, so it both changes the cache key and verifies the bytes). This is a recommendation to the orchestrator/registration owner; this review made no live edit. The meaningful run used `--no-cache`, so its FAIL is not cache-derived.

## Read-only checks performed

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-test-runtime-witness-1201/run-g5-emitter-current-runtime-nodes.sh` — PASS.
- Python AST parse of `astrid/sdk/timeline/commit.py` — PASS.
- Exact Agent/Runtime commit/tree, clean-worktree, schema SHA, and Composition SHA checks — PASS.
- Static inspection of `request-test`, `test-run`, `suites.conf`, wrapper guards, service logs, and worker diff — PASS for the required invocation/zero-test controls.
- No full suite, browser, localhost body, live network call, daemon, Git mutation, shared dependency mutation, product edit, test edit, pin edit, or Runtime edit was made by this review.

## Recommendation

Keep the service result as **FAIL**. The owning implementation/review should resolve the public-bundle versus source-bound emitter contract, then rerun this exact node through the service after updating the registration with the literal wrapper hash. Do not claim the refusal/history proof until that rerun executes past line 284.
