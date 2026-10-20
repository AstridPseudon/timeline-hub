# Runtime current activation-join triage

Date: 2026-10-20

## Decision

Both remaining marked-integration failures are classified as ordinary test-fixture/environment path failures. No Runtime product fix, new profile, metadata override, shared-package write, or Agent security change is justified by this run.

The temporary Agent checkout made by `tests/test_astrid_activation_join.py:93-97` copies only the `astrid/` package. It does not copy the source metadata file required by `astrid/version.py`, nor the vendored `astrid_runtime_client/` package required by later host paths. The real current Agent checkout has both.

## Current provenance

- Runtime worktree: `601d533d91e3726c4f7ae74723e8eff4adbe2f90`.
- Runtime release: `0.2.13`; schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- Agent integration checkout: `a760ecca02111b0e0841510926f200e398f3b6cb` (`tl/integration`).
- Agent vendored client: `0.2.13`, with the same schema digest; imports resolved from `/home/user/work/agent` and this Runtime worktree under `/home/user/work/venv-agent`.
- Marked-run snapshot: `a3f42fa9d8187b338e987fdedae50663bfd4e85f`.

## Evidence

The one permitted central run was:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_astrid_activation_join.py
```

Result: `2 failed in 3.63s`:

- `test_runtime_relay_to_committed_generic_host_activation_receiver_cpu`
- `test_runtime_relay_to_generic_host_successor_finalization_cpu`

The joined case's existing artifact, `joined-events.host-exception.json`, records the underlying exception before relay cleanup:

```text
FileNotFoundError: .../astrid-checkout/pyproject.toml
```

The traceback is `astrid/__init__.py` -> `astrid/version.py` -> `_source_version()`. The child has no installed `astrid` distribution metadata, so the source fallback opens the copied checkout's missing `pyproject.toml`. The same traceback is present in `joined-events.host-stderr.txt`.

The generic-host case reaches the relay's bounded `operation_unresolved` envelope. Its test-side relay does not persist the host child's stderr, so its immediate child exception is not independently captured. Its temporary checkout has the same missing `pyproject.toml`, and the shared fixture is the same copy-only-`astrid/` path. The later `receive_frame()` “unsolicited frame” failure in the joined case is secondary to the host failure and relay cleanup response, not evidence of a new framing regression.

Read-only checks against the central artifacts showed:

```text
/tmp/.../astrid-checkout/pyproject.toml                         missing
/tmp/.../astrid-checkout/astrid_runtime_client/contract_metadata.py missing
/home/user/work/agent/pyproject.toml                            present
/home/user/work/agent/astrid_runtime_client/contract_metadata.py present
```

## Minimal repair recommendation

The Runtime/Agent test owner should repair only the fixture's temporary checkout construction: copy `pyproject.toml` and the current Agent `astrid_runtime_client/` package alongside `astrid/`, into each test's private `tmp_path`. Do not install into the shared venv or node/package trees. Then rerun this same marked file once to see whether any protocol failure remains after the host can actually import the current Agent source.

No source change was made in this Runtime worktree. The first test's exact host traceback remains unpersisted by its relay harness; that is the only residual uncertainty in this classification.
