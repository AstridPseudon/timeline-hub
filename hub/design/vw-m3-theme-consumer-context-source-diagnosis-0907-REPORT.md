# Theme consumer-context diagnosis — 0907

## Verdict

The 0901 failure is a fixture launch-context mismatch, not a product Theme,
resolver, Root, source-authority, Runtime, or materialization defect. No
product hunk is justified. Do not relax _validated_runtime, add a launch
state exception, or claim Theme parity from the materialization result.

The 0901 correction itself is correct: admission and managed Theme
materialization passed, including the retained theme.json contents. The
failure occurred later, when Root preparation called runtime validation.

## Exact context mismatch

Retained central result:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-final-normal-envelope-one-proof-0901-integration-viewing-theme-normal-props-0234-1021090154-3697

Retained validation artifact:

/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/support/remotion-validation/remotion-validation-caebf2e085679064777bbd0576b03870.json

Its host variants were launch-validated from the fixture environment. Both
contain this registry selector:

ASTRID_PACKS_PATH=/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/workspace/astrid/packs

The same host context also records:

- ASTRID_REMOTION_PROJECT_DIR=/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/workspace/remotion
- ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
- ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages
- HOME=/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/home
- PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin
- PWD=/home/user/work/wt/.test-vw-m3-theme-final-normal-envelope-one-proof-0901-integration-viewing-theme-normal-props-0234-1021090154-3697

The fixture creates that launch context at
tests/integrations/test_generic_host_remotion_render.py:239-241, snapshots
it at :286, and calls _prepare_render_validation at :287-293. The validation
helper passes the host environment as the host context at
astrid/sdk/host_bootstrap.py:751-786; it also records the filtered worker
contexts.

Before the later consumer call, the fixture executes
monkeypatch.delenv("ASTRID_PACKS_PATH", raising=False) at
tests/integrations/test_generic_host_remotion_render.py:569-572. That is
needed only to prevent SDK discovery from combining the copied workspace pack
tree with the checkout tree. It changes the current pytest process after the
launch artifact already exists. The current consumer registry context is
therefore the same effective context above except that ASTRID_PACKS_PATH is
absent.

The comparison is exact, not a loose environment check:

- remotion_runtime.py:1082-1091 builds the consumer context from the current
  process environment using probe_context and _registry_context.
- remotion_runtime.py:1106-1113 selects the artifact role and requires one
  exact context match.
- _registry_context includes ASTRID_PACKS_PATH at :474-491; the copied
  workspace pack root is not removed by _normalize_registry_selectors
  (:507-539) because it is not the checkout’s implied pack root.

The failure then follows the retained stack:

root_preparation.py:107 -> run.py:266-296 ->
remotion_runtime.py:1181-1206 -> _validated_runtime:1109-1113.

The exact error was:

runtime validation consumer context differs: this process's environment was not validated at launch (only the host and Remotion-capable capability workers are)

The retained materialized file
/tmp/pytest-of-root/pytest-120/test_generic_host_normal_impor0/materialized-attempt/managed-objects/theme.json
was already checked before this failure. Thus materialization succeeded;
Root/props, one-resolver, default separation, and forged-source assertions
were not reached and remain unproven.

## Frozen Runtime and d971 normal caller

Frozen Runtime 8f105c26e3b62f9c2683f717a9773a12bc775a8e constructs the outer
task envelope at runtime_protocol/service.py:5466-5492:

{input_object_ids, schema_version, capability_digest, spec=body["spec"]}.

It exposes that admitted shape at :6383-6388 and returns the same immutable
claimed shape at :7125-7132.

The selected d971 normal host path preserves the claim snapshot at
astrid/core/execution/generic_host.py:10284-10289, calls run_task at
:10333-10338, and passes the envelope directly to _materialize_inputs at
:9179-9199, including authorized_input_object_ids. The materializer accepts
that envelope at :6460-6474, unwraps exactly one layer through
_admitted_spec_envelope (:2254-2286), and fetches the managed Theme at
:6888-6904.

This confirms 0901's three-line fixture correction. There is no product
forwarding hunk to propose.

## Smallest unapplied fixture correction

Keep the discovery-only deletion scoped to the SDK invocation, so the
launch-validated environment is restored before materialization/Root probes:

```python
with monkeypatch.context() as invoke_env:
    invoke_env.delenv("ASTRID_PACKS_PATH", raising=False)
    result = sdk.invoke(...)
```

Replace the existing deletion plus sdk.invoke block at :568-596 with that
scoped form, preserving all existing assertions and the 0901 materializer
call. No production code, authority, DTO, resolver, or validation relaxation
is needed. This is a proposal only; it was not applied here.

## Live _validated_runtime callers in d971

- astrid/sdk/host_bootstrap.py:1500-1515: reuse an existing host launch;
  validates the reused host environment and marks it stale on mismatch.
- astrid/core/execution/generic_host.py:7618-7656: validates a projected
  Remotion-capable worker context before dispatch.
- astrid/core/rendering/remotion_runtime.py:1202-1206: normal runtime-tool
  resolution; this is the path reached by the failed Root probe.
- astrid/packs/rendering/rendering/renderers/remotion/run.py:431-446:
  launch-bound registry regeneration validation.
- astrid/core/rendering/remotion_runtime.py:1324-1330: status/tool
  resolution through resolve_remotion_runtime_tools, which delegates to the
  :1202 caller.

## 0901 shell parsing deviation

The first held shell used sed to strip the prefix:

```sh
RESULT_BASENAME=$(sed -n "s#^$ORCH/tests/##p" "$REQ_STDOUT" | head -n 1)
```

request-test returned a directory ending in /; sed removed only the prefix,
so the value still ended in /. The subsequent guard rejected the slash and
exited before wait-test, releasing the lock. The same request was later
awaited once under a reacquired lock; no retry was submitted.

Trivial robust existing command:

```sh
RESULT_BASENAME=$(basename -- "$(sed -n "s#^$ORCH/tests/##p" "$REQ_STDOUT" | head -n 1)")
```

basename removes the returned directory's trailing slash and yields the
single result basename expected by wait-test.

## Evidence

- Central named suite: one request, exit 1 in 100.98s. Failure was after
  managed Theme materialization, at Root validation. No retry, alternate,
  browser, render, MP4, parity, or full run was performed by this diagnosis.
- 0901 result log SHA-256:
  0a64f6b3be9622c69e1f4634039f7921ced35305da3beb99a19e3af291512795.
- 0901 result summary SHA-256:
  df00cc3e42e8d0d20d233f934cb036d8d363f240cd5cec997910d0a7ef2683aa.
- Read-only retained-context control: both host variants in the validation
  artifact contain the copied workspace ASTRID_PACKS_PATH; the fixture's
  post-line-572 environment cannot match either variant because that key is
  absent. No source or retained evidence indicates a product defect.

