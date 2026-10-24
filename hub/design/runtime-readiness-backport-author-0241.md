Implemented the cost-only backport; **qualification is blocked**.

- Base: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Changed only `service.py`, `timeline_commit_store.py`, and the new authenticated-history regression. All three are byte-identical to reviewed `9a99d915f` / integrated `45c3a7f47`; reverse patch check passes.
- Computed final tree: `be4114705127f9ee9e86b26cd6de3f467e771c01`.
- Own commit awaits the post-exit harness. Wrote commit message `perf(runtime): backport R-readiness-compatible authentication` and `BLOCKED`; no `DONE`.

The mandated command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-079580ca /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_history_boundaries.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_history_authenticated_read.py
```

returned **105 passed, 40 setup errors**: the named Agent079 checkout is absent.

The same command with `ASTRID_CHECKOUT=/tmp/w-fabb04d042/readiness/agent079`, an exact archive of local Agent commit `079580ca46af77e0292d49dc34386b25c8391f99`, returned **144 passed, 1 failed in 58.10s**. No skips or deselections.

The failure, `test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]`, also fails on untouched exact2a9 using that Agent source: `sequential original or landing input does not match its authenticated head`. Its passing-behavior expectation remains unchanged.

Other checks:

- Structural regression on exact2a9: **RED**, three authentications; candidate: **GREEN**, one, with equal replies and no writes.
- `pyright --pythonpath /home/user/work/venv-runtime/bin/python --outputjson runtime_protocol`, independently on exactbase and candidate: **1,449 each; zero new/removed normalized identities or multiplicities**.
- `ruff check --no-cache --output-format=json runtime_protocol/service.py runtime_protocol/timeline_commit_store.py tests/test_timeline_history_authenticated_read.py`: **44 unchanged existing findings**; new regression clean.
- `git diff --check`: passed.
- Protected client/contract/schema/generated/pin/lock/metadata diff against exact2a9: empty; no deletions.

All four candidate client files match Agent079 exactly:

| File | SHA-256 |
|---|---|
| `__init__.py` | `78a69901f7c68d67b152410732f1c42dd30954ca07e7b4b9a319d4ddbd9035e6` |
| `contract_metadata.py` | `a79b2e12de96ec8f2c4bf7b6811ccb3538baf18ca839172f7a3d7bf525029aae` |
| `generated.py` | `9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904` |
| `timeline_commit_types.py` | `88c67d9eb650b445b8ad04c9011c1f44f1ec5e9f72a4a733050515de7ec0b616` |

The production GET commits route calls `list_timeline_commits`, which reaches this operation-local fix. No persistent cache or prior-result trust was introduced.

Integration remains `45c3a7f476e1c5f74fafc15956a58b9871eee21f`, already owning the production cost source and its current export. This dedicated proof branch is **not integrated or adopted**. No browser, journey, full suite, timing, bench, or provisioning run occurred; historical hang cause remains **UNKNOWN**.

Next: harness records the commit identity; orchestrator resolves the missing checkout and pre-existing Agent079/exact2a9 transcript failure before claiming the required 145-pass qualification.