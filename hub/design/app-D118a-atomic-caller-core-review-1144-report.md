# D118a Protected Core Review: PASS

Reviewed author commit `8a4103dd16bb32306ca6c782dcd9a7a4a908de6d` against base `0ad49261ed36f043b059c07de989bd39cd3a5889`.

The diff is exactly one production line: `_bundle` → existing `_capture_bundle` in `timeline_document.py`. Public bundle privacy remains intact; detached publication receives the authenticated exact revision/publication pair and `_runtime_document`.

Runtime: commit `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, clean.

Tests:

- Original atomic node: `1 passed in 2.57s`.
- Private source/wrong-pair/no-write controls: `4 passed in 18.19s`.
- Ruff, mypy (`--follow-imports=skip`), py_compile, and `git diff --check`: passed.
- Original test SHA256: `c4e95a4cdc74fe8de9b151c818492f6a2fd4301c699a43bc686611bcbdeff5a4`, unchanged.
- Original test AST: equal; 48 assertions preserved.
- All non-target blob objects match base.

Original XML:

```xml
<testsuite errors="0" failures="0" skipped="0" tests="1">
  <testcase name="test_complete_json_script_commit_authenticates_materialized_atomic_scopes"/>
</testsuite>
```

Private controls XML:

```xml
<testsuite errors="0" failures="0" skipped="0" tests="4">
  <testcase name="test_session_capture_reload_and_function_keep_verified_pair"/>
  <testcase name="test_session_pair_authentication_refuses_without_writes[wrong-revision]"/>
  <testcase name="test_session_pair_authentication_refuses_without_writes[wrong-publication]"/>
  <testcase name="test_session_pair_authentication_refuses_without_writes[missing-entry]"/>
</testsuite>
```

Evidence: [facts.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118a-atomic-caller-core-review-1144/evidence/facts.md), [facts.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118a-atomic-caller-core-review-1144/evidence/facts.json).

Reviewer ledger: The production caller uses the existing private authenticated capture seam; `_bundle` remains caller-visible and source-private. Exact pair binding, stale/wrong-pair refusal, no-write behavior, emitter source binding, and atomic publication receipt were independently verified. No tests or source were modified by this review. No adoption, gate, or full-suite claim is made; the later Agent unfiltered core suite remains owed.