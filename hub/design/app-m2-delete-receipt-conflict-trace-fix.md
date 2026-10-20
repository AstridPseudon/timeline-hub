# App M2 parent-delete receipt/conflict trace fix

## Result

Both reported failures were test expectation errors; no App product code changed.

- Runtime `MutationReceipt.receipt_id` is the persisted transaction/publication identity. Its separate `idempotency_key` is the request retry identity. The captured wire from the prior central run showed `receipt_id=eeb52a6f-6c82-4baf-8609-965fb94815be` and request key `txn-37aea606741a40d287324637025fd4b9`, matching the Runtime source and generated DTO.
- Runtime/App outbox rejection is additive: `pending.outcome={kind:"rejected",...}` and dependent `intent.conflict` are recorded, while the original intent payload/guards and `pending.request` bytes/key remain unchanged. This is the existing `commitOutbox.ts` model and is covered by its unit tests.

## Expectation ledger

| Old assertion | New assertion | Preserved evidence |
| --- | --- | --- |
| `receipt.receipt_id === request key` | `receipt.receipt_id` is non-empty; `receipt.idempotency_key === request key` | publication identity remains carried by `receipt_id`, and `receipt.result === data`; accepted retry still compares the complete receipt/result object exactly |
| retained `intents` and `pending` equal the pre-409 snapshot byte-for-byte | strip only additive `intent.conflict`; compare all original intent fields and `pending.request` exactly; assert rejected conflict state and its reload/recovery equality | original command/guards/body/key remain exact, visible real 409 remains required, remote head/history remains Agent move, no legacy writes remain required |

## Source and tests

- App base commit/tree: `b91aa0c16cc9817b8078fdfe11c7bfca95853a52` / `a3ea802324e3d269c474046fe71526e99fea5228` (working tree has only `tests/e2e/local/clip-delete-command.spec.ts` modified).
- Prior captured source tuple: Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`; Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`; public Composition 0.0.12 SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- `node --experimental-vm-modules --test scripts/testing/current013-parent-delete.test.mjs scripts/testing/current013-integration.test.mjs` — 2/2 passed.
- `node node_modules/eslint/bin/eslint.js tests/e2e/local/clip-delete-command.spec.ts` — passed.
- `node_modules/.bin/vitest run --no-cache --configLoader=runner --config .vitest-local.config.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/commands/commitSession.test.ts` — 123/123 passed; private config was removed afterward.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/tl-app-delete-runtime-contract /home/user/work/runtime/tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge /home/user/work/runtime/tests/test_timeline_commit_port.py::test_created_timeline_provenance_and_exact_retry_survive_restart` — 2/2 passed.
- Required new central exact-source two-case run was not available: `/tmp/.../tests/suites.conf` contains only the obsolete pre-fix `e2e-parent-delete-treea3ea8023...` registration. It was not reused. Browser/localhost, full, TypeScript, build, install, and central qualification remain unverified.
