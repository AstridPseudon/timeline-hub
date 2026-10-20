# Runtime voiceover script input retention

Date: 2026-10-20 (UTC)

## Result

Added one bounded normal-producer proof in
`tests/test_timeline_producer_guards.py`.

The existing generic task carrier now accepts the publication-only form
`runtime_dependencies.publication.admitted_target` on a normal task with
explicit `input_object_ids`; the existing two-edge continuation validation is
unchanged. The proof uses the existing D13 admission/claim fixture and checks:

- a UTF-8 `execution_request.inputs` descriptor and its ordered
  `input_object_ids` mirror;
- project-owned CAS admission and the original four-field admitted target;
- live ordinary project-document update after admission;
- unchanged task descriptor, target, and raw old CAS bytes;
- restart and exact idempotent `create_task` replay of the original task and
  input identity.

This is exact CAS input custody evidence only. It does not claim a verified
DocumentPin, a script-specific authority field, or a qualified outer
voiceover workflow.

## Source changes

- `runtime_protocol/store.py`: recognize the existing publication-only target
  carrier as a normal producer task; edge-bearing `runtime_dependencies`
  remains the existing two-predecessor continuation shape.
- `tests/test_timeline_producer_guards.py`: one focused UTF-8 source-update,
  claim, restart, and exact-retry case.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_producer_guards.py \
  tests/test_task_continuations.py \
  tests/test_execution_binding_contract.py \
  tests/test_remote_worker_deployment.py
```

Result: `85 passed in 22.36s`.

No full, render, model-call, live-socket, or shared-dependency write was run.
