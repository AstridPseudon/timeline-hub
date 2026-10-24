## Report

Read the plan, U2c handoff, Agent cause review, and Runtime history.

Result: the supported equivalent is to omit the removed keyword:

```python
daemon = real_runtime(
    <realm_root>,
    support_root=<support_root>,
)
```

`real_runtime()` → `new_runtime_daemon()` → `RuntimeDaemon(root, **kwargs).start()` preserves the real daemon path and worker credential construction.

Current authority:

- Actor: `WORKER_ACTOR = "astrid-pack-host"`
- Scopes: `WORKER_SCOPES` in `runtime_protocol/daemon.py:26-35`
- Owner credential placeholder: `<daemon.token>`; admin authority
- Worker credential placeholder: `<daemon.worker_token>`
- Worker path: `<support_root>/credentials/astrid-pack-host.token`
- Construction: `runtime_protocol/daemon.py:128-174`
- Agent fixture paths: `tests/conftest.py:55-60`, `tests/helpers/runtime.py:118-124`

`production_worker_credentials` is absent from the current constructor. Passing it raises `TypeError`; there is no same-authority compatibility API. The old owner-token alias is intentionally gone. `tests/runtime_credentials.py:13-16` provisions arbitrary, narrower executor credentials and is not equivalent to the production pack-host credential.

Exact source facts:

- Current Runtime: `2b49da8d6d8dbb8245a1a7cc8d7eee7d3bdaae65`
- `runtime_protocol/daemon.py` blob: `3d29579fe2308c27c39d4961ee11988bd522ae6b`
- `tests/runtime_credentials.py` blob: `9db6e73296390eb361bf2730e0997f52eb95a3e5`
- Selected files are identical at `40427e8b5` and `8ea0766f5`
- Agent U2c base: `699236a28581017c4d928137331e4893a1534bea`
- Cause review: `f6131eeb47`
- Switch history: introduced `d181fbc3`, hardened `1ac2a367`, removed `8c9b77d`

Checks:

- `git diff --check` — passed
- Selected-source equality checks against `40427e8b5` and `8ea0766f5` — passed
- Worktree — clean
- No tests, daemon/socket probes, credential creation, full suites, or installs run per task constraints

No Runtime changes were made. Agent should remove the two stale keyword uses in `tests/integrations/test_generic_host_activation_acceptance.py` only. The four abort-observation failures remain Agent-owned; the socket failure requires the supported external/net test route.