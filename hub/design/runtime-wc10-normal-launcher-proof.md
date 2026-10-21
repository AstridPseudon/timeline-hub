# Runtime WC10 normal-launcher proof

Status: **blocked on the required installed-host carrier** (2026-10-21).

## Intended proof

The proof is the existing product command
`astrid-runtime up --profile astrid --data-root <support-root> --json`, using a
real installed Runtime and the normal profile manifest. It must observe the
normal startup/status/authenticated door, create an empty timeline through the
existing client API, and read the Runtime-owned canonical baseline. The read
must show the `bootstrap` head and must not use or record
`publish_parent_composition`.

The Runtime source change under test is already present at `8f70a818`:
`LocalRuntimeBoundary._argv` maps the validated `astrid` source profile to
`--authoring-profile astrid` on the default `runtime_protocol start` child
argv. The low-level CLI and direct `RuntimeDaemon` defaults remain neutral;
the existing boundary tests cover that guard and the unmapped-profile refusal.

## Exact source tuple

- Runtime: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime client compatibility is the normal `0.2.14` contract from the
  Agent tuple.
- The staged Runtime worker tree includes the launcher forwarding change;
  no live Runtime caller was changed. Agent's `remote.py` caller and the
  frozen Runtime `publish_parent_composition` route remain unchanged.

## Blocker

The reusable installed Runtime fixture is suitable for the launcher layer,
but it does not contain Agent. The available installed child profile
`/home/user/work/venv-agent-child-s2` contains Agent from `d8749a9c`, not the
required `6efc8150`, and has no installed `astrid-runtime` package. The
`6efc8150` Agent and `95bd3c5f` Runtime are available as clean source
checkouts only. Importing them with `PYTHONPATH` would bypass the installed
host/profile custody this proof is specifically required to establish, so it
is not an acceptable validation override.

The normal carrier needed before this proof can run is one immutable installed
environment containing the Runtime `95bd3c5f` package/client and Agent
`6efc8150` package/client, with the profile fields shaped like the existing
installer contract:

```json
{
  "profile": "astrid",
  "runtime_checkout": "/install/lib/python3.11/site-packages",
  "source_checkout": "/install/lib/python3.11/site-packages",
  "runtime_environment": "/install"
}
```

The test can then reuse the existing ephemeral workspace/profile helper and
invoke the installed `astrid-runtime` entrypoint without source import
overrides. The carrier must be built non-editably from the exact tuple and
remain read-only during the run.

## Evidence and limits

Local no-socket preflight passed:

```text
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_runtime_boundary.py::test_default_product_runtime_argv_forwards_validated_authoring_profile tests/test_runtime_boundary.py::test_default_product_runtime_argv_rejects_unmapped_authoring_profile tests/test_runtime_boundary.py::test_direct_runtime_defaults_remain_neutral tests/test_runtime_boundary.py::test_startup_admission_budget_is_validated_and_forwarded
4 passed in 0.41s
```

The real launcher -> provider -> canonical empty create/read proof was not
run, and no named socket test lane was requested, because the only available
installed Agent carrier is the wrong commit and the exact tuple is source-only.
No claim is made for normal startup, door authentication, provider loading, or
canonical baseline read until that carrier exists.

## Later marked-run result (2026-10-21)

The manager's newer, explicitly marked request was awaited exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-wc10-installed-complete-one-proof-0303-wc10-installed-launcher-integration-1021031341-3134
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
exit=1; 1 failed in 1.60s
```

This is a setup failure, not an executed normal-launch proof. The source
identity and cleanliness assertions ran first, then `_approved_distributions`
failed before `_make_installed_environment` could create a private venv:

```text
AssertionError: approved shared inventory is missing ['aiofiles', 'annotated-types', 'anthropic', 'anyio', 'asyncstdlib', 'certifi', 'cffi', 'charset-normalizer', 'click', 'cryptography', 'distro', 'docstring-parser', 'fal-client', 'filelock', 'google-auth', 'google-genai', 'h11', 'httpcore', 'httpcore2', 'httpx', 'httpx-sse', 'httpx2', 'idna', 'jiter', 'msgpack', 'numpy', 'openai', 'opencv-python-headless', 'pillow', 'platformdirs', 'pyasn1', 'pyasn1-modules', 'pycparser', 'pydantic', 'pydantic-core', 'pyjwt', 'python-dotenv', 'requests', 'scenedetect', 'sniffio', 'tenacity', 'tqdm', 'truststore', 'typing-extensions', 'typing-inspection', 'urllib3', 'websockets', 'xxhash']
```

Therefore this run produced no installed authority, installed bytes, package
provenance, normal CLI/bootstrap, door authentication, provider load, or
canonical read. The test's later original assertions—including the `bootstrap`
head and absence of `publish_parent_composition`—were not reached. It also did
not reach the private-install guards for no shared symlinks, `-I`/no
`PYTHONPATH`, exact distribution versions, or module origins under the private
site. The expected product tuple remains Runtime launcher `8f70a818`, normal
Runtime/client `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `0.2.14`, Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb`, and fixture `efd8e21347c90cd03bf666bf1c8752fa7b14e595`
(tree `7ecac255c50d2935ddf9a37d3fc9ba0bda434b60`). The fixture expects product
distributions `astrid==0.1.0`, `astrid-runtime==0.1.0`, and
`astrid-runtime-client==0.2.14`, but no installed environment reached those
checks.

No runtime source, shared venv, shared symlink, or `PYTHONPATH` override was
changed by this run. Because setup stopped before environment creation, there
were no generated wheels, support realm, socket, or custody bytes to clean up;
the central test service retains its result directory. This remains a bounded
fixture/inventory blocker and makes no D13 render or consumer-migration claim.
The earlier unmarked request's `exit=5`/one-deselected result is retained above
as historical context and is not normalized into this result.

## Matched-runner result (2026-10-21 03:18Z)

The one authorized corrected-runner request was executed exactly once:

```text
request: rt-m2-wc10-matched-runner-one-execution-0318
suite: wc10-installed-launcher-integration
request id: rt-m2-wc10-matched-runner-one-execution-0318-wc10-installed-launcher-integration-1021031824-22571
command: env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_wc10_installed_launcher.py::test_wc10_installed_normal_launcher_provider_bootstrap
result: exit=1; 1 failed in 31.26s
```

The corrected outer interpreter reached the private non-editable install and
the normal installed launcher. The product wheels were built and installed as
`astrid-runtime==0.1.0`, `astrid==0.1.0`, and
`astrid-runtime-client==0.2.14`. The launcher returned a healthy `wc10` realm,
the status check returned `support.healthy == true` and `health.status ==
"ok"`, and the isolated child reached `WorkspaceClient.health()` successfully.
The retained realm contains the `WC10` project and its `wc10-project`
idempotency receipt, so the project write itself completed.

The first failing assertion was the unchanged operation's
`client.create_project(...)["project_id"]` at `tests/test_wc10_installed_launcher.py:471`.
The pinned Agent `astrid.sdk.workspace_client.WorkspaceClient._call_generated`
preserves mutation receipts by returning an outer `{"data": ..., "receipt":
...}` envelope. The generated client data contains the project resource, but
the test indexes `project_id` at the envelope level and raises `KeyError`.
This is an Agent-client/WC10 assertion contract mismatch, not an installed
dependency or launcher setup failure. No test or product source was changed
to mask it.

Installed evidence retained by the central run:

- private site: `/tmp/pytest-of-root/pytest-20/test_wc10_installed_normal_lau0/installed-runtime/lib/python3.13/site-packages`;
- wheel SHA-256: Runtime `4c7242691001d52aef6f702a8270119f59e462180d07d1218cbf7106235c26f4`, client `1f9bf541007dc6deacb3be04f090a21be884e9b057992e9f9c7e8c83f96aa`, Agent `bdc71a0e92c619c069aba663b8835f23e69e398ed883dba862395e42afd6ba6`;
- installed Runtime module hashes: `server.py` `3d89f77238fad1e465a09bf7f9c6c3439c02338e5edf7da72c197bbb16928598`, `service.py` `0beb8c3ce2e374a76138bd82259b529f6f3d32182a8e007a0eaa3cdb1fcb0be8`, `store.py` `4d1ece5a7f7b64ddbf4fb9edd8d6fc4c94e4caf448dc690bab0853b677286f4c`;
- installed client `generated.py` hash `e2e66babca52a7ff95b8387dd6b36a5e46b4a4085bc9082ea664ab8d054bd468`.

The child operation used the test's private command with `-I -B` and a child
environment with `PYTHONPATH` removed. The failure occurred before timeline
creation, provider bootstrap, canonical history/read, `bootstrap` head, and
the `publish_parent_composition` negative assertion. There is no installed
origin proof for those later assertions and no D13 render or whole-WC10
consumer claim.

Setup history remains preserved: the earlier default-targeted request exited
5 with one test deselected; the marked `venv-runtime` request exited 1 before
private installation because its 54-distribution inventory was incomplete;
this is the first request to reach private installation and the launcher.

Status remains **blocked**. Resolving the response-shape contract requires an
Agent/test-owner decision; no retry is authorized by this task.
