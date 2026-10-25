## F/D134 measurement report

- Replaced only the authorized `agent-core-full` suite row with the exact 1848 recipe and frozen tuple.
- Service: `agent-agent-core-full-1025191128-18455`
- Command: `bin/request-test integration:agent agent-core-full --no-cache`
- Result: terminal `fail`, exit 1. Preflight exit 0.
- Counts: 8,926 passed, 190 failed, 180 errors, 86 warnings, 173 subtests passed; 22 roots, `-n 3`, `addopts=`, cache disabled, timeout 45.
- Source tuple and all four checkout trees/origins/clean states reverified at submit.
- Core/REG open counts: `UNKNOWN` pending independent result/classification review. Retirement 0; no ship, custody, or release credit.
- Raw log/XML remain private; safe evidence is in [`evidence/`]( /home/user/work/wt/agt-F-D134-measurement-1909/evidence).

Validation passed:

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python -P -m json.tool evidence/*.json
git diff --check
```

The initial submission stopped before body execution due to the recipe’s non-executable mode; it was corrected to invoke the unchanged script via `bash`. DONE marker and commit message were written.