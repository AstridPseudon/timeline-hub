## PASS — F-harness G4 tuple review

Reviewed only the two runner files:

- `tools/run-discovery-original-0603.py`
- `tools/run-generic-reopen-original-0605.py`

Verified:

- Agent `0ff3d103…`, tree `1d613f…`, physical clean carrier `agt-pin-0ff3d103`
- Candidate binding `venv-agent-child-final-0ff3-becfe`
- Runtime `becfe6db…` and canonical client identity unchanged (`d79568df…`)
- Diff contains only approved Agent pin/path/candidate substitutions
- Original 9/12 assertions, 10 logical calls, 45s/30s watchdogs, Store/RECORD/lease/context/profile/client/pre/post guards preserved
- Original source hashes independently match; normalized AST fingerprints are unchanged
- Wrappers remain unchanged and call the reviewed runners

Checks passed:

- `py_compile`
- `ruff check --no-cache`
- `mypy --follow-imports=skip`
- `bash -n` both wrappers
- Independent AST/source-hash/carrier parity checks
- `git diff --check`

No candidate request, provisioning, preflight, original runner, browser, full suite, or process probe was run. No product edits made.

Commit message recorded:

`review(F-harness-G4-tuple-review-0848): qualify approved runner rebinding`

Recommended next step: normal merge queue, followed by integrated static proof.