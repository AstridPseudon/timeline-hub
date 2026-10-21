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
