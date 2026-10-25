# Runtime P2 SWAP history-tag review

Verdict: **FAIL** for exact candidate `2867a197748124b42dcb42bb5171df421b5b1a70` against base `369ffa7c00bd3d45c610fac7651ff79e7a283a1a`.

## Findings

- `runtime_protocol/service.py:2529-2546` adds the intended boundary emission for `CommitRejected` and `ConflictError` history refusals. The public failure is still produced by `public_failure` or re-raised unchanged.
- `runtime_protocol/timeline_commit_execution.py:164-194` has fixed tags for four baseline categories and six port messages, with `history_provider_or_store_guard` as fallback.
- The protected sources are unchanged at the handoff hashes. The 31 direct `reject("history_unavailable")` sites in `runtime_protocol/timeline_commit_store.py` (including sites with messages such as `canonical film differs from accepted publication`, `timeline catalog facts are corrupt`, `history ancestry contains a cycle`, and `inverse stage history targets are unavailable`) all reach the fallback; none has a distinct private tag.
- `runtime_protocol/timeline_commit_reference_projection.py:147` raises a deliberate `ReferenceProjectionError("history_unavailable")` from `apply_reference_projection`. `TimelineCommitStore.accept` only translates the prepare-time error at `timeline_commit_store.py:1827-1840`; the apply-time refusal at `:1860-1864` escapes to the coordinator/service generic exception path, so it becomes a `catchall:...` diagnostic and public `503`, not a history-tagged private refusal. This is a concrete source/public-behaviour gap, not merely missing test coverage.
- Baseline verification exposes four intentionally grouped tags, but the many other `_require` history integrity reasons in `timeline_commit_baseline.py` are not individually mapped and therefore also fall back when they surface. The fallback therefore still collapses real roots.

The output line is bounded by the existing 4096-byte formatter and history-tag paths pass no exception object, so the handled paths emit one fixed-vocabulary private line with empty exception classes/frames. No payload, URL, bearer, raw exception text, or stack is added by this candidate. The existing private `request_id` correlation field remains present as in D102; no new shared provider context key is introduced. Public schema/envelope/API files are untouched.

## Coverage and evidence

The new three-test file proves: one fake provider refusal uses the fallback, one mapper example for a port message, and one monkeypatched baseline boundary. It does not exercise a real store emitter or real port emitter, and does not establish RED/GREEN evidence per tag. Existing port/baseline tests assert public `history_unavailable` details but do not capture stderr tags. The real registered provider path is wired through daemon startup (`runtime_protocol/daemon.py:239-257`) and `RuntimeService.register_timeline_commit_provider` (`runtime_protocol/service.py:2391-2411`) into the coordinator, but the candidate tests use a fake provider.

Exact App-15203 native SWAP replay was not run; the handoff records the retained D112 harness as not allow-listed. No native replay or GREEN claim is inferred. The known D102 fake-only/native-seed warning remains applicable.

## Commands

- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_history_diagnostics.py tests/test_timeline_commit_redacted_diagnostics.py tests/test_runtime_unavailable_reason_tags.py tests/test_timeline_commit_execution.py` — **38 passed**.
- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_port.py tests/test_timeline_commit_baseline.py tests/test_timeline_commit_routes.py tests/test_timeline_commit_acceptance.py` — **229 passed, 2 failed, 1 deselected**. Both failures are the existing authorizer replay cases: `PRAGMA data_version` is denied before candidate logic, yielding `sqlite3.DatabaseError: not authorized`; no candidate-specific regression was identified.
- `ruff check runtime_protocol/service.py runtime_protocol/timeline_commit_execution.py tests/test_timeline_history_diagnostics.py` — repository baseline reports 34 existing diagnostics; no diagnostic falls on the candidate-added helper/service lines or the new test file.
- `pyright runtime_protocol/service.py runtime_protocol/timeline_commit_execution.py` — **zero diagnostics**.
- `python -m compileall -q runtime_protocol/service.py runtime_protocol/timeline_commit_execution.py tests/test_timeline_history_diagnostics.py` — **passed**.
- `git diff --check 369ffa7c0..2867a197748124b42dcb42bb5171df421b5b1a70` — **one pre-existing/new-test EOF blank-line warning** at `tests/test_timeline_history_diagnostics.py:123`.

Source and protected-file hashes are recorded in the accompanying JSON evidence. No source edits were made by this reviewer.

## Ready handoff

First return to Luna should add stable tags at the live-owned store/reference-projection boundaries (or a precise boundary adapter that preserves the exact source category), add real-provider RED/GREEN stderr assertions for each supported emitter group, and repair the apply-time reference-projection refusal without changing guards, writes, CAS, trust, context, or public failure details. Re-run the targeted diagnostics and the exact allow-listed smoke before any native replay claim.
