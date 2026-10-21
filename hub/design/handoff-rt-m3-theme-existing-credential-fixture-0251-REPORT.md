# Runtime handoff: existing credential fixture for Viewing Theme host test

## Result

The Theme host test has a fixture-only correction. Remove the stale
`production_worker_credentials=True` keyword from the daemon start:

```python
daemon = real_runtime()
```

For the frozen SDK-style direct constructor, the equivalent is:

```python
daemon = RuntimeDaemon(
    tmp_path / "realm", support_root=tmp_path / "support"
).start()
```

Keep the existing credential split unchanged:

```python
generated = WorkspaceClient(daemon.endpoint, daemon.token)
host = GenericPackHost(
    ..., client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
    executor_id="astrid-pack-host",
)
```

Do not replace `daemon.worker_token` with the owner token, read an ambient
credential, or add a compatibility alias.

## Source comparison

The rejected keyword is not a supported Runtime API on any requested tuple:

- Frozen physical-parity server `8f105c26e3b62f9c2683f717a9773a12bc775a8e`
  has `RuntimeDaemon.__init__` at `runtime_protocol/daemon.py:53` with no
  `production_worker_credentials` parameter.
- Actual public `013` integration Runtime `9d1c43c647301da48a6e86ad82e466b501bd2418`
  has the same constructor shape and the same credential provisioning code.
- Staged newly published `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
  changes daemon services/logging and IPv4 binding, but does not add that
  keyword or alter the normal worker credential setup.

On public `9d`, `RuntimeDaemon._provision_credentials` at
`runtime_protocol/daemon.py:123-169` always provisions the owner credential,
then (when no `local_worker_profiles` are configured) provisions the separate
`astrid-pack-host` worker actor. Its scopes are the existing
`WORKER_SCOPES` at `runtime_protocol/daemon.py:26-35`:
`handshake`, `worker:register`, `worker:execute`, `projects:read`,
`tasks:read`, `objects:read`, and `objects:write`. The worker bearer is
rotated/reconciled by the existing `CredentialStore` path; it is not a
production-mode opt-in.

The current Agent/Main fixture API confirms the normal path:

- `tests/conftest.py:44-63` — `real_runtime(...)` delegates daemon options to
  `new_runtime_daemon(...).start()`.
- `tests/helpers/runtime.py:118-124` — the helper initializes the realm and
  calls `RuntimeDaemon(root, **kwargs)`.
- The analogous current Theme test at
  `/home/user/work/agent/tests/integrations/test_generic_host_remotion_render.py:193,235-239`
  should therefore call `real_runtime()` and continue passing
  `daemon.worker_token` to `RuntimeProtocolClient`.
- The normal GenericPackHost fixture at
  `/home/user/work/agent/tests/integrations/test_generic_host_runtime_control2.py:60-68`
  also starts with `real_runtime()` and uses the ordinary daemon credentials.

`authoring_profile="astrid"` is only needed by fixtures that exercise the
timeline commit provider (for example `tests/test_timeline_ordinary_http.py:69`).
The Theme GenericPackHost test does not commit a timeline, so adding it would
be unnecessary fixture scope; it does not replace the worker credential.

## Evidence

Central targeted Runtime test service, on the assigned source snapshot:

```text
request-test rt-m3-theme-existing-credential-fixture-0251 targeted \
  --files "tests/test_production_worker_credentials_luna.py"
```

Result: **5 passed in 2.22s, exit 0**
(`rt-m3-theme-existing-credential-fixture-0251-targeted-1021025137-32371`).
This existing lane verifies distinct owner/worker credentials, worker scope,
worker bearer rotation across restart, and worker control-plane restrictions.

No Theme media import, CAS admission, host materialization, resolver/props
assertion, MP4, browser, or duplicate normal CAS admission run was performed.
No Runtime source or public auth/API change is needed; this is not a Runtime
regression.
