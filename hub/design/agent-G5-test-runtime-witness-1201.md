# G5 bounded current-Runtime witness — agt-G5-test-runtime-witness-1201

## Result

The one meaningful central test-service execution was a genuine FAIL. No PASS or zero-test credit is claimed.

- Agent source tree: `0f15546b263450058f6d4a26ce0ad7ff901ed57d`, with source parent `b4a5b3b7ef524049e569c9694aa730b9368f8ad0`.
- Runtime: `/home/user/work/wt/rt-pin-3b926efa`, commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`, clean before execution.
- Normal Agent producer pin: `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Frozen schema file SHA-256: `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- Frozen Composition artifact SHA-256: `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

Service ID/result: `agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910`, result directory `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G5-test-runtime-witness-1201-g5-emitter-current-runtime-nodes-1023120356-29910/`.

Exact central command:

```text
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-test-runtime-witness-1201/run-g5-emitter-current-runtime-nodes.sh tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_emitter_null_presence_and_track_roundtrip_is_authenticated
```

The runner enforced `-m integration`, `-o addopts=`, `-p no:cacheprovider`, and rejected every selector except this exact node. Same-process origin witnesses passed before, at session start/finish, and after:

- Agent and generated client loaded from the central synthetic snapshot of the exact Agent tree.
- Runtime loaded from `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/__init__.py`.

The node ran once: `1 failed in 4.07s`, no skip and no zero-test result. Setup assertions passed through `loaded.ok`, accepted revision/head equality, and the authenticated `voiceover` source binding. The first failure was test line 284:

```text
invalid_commands = emit_document_commands(before, unsupported)
```

The current production path raises `DocumentPatchError: cannot emit a source-bound doc.patch: '_runtime_document'`. The underlying failure is `KeyError: '_runtime_document'` at `astrid/sdk/timeline/commit.py:308`, reached through `astrid/sdk/timeline/emitter.py:179`/`265`. The authenticated bundle returned by the current Runtime lacks `source_mapping['_runtime_document']`, so the emitter cannot construct the expected invalid command; no refusal/history assertions after line 284 ran.

## Invocation corrections

Two pre-test service attempts did not execute the node. The first (`...1023120116-22440`) exposed an incorrect runner assertion: normal `34e` client `SCHEMA_DIGEST` is `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`, while the frozen schema file remains `d106…`. The second registration was a cache hit of that preflight failure (`...1023120217-7687`). The runner was corrected to check both values separately and to compare the central snapshot’s `HEAD^` with the Agent source commit, because the service uses a synthetic `commit-tree` HEAD.

No product, test, fixture, generated, pin, contract, dependency, Runtime, or repository files were changed. No replay follows this genuine source-path failure.
