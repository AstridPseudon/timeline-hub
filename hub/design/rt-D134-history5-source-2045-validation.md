# D134 source-only validation

## Scope and decision

- Base/head: `a30e74e901a28b39c28facba3deb00d76f186e23`.
- Parent/head tree: `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Assigned paths are unchanged; `git status --short` is clean.
- AST comparison against `git show <base>:<path>` is equal for all three assigned files.
- Decision: `UNAPPLIED_EXACT_MISSING_AUTHORITY`; no source or test delta was justified.

## Checks run

`/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py`

- PASS, exit 0: `All checks passed!`

`PYTHONPYCACHEPREFIX=/tmp/w-9dd0fad8f0/rt-D134-history5-source-2045-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py`

- PASS, exit 0. The private cache is outside the worktree and shared installs.

`git diff --check`

- PASS, exit 0.

`/home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_m1_legacy_archive_read.py`

- PASS, exit 0: `Success: no issues found in 3 source files`.
- Inherited diagnostics: none.

AST comparison command:

```text
tests/editing_conformance/test_gate1_fresh_word_transcript_frontends.py ast_equal=True
tests/editing_conformance/test_prepared_video_birth.py ast_equal=True
tests/editing_conformance/test_m1_legacy_archive_read.py ast_equal=True
```

## Functional lane

Functional execution was **NOTRUN**. The admission check had 4,417,792 1-KB blocks available, below the required 5,242,880-block (5 GiB) floor. No pytest/provider/body/full/family/core/P1-P5 run was submitted, and no `originals.xml` was produced.

## Findings

- Gate1 `[cli]`, `[python]`, and `[sheet]` retain the exact historical schema/runtime pin assertions and all frontend/roundtrip predicates. Current source observations differ, but no qualified authority authorizes refreshing those literals.
- Prepared video retains the exact reviewed Runtime source/tree assertions and all preview/accept/retry/refusal/inverse predicates. No qualified replacement source/tree authority is available.
- M1 legacy archive retains the exact held baseline/current pair reads and the `on`/opaque/readback/anchor predicates. Removing or normalizing the missing legacy field would destroy the test's stated purpose.
- The retained 1937/2003/2011/2016/2020 packets classify these as setup/expectation boundaries only. They do not authorize migration, pin refresh, product-fault credit, or behavior closure.
