## PASS_SOURCE — A

- Candidate: `tl/agt-D86-M1-functional-0145` (`4f4f26c706`)
- File blob: `test_commit_runtime_m1.py` `d0689387aa984830f90529329e6d019f61f21854`
- Split `timeline.duplicate` into semantic step `copy` and emitted `doc.patch` commands into `baseline`.
- Preserves all commands, claims, inputs, patches, history fields, opaque values, decorators, and all 10 parametrized selectors.
- Matches C0’s contiguous step partition and semantic-step empty-patch rules.
- `FAIL_SOURCE`: none.

## PASS_SOURCE — B

- Author baseline: `tl/agt-D86-ordinary-script-0121` (`04ee36aa64`)
- Candidate: `tl/agt-D86-script-return-0145` (`96dbc67014`)
- Candidate file blob: `test_timeline_script.py` `91c85a2cbeed4a68b5ce08943a11d1cd14dc8dcc`
- Replaced only the stale `parent-2` assertion at the original first-return site.
- Independently matched the active `document_from_bundle()` production identity formula over canonical `project_id`, `timeline_id`, parent payload, and dependency manifest.
- Original rebind inputs, old-script text, binding-head assertion, callers, predicates, and selectors remain live.
- The two other migrated family files are byte-identical to the author baseline.
- `FAIL_SOURCE`: none.

## Checks

Using pinned `/home/user/work/venv-agent` tools:

- In-memory compilation: baseline and candidate A/B sources passed.
- Ruff 0.12.0: all scoped baseline/candidate files passed.
- Mypy 1.17.0: baseline and candidate shadow checks passed.
- `git diff --check`: A and B passed.
- No pytest, collection, fixtures, helpers, Runtime service, browser, or full-suite execution performed as required.

Runtime contract reference: `contract/commit-v2.md`, blob `257024df6fa93be767f0c74ee10014a6770c4fcb`.

No worktree source files were changed. Commit message and empty `DONE` marker were created. Functional behavior remains for later main-branch verification.