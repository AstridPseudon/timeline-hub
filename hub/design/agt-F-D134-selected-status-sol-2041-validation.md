# Validation

SOURCEPASS; live behavior unqualified.

- `python3.11 "$TMPDIR/source_audit.py" "$TMPDIR"`: exit 0. AST parsed with feature_version=(3,11), py_compile wrote only private TMPDIR/selected.pyc. Whole source equals first return except two status constants. Against original a30e74e901, only HTTP bootstrap and those constants differ; all authored requests, remaining predicates, helpers and seven UNKNOWN cases are exact. Permanent hashes/predicate counts are in source-manifest.json and predicate-map.json.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/sdk/test_timeline_selected_schema_runtime.py`: exit 0, All checks passed (Ruff 0.12.0, governing pyproject.toml).
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir="$TMPDIR/mypy" --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py`: exit 1, known baseline only: line 15 yaml import-untyped; missing types-PyYAML. No dependency installation or suppression.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 -- tests/sdk/test_timeline_selected_schema_runtime.py`: exit 0.
- `git diff --check`: exit 0. Relative first-return delta: one file, two insertions/two deletions, status constants only.
- Import/contract probe used `env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -B -c ...`: exit 0. Exact module origins and contract metadata are preserved in compatibility.json; validate_timeline_commit_provider(commit.create_runtime_commit_service()) passed.
- `git -C /home/user/work/wt/rt-pin-ab1e4f61 rev-parse HEAD HEAD^{tree}`: ab1e4f6141987706132916e2da16477f5a019464 / 7d8e77b2f5a4af79305c9212ce5174d3ea9fd657. `git ... status --porcelain`: empty. Manager checkout receipt exists.
- Pre-live guard `python3.11 - <<'PY' ... shutil.disk_usage('/home/user').free; inspect workers/*/meta + running and live tests/*/heavy ... PY`: exit 1. Available 6,133,731,328 bytes (>=5,000,000,000); active heavy worker agt-F-D137-real-child-core-2044. The no-heavy assertion refused. STOP; no retry or alternative route.

No pytest node or central suite was executed/requested in this worker. No full/family/core/browser/render suite was run. No historical retry control was rerun; its source/expectations are unchanged.

Planned exact command for the three local nodes, NOT RUN:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider -m integration --basetemp="$TMPDIR/selected-three" tests/sdk/test_timeline_selected_schema_runtime.py::test_native_rebase_after_v2_and_selection_removal_uses_original_object 'tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[pin]' 'tests/sdk/test_timeline_selected_schema_runtime.py::test_native_reselection_conflicts_while_disjoint_peer_and_exact_retry_survive[element]'
```

HTTP exact node, NOT RUN: tests/sdk/test_timeline_selected_schema_runtime.py::test_http_attached_selected_param_retains_original_pin_after_v2_removal_restart. The central targeted route hardcodes mutable /home/user/work/runtime; it was not substituted for immutable ab1e. Clarification of the brief's --net own-node route was requested before the no-heavy refusal; no answer/permission was assumed.

Exact import/contract probe command (PASS, exit 0):

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -B -c 'from pathlib import Path; import json; from tests.helpers.runtime import use_runtime; r=use_runtime(); import astrid, runtime_protocol, astrid_runtime_client, banodoco_timeline_schema; from astrid_runtime_client.contract_metadata import CONTRACT_VERSION, SCHEMA_DIGEST; from astrid.sdk.timeline import commit; from runtime_protocol.timeline_commit_provider import validate_timeline_commit_provider; assert r == Path("/home/user/work/wt/rt-pin-ab1e4f61"); assert Path(astrid.__file__).resolve().parent.parent == Path.cwd(); assert Path(runtime_protocol.__file__).resolve().parent.parent == r; assert Path(astrid_runtime_client.__file__).resolve().parent.parent == Path.cwd(); assert validate_timeline_commit_provider(commit.create_runtime_commit_service()); print(json.dumps({"astrid": astrid.__file__, "runtime": runtime_protocol.__file__, "client": astrid_runtime_client.__file__, "schema": banodoco_timeline_schema.__file__, "contract_version": CONTRACT_VERSION, "schema_digest": SCHEMA_DIGEST, "provider_contract": "PASS"}, indent=2))'
```

Interpretation recorded for review: the brief's “noheavy” was treated as a live-admission condition requiring no active heavy worker or suite. If the orchestrator intended only to forbid this worker starting heavy work, that interpretation needs correction before fresh qualification. This worker did not test that alternative after the guard refused.


