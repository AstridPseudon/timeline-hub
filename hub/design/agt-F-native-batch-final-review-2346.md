# FAIL — F-D85 protected source review

Reviewed cumulative return `b9f0140619` (`tl/agt-F-native-batch-return-2342`), equal to `HEAD`. Only the permitted test file differs from the common ancestor.

Finding: the helper converts native captured commands into a detached document via `execute()` before invoking the real CLI. `commit_document` then emits `doc.patch` commands through `Timeline.commit`; its `submit()` call omits CLI provenance, so Runtime source defaults to `"python"`.

This cannot satisfy retained assertions requiring:

- native commands and claims;
- `rationale` preservation;
- `source.via == "cli"`.

Relevant seam: [test_native_batch_ingress.py:153](/home/user/work/wt/agt-F-native-batch-final-review-2346/tests/editing_conformance/test_native_batch_ingress.py:153), [cli_native.py:109](/home/user/work/wt/agt-F-native-batch-final-review-2346/astrid/packs/timeline/cli_native.py:109), [commit_session.py:241](/home/user/work/wt/agt-F-native-batch-final-review-2346/astrid/sdk/timeline/commit_session.py:241), [sync.py:536](/home/user/work/wt/agt-F-native-batch-final-review-2346/astrid/sdk/timeline/sync.py:536).

Checks passed:

- AST conservation of all 24 assigned selectors: PASS
- In-memory compile baseline/candidate: PASS
- Ruff baseline/candidate: PASS
- Mypy baseline/candidate: PASS
- `git diff --check`: PASS

No pytest, service, build, or functional claim made. No merge requested due to FAIL. Product seam is outside the permitted file; route to Sol/product remediation, then repeat protected review. `DONE` created.