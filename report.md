# P4 independent review — PASS

Reviewed `tl/ap2-P4-history-records-sol-0548` at commit `7a62327b75840f3a45e83719d52e57422946d920` (tree `b07b812ac26d793f26b2edf37efd724d94a0ac3a`) against `d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de` (candidate test blob `033482ec2b94c5ae4a6b5c456e2d9fab3f454022`).

## Result

PASS. The candidate is limited to the settled P4 correction in `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py`: the expected execution now receives `bundle_from_document(base_document)`, while `commit_request=request` and `evaluated_head=base_head` remain unchanged. The explanatory comment accurately describes the provider input boundary.

Independent source-path review confirms `RuntimeCommitService.commit` calls `_load`, `_load` obtains `revision_closure` and returns `bundle_from_document(document)`, and public `open_bundle(..., publication_id=...)` adds the authenticated client-facing `base_parent.publication_id` after validating the original revision/publication pair. This explains the reported sole dependency-pin difference without stripping or fabricating record data.

The test still has all 66 baseline AST assertions with unchanged assertion fingerprints. Full request fields, command/label/steps/merge/reads/dry-run assertions, canonical document, digest, receipt, complete `records.commands`, step patches, history entry, previous/base head, and persisted current-head readback remain asserted. No product/helper/schema/generated/client pin/lock/suite/launcher/fixture changes were introduced.

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py -m integration` — PASS; exactly 1 test collected. The test body was not run; no HTTP/socket/daemon/browser/full/service run was requested.
- `ruff check tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — PASS.
- `mypy --config-file pyproject.toml --follow-imports=skip --ignore-missing-imports tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` — PASS; no issues in 1 source file.
- `git diff --check d8ab46e235e1ab5d2a1f9f9a37e0508235c5b2de 7a62327b7` — PASS; candidate diff is 3 insertions/3 deletions in the named test only.
- AST comparison of the baseline and candidate test — PASS; 66 assertions in each, unchanged fingerprints.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py -k 'test_move_inverse_returns_exact_runtime_result_and_complete_original_state'` — PASS; 1 passed, 111 deselected. This is the smallest separate offline provider differential used; the heavy Runtime witness was not duplicated.

## Limits and next step

The live integration test, original test body, Runtime HTTP/service witness, browser/build/full suite, and central service were intentionally not run under the task limits. No blocker found. Manager may promote this candidate for the existing original single-HTTP gate after PASS.
