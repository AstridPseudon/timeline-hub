# D73 independent source validation

Candidate: Composition `afda6c66a11608d8cb012df1a54bf2489d8c20b3`, tree
`67bd2d4ee1d50bd95ebb8b0de55d4d1ed1e3e87f`.

## Requested commands

### Controls — exit 0

```bash
TMPDIR=/tmp/w-d73-source-review-LSLwBe ./ops-d73-exact-nodes/dry-check.sh --controls
```

Result: **7 tests passed**. Both named rows were exercised through the actual
central parser and launcher `run --` path:

```text
d73-ab1e-selected4-exact-nodes: run positive exit=17 calls=1; poison exit=1 calls=0
d73-ab1e-fork-exact-nodes: run positive exit=17 calls=1; poison exit=1 calls=0
Ran 7 tests ...
OK
```

The private stub wrote bounded XML only; this is control evidence, not a
functional test result.

### Missing census — exit 1 (expected)

```bash
env -u D73_MANIFEST ./ops-d73-exact-nodes/dry-check.sh --source-check
```

Result: exit **1**, with `status=NOT_READY`, `source_ready=false`,
`body=NOTRUN`, `preflight=NOTRUN`, all 26 required manifest keys reported
missing, both central rows reported absent, both fresh per-ID result sets
reported NOTRUN, and interpreter/schema readiness reported unqualified.

### Static and binding checks — all exit 0

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache --config /home/user/work/agent/pyproject.toml ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py
/home/user/work/venv-agent/bin/ruff format --check --no-cache --config /home/user/work/agent/pyproject.toml ops-d73-exact-nodes/check.py ops-d73-exact-nodes/test_recipe.py
bash -n ops-d73-exact-nodes/dry-check.sh /home/user/work/wt/agt-pin-2eca9a1d/tools/p4-d73-pinned-launch.sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY'
from pathlib import Path
for path in sorted(Path('ops-d73-exact-nodes').glob('*.py')):
    compile(path.read_text(), str(path), 'exec')
    print(f'compile: PASS {path}')
PY
./ops-d73-exact-nodes/dry-check.sh --bind-check /tmp/w-d73-source-review-LSLwBe/selected-ID/d66 /tmp/w-d73-source-review-LSLwBe/fork-ID/d66
git diff --check
```

Observed: Ruff check passed; format check reported both files already
formatted; both shell files parsed; both Python files compiled in memory;
binding reported distinct `selected-ID.xml` and `fork-ID.xml`; diff check was
clean.

## Read-only identity checks

- Candidate files match the hashes in `source-manifest.json`.
- Central `request-test`, `test-run`, and `tests/suites.conf` hashes match the
  unchanged reviewed inputs.
- Agent `2eca9a1da94…` and Runtime `ab1e4f614198…` are canonical, clean,
  origin-matched checkouts with matching receipts.
- Protected launcher/source/control hashes match; the Runtime lock is bound to
  `ab1e4f614198…`, producer `astrid-runtime`, and all 15 file hashes match.
- Central candidate rows are absent, as the source-only task requires.

No product or central files were changed. No commit/merge/rebase/checkout,
installation, network acquisition, provider body, child request, or full suite
was run.
