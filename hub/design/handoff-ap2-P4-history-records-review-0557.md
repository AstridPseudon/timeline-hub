# P4 history-records independent review — PASS

- Candidate SHA: `7a62327b75840f3a45e83719d52e57422946d920`
- Candidate tree: `b07b812ac26d793f26b2edf37efd724d94a0ac3a`
- Reviewed against: `d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de`
- Reviewed test blob: `033482ec2b94c5ae4a6b5c456e2d9fab3f454022`
- Scope: PLAN §3 P4 and C0 §§1–5, 7; no source-stage integration merge.

## Decision

PASS. The only candidate change is the expected-plan input correction and comment in `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`: expected execution uses `bundle_from_document(base_document)`, while the full recorded request and evaluated original head remain unchanged. Production verification confirms Runtime `commit.py` `_load` uses `bundle_from_document(revision_closure)`; public remote `open_bundle` adds the authenticated `base_parent.publication_id` annotation only after validating the exact original pair. The reported dependency-pin difference is therefore a real provider-boundary distinction.

All 66 baseline AST assertions are unchanged. Full commands, label, steps/patches, merge, reads, dry-run, canonical document, raw/source mapping, digest, receipt, complete records/commands (including dependencies/effects/bindings/steps), history, head, and persisted readback assertions remain present. No dropped fields, subset comparison, fabricated source fact, or unrelated file change found.

## Commands/results

1. `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py -m integration` — PASS; 1 test collected. No test body/live HTTP/socket/daemon run.
2. `ruff check tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — PASS.
3. `mypy --config-file pyproject.toml --follow-imports=skip --ignore-missing-imports tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — PASS.
4. `git diff --check d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de 7a62327b7` — PASS; 3 insertions/3 deletions, named test only.
5. Baseline/candidate Python AST assertion comparison — PASS; 66/66 unchanged.
6. `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py -k 'test_move_inverse_returns_exact_runtime_result_and_complete_original_state'` — PASS; 1 passed, 111 deselected. Minimal separate offline differential; author’s heavier witness was not duplicated.

Limits: no original P4 test body, full suite, browser/build, Runtime HTTP/service witness, or central test-service request. No blocker. Existing original single-HTTP manager gate may proceed after this PASS.
