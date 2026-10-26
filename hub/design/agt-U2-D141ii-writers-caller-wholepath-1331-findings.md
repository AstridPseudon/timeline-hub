# D141ii whole-path caller investigation

## Verdict

The second review's F5 remains open. Both actor parameters still test only the private presenter with a fabricated `SimpleNamespace` request and fabricated refusal. The supported CLI-to-Runtime path is present and a genuine CAS selector route passes, but no existing test proves actor-specific public output after a structured conflict has crossed the Runtime/generated-client boundary. F7 independently reproduces as an environment failure only.

No source, test, configuration, dependency, Runtime, branch, or Git-internal files were changed. No pytest suite was run.

## Actual supported path

The production `commit` command dispatches as follows:

1. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/packs/timeline/cli.py:2239-2243` calls `cli_native.commit_document`.
2. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/packs/timeline/cli_native.py:174-205` loads the detached file, calls `_preview_detached_document`, catches `WorkspaceClientError`, and passes it to `_document_error`; `print_result` emits the public JSON or human result.
3. `cli_native.py:145-171` opens `TimelineSession` and constructs a `Timeline`; the commit call at `cli_native.py:168-171` reaches `Timeline.commit`.
4. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/timeline/commit_session.py:163-254` captures the request, freezes the body/key in `TimelineSession.submit`, and only re-evaluates a function commit after an explicit conflict. A label/document commit does not retry or re-run after refusal.
5. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/timeline/sync.py:525-601` writes the outbox flight, calls `self.client.timelines.commit`, turns structured `status in {conflict, refused, invalid}` details into `CommitConflict` at lines 559-569, and leaves the flight/history unchanged.
6. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/remote.py:335-445` dispatches `commit_timeline` to the SDK workspace client and converts `WorkspaceClientError` into a `DomainResult.failure` while retaining `code`, message, and details.
7. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/workspace_client.py:485-500` forwards the exact body and `Idempotency-Key` to the generated client. `workspace_client.py:218-325` converts generated `ApiError` into `WorkspaceClientError`, retaining status/code/message/details.
8. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid_runtime_client/generated.py:963-965` sends the generated `POST /v1/projects/{project}/timelines/{timeline}/commit`; `generated.py:599-604` decodes an HTTP error's JSON `code`, `message`, `request_id`, and `details` without discarding structured conflict fields.
9. Runtime's HTTP route `/home/user/work/runtime/runtime_protocol/server.py:301-341` authenticates `identity`, sets `publisher = identity["actor"]`, and calls `RuntimeService.commit_timeline` with the canonical path and publisher.
10. `/home/user/work/runtime/runtime_protocol/service.py:2468-2580` validates the request and binds `publisher` into the provider context. Provider failures are projected by `public_failure` (`/home/user/work/runtime/runtime_protocol/timeline_commit_port.py:89-103`) back to the public 409/code/details shape.
11. The genuine Agent provider creates conflict details from the authenticated base/current pins and conflict paths at `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/timeline/commit.py:1160-1452`; in particular dependency/media conflicts include `base`, `port.head()` as `current`, path, and `status="conflict"` (lines 1204-1214), while CAS acceptance races retry internally up to three attempts (lines 1336-1452).

## Actor authority versus presentation

Runtime's authoritative actor source is the authenticated bearer identity, not the request body: `server.py:304-326` obtains it and `server.py:333-341` passes it as `publisher`; accepted data is stamped from `context["publisher"]` at `/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1881-1895`. The history metadata contract likewise says publisher is added from authenticated execution context, not accepted from the request (`timeline_commit_store.py:96-110`).

The conflict envelope is different. The provider's `_failure` path and `CommitFailureDetails` carry `base`, `current`, `conflicts`, `reason`, `path`, `hint`, and `suggested_command`; `current` is only a revision/publication pin. The generated error fixture at `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/fixtures/runtime-responses/publish_conflict_409.json:2-22` confirms there is no `publisher` or actor field in the structured conflict.

`/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/packs/timeline/cli_native.py:13-43` therefore does not preserve an actor ID. It presents a category by testing whether `current.revision_id` starts with `astrid.editor.timeline.`; otherwise it says `someone`. `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/astrid/sdk/timeline/revisions.py:17-62` documents these namespaces as revision-source categories (`app` versus `astrid`), not authenticated actor identities. The current presenter does not consult the authenticated `publisher`, history, or `revision_source`.

The two protected cases are namespace cases, not two transported actor IDs:

- `astrid.editor.timeline.5fb2249e...` presents “the editor”.
- `authoring-parent-revision-38cecaa5...` presents “someone”.

The second review's current test at `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_verbs_working_copy.py:595-627` fabricates both revisions and calls `_document_error` directly. The original protected test at the base, `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_verbs_working_copy.py` as shown by `git show 14ccf296f3:tests/packs/timeline/test_verbs_working_copy.py:599-621`, used a fabricated legacy `store.publish_bundle` path; it did not establish the new supported caller either. Both are insufficient for the requested whole-path proof.

## Passing genuine CAS route and smallest reusable setup

The closest passing current caller test is `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_cli_status_publish.py:412-438`, `test_normal_commit_cas_refusal_preserves_file_and_does_not_retry`. It drives the real CLI `commit` handler, real detached document loading, `TimelineSession`, the real Agent `create_runtime_commit_service`, and the Runtime conflict semantics. It proves conflict code, unchanged file, unchanged history, and exactly one additional transport call. Its fixture is `normal_commit` at lines 65-127, backed by `tests/sdk/test_timeline_public_command.py:28-88`; that fixture uses a real `DetachedRealm` and provider but a hand-written `RemoteTimelines._typed` adapter, not the generated HTTP client.

The stronger real-Service fixture is `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/packs/timeline/test_cli_document_commit.py:19-153`: it creates a real `RuntimeService`, registers `create_runtime_commit_service`, and routes CLI commit calls through `service.commit_timeline` at lines 101-118. It still uses a hand-written `Reader._typed`/`SimpleNamespace` transport and hard-codes `publisher="actor-1"`; it is not generated-client/HTTP evidence.

The existing generated-client structured-error proof is `/home/user/work/wt/agt-U2-D141ii-writers-caller-wholepath-1331/tests/sdk/test_runtime_response_conformance.py:220-234`. It uses `GeneratedWorkspaceClient` with an injectable transport and proves the 409 details/request ID/Idempotency-Key survive. It stops at `WorkspaceClientError` and does not invoke the CLI.

The existing real generated-client plus public CLI setup is in the Runtime integration source: `/home/user/work/runtime/tests/test_timeline_commit_integration.py:432-448` starts the authenticated door, and `/home/user/work/runtime/tests/test_timeline_public_s2_mixed_cli_journey.py:145-164` creates `AstridClient` and the public CLI helper. The journey at lines 238-420 observes the real 409 wire response and proves `code="conflict"`, `reason="dependency_changed"`, exact body/path/key, no write, and later retry behavior (lines 384-394), but it does not assert either actor-specific CLI diagnostic.

Thus the minimal existing *pieces* are:

- current Agent `test_cli_status_publish.py:412-438` for the supported CLI/CAS/no-retry predicates;
- Runtime `_start_door` plus `AstridClient`/`_cli` above for actual generated-client transport;
- generated-client conflict decoding in `test_runtime_response_conformance.py:220-234` as the structured-detail control.

No single existing fixture joins all three pieces and seeds both protected revision namespaces. The Agent provider's normal accepted revision identity is always `authoring-parent-revision-*` (`commit.py:401-419` and Runtime's equivalent authoring identity at `/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1833-1847`). The `astrid.editor.timeline.*` head must come from an App/editor-authored seed or an equivalent retained Runtime fixture. That missing seed is a finite setup obstacle, not evidence to replace with a private presenter test.

## Finite remaining obstacles

1. **F5 / caller coverage (behavioral, open):** both parameters remain private `_document_error` tests with fabricated `Refusal` and details. They do not cross `commit_document` → `TimelineSession` → generated `commit_timeline` → Runtime 409 → `WorkspaceClientError` → public renderer.
2. **Actor source availability on conflict (semantic boundary):** Runtime's structured conflict has no authenticated `publisher`; it returns only a current head pin. The current CLI can preserve only the revision-namespace category, not a true actor ID. A proof must either state that namespace-category presentation is the intended requirement or use an existing history/seed authority; this investigation does not invent an auth mechanism or alter the envelope.
3. **Both namespace seeds (fixture/transport):** current Agent commits naturally produce `authoring-parent-revision-*`; the editor namespace requires an App/retained seed. The current local CLI fixtures do not provide that seed through the generated HTTP client.
4. **F7 / exact mandated mypy:** the exact command fails before checking `cli_native.py` because the shared Python 3.13 environment selects the repository's Python 3.11 target while installed NumPy stubs contain Python 3.12 `type` syntax. The explicit `--python-version 3.12` diagnostic passes, but it is not a replacement for the mandated command.

No other finite obstacle was found in the requested scope. The supported transport preserves structured details; the genuine CAS route preserves no-write/no-retry behavior; force remains parser-refused; and no source repair is justified by this read-only investigation.
