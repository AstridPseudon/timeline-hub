# Handoff

## Result

F5 is still open: the two actor cases at `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_verbs_working_copy.py:595-627` call `_document_error` directly with fabricated details. They do not exercise `commit_document`, `TimelineSession`, generated `commit_timeline`, Runtime's authenticated 409, `WorkspaceClientError`, or public CLI rendering.

The closest passing control is `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_cli_status_publish.py:412-438`: real CLI/provider CAS, unchanged file/history, exactly one transport call, but generic conflict output only. The generated-client detail control is `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/sdk/test_runtime_response_conformance.py:220-234`; it does not reach CLI. The real door/generated-client/public CLI setup is `/home/user/work/runtime/tests/test_timeline_commit_integration.py:432-448` plus `/home/user/work/runtime/tests/test_timeline_public_s2_mixed_cli_journey.py:145-164`, whose current journey observes raw 409 details but not actor wording.

## Authority finding

Runtime's accepted `publisher` is authoritative and comes from the authenticated HTTP actor (`/home/user/work/runtime/runtime_protocol/server.py:304-341`, `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1881-1895`). Conflict details do not carry `publisher`; they carry only base/current revision/publication pins and conflicts. The current CLI wording is therefore revision-namespace presentation (`astrid.editor.timeline.*` => “the editor”, otherwise “someone”), not actor-ID preservation. Both protected cases are namespace cases, not actual actor IDs transported through the conflict.

## Finite obstacles

1. Caller-level F5 proof is absent.
2. The conflict envelope has no actor/publisher field, so exact actor identity cannot be proven from the conflict alone; only namespace-category wording can be checked without a history lookup or contract change.
3. Normal Agent commits produce `authoring-parent-revision-*`; the editor namespace needs an App/retained seed. No existing fixture joins both namespace seeds with generated HTTP transport and public CLI output.
4. F7 exact mypy is `FAIL_ENVIRONMENT` at NumPy `__init__.pyi:737` (Python 3.12 `type` syntax rejected under configured Python 3.11 target); `--python-version 3.12` passes diagnostically.

No other finite obstacle was found. No source/test repair or pytest run was performed.
