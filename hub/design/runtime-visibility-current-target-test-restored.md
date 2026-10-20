# Runtime visibility current-target regression restored

The e7 visibility-proof parameterization now restores the prior c9 request
shape for its `legacy_target_version` case. That negative case sends both
`expected_version` and the current `version`, while the separate
`missing_event` case continues to exercise an absent-target request. The
positive exact-new-visibility replay case and all other malformed-evidence
cases are unchanged.

Only `tests/test_timeline_legacy_authority.py` changed. No Runtime product
code, public schema, socket test, or broad suite was touched.

Evidence:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH="$PWD:/home/user/work/agent" /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_legacy_authority.py -k 'visibility_receipt_proof or exact_new_visibility_replay'
9 passed, 42 deselected in 5.95s

git diff --check
passed
```

`runtime_protocol/service.py` SHA-256 is unchanged from e7:
`ee6c75b0f39e2bb456f296f069a42e28b4b9c2f5c9c75251c6054a6f9bb451c3`.
