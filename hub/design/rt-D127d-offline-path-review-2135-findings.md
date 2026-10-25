# D127d independent review

Verdict: **UNAPPLIED is supported; actual performance remains UNPROVED.** The branch is exactly Runtime `684b3d7b6ac5381ed92a363fa7c941031622e1f3`, tree `7051fd435bc4b328954800bf171f5823ae00b2dd`, and is clean. Its only changes are the durable benchmark and eight additive guard tests. No production optimization or behavior change is present.

## What the artifact proves

The retained fixture is unchanged (`tests/fixtures/timeline_sequential_capture.json`, SHA-256 `51e353be...5976cd`): 200,611 file bytes, 200,610 canonical bytes, two commands. The helper calls the existing `validate_sequential_capture` and `validate` functions with the retained request, prepared candidate, source, base and continuation map. The independent one-warm run measured 123.629 ms warm median and 54 `CanonicalDocument` validations plus two `Recorder` validations. Synthetic scaling reached 54,643 canonical bytes and 54 repeated checks; its maximum warm validation+digest sample was 205.264 ms and detached-copy sample 87.888 ms.

These are helper-only measurements. They neither execute a Runtime handler nor construct a registered Agent provider, request port, SQLite store acceptance, lifecycle admission, HTTP/door path, or exact App element document. They cannot explain or ratio the separately retained 21.740631 s element handler / 13.780929 s provider figures or the named 1.75 s native control. The App safe evidence also retains unknown request completion/response dimensions and missing deterministic call-count/cProfile tables; no source-specific cost owner follows from those measurements.

## Whole-path source result

The live route is:

`RuntimeHandler._timeline_commit` → `RuntimeService.commit_timeline` → `_execute_timeline_commit` → `CommitExecutionCoordinator` → registered `astrid.sdk.timeline.commit.RuntimeCommitService.commit` → `RequestCommitPort` → `TimelineCommitStore.preview/accept` → `timeline_commit_auth.validate[_sequential_capture]`.

The earlier exclusion of `runtime_protocol/timeline_commit_auth.py` would have missed the actual expensive-looking traversal seam. `_capture_document_images` validates a full `CanonicalDocument`, maps all physical images, checks image uniqueness, and rehashes every payload (lines 2338–2362). `validate_sequential_capture` checks both original and landing command boundaries and record correspondence (lines 2563 onward), while `validate` replays reads, manifests, steps and command outputs (lines 2873 onward). This establishes repeated traversal as a real source characteristic, not a proved defect.

The surrounding guards are source-bound and must remain: authenticated route identity and idempotency (`server.py:300-340`); active project/timeline and request hash (`service.py:2485-2559`); coordinator lookup/reconciliation and close handling (`timeline_commit_execution.py:373-431`); request-bound detached capture, mutex/history reads, ancestry/closure reauthentication, observed-head requirement and capture clearing (`timeline_commit_port.py:182-322,660-710`); verification/read transaction/store-version and acceptance transaction (`timeline_commit_store.py:168-192,381-470,1789-1847`); and digest, ownership, binding, replay, read and no-write checks in `timeline_commit_auth.py`.

## Smallest feasible offline production-path replay

Use the existing `tests/test_timeline_commit_integration.py::editing` fixture, which restores the committed `precut-music-documents-v31.tar.gz` realm, registers `load_timeline_commit_provider("astrid")`, blocks rendering, and calls the real `RuntimeService.commit_timeline` path. The controlled input should be:

1. Capture one real `capture_move` command against the fixture's authenticated head and time the existing `Editing.commit` call.
2. Reuse the same base document to prepare one disjoint real `capture_move`, accept the first command, then commit the second. This forces provider history reads, landing re-execution/revalidation, port head observation, store merge/CAS and authenticated acceptance while retaining all normal guards.
3. Run the exact same candidate as `dry_run=True` to exercise the preview branch, then repeat the accepted idempotency key to exercise durable replay without provider execution.
4. Record only outer wall timings and existing stage entry/exit counts; do not alter `_capture_document_images`, memoize trust, remove detachment, widen reads, change mutex/transaction scopes, or create a new authorization gate.

This is source-complete for the offline in-process production commit path, but it is not a claim that the fixture equals App's element request. Exact element dimensions/history and daemon/door lifecycle remain unknown and require the already-authorized central venue if they are later admitted.

The frozen R4 Runtime reference does not contain the v2 `timeline_commit_*` modules; it is a historical schema/control comparison, not a runnable control for this path. The current provider seam is read from the current Agent integration checkout and the App harness only for seed-shape provenance; no checkout or external worktree was modified.

No cause or fix is recommended by this review. Release remains held pending a source-complete replay and independent review of any behavior-preserving candidate, followed by the normal exact-provider smoke.
