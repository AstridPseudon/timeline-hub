# F-authoring-ABA finite report

**Verdict: FAIL**

- Exact packet: `agt-F-final-source-join-0816-authoring-current-becfe-nodes-1024085217-20732`
- Requested test: `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
- Result: exit 1; 1 failed in 40.19s.
- First failure: line 1090, expected `transport_error`, received `transport_timeout`.
- Original test blob: `e55be12f88d23fddba3dd36614eb91745c1f8adf`
- AST inventory: 59 assertions. Assertions 1–41 passed/reached; assertion 42 failed; assertions 43–59 did not run.
- Therefore retry, durable undo receipt/history, disjoint rebase, and A→B→A protection are unverified.
- No prior ambiguous-path failure appears in this packet, but that is not evidence of durable lost-ack success.
- The hook firing and durable acceptance are not evidenced: `undo_wire` and flight assertions occur after the first failure.

Pins verified from retained output/current repos:

- Agent `0c2c28da…`, tree `4ce9de35…`
- Runtime `becfe6db…`, auth blob `979225ab…`
- Source123 commit `a0dca169…` is present.
- `git diff --check`: pass.
- Worktree remains clean; no production/source/test changes made.
- Retained `11466FAIL` and `26998precollection` exit 4 were not modified or rerun.
- Recorded profile hashes could not be independently re-read because the retained ephemeral profile path is gone.

Commit message was written and `DONE` created. Recommended next step: bounded Agent-side investigation of the timeout/error mapping while preserving the strict `transport_error` expectation and all 59 original predicates.