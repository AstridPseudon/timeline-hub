# D136a/D100 independent result review

## Finding 1 — actual original9 is a finite bounded failure

The preserved private XML was parsed in place. It contains the exact retained nine selectors: 9 testcases, 9 setup errors, 0 failures, 0 skips, and 0 passes. Every error carries the same first message: `candidate: all authored fps declarations must retain their typed locations`. The private XML, log, and run metadata remain mode `0600`; no raw artifact was copied or published.

The run used the reviewed Agent source and immutable Runtime pin recorded by the receiver. Its published admission readings and source/module hashes are consistent before and after. No retry, selector substitution, fixture adaptation, alternate Runtime, full suite, browser, socket, native-provider, collector, or new result run was used.

## Finding 2 — first proven source seam

The setup failure is at the first explicit source commit, `capture-source-init`, not at a later saved-projection assertion:

1. `tests/sdk/test_capture_source_runtime.py:262-268` calls `capture_initialize` with an explicit typed `output.fps` value of `30`, then submits that command through Runtime `commit_timeline`.
2. `astrid/sdk/timeline/native_initialize.py:7-22` requires the pristine empty baseline and writes the supplied object at `parent.config.output` on line 19.
3. `astrid/sdk/timeline/commit.py:1410-1417` invokes final validation with the resulting candidate and the pre-command bundle as baseline.
4. `astrid/sdk/timeline/validation.py:95-108` maps the candidate's authored output declaration to `parent.config.output.fps`, while the pristine baseline has no such declaration.
5. `astrid/sdk/timeline/validation.py:141-145` requires the two location sets to be equal and raises at lines 143-144.

Therefore the caller does not remove a genuinely typed `output.fps`. The new guard rejects a candidate-only authored declaration during initialization. This is not the semantic default/open-canvas path: the first command supplies `fps=30`, and the traceback reaches `_validate_fps` directly. The open-canvas fallback in `_timing_evaluators.py` is not the observed first seam.

## Finding 3 — whole-path caller/provider review

The production path remains one canonical route:

- App `RuntimeDataProvider.commitTimeline` validates project/timeline and verified revision/publication identity, calls the generated client, and refuses a preview as an accepted mutation (`dataProvider.ts:751-767`).
- App `RuntimeClient.commitTimeline` delegates through the mutation/session boundary (`client.ts:739-745`). The mounted outbox/bootstrap ports point to this method (`dataProvider.ts:506-519`, `522-535`).
- Public Agent `WorkspaceClient.commit_timeline` delegates only to generated `commit_timeline` (`workspace_client.py:485-500`); the remote dispatcher and authoring writer use that same operation (`remote.py:355-356`, `1547-1559`).
- Runtime's HTTP route authenticates `projects:write`, checks route/body identity, requires the idempotency key, and invokes `RuntimeService.commit_timeline` (`server.py:300-340`).
- Runtime validates the request/path and enters the coordinator (`service.py:2469-2483`, `2485-2559`); the coordinator binds invocation identity, calls the registered provider, verifies its outcome, and handles replay/refusal semantics (`timeline_commit_execution.py:373-431`).
- Startup loads only the explicit `astrid` provider profile and validates its exact ABI/contract (`timeline_commit_provider.py:70-93`); service registration is startup-only and installs verified baselines before serving (`service.py:2412-2432`).

No alternate provider, fallback writer, mutable environment substitute, or public payload/private-identifier leak was found in this read-only path review. The C0 request/reply authority remains at Runtime; the App and Agent callers do not become writers.

## Disposition

Source/product release remains held. Existing 27-pass/source/security reviews are reused as bounded prior evidence only; the 45 source checks from the receiver are not nine-behavior or full-scope credit and were not duplicated.

Smallest owning continuation: the existing Runtime D136a owner should adjust the final FPS location guard so a newly authored canonical typed declaration (including `timeline.init`'s `parent.config.output.fps`) is not rejected merely because the pristine baseline had no declaration, while retaining finite-number validation, the typed-output guard for removed/moved existing declarations, and the open-namespace/fallback rule. Do not migrate the fixture or lower the test assertion. This review made no product change.
