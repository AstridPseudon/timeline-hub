# D141ii writer-caller protected review: PASS

## F5 — closed through the supported caller

Both exact actor-namespace cases pass through the public `commit` parser and `commit_document`, then `TimelineSession`, `RemoteTimelines`, `WorkspaceClient`, the generated `commit_timeline` method, Runtime's commit service and real provider conflict, generated error decoding, SDK error conversion, and public JSON rendering. The tests do not call `_document_error` or `_commit_conflict_message` directly and do not fabricate an exception.

The helper binds the request's `base_revision_id=rev-0` and `base_publication_id=bootstrap`, asserts the generated POST path and idempotency key, executes the provider against `DetachedRealm`/`DetachedPort`, and asserts Runtime's actual 409/public-failure details. `current` is the resulting Runtime head; the actor wording is derived from the retained revision namespace before the invocation. File bytes, documents, entries, accepted state, prepared state, and call count remain unchanged after refusal. Force-overwrite wording remains refusal-only.

The manager clarification controls the interpretation: IDs 12/13 preserve revision-namespace diagnostics (`astrid.editor.timeline.*` means “the editor”; the authoring namespace means “someone”), not an authenticated actor-ID field. Runtime's conflict envelope carries base/current pins and conflicts, not publisher. The test proves supported caller propagation for that original namespace-message purpose. It does not claim live bearer-door authorization or SQLite persistence; those are outside this protected scope and would require an additional gate.

## F7 — environment finding retained honestly

The exact default mypy command fails identically on baseline and candidate while parsing the installed NumPy stub's Python 3.12 `type` syntax under the repository's configured target. The explicit `--python-version 3.12` diagnostic passes on both. This is `FAIL_ENVIRONMENT`, not a source finding and not a substituted green result.

## Prior finite findings and lineage conservation

F1–F4 and F6 remain closed only through the prior exact 29-selector evidence plus exact source/blob/AST conservation, as directed; no broad duplicate run was performed. The original 15 purpose mappings are preserved in `per-id.json`, with IDs 5/6, 10/11, and 12/13 represented by their distinct exact parameter selectors. The final integrated selector packet separately contains 38 retained inverse selectors plus 15 writer selectors (53 original purposes / 53 actual selector nodes).

## Owner-facing reply-shape changes

The reviewed lineage changes legacy writer surfaces to the approved C0 shapes: accepted commit envelope; bounded human/JSON output; partial-publication refusal with receipt details; shell plus `timeline.init`/`doc.patch` empty create; requester-owned guarded render publication; and typed conflict/approval/restart responses retaining base/current/request authority. The final Sol delta changes tests only and introduces no new reply shape.

## Limits

No full, core, browser, install, render, child, live-journey, or broad suite was run. No Runtime/App/Composition worktree was modified, no branch/Git-internal operation was performed, and no product repair was justified.
