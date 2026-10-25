# D120 current element11251 whole-path facts

## Result

Overall readiness is NO-GO: the retained run exited 1 after 643 seconds with readiness 1 PASS, five original cases PASS, two FAIL, and one NOTRUN. This investigation found the first observed failure at the App element completion/status boundary. It did not prove a Runtime or Agent failure and does not justify a source repair.

Pinned tuple: App 34d4644589970274a5252c0f7c68b6288eb0b0b4 / tree 48d71e1a0c18a13668e1d1e086def9dd6210affe; Agent 070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2 / tree 6056414359ae9fce08d999d54cbecf719fda33c3; Runtime 7070f1378d1917fcce69857ebd33cd2b3015568b / tree cd68015cb9fe85a6ecd2d15dd7e2eac69f67e2b1; Composition 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 / tree 5ab5191a296980a0a6bcd1178ab6902d6478a148.

## Actual call path

The element test at tests/e2e/local/three-products.p2-elements-assets.spec.ts:1038-1052 clicks Apply and waits for status text applied. ElementsLibraryPanel.tsx:46-107 sets that message only after capturedAdapter.execute(...) resolves. The adapter (element-adapter.ts:389-497) applies the operation locally, then awaits routes.save. The element save route (useTimelineSave.ts:743-801) adopts the local document and awaits handoff.flush. The handoff (timelineLocalSaveHandoff.ts:575-627) appends an atomic v2 commit intent and flushes the session; localSaveSession.ts:158-208,315-321 waits for the outbox pump to obtain an acknowledged saved state.

The pinned Runtime path is request handling in runtime_protocol/server.py:294-321, Runtime commit execution in timeline_commit_execution.py:222-275, and Agent provider validation/execution in astrid/sdk/timeline/commit.py:1160-1190. The source path is identifiable, but the retained evidence does not correlate this element request to a Runtime request or Agent outcome.

## First observed boundary and timing

The safe element diagnostic has local correlation apply-1. The trace recorded Apply at 42882.602 ms, started the applied-status wait at 43164.572 ms, and ended that wait at 48239.326 ms. Diagnostic read occurred at 48261.214 ms and page close at 48281.304 ms. Therefore the nominal 5-second applied wait hit before test-context teardown. The retained state was connected, dialog present, status pending, and button applying. The later response wait failed because the page/context was closed; that is not evidence of a server result.

The network trace retained a commit-classified POST initiation with no response, plus another unresolved POST whose semantics are not inferred. The diagnostic recorded a scoped commit with an idempotency key present, but response status UNKNOWN, response none, and terminal pending. The first actual observed failure is consequently App completion/status while the commit remains pending. Runtime outcome, Agent outcome, and whether a response was lost remain UNKNOWN.

## Runtime evidence and limits

Six retained Runtime phase namespaces were available: four populated through an HTTP phase, one had authorization/provider raised states without an HTTP phase, and one was empty. All six stderr files were empty. None carries the local apply-1 correlation, so no namespace can safely be assigned to element11251. The retained Runtime records also leave the caller receipt boundary, client-to-server receive boundary, and exact execution-lock wait boundary unknown. Producer1145’s terminal extraction was used as existing evidence and not duplicated.

## Passing-path comparison

The five authentic passing cases were popup ADD occurrence fork/A2 commit, single parent move, transition None single, transition None bulk, and automatic child placement. Each reached accepted/canonical closure, history, reload, guarded native Undo, and no legacy tail. The element case is distinct in using the App element adapter through elementTimelineRoutes.save and handoff.flush; it failed before its request/reply, canonical readback, history, and guarded-undo assertions. This is a bounded path difference, not proof of a hidden payload or Runtime cause.

## Exact missing evidence and disposition

The finite missing facts are: cross-layer correlation from apply-1 to Runtime; whether Runtime accepted, merged, refused, or never received the request; whether an accepted response was lost after server processing; and whether the App outbox retained pending or accepted state after page close. No minimum unapplied repair can be named without those facts. No source, test, pin, timeout, guard, input, assertion, collector, or service probe was changed or added.

Artifact and source SHA-256 hashes are recorded in facts.json. The retained trace ZIP hash is 9e4338be3235e38cb1377bad8f2994785238e7ab5f8ca2ef2d5c6f0cc75cb668; diagnostic JSON hash is 3ebfb19267ac21080a387bd2a0464d503be26152bb254c075932ee544d402821.
