# Runtime e7 visibility-proof review

## Verdict: BLOCK

Reviewed `c9deaa50cbcea31af27c9f37ffe5ce5d68953030..e7a328115dcc518f3c355de087eaa630be28c55c` in
`/home/user/work/wt/rt-m2-review-e7-visibility-proof`.

- HEAD: `e7a328115dcc518f3c355de087eaa630be28c55c`
- HEAD tree: `869054b766fbc70393ed1c02e615691adc9a0f8b`
- Delta: only the requested 18-line Runtime replay-proof change and 48-line test refactor.
- No product edits made by this review.

The Runtime change is otherwise sound. Before replay it requires the exact
existing `timeline.recover` receipt/request hash, the receipt's single event
ID, matching timeline stream, `timeline.recovered` kind, exact closed
`{project_id, version}` payload, matching project, and positive non-boolean
integer `version == expected + 1`. Malformed, legacy `target_version`, wrong
project/version, missing-event, and `{}` evidence fail closed before replay or
writes. The normal producer and HTTP path emit that exact closed payload. The
focused injected-DB counterexample also refused correctly; this is local
fail-closed corruption evidence, not a normal API exploit or escalation.

### Blocking finding

The test dedup weakened a required prior assertion. The former current-target
legacy test sent:

```python
{"expected_version": archived_version, "version": archived_version}
```

The parameterized replacement at
`tests/test_timeline_legacy_authority.py:262` now always sends only
`{"expected_version": archived_version}`. Its `legacy_target_version` case
only places `target_version` in the injected event payload, so it no longer
proves refusal for the old current-target request shape. The implementation
still refuses the focused counterexample, but the regression proof no longer
preserves that prior assertion, contrary to the brief's no-coverage-weakening
requirement.

Minimal fix: retain at least one parameterized case with
`body["version"] == archived_version` and the legacy `target_version` event
payload, while retaining the absent-target missing-event case separately.
No Runtime/product change is required.

## Evidence

Passed as existing e7 evidence:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_legacy_authority.py -k 'visibility_receipt_proof or exact_new_visibility_replay'
9 passed, 42 deselected

ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_runtime_domains.py tests/test_timeline_legacy_authority.py -k 'generated_timeline_visibility_is_project_catalog_state or service_catalog_visibility_unarchives_current_or_absent_version or visibility_receipt_proof or exact_new_visibility_replay or historical_recover_refuses'
11 passed, 59 deselected
```

Additional focused review run:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent:$PWD/tests" /home/user/work/venv-runtime/bin/python <stdin script for the former current-target legacy case>
focused current-target legacy counterexample: PASS
```

`git diff --check c9deaa5..e7a3281` passed. No broad/full suite was run.
