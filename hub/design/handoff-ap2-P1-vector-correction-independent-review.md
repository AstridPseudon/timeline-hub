# P1 vector correction independent review

Result: **PASS** for merge of the source-vector slice only.

- Review SHA: `14424f034d249cf992b1f7a34c32e3412d5af6de`
- Base SHA: `649ba6481922782346864e3c2ca76a6051b0a7a3`
- Reviewed donor SHA: `d8e1578bd9f717eb975addb50c2654de70815475`
- Diff: exactly two modified paths, 96 insertions and 56 deletions:
  - `tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json`
  - `tests/sdk/test_p1_doc_patch_requests.py`
- Donor blob identity: both review blobs equal donor blobs:
  - fixture: `e52ce1c7449a8494da9bd5397f73c0907568c0cc`
  - test: `287b730f3609f71635172b7223b95a858f80d036`
- Review SHA-256:
  - fixture: `85518dbec312ba8b02c94cf799e52f53e714492bf3f059b2734d72d3ec63cdbe`
  - test: `3b6b33b114ad1e21d1495d206f694b221ec9d109d84bc448e10f84dd3ea9df16`
- All outside blobs are exact base: `git diff --quiet 649ba6481922782346864e3c2ca76a6051b0a7a3..14424f034d249cf992b1f7a34c32e3412d5af6de -- . ':!tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json' ':!tests/sdk/test_p1_doc_patch_requests.py'` exited 0.
- Physical roots/paths are corrected to `internal-revision:ir` plus `clips/id:c` for the four internal vectors.
- Trim vector retains five authored changes and provider effects: `hold 17→4.0`, `app.astrid.for 19→absent`, `app.astrid.until null→absent`.
- Native source fixture hashes all match the recorded values; no source fixture changed.
- No provider-test import/deletion, required-success refusal, skip/xfail, product/schema/generated/pin/lock/launcher edit, or provider/full claim was introduced. The disjoint witness remains legacy `rebased`; red membership-removal precedence and the real mounted App/Runtime/Agent H3 chain remain unverified.

## Commands and logs

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
.........................                                                [100%]
25 passed, 1 warning in 4.09s
warning: PytestConfigWarning: Unknown config option: timeout
exit 0

/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_requests.py
All checks passed!
exit 0

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_requests.py
Success: no issues found in 1 source file
exit 0

git diff --check
clean (no output)
exit 0
```

No broad/provider/full/browser/heavy/socket suite was run, per task.

