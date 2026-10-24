Implemented the scoped no-op fix on base `415181d983`.

- Unchanged publication uses an existing guarded, equal-value `doc.patch` on parent config.
- Reuses one authoring compilation and preserves the complete v2 reply plus compatibility aliases.
- Preserves no-authored-changes feedback, Runtime replay, stale-head checks, and media/security boundaries.

Acceptance: **6 passed in 1.97s**—the four specified original nodes plus two new strict controls.

Exact pytest invocation, from `/tmp/w-ff1bf566a4/authoring-view`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/tmp/w-ff1bf566a4/authoring-view:/home/user/work/wt/rt-F-authoring-noop-sol-0216:/home/user/work/runtime \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
ASTRID_CHECKOUT=/home/user/work/wt/rt-F-authoring-noop-sol-0216 \
/home/user/work/venv-agent/bin/python -m pytest -q \
-c /home/user/work/wt/rt-F-authoring-noop-sol-0216/pyproject.toml \
--rootdir=/tmp/w-ff1bf566a4/authoring-view -o addopts= -p no:cacheprovider \
tests/timeline/test_authoring_feedback.py::test_unchanged_checkout_reports_no_authored_changes_and_unknown_imports_by_default \
tests/timeline/test_authoring_feedback.py::test_next_actions_quote_authoritative_scope_and_parse_supported_options \
tests/timeline/test_authoring_feedback.py::test_target_bound_sdk_defers_replay_and_stale_decisions_to_runtime \
tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping \
tests/timeline/test_authoring_commit_noop.py
```

The local view used exact `b7820cebaf` bytes for the two reviewed fixture files; originals remain untouched. Two-file patch SHA256: `bd01aeec1502e435bfead60ae84304691af9885e4bbf21747f615c87e1574d16`.

Changed-file checks:

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/authoring_commit.py astrid/core/timeline/authoring_bundle.py tests/timeline/test_authoring_commit_noop.py

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --cache-dir "$TMPDIR/mypy-final" --no-error-summary --no-pretty --follow-imports=skip astrid/sdk/timeline/authoring_commit.py astrid/core/timeline/authoring_bundle.py tests/timeline/test_authoring_commit_noop.py

git diff --check
```

All passed. Parent/final normalized Ruff and mypy diagnostics: **zero new**. In-memory compilation passed for all three changed files.

No blockers. No full/browser/gate suites run; broader neighbor behavior is unverified. Removal, reorder, unplaced-shot, and retired-seed issues remain separate continuations. Recommend Agent review, then its home merge queue.

`commit-msg` and `DONE` written. No git mutations performed.