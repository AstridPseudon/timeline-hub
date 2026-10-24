Implemented the opt-in capture plugin and focused offline tests. **Independent Luna review: PASS.** No original or live body was executed.

- Added `tests/helpers/wc6_completion_capture.py`: observes the first selected `wc6-undo` invocation through existing session/service/coordinator/provider/port calls. Records boundary outcomes, exception identities, accessible hook state and already-returned receipt/history metadata in an exclusive private sink under `$TMPDIR`.
- Added `tests/sdk/test_wc6_completion_capture.py`: **13 controls**, including the real mounted methods with offline storage dependencies.
- Production files, registry, conftest and original test remain unchanged. Original blob remains `e55be12f88d23fddba3dd36614eb91745c1f8adf`, with **59 assertions**.

Exact validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-460c2d39" /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider --timeout=45 --tb=short tests/sdk/test_wc6_completion_capture.py tests/sdk/test_timeline_undo_transport.py
```

**19 passed in 0.84s.**

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/helpers/wc6_completion_capture.py tests/sdk/test_wc6_completion_capture.py
/home/user/work/venv-agent/bin/python -m mypy --python-version 3.12 --cache-dir "$TMPDIR/mypy" --follow-imports=silent tests/helpers/wc6_completion_capture.py tests/sdk/test_wc6_completion_capture.py
git diff --check
```

All passed.

Future opt-in command, **only in the test-service owner’s authorized preserved environment, retaining its pins/profile and budgets**:

```bash
/home/user/work/venv-agent/bin/python -m pytest -oaddopts= \
  -p tests.helpers.wc6_completion_capture \
  --wc6-completion-sink="$TMPDIR/wc6-completion.jsonl" \
  tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
```

SHA-256:

```text
capture helper  067e0ff1f87f0f0d59f7dae240a5317a947a6c1e3143d82ecf2cb189452c0a2c
offline tests   cf13c5c13424d6dce2006a1e056b23d386b0d1e3a2042813ecb4f84ed63f2add
original file   0c23fc68bfcd32342cd4331a69a725d8d2ffe4d48527dfc795f402f222fbc487
coordinator     2b0c256757f1bf0b3ab3124840250d2d8ef5dbec31a259c4b1e924e295619dd6
```

The tested coordinator hash also matches original Runtime `becfe6db`.

Decision: use tracing to preserve existing calls and lifecycle. No outside hunk is required. Tracing adds overhead, so resulting capture cannot establish original timing or causality. Later retries fall outside the bounded observation; unavailable boundaries are explicit, and result capture excludes film documents.

Nothing blocked. Original20732 remains FAIL/unknown cause. Next step is orchestrator review alongside retained-artifact recovery; any future original execution remains separately controlled.

Commit message and `DONE` were written. No commit or push performed.