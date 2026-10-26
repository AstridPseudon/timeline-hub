# Protected review: FAIL

The exact final 22-selector run passed (`22 passed`), but the migration does not preserve every protected assertion/caller proof required by D141ii. The author’s 22 green nodes therefore do not earn protected PASS.

## Finite findings

1. **F1 — IDs 5 and 6 lose explicit one-attempt proof.** The migrated CAS tests assert refusal, unchanged file, and unchanged history, but do not assert the supported `commit_timeline` transport was called exactly once. The original protected cases asserted one writer call; the owner scope requires no-retry behavior to remain live. `tests/packs/timeline/test_cli_status_publish.py:389-413`.

2. **F2 — ID 7 loses accepted-head authority.** `test_commit_migration_forwards_key_once_and_refuses_force` checks accepted status, receipt key, label, and one labeled call, plus parser refusal of `--force`, but never checks the returned/landed accepted revision or head authority. The approved change only replaces `force=True` forwarding with refusal; success/head authority remains protected. `tests/packs/timeline/test_cli_status_publish.py:29-50`.

3. **F3 — ID 8 drops the JSON half and call ordering.** The migrated summary test runs only human mode. It no longer asserts the exact five-key JSON envelope, `data == receipt`, or that edits/cuts are read before the single commit call. These were explicit predicates of the original test and are not established by the current one. `tests/packs/timeline/test_cli_status_publish.py:369-385`.

4. **F4 — ID 9 drops explicit unchanged status and zero mutation-call proof.** The clean-copy test checks null receipt, unchanged history length, and unchanged bytes, but not the new `status == "unchanged"` reply shape or that no commit transport call occurred. The owner disposition names both unchanged status and no-op/no-write behavior. `tests/packs/timeline/test_cli_status_publish.py:415-423`.

5. **F5 — IDs 12 and 13 are presenter-only tests, not supported-caller tests.** Both migrated actor cases call private `_commit_conflict_message` directly with a fabricated `SimpleNamespace` and details mapping. They do not drive `commit_document`/`_document_error` through the authenticated commit path, so the actual supported caller’s editor-specific and generic actor output is unverified. The brief forbids source-only analogue credit. `tests/packs/timeline/test_verbs_working_copy.py:595-617`.

6. **F6 — ID 18 materially weakens the protected empty-create assertions.** The migrated test checks shell, identity, a timeline-init command prefix, a partial output, clips, and empty child lists, but drops the original parent name, full config/defaults, registry, occurrences, exact command output, history/bootstrapping, base pair, and recorded step-read assertions. A separate D66 test is stronger, but the assigned migrated ID itself must preserve its protected predicates; relying on a counterpart is not a repair of this weaker replacement. `tests/v10/test_timelines_create.py:517-552`.

7. **F7 — exact mypy reproduction is not green.** The required command `mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py` fails before checking the target because the shared environment’s NumPy stub contains a `type` statement rejected by the configured mypy Python version. Ruff, py_compile, and git diff --check pass. This is an environment validation failure, not a source finding, but the author’s mypy PASS is not independently reproduced.

## Positive checks

The 15 assigned migrated selectors all executed and passed; the seven neighboring current selectors also passed, for 22 PASS / 0 FAIL / 0 ERROR. The diff is exactly the eight allowed files: seven named test files plus `astrid/packs/timeline/cli_native.py`. The Runtime remains the configured source at commit `95d98f038320d5d46bd679ac000ab3e15825c935`; no installer, inverse, schema, lock, Runtime, or unrelated blob changed.
