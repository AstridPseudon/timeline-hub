# Operation-route authority parity audit

2026-10-20. Read-only product audit, before operation-host activation.

**Verdict:** no new endpoint, scope, or project authority expansion found for the agreed **same-origin local workspace → Vite → discovery proxy → normal Runtime listener**. The operation route uses the same product bearer and Runtime handlers as ordinary `/api/runtime`. It pins their selection for an operation instead of rediscovering between calls. Neither local proxy has RuntimeDoor's closed browser route table. `views` remains denied at RuntimeDoor and paired relay; its reachability through both local proxies is existing normal-token authority, not a new door permission.

**Activation:** no additional authority-parity hold for this local transport. This audit does **not** activate the host or discharge the agreement's separate actual acceptance/receipt/restart, stale-await, native capture, outbox, and current-tuple gates. Hosted absolute RuntimeDoor and paired operation transports remain unsupported. No product fix, endpoint ban, policy change, or owner decision is requested.

## Sources and contract boundary

Audited App tree: `0f1d6984ac07f16e6d39f5e3be528a6d19783406`; App `origin/main`: `17e46de99b7cef52fe494de1703a9865a8d4be24`. Runtime integration: `129493b2aff614560d9b7ac2577957e799cf30ec` in `/home/user/work/runtime`. During final verification Runtime advanced to `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`. A diff of the traced files found only an unrelated strict-JSON/empty-shell bootstrap change in `timeline_commit_store.py`; its membership/authorization code was unchanged (line offsets moved). The cited Runtime lines and targeted evidence refer to the audited source above, not a qualification of the later merge. No frozen R4 branch or integration worktree was modified.

Contract sources under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/`:

- `PLAN.md`: decisions 2/4/12, retained local-door origin/credential/project checks, gate 4; hosted/paired relay deferred.
- `design/runtime-app-proxy-operation-agreement.md`: Runtime ACK 2026-10-20T10:11:13Z; bounded initial same-origin transport, normal auth/scopes on every upstream request, existing route/profile/header restrictions preserved, no broadening ordinary App credential authority; no hosted/paired support inferred.
- `design/app-proxy-operation-lifetime.md`: separate local dispatch lifetimes, pinned endpoint/credential, retirement, uncertain already-dispatched requests, separate activation qualification.

Exact implementation sources (line numbers refer to these trees):

| Boundary | Source |
| --- | --- |
| Credential creation, actor, discovery selection | Runtime `astrid_runtime/bootstrap.py:527-546,643-655,964-982` |
| Owner-authorized product provisioning | Runtime `astrid_runtime/runtime_boundary.py:117-149`; `runtime_protocol/server.py:411-434` |
| Credential grant and recheck | Runtime `runtime_protocol/auth.py:186-194,223-243`; `runtime_protocol/server.py:108-116,275-319` |
| Local launcher identity/profile checks and wiring | App `scripts/dev-local-workspace.mjs:324-394,414-479,489-494,580-609,708-714` |
| Vite normal versus operation routes | App `config/vite/vite.config.ts:42-53,88-99,145`; `config/vite/runtimeProxy.ts:10-95` |
| Normal versus pinned discovery forwarding | App `scripts/runtime-discovery-proxy.mjs:31-85,119-145,159-207,210-223,255-321,324-420,455-470` |
| Browser operation identity and commit request fences | App `src/integrations/runtime/operationHost.ts:33-40,65-81,98-195,207-250`; normal client scopes `client.ts:43-52`, launch identity `client.ts:81-94` |
| Origin selection and transport distinction | App `src/integrations/runtime/connection.ts:3-18,59-85`; operation bind `operationHost.ts:69-70` |
| Door closed route/method/header policy and product check | Runtime `runtime_protocol/door.py:1-20,55-65,130-205,247-294,522-609` |
| Paired relay separate admission/classifier | App `config/vite/pairedRelay.ts:121-135,139-177,257-268`; `config/vite/pairedRoutePolicy.ts:16-22,48-96,140-205,208-232` |
| Project and resource membership; views | Runtime `runtime_protocol/server.py:294-319,582-587,667-685`; `service.py:1318-1325,2278-2295,2549-2585`; `timeline_inspection.py:551-565`; `timeline_commit_store.py:90-104` |

Baseline read with `git show origin/main:scripts/runtime-discovery-proxy.mjs` and `git show origin/main:config/vite/runtimeProxy.ts`: ordinary Vite stripping `/api/runtime` and generic discovery-proxy forwarding with its bearer predate operation transport. Main proxy lines 118-136 already forward the supplied path without a door route classifier; current corresponding lines are 402-420.

## Issued authority and scope fences

Bootstrap generates a random 64-hex product token and `astrid-` actor derived from its digest, held in owner-only `credentials/astrid.json` with `version: 1`, `scope: astrid`, and `actor_id`. The discovery file points to this product file. The daemon's own owner credential is a different token (`runtime_protocol/daemon.py:123-127,274`); the product proxy does not select it in the supported launch.

Bootstrap uses owner/bootstrap authority to call `POST /v1/credentials`. Runtime installs the supplied product token with **exactly**:

```text
handshake
objects:read
objects:write
projects:read
projects:write
tasks:read
tasks:write
```

There is no `admin`, `credentials:provision`, `worker:register`, `worker:execute`, separate views scope, origin grant, project ID grant, or selected-project restriction in that issued credential. `CredentialStore.require` reloads the bearer generation and checks the required scope on every authenticated handler call; disabling/revoking it invalidates a pinned operation too. A local operation handle is only a registry lookup for this server-held credential, not a Runtime credential or a wider grant.

The launcher checks product actor/profile/catalog realm root, health instance, handshake actor/realm/protocol/negotiated scopes, and realm before starting the local App. Acquisition reads that same discovery credential, checks product metadata/non-reserved actor and the selected `astrid` catalog realm/root, and captures endpoint/token/identity. It does not mint a bearer or add grants. Browser bind additionally checks launch actor/realm/instance, accepted schema, targeted-execution capability, and negotiated scope array against the normal client's seven scopes before exposing the operation.

Limit: acquisition itself does not authenticate its file metadata against Runtime before returning a handle. Browser negotiation checks **negotiated** scopes. Runtime `service.py:776-791` returns the requested authenticated-scope intersection, not an inventory of every actual bearer grant, so that response alone is not proof of absence of extra grants. Exact issued authority here is established by the provisioning route and real CredentialStore probe, not inferred from `scope: astrid` or a successful handshake. Ordinary proxy forwarding likewise relies on the selected token's real grants. This audit does not qualify arbitrary hand-edited/overgranted credential files or arbitrary Vite upstream configurations.

Realm/instance fences select one local Runtime; they are not actor-to-project ACLs. The product token can read/write another project in that same Runtime when the route's ordinary scope and service validation allow it. A request naming project B with a timeline/revision/media resource owned by A is a different case: Runtime validates ownership/membership. The operation entry contains actor/realm/instance, **no project**. The browser `transmit` adapter checks saved project/timeline path and body, actor/realm, non-dry-run identity, and pre-write health; these are request-consistency fences, not a capability limiting the raw handle to one project. Commit rechecks bearer publisher inside acceptance and validates route/body project/timeline identity and store membership.

## Acquisition and forwarding policy

Both Vite admission and discovery-proxy admission inspect raw headers for operation traffic. The configured allowed origin must be an exact HTTP loopback origin; Host must occur once and exactly match the configured hop. Vite expects the App origin's Host; the discovery proxy expects `127.0.0.1:<proxy-port>` after Vite's `changeOrigin`. Origin must occur exactly once and equal the configured App origin. Only GET/HEAD may omit Origin, with exactly `Sec-Fetch-Site: same-origin`; POST acquisition and DELETE retirement do not have that exception. Duplicate/mismatched Host/Origin/Fetch Metadata, cross-site metadata, unconfigured origin, hosted HTTPS origin, and missing-origin POST fail admission. Browser acquisition uses same-origin mode, omitted cookies, no-store, and redirect-error. A local process able to manufacture these headers is within the local product trust boundary; this is not local-process authentication.

The control URL is exactly `/runtime-config/v1/operation`; POST takes `{}`, DELETE takes the one validated local handle. Forwarding takes one live handle and only GET/HEAD/POST/PUT/PATCH/DELETE. `operationTarget` accepts an origin-form `/v1/` suffix and rejects traversal, encoded separators/double encoding, malformed escapes, whitespace/control characters, fragments, and backslashes. This is a path-shape check, **not** an endpoint allowlist or full RuntimeDoor canonicalizer. A syntactically accepted admin path still fails Runtime authorization.

Vite strips browser authorization/cookies/hop headers; the pinned forwarder strips those plus Host and the operation handle, then sets `Authorization: Bearer <captured token>` immediately before Node dispatch. Original request method/path/body/idempotency key proceed to ordinary Runtime authorization. The normal local proxy already replaces browser authorization with the same discovery bearer and forwards generic paths. The operation response suppresses secret/cookie/hop headers and marks no-store; an upstream 401/403 retires the entry and becomes a generic unavailable response rather than granting access.

Pinning intentionally differs from rediscovery: changing discovery alone does not retarget or revoke a live entry. It can still address the previously selected Runtime with the captured credential until retirement/expiry or Runtime refusal. The agreement explicitly requires this lifetime; it is not a newly minted authority or guaranteed remote-validity observer. An already-handed-off request may still accept, and uncertain outbox work must remain recoverable. Actual upstream credential disable/revocation still refuses the next authenticated request.

## Route comparison

| Request | Normal local `/api/runtime` | Local operation handle | RuntimeDoor / paired relay |
| --- | --- | --- | --- |
| `GET /v1/doctor`, realm purge, provisioning, worker claim | Forwarded; ordinary product bearer lacks required admin/provision/worker scope | Same Runtime refusal; operation retires on 403 | Closed table denies before handlers |
| `GET /v1/projects/B` for another valid project in the selected realm | `projects:read` permits it | Same token permits it; handle has no project grant | Project-shaped read route allowed; no per-project actor grant added |
| Project B route containing project A's timeline/revision | Service membership refuses | Same service membership refuses | Route classification is not membership; Runtime must still refuse |
| `POST /v1/projects/P/timelines/T/views` | Forwarded under `projects:write`; service persists declared-input view artifacts with ordinary key/ownership validation | Same path, token, handler, and validation | **Denied**: absent from both closed tables; explicitly covered by privileged-route tests |
| `/runtime-config/v1/operation` | New local control seam | Acquires/retires local registry binding | Unsupported; neither table admits it |

RuntimeDoor uses exact configured **HTTPS hosted** Origin and `127.0.0.1:<door-port>` Host, rejects browser cookies/bearers, validates the product token's actual stored actor and exact seven scopes, applies its closed route/method/header table, then dispatches the ordinary handler. Paired relay has separate origin/pairing-cookie/connector admission and a closed classifier plus forwarding-header set. Its table is not even identical to the current door table (for example the door has commit routes added locally while this paired table does not). Neither is the policy applied by the pre-existing local workspace proxy. `runtimeOrigin() === ''` by itself does not prove a transport is supported: paired relay can also be same-origin, but its deployed admission/classifier and the operation's exact HTTP-loopback requirement still apply. No transparent fallback is authorized here.

## Executed evidence

All commands ran from the assigned App worktree. Notes are under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-operation-route-authority-parity-audit/notes/`.

```sh
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-operation-route-authority-parity-audit/notes/proxy-policy.test.mjs
```

Exit 0, **3 named tests passed**: production normal rewrite versus operation target and paired route classifier; acquisition origin/Host negative cases; same fixture endpoint/token selected by normal discovery and bound registry, with intentional rotation lifetime difference. No sockets. An earlier `node --test` invocation of this same file exited 0 with only one file-level result; the direct invocation above emitted all three named tests. These probes supplement the source policy trace; they do not qualify activation.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-operation-route-authority-parity-audit/notes/credential-boundary.py
```

Exit 0, **1 local-service test passed**. Invokes real provisioning/authorization/dispatch with socket-free RuntimeHandler and a temporary real RealmStore/RuntimeService/CredentialStore. Confirms exact issued grants, admin/provision/worker negatives, allowed other-project read, rejected foreign timeline/view membership without writes, door views denial, and subsequent disabled-token refusal. It overrides response serialization only, not `_identity`, grants, or service ownership checks. All mutations are to disposable fixtures; no running Runtime is contacted.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-operation-route-authority-parity-audit/notes/pytest /home/user/work/runtime/tests/test_door_routes.py /home/user/work/runtime/tests/test_timeline_commit_routes.py /home/user/work/runtime/tests/test_timeline_native_inspection.py::test_selector_miss_validation_and_project_scope /home/user/work/runtime/tests/test_timeline_commit_read_basis.py::test_foreign_scope_and_consumer_reads_do_not_write_or_invoke_provider
```

Exit 0, **1,294 passed in 2.19s**. Existing Runtime suites: closed door policy including views/admin/foreign prefixes, commit request and publisher fences, real-service project membership. Selected tests open no sockets.

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/runtime /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-operation-route-authority-parity-audit/notes/pytest-views /home/user/work/runtime/tests/test_timeline_native_inspection.py::test_markdown_png_custody_and_dedup
```

Exit 0, **1 passed in 0.79s**. Existing real local-service positive for persisted views, project object custody, deduplication, changed-key-input refusal, and reopen/retry. This positive behavior was retained.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/paired/pairedRoutePolicy.test.ts
```

Exit 0, **1 file / 1,944 tests passed**. Existing App paired route/header policy suite, including views/admin negatives. Initial identical command without `--require .../snapshot-vitest-runner.cjs` exited 1 before collection (`ReferenceError: __dirname is not defined`); the existing central runner preload supplies config directory resolution. No test or product code was changed to repair it; config runner/no-cache avoided shared dependency cache writes.

`git diff --check`, `git diff --exit-code HEAD`, and `git status --short --untracked-files=all` passed with an unchanged product worktree. No full suite, build, browser, tsc, install, network external, production write, socket listener/probe, or central test request was run. Shared dependencies/venvs/runtime installations were read-only; Python bytecode/cache writes were disabled and fixture outputs cleaned up. The requested report is saved in the orchestrator design directory; the product worktree is unchanged. No tests were skipped, disabled, weakened, rewritten, or deleted.

Next step: keep the existing activation gates with the App/Runtime owners. Apply this verdict only to the agreed local workspace wiring; any later RuntimeDoor/paired operation design needs its own owner agreement and negative route/header qualification, with views still denied there.
