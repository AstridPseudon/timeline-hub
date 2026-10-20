Implemented WC6 HTTP ACK proof correction in `tests/timeline/test_authoring_media.py`.

- Drops the response before any HTTP bytes are sent.
- Asserts `WorkspaceClientError`, status `0`, code `transport_error`.
- Verifies identical outbox body/key replay, durable receipt/head/history, F1 verification, redo, and ABA guards.
- Product code remains unchanged from `841581fc`.

Test:

```text
native-script-current-integration --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
```

Result: **1 passed in 14.35s**.

Proof report: [agent-wc6-http-ack-final-proof.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc6-http-ack-final-proof.md>)

Commit message and `DONE` written.