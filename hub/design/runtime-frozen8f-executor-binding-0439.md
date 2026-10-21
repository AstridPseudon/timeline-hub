# Frozen Runtime 8f executor credential binding

## Answer

The supported binding is actor identity, not a constructor option or a
separate registration API. Before `GenericPackHost.register()`, provision a
worker credential whose actor is exactly the host's `executor_id`, then give
that credential to the normal host client. Keep the owner credential on the
owner client.

For the c955 proof's custom executor, the identities are:

```text
owner actor / credential:  owner / daemon.token (or daemon.credential_path)
worker actor / credential: astrid-theme-proof-host / credential provisioned for that actor
host executor_id:          astrid-theme-proof-host
```

The supported fixture-side setup is:

```python
from runtime_protocol.daemon import WORKER_SCOPES

executor_id = "astrid-theme-proof-host"

# Owner remains the only owner-side client for project/media/task setup.
owner = AstridClient.open(
    endpoint=daemon.endpoint,
    credential=daemon.credential_path,
    realm_id=daemon.service.realm["id"],
    actor_id="owner",
    client_name="generic-remotion-theme-proof-owner",
    client_version="test",
    protocol_version="workspace.v1",
)

# This is the existing CredentialStore method. The actor must match the
# GenericPackHost executor id. WORKER_SCOPES includes worker:register.
worker_token, worker_path = daemon.credentials.provision(
    executor_id, list(WORKER_SCOPES)
)
worker_client = RuntimeProtocolClient(
    daemon.endpoint, worker_token, credential_file=worker_path
)
host = GenericPackHost(
    pack_roots=[workspace / "astrid" / "packs"],
    client=worker_client,
    executor_id=executor_id,
    attempt_root=tmp_path / "attempt",
)
host.preflight("rendering.render")
registration = host.register()
assert registration["registration"].executor_id == executor_id
```

For a process launcher, use the same `worker_path` and matching executor id:

```text
python -m astrid.core.execution.generic_host run --register \
  --runtime-endpoint <daemon.endpoint> \
  --credential-file <worker_path> \
  --executor-id astrid-theme-proof-host ...
```

The CLI reads the token from `--credential-file` and constructs the normal
`RuntimeProtocolClient`; the owner token is not passed to the host. The
launcher must not use the daemon's shared default `astrid-pack-host` token for
a different executor id.

## Frozen source trace

All Runtime references below are from Runtime
`8f105c26e3b62f9c2683f717a9773a12bc775a8e`. The Runtime daemon's supported
default actor is `astrid-pack-host`, and its worker scopes include
`worker:register` (`runtime_protocol/daemon.py:26-35`). The constructor at
`runtime_protocol/daemon.py:53` has no `production_worker_credentials`
keyword. Normal startup provisions owner and the shared default worker at
`runtime_protocol/daemon.py:123-169`; this does not bind that default actor to
an arbitrary custom executor id.

`CredentialStore.provision(actor, scopes, ...)` is the existing credential
provisioning method (`runtime_protocol/auth.py:147-184`). The binding check is
explicit and exact in `runtime_protocol/service.py:794-811`: HTTP identities
are accepted when `identity["actor"] == executor_id` or when they carry
`admin`; a different worker actor raises `worker credential is not bound to
executor`. Registration calls that check before any registration work at
`runtime_protocol/service.py:6865-6878`. The HTTP route authenticates
`worker:register` and passes the resulting identity to registration at
`runtime_protocol/server.py:1108-1113`.

The generated client carries the token as a bearer credential in
`packages/python/astrid_runtime_client/generated.py:597-611`, and its normal
`register_executor` call is `:1402-1404`. The existing Runtime test helper
`tests/runtime_credentials.py:4-16` demonstrates provisioning by executor
actor, but intentionally omits `worker:register` because it is for a worker
that claims after owner registration. For pre-registration, use the same
existing `daemon.credentials.provision` call with `list(WORKER_SCOPES)`.

The normal local host launcher already projects `--credential-file` and
`--executor-id` together at `runtime_protocol/local_worker_composition.py:349-352`.
The general launch projection does the same at
`runtime_protocol/remote_worker_deployment.py:818-855`.

## c955 fixture trace

Agent fixture commit:
`c955e7558116832462df5c426a3a4761cedb3f42` (`test(rendering): scope Theme
proof to Root props`). Its `real_runtime()` fixture delegates to the normal
Runtime daemon without adding a binding (`tests/conftest.py:43-63`; the
fixture's daemon factory is `tests/helpers/runtime.py:118-124`).

The owner side of the actual test uses `WorkspaceClient(daemon.endpoint,
daemon.token)` at `tests/integrations/test_generic_host_remotion_render.py:486-500`
and `AstridClient.open(... credential=daemon.credential_path,
actor_id="owner", ...)` at `:508-515`. Those are the correct owner
credentials for project and media imports.

The failing host setup is at `:546-550`:

```python
client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
executor_id="astrid-theme-proof-host",
```

`daemon.worker_token` is the default `astrid-pack-host` actor, while the host
claims `astrid-theme-proof-host`. Runtime 8f therefore rejects registration
before SDK admission, exactly matching the reported HTTP 401.

The c955 host adapter documents that worker credentials are the distinct
boundary and that the credential actor is bound to `executor_id`
(`astrid/core/execution/generic_host.py:4397-4410` in c955). Its constructor
accepts the normal client and explicit executor id at `:5140-5158`; its
registration path sends the executor descriptor through the client at
`:4571-4598` and `:6297-6303`. The CLI reads `--credential-file` and creates
that same client at `:13539-13555`.

## Existing coverage and bounded witness

Existing Runtime coverage proves the two halves, but not this exact custom-id
GenericPackHost registration in one test:

- `tests/test_production_worker_credentials_luna.py:15-69` proves default
  startup gives the worker a distinct scoped credential, and that it cannot
  use owner-only project mutation.
- `tests/test_production_worker_credentials_luna.py:125-181` proves the
  default `astrid-pack-host` worker can claim with its matching executor id.
- `tests/test_runtime_domains.py:213-220` uses the existing
  `provision_executor_token(daemon, "domain-executor")` helper for a custom
  actor after owner registration, then claims/fails through the generated
  client.
- `tests/test_stage1_runtime_contract_completion.py:71-92` proves matching
  executor identity can re-register and a different actor is refused.
- `tests/test_second_client_e2e.py:73-80` passes owner and worker credentials
  separately to the normal second-product launcher, with a matching
  `--executor-id`.

Because the requested task forbade live sockets, I ran one ephemeral direct
`RuntimeService` witness (no raw SQL): provisioned separate owner and
`astrid-theme-proof-host` worker credentials, registered the custom executor
with the matching worker identity, observed it as owner, and verified the
`astrid-pack-host` identity was refused with the exact binding error. This
confirms the frozen service seam; it does not claim the prohibited live
GenericPackHost/Theme run.

## PEER REPLY — plain English, for Viewing

The 401 is caused by a credential-name mismatch before the SDK runs. Runtime
8f binds a worker bearer to the executor by exact actor name. Your c955 test
uses the shared `daemon.worker_token`, whose actor is `astrid-pack-host`, but
the host registers as `astrid-theme-proof-host`.

Keep the owner exactly as it is for imports and admission. Before constructing
the host, provision a worker credential for `astrid-theme-proof-host` with
`daemon.credentials.provision("astrid-theme-proof-host", list(WORKER_SCOPES))`.
Pass the returned token to `RuntimeProtocolClient(daemon.endpoint,
worker_token, credential_file=worker_path)`, and keep
`executor_id="astrid-theme-proof-host"` on `GenericPackHost`. For a launched
host, pass the matching path with `--credential-file` and the same
`--executor-id`.

That is the existing normal binding path. Do not pass the owner token to the
host, do not use the unsupported `production_worker_credentials` constructor
keyword, and do not add a credential API or widen scopes. The direct frozen-8f
witness accepted the matching pair and rejected the wrong actor.
