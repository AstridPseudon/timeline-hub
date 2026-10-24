## Verdict: PASS

Reviewed Sol repair `40d6f6833b` and staged row.

- Runner SHA: `6eb755728488122c905d8111e8e68a93d6961e679d2b10a804240b0b311b837e`
- Wrapper SHA: `b1bda1c3771c29588c70a3ad20369ee908e78f1a65bae7da97258055a0cce29a`
- Row SHA: `8d5b3fd0aa08bf70a349ca226bb7324e75cbb6ec01446538be6c779d8fac3122`
- Row’s reviewed script SHA matches the runner.

Source checks confirm fixed bb50/f320 carriers, normal bench registration and lease custody, authenticated receipt/projection, client identity, locks, RECORDs, direct URLs, immutable metadata, Node 20/profile/archive/full dependency resolution, installed production origins, unchanged 12-assertion selector, 30-second timeout, durable setup `NOTRUN`, and fail-closed post-custody checks.

Static verification:

```text
python3 -m py_compile ... — PASS
ruff check --no-cache ... — PASS
mypy --follow-imports=skip ... — zero issues
bash -n ...sh — PASS
git diff HEAD^ --check — PASS
staged row bash syntax — PASS
```

No candidate bb50/f320 child exists. No preflight, provisioning, Node, pytest, probe, install, or original-body execution was performed; runtime compatibility remains unverified.

Future caller is the staged row’s exact normal-service command:

```text
bash tools/run-generic-reopen-original-0605.sh run-original \
  --source-root /home/user/work/wt/agt-pin-bb50a43c \
  --child-name venv-agent-child-generic-bb50-f320-0638 \
  --reviewed-script-sha256 6eb755728488122c905d8111e8e68a93d6961e679d2b10a804240b0b311b837e \
  --tmpdir <private-tmp> --evidence <private-evidence>
```

No product or test changes were made; no v2 wire-surface claim is made.