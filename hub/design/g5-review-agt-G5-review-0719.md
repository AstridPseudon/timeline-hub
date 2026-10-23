# G5 independent review — FAIL

- Source `0f87c51cfce84a503d5af13a5771c9bfdcbf426b`; base `4edc4b321cae5cfc58252d7ed89e3f0408238646`.
- Scope: 8 files, `15 insertions / 866 deletions`; no review source/test edits.
- Blocking: `timeline_duplicate.py:225` and `cli_working.py:493` call retired `Checkout.publish()` and are reachable from duplicate/restructure. They raise at `timeline/publish.py:89`; duplicate has already created the destination and then archives it in its failure path. `_cmd_publish`/`_configure_publish` remain dead source (`cli.py:2944`, `3670`) and `_cmd_publish:2983` still references the retired method.
- Exact repair: move duplicate/restructure through existing `timeline.open().commit` + G3 emitter/session, preserving validation, equivalence, idempotency, narration/transcript follow-up; delete dead separate-publish code. Do not add an executor or restore deleted store writers. Keep attached native `publish`.
- Independent P4 node: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_commit_v2.py::test_p4_single_edit_uses_python_facade_g3_and_real_engine_fake_transport` → fixture setup `AttributeError` at `tests/sdk/test_timeline_sync.py:154` because `store.publish_bundle` is deleted. Future harness may use `raising=False`; the sentinel still catches hidden calls and all product assertions remain meaningful.
- Quality: scoped Ruff direct check `FAIL` 21 inherited findings; `make ruff` `FAIL current=2148 vs baseline=2149`; private mypy `FAIL current=1905 vs baseline=1912` (delta -7, completed ~62s); vendor lock, artifact manifest, compileall, and `git diff --check` PASS.
- Preservation: no direct production references to `publish_bundle`, `three_way`, or `document_diff`; native engine/capture/emitter/session/writers/auth/undo/fork/reader and v2 request/reply fields are untouched. Full/live/browser suites unverified.

Verdict: **FAIL; do not merge; P1 GO remains gated.**
