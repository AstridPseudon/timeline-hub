# Agent private 0.2.15 managed-action source review

Status: blocked at the existing Python-action host boundary; no unsafe action
or declaration change made.

## Finding

The requested outer split is not executable from the owned files at Agent
commit `4d4535882f1e028805c3da178bf9a7fa53696da`.

The normal registered assembler precedent is a command action. It declares
`authoring_proposal` as a file at `{out}/authoring-proposal.json`, sets
`metadata.output_result_manifest: true`, and its command receives `{out}`.
That is the correct managed-output carrier, but this action is currently a
Python action and its Python function cannot see that carrier or the outer
claim identity.

## Exact seam and evidence

- `astrid/core/execution/executor/runner.py:323-331` constructs Python-action
  values from declared inputs/defaults and `request.inputs` only.
- `astrid/core/execution/executor/runner.py:384-436` invokes
  `function(**dict(values))`. It retains `request.out` only for output
  harvesting; it does not pass `out` or the admission mapping to the action.
- `astrid/core/execution/generic_host.py:9478-9559` owns the attempt output
  directory and sends it as `request.out`; the same host scope has the claimed
  task, attempt, executor, fence, and runtime epoch.
- `astrid/core/execution/generic_host.py:7436-7565` can expose network
  admission through `ASTRID_NETWORK_ADMISSION` only when a network policy is
  active. This action is intentionally `network: false`, so that is not an
  existing context carrier for this task.
- The existing command binder can provide a limited set of host-owned command
  ports, but it does not provide the complete required producer identity to a
  Python action, and adding caller-facing identity fields would violate the
  brief.

Therefore `run.py` cannot safely construct the required six-key proposal with
the outer `producer` identity, nor write it to the managed destination, while
retaining the current action/input surface. Returning an in-memory JSON
proposal would not settle the declared managed `timeline/authoring-proposal`
artifact. Reusing inner speech `run_id`/`task_id`, ambient environment values,
or caller-supplied fields would be an authority violation.

## Smallest private adaptation

Adapt the existing Python-action runner/host boundary (outside this worker's
ownership) to expose the already-owned `ExecutorRunRequest.out` and the
already-owned admission/claim identity through an internal host context, or
convert this one action to the existing command/manifest path with a
host-owned context file. The adaptation must remain internal: no new caller
DTO, action input, scope, credential, route, or identity source. It should
provide the exact outer `task_id`, `attempt_id`, `executor_id`, `fence`, and
`runtime_epoch`, plus the existing output root, and refuse when any field is
missing or inconsistent. Once that seam exists, the owned action changes are:

1. retain the current action name and eight caller inputs;
2. stop before caller-bound `publish` and return the producer batch from the
   shared worker;
3. write the batch to the existing `authoring-proposal.json` managed output;
4. declare one `authoring_proposal` file output with
   `artifact_type: timeline/authoring-proposal` and
   `output_result_manifest: true`; and
5. keep the report advisory only if the host contract supports it, never add a
   receipt or fabricated publication result.

## Assertion adaptation inventory

No existing positive assertion was removed or weakened. The shared positive
tests in `tests/packs/video_editing/test_draft_voiceover.py` must remain
positive after the parallel shared-worker change, including unchanged/plan,
ripple/hold, source-window, provenance, history, retry, receipt, and undo
coverage. For independent review after the host seam is available, action and
output assertions should change only as follows:

- replace the old action-level `report`/`receipt` success shape with the
  existing six-key proposal and one managed `authoring_proposal` output;
- assert the proposal producer is the outer claim identity, not inner speech
  identity;
- assert `timeline/authoring-proposal` and the standard manifest are settled;
- assert no direct publication/receipt is fabricated by the producer; and
- add strict refusals for missing output context or any missing/mismatched
  outer identity field.

## Verification

The existing direct shared behavior lane passed:

```text
/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/video_editing/test_draft_voiceover.py
22 passed in 0.68s
```

The system Python invocation was also attempted but could not run because
`/usr/bin/python3` has no pytest module. No full, live, or browser suite was
run.
