# P1–P5 corrected final proof map

Report-only completion. No product, test, generated, pin, suite, or Git changes were made. No final qualified tuple exists.

Inspected identities:

- App: `66354161950d1e747965c095ea97b881d2592708`, tree `9a37265f0286128df7e6240a9df9877d959474af`
- Independent review refs: Agent `1f15f274824fadca722feb8676e6746dbd237f64`, tree `1ac5f2d6de4083d3959bf59e8fc8167d5ae3400e`; Runtime `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`
- C0: `contract/commit-v2.md`, blob `257024df6fa93be767f0c74ee10014a6770c4fcb`, SHA-256 `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`

## P1

Source: `tests/e2e/local/three-products.p1-chain.spec.ts`  
Blob `5a2029d5f61a5cb665e1fb59c9fe13c9fff0bfde`; SHA-256 `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`.

Cases:

- `P1 split -> trim new clip: accepted split, merged trim after Agent edit, lost ACK restart and exact retry`
- `P1 split -> trim new clip: a real Agent move refuses the stale trim and the App rolls back with a message`

Correct ownership: mounted App gestures perform split and trim through `useTimelineSave → persisted outbox → RuntimeDataProvider.commitTimeline → generated client.commitTimeline → Runtime /v1/.../commit`. Agent supplies only the intervening label/move through `astrid.commitCaptured`.

Preserved assertions include created-ID/doc.patch insertion, closure and opaque preservation, accepted/merged replies with `rebased_onto`, label preservation, exact request/key retry after reload and Runtime restart, canonical history/readback, rollback message, rejected outbox, structured `409 value_conflict`, and no legacy writes.

## P2

Preserved eight cases across:

- `tests/e2e/local/three-products.p2-elements-assets.spec.ts` — blob `836d144bc0e3bbd8f1677d23e96385bcd8127daa`
- `tests/e2e/local/three-products.p2-popup.spec.ts` — current blob `c5926a2d304b96bc9ded59a71c8079d90ac3ac32`
- `tests/e2e/local/three-products.p2-tour.spec.ts` — blob `45a8088fafd72a462409e444c0294e8a35682a0f`

Cases cover mounted element edit, registerAsset, automatic child placement, popup ADD, popup SWAP, parent move, transition-`None` single clear, and transition-`None` bulk clear, each with exact field/closure preservation, reload, and guarded Undo.

The historical `full-e2e-three-products` guard is stale for the current popup source; this is a historical lock issue, not a defect in App runs `23809`/`9310`. Those runs were not repeated.

## P3

Source: `tests/e2e/local/three-products.spec.ts`  
Blob `9091d36fa38e961a9089e668beb456495e9338b8`; SHA-256 `741bcfb986fe0e80bbf81a40f741418991ed7e59cda59e578060b818e7d7cd94`.

Case:

`M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent`

Support source: `tests/e2e/local/support/gate5-reset-precondition.test.mjs`, blob `ce3fcbe67a5f9199df4150c7471cbec8e4291428`; SHA-256 `456489a94f83eba97e6d72a5d7a8c8d104f2c2116086a02b04c155631441a38f`.

## P4

SDK tests under `tests/sdk/test_p4_*.py` are support evidence only; they use fake, detached, or monkeypatched boundaries.

The three real Runtime-service proof nodes are:

- `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
- `tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo`
- `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document`

Existing route:

```text
request-test integration:agent p4-v2-http-nodes --files "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo tests/editing_conformance/test_p4_note_rerun_v2_runtime.py::test_http_note_conflict_reruns_public_function_from_verified_peer_document"
```

`p4-v2-http-nodes` requires `--files`. The nodes preserve CLI/Python/sheet production commit, show/history/readback, ten-note per-step undo/redo after restart, and exact `[200, 409, 200]` conflict rerun.

## P5

Sources:

- `tests/test_timeline_commit_integration.py` — blob `899489213da5a6a5b1e29430359830463da95501`; SHA-256 `867a33c5c1cda39e1cb540d1fb378b3987eaacc8ceb89d67c3f23711ec400534`
- `tests/test_timeline_commit_crash.py` — blob `9a5a1dfb1422c0f031e16dd59df921cd0d29d4a2`; SHA-256 `9a7d201f6d3e2d66898ab6f901a5567c9808bf23520be5b50d06a148813f1e63`

Preserved qualification is exactly the prior 14 integration tests plus 24 current-provider crash tests, on Runtime `62c454ac/tree b84e048` and Agent `f894c3c9/tree d24f25a`.

- Existing command: `request-test integration:runtime commit-integration`
- Existing command: `request-test integration:runtime first-capture-integration`
- Prior exact 24-case command: `request-test integration:runtime marked-integration --files tests/test_timeline_commit_crash.py`

The 24 cases are the parameterized commit/restore acceptance-boundary, retained-input, and host-boundary first-capture nodes. Restore is genuine Runtime crash/idempotency coverage at `/v1/.../composition-revisions/{revision}/restore`; it is not an alternative App authoring authority.

## C0 envelope

Preserve the complete request fields: `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands(schema_version,op,version,select,args,created)`, `label`, `steps(id,label,intent,tags,command_ordinals,patch,reads)`, `merge`, `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, `group_id`.

Replies preserve `data`, `receipt`, `accepted|merged`, authentic historical `rebased`, canonical document/digest, `id_map`, base/previous/accepted heads, merge mode, provider/compiler/publisher, records/effects/dependencies, steps/history/undo steps, preview/required/would-status, structured conflict reason/head, and invalid `code/path/hint/suggested_command`.

## HOST/repo-key routing correction

`request-test` accepts `integration:REPO` or worker metadata, then suite lookup is by the repo key in `suites.conf`. `test-run` executes that repo’s registered command, which may select another service through `ASTRID_CHECKOUT` or `ASTRID_RUNTIME_CHECKOUT`.

Therefore, absence of an `app`-prefixed P4/P5 row does not prove App-HOST execution is unsupported and does not require a new suite entry.

The remaining genuine App-host input is an available registration/checkout carrying the exact final Agent/Runtime tuple, authenticated child/import identities, and preflight. Until that exists, P1–P5 remain mapped but not final-tuple qualified. Safety/classifier refusal must stop the affected action; no alternate route is authorized.

## Verification

- `git diff --check HEAD` — passed.
- `git status --short --branch` — clean.
- No tests, browser, HTTP, socket, backend, service, `request-test`, build, install, or full suite was run.