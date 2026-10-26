# Validation

## Source and Runtime custody

- Candidate: Agent `57b38b5b9ce672f307afe46c61add43df6350fef`, tree `5439ca22bc7d3cd334dce9a80a4ff0dc6827ccae`, clean.
- Base: Agent `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.
- Runtime: `/home/user/work/runtime`, `tl/integration`, `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`, clean.
- Canonical 15 check: PASS, all 15 Agent lock mappings matched the current Runtime `contract/artifacts.json` and source bytes. No Runtime source or manifest mutation occurred.
- Available-byte trace: minimum observed free bytes `4524126208`, above the `4000000000` stop; private raw XML/log and trace mode `0600`.

## Static review

- `/home/user/work/venv-agent/bin/ruff check astrid/packs/rendering/docs/scripts/timeline_document.py` — PASS.
- `/home/user/work/venv-agent/bin/python` AST parse of the changed file — PASS.
- `/home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml astrid/packs/rendering/docs/scripts/timeline_document.py` — PASS, no issues.
- `git diff --check 8585ed9c0404d0187b2ce70242d25114a32747c2..HEAD` — PASS.

## Targeted tests

Environment was set from this worktree as required:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/runtime
PYTHONPATH=/home/user/work/wt/rt-F-D141u-hosted-REG-review-0611:/home/user/work/runtime
```

Exact command:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<private>/two.xml tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime
```

Result: **PASS**, `2 passed in 2.97s`; JUnit reports 2 tests, 0 failures,
0 errors, 0 skipped. Module origins are recorded in `source-manifest.json`.

No full, core, browser, Farm, P4, or P5 suite was run. No test or fixture was
authored or modified.
