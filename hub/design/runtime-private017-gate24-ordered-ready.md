# Runtime PRIVATE017 Gate2/Gate4 ordered-record readiness

Date: 2026-10-21 UTC

Status: READY for one matched normal PRIVATE017 Agent-pin execution after the
Runtime artifact review and the Agent pin review. This document does not claim
native qualification, HTTP execution, adoption, or a public release.

## Exact reviewed Runtime carrier

| field | value |
| --- | --- |
| Runtime commit | `42a7203f49bb89f299ec854cfbf2b1444e815a7c` |
| Runtime tree | `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` |
| package | `0.2.17` (private candidate) |
| health/schema digest | `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd` |
| raw timeline bundle | `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f` |
| artifact version | `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0` (76 artifacts) |
| component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| schema inventory | 65 definitions / 37 closed clauses |

The reviewed Agent source provenance is `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`,
tree `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`, raw schema
`sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
canonical schema
`sha256:9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
That source is provenance for the reviewed optional carrier only, not an
execution pin.

## Required future normal Agent pin

The manager must supply and record these exact values before the body runs:

```text
AGENT_PIN_ROOT=<clean normal PRIVATE017 Agent checkout>
AGENT_PIN_COMMIT=<exact future normal Agent commit; missing now>
AGENT_PIN_TREE=<exact future normal Agent tree; missing now>
AGENT_PIN_STATUS=clean
AGENT_PIN_CONTRACT_VERSION=0.2.17
AGENT_PIN_SCHEMA_DIGEST=sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd
AGENT_PIN_RUNTIME_SOURCE_COMMIT=42a7203f49bb89f299ec854cfbf2b1444e815a7c
AGENT_PIN_RUNTIME_PRODUCER_VERSION=sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0
AGENT_PIN_CONSUMER_SHA=<record only if supplied by the manager; do not guess>
```

The pin's `runtime.lock.json`, generated Python metadata, generated TypeScript
metadata, and source/tree identity must agree with those values. Historical
ed5, C3d, and any other old Agent checkout must not be substituted.

## One owner proof

The new node is in the smallest suitable existing integration module:

`tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo`

It reuses the module's existing `agent` fixture and `_commit` helper. The
fixture imports Runtime's `RuntimeService`, `RealmStore`, `route_path`, and
`MediaReads`; the existing Agent fixture imports `astrid.sdk.timeline` only at
body time and loads the actual provider with
`runtime_protocol.timeline_commit_provider.load_timeline_commit_provider("astrid")`.
The supported authoring profile is the existing Astrid profile, with the
fixture's renderer import/evaluation blockers still active. The Runtime client
preflight for the eventual run must import `runtime_protocol` from this exact
Runtime tree and `astrid_runtime_client` from the exact Agent pin.

The test creates an ephemeral realm with `RealmStore.initialize(tmp_path /
"realm")`, creates a project and `main` timeline through normal APIs, and
uses `commit_timeline(..., invocation_path=route_path(project, "main"))`.
It does not seed accepted history with SQL, use a fake provider, force schema,
override client/health metadata, or introduce a fixture/framework.

The lifecycle is one owner proof, not a duplicate Agent lifecycle:

1. A real provider batch creates `config.app` siblings `before`,
   `com.example.compiler-canary`, and `after`; the target contains a null
   `gone` value and the siblings contain opaque/null data.
2. A real `project-data.write` `mode: "remove"` deletes the target key and
   prunes its now-empty namespace. The accepted `CommandRecord` must contain
   the two writes and `insertion_order: ["before",
   "com.example.compiler-canary", "after"]`.
3. The accepted response is treated as a lost acknowledgement. After Runtime
   restart, the original body and idempotency key are retried with the receipt
   response compared exactly; the provider is guarded against a second call,
   and the complete durable SQL dump/history must remain unchanged.
4. A guarded inverse restores the exact raw app sibling order, null value,
   opaque values, and target namespace. An inverse of that inverse removes the
   namespace again and restores the exact removed order.

No partial-write assertion is weakened: the retry checks the full durable dump
and history, while the lifecycle checks the canonical readback and exact
recorded writes. Existing same-key refusal/corruption neighbors remain the
source of negative coverage; this node does not build a matrix.

## Collection and eventual argv

Local truthful collection, with no provider body execution:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  --collect-only -m integration \
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

Result: `1 test collected in 0.57s`. The first probe without `-m integration`
reported one deselected node and did not execute it; it is not evidence of
collection. The eventual named Runtime integration lane must use this exact
selector/argv shape with the supplied pin substituted:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT="$AGENT_PIN_ROOT" \
  PYTHONPATH="$PWD:$AGENT_PIN_ROOT" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  -m integration \
  tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

The manager must perform the same `--collect-only -q` guard first and refuse
zero/nonzero collection. The actual body remains unexecuted in this handoff;
no HTTP/socket/full/browser/render/install/generation run was performed.

## Isolation and handoff

Storage is the test's `tmp_path` realm only. Shared Runtime/Agent virtualenvs,
node modules, caches, and worktrees are read-only. The final matched run is a
manager action after both artifact and pin reviews. Agent should reuse this
node as the sole ordered lifecycle owner proof rather than launch a duplicate
remove/inverse/retry run.
