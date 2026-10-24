# R5 family review — FAIL

Candidate: `2c3a539895a075c9796d630332daf3b9e04c76bb`  
Tree: `6e71b4a6807a5b914d133d6f6243ab5f351966c7`  
Original: `458595850c354f4403dabc58a72b98bebbc2c3a3`  
Original tree: `703b1aac733ad3c977399e67cd4e23d6ae85e7bb`

Only `tests/test_timeline_headless_overwrite_refused.py` differs; no tracked edits were made.

Checks:

- Targeted pytest: `12 passed`
- Ruff: passed
- In-memory compile: passed
- `git diff --check`: passed
- Pyright: parent 4 existing `reportOptionalSubscript`; candidate 0; zero new normalized diagnostic identities/multiplicities
- No skips, xfails, deselection, or guard weakening
- No full suite or final gate run

Findings:

1. Refusal coverage remains weakened. `_refused_headless_create()` calls `create_timeline()` without the original submitted publication body or command and only checks generic same-ID conflict details. Authored, empty-shell, hidden-content, and scoped-row cases therefore do not exercise their original raw inputs or source-specific predicates.

2. The hidden-content test constructs `body` but never submits it; the `body["parent_composition"] == ...` assertion is tautological. The original public `head_revision_id is None` assertion and `headless_content_not_empty` reason are gone.

3. The scoped-row variants manually assert `timeline_scope_is_empty()` is false, then invoke the generic adoption refusal. They would still pass if production rejected all same-ID shells unconditionally.

4. The genuine-empty bootstrap and CAS edit are current-path positives. CAS uses the real Agent provider through `RuntimeService.commit_timeline` → coordinator → `RequestCommitPort` → Agent provider (`/home/user/work/agent`, SHA `521c88802330901281cc37ba25818baf2575f05e`). The exact retry does not invoke the provider again (`calls == 1`). However, the test uses `authorize=lambda: None`, so the HTTP door’s strict identity check is not exercised.

5. Accepted CAS assertions cover canonical document, prior head pins, receipt, history command record, event, closure, and content digest, but do not assert the full requested v2 response surface: head/revision digest projections, effects, bindings, dependencies, step records, or undo steps. No merged/invalid/preview case is covered here.

The retained legacy route 410/no-write test is valid additional authority evidence, but it does not replace the missing current-equivalent refusal and positive assertions.

Recommended next step: revise the refusal cases to submit faithful current commit/adoption inputs and bind each assertion to the corresponding authored, hidden, and scoped-row predicate; retain the 410 test and expand accepted-response/provider/auth-boundary assertions.