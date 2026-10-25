# FAIL_SOURCE — F-D85/D86 review

Reviewed author commit `95fe9d2e90` against base `bc498acf58`, author brief/report, and `commit-v2.md` sections 1–5.

Finding: `test_attached_param_commands_keep_exact_cli_ingress_and_unchanged_write_history` is not source-valid.

- The test captures a native `clip.set-params` command, locally executes it, then converts the result into a detached document at [test_commit_runtime_native_checkout.py:223](/home/user/work/wt/agt-F-native-frontends-review-0000/tests/editing_conformance/test_commit_runtime_native_checkout.py:223).
- `commit --file` routes detached changes through `Timeline.commit`, whose free-edit path invokes the document emitter ([cli_native.py:109](/home/user/work/wt/agt-F-native-frontends-review-0000/astrid/packs/timeline/cli_native.py:109), [commit_session.py:87](/home/user/work/wt/agt-F-native-frontends-review-0000/astrid/sdk/timeline/commit_session.py:87)).
- The emitter constructs `doc.patch` commands ([emitter.py:294](/home/user/work/wt/agt-F-native-frontends-review-0000/astrid/sdk/timeline/emitter.py:294)).
- The assertion still requires the accepted commands to equal the original native command at [test_commit_runtime_native_checkout.py:248](/home/user/work/wt/agt-F-native-frontends-review-0000/tests/editing_conformance/test_commit_runtime_native_checkout.py:248).

This violates the required preservation of native commands/claims and cannot pass by AST conservation alone. No semantic fix or interface change was made.

Checks:

- Candidate and baseline compilation: PASS.
- Scoped Ruff candidate and baseline: PASS.
- Scoped mypy candidate: PASS. Baseline not rerun; author evidence records equal baseline/candidate totals.
- `git diff --check`: PASS.
- All seven selectors/decorators/parameters preserved; frontends file unchanged.
- No pytest, product tests, service, build, or functional execution run.

Verified hashes: Runtime `732c48c6f5`, R4 SDK `11caf1d9de`, R4 Runtime `31c7ac3a00`.

Recommended next step: return to the author for a bounded correction of the parameter CLI case, preserving the required native command/provenance assertions.