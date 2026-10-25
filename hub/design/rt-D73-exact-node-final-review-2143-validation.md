# Validation

All checks were read-only against the exact Composition and Agent/Runtime
receipts.

## Passed

- `bash -n ops-d73-exact-nodes/dry-check.sh` — PASS.
- `git diff --check HEAD^ HEAD` — PASS.
- `./ops-d73-exact-nodes/dry-check.sh --bind-check /tmp/d73-selected-req/d66 /tmp/d73-fork-req/d66` — PASS; distinct central IDs produce distinct XML paths.
- Exact launcher, selected-file, fork-file, and focused-control SHA-256 checks — PASS.
- Agent checkout clean/head/tree and Runtime checkout clean/head/tree checks — PASS.
- Exact four selected selectors plus one fork selector and fixed `-m pytest -q -o addopts= -m integration -p no:cacheprovider --timeout=45` argv — PASS by source inspection.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-420d59a40c/d73-final-control/pycache PYTHONPATH=/home/user/work/wt/agt-pin-2eca9a1d:/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_d73_pinned_launcher.py` — PASS, `2 passed in 0.46s`.

## Honest non-results

- Candidate `--source-check` — NOTRUN as a valid D73 admission: the real
  rendered manifest is missing. A diagnostic run with an existing key/value
  launcher manifest failed at the candidate's JSON parser (`manifest JSON
  parse failed`), confirming finding `D73-CODE-1`.
- Candidate `--controls` — NOTRUN because it requires the missing rendered
  manifest and currently cannot pass the parser. The direct focused pytest
  control above is not a production receiving run.
- Central request-test/test-run rows — NOTRUN; both exact rows are absent from
  the read-only central suite registry.
- Selected4/fork functional bodies, HTTP/socket/provider, full suites, and
  installed-route acceptance — NOTRUN by scope and missing receiving inputs.
