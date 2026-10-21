# Agent private15 trusted Python host context

Implemented on Agent base `4d453588`, for independent custody review. No Runtime,
normal-pin, live, browser, or full-suite qualification is claimed.

## Source change and custody

The existing GenericHost private worker admission envelope is the smallest
available process carrier. Its existing task/attempt/fence and source/definition
fences remain in use. For Python actions declaring the existing
`timeline/authoring-proposal` artifact, a cohesive private helper adds the
retained claim's `executor_id`, `runtime_epoch`, and existing `admitted_target`
to that same private admission mapping. These values are not action inputs,
request fields, environment variables, or a new public wire contract. The only
serialized delta is those three values inside the existing host-worker admission
envelope. `ExecutorRunRequest`, public DTOs, Runtime C3d/schema84fc, grants,
scopes, endpoints, and storage are unchanged.

The helper requires all five outer producer coordinates. It compares task,
attempt, and fence against the host admission, executor against the registered
host executor, and epoch against the observed Runtime. The executor is the
claimed **host worker ID**, never the capability ID or inner speech executor.
The exact four-key target comes only from the retained admitted task spec and
must match its project. Missing, invalid, conflicting, or boolean-as-integer
coordinates refuse. No fallback identity is synthesized.

The Python runner retains its admitted-definition/source checks and contained
source loader. Around the existing function call and output validation only, it
installs `_action_context._ActionContext` in a private ContextVar. This object
is never serialized, put in the request, attached to AstridClient, or returned.
It exposes read-only producer/target mappings and the existing request.out.
It requires runtime invocation, matching task/project, and the live attempt's
`outputs` directory; there is no run_root fallback. PID/thread, directory
identity, active-lifetime, copied-context expiration, and nested-use checks
fence access. Finally always retires the view. Ordinary Python actions retain
existing kwargs/defaults/JSON results without acquiring producer context.

The existing private/delegated worker branch still strips identity and does not
receive this context. Network admission, broker policy, cancellation, tracked
child/process custody, managed-session one-shot tokens, harvesting, and Runtime
settlement paths are unchanged. This adds no network authority; the action
remains `network: false`.

GenericHost grows seven lines and runner three net lines; the implementation is
in one 162-line helper. No giant-file threshold or inventory was changed.

## Shared-worker seam and minimal private adapter

Parallel shared source `8e7b828d5` reads
`getattr(client, "trusted_execution_context", None)`. A plain caller-provided
client attribute is **not evidence of custody**. Its source report's claim of a
trusted attribute must be read with this limitation.

The named action passes an ephemeral private `_PreparationClient` view to that
existing shared function. Its read-only `trusted_execution_context` property
returns only the currently active host context's five coordinates, never the
underlying client's attribute. Other reads use existing client facilities.
Nothing is installed on or restored into AstridClient. The view expires with
the invocation. Its authoring-target view forbids `publish`, so executing this
branch with the older shared implementation fails before a publication rather
than publishing and subsequently discovering that no proposal was returned.

This adapter is necessary to connect the already-written parallel helper
without overwriting its owned file or introducing a public client API/argument.
It is not a general authority framework. The direct shared function accepting
an arbitrary client's mapping is not independently authenticated by this
change; review the **managed action path through this private view** as the
custody boundary. A future direct managed caller must use the same trusted
accessor/view, not treat any client attribute as authority.

## Exact output/assertion conversions

- `run.py` retains the existing action name and eight parameters. It calls the
  existing shared helper with the private preparation view; it does not alter
  speech generation or capture. The old `{report, receipt}` return becomes
  `{authoring_proposal: proposal}`. Before any file write, producer and admitted
  target must match the live context and `build_producer_batch` validates the
  existing proposal/commands without changing its digest or inserting a guard
  into the settled proposal itself.
- The existing atomic JSON writer writes `authoring-proposal.json` to the
  host output directory. Existing `build_manifest`/`write_manifest` describe
  exactly one primary result named `authoring_proposal`, with artifact type
  `timeline/authoring-proposal`. Existing runner/host harvesting and Runtime
  producer settlement remain responsible for acceptance. No publication result
  or receipt is fabricated.
- `pack.yaml` changes only this action's description, plan-only description,
  output declarations (two JSON report/receipt ports to one existing managed
  proposal file), and `metadata.output_result_manifest: true`. Its eight
  inputs/defaults and `network: false` remain. STAGE describes that contract.
- Shared planned/unchanged results stay advisory. The host requires a typed
  settled file when this output is declared (`outputs_required`), and the
  proposal command batch must be nonempty. The action therefore explicitly
  reports a missing proposal for these advisory results. It does not invent a
  no-op edit, a successful proposal, or an advisory artifact to bypass that
  contract. The original shared plan/unchanged positives remain unchanged.
- No pre-existing test or expectation was edited, skipped, deleted, or marked
  xfail in this branch. `test_draft_voiceover.py` is byte-unchanged and its
  original 22 cases pass. The new action assertions cover the new managed
  output contract; they do not convert an old passing behavior into refusal.
  Parallel shared-worker assertion conversions remain separately reviewable.

## Direct evidence

Final direct command, from this worktree:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py
```

Result: **180 passed**. Tests cover the real GenericHost dispatch seam (intercepted
before launch), real Python runner/source loader and manifest harvest with a
stubbed preparation boundary, ordinary action preservation, all missing outer
coordinates, forged/mismatched producer and target, ambient/caller isolation,
output override refusal, lifecycle/exception/next-invocation cleanup, directory
replacement, and PID/thread mismatch. They do not claim Runtime acceptance.

Other checks:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_structure_baseline`
  passed: current=14, new=0, fixed=0.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m mypy --follow-imports=skip --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private15-trusted-python-host-context/mypy-cache astrid/core/execution/executor/_action_context.py astrid/packs/video_editing/actions/sync_draft_voiceover/run.py`
  passed: no issues in 2 files.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check astrid/core/execution/executor/_action_context.py`
  passed. Per-file Ruff stdin comparison against HEAD also found identical
  finding counts/codes on runner, GenericHost, and the action (the action retains
  its one pre-existing E402); the new helper has zero findings.
- `git diff --check` passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline`
  exits 1 because current=2186 versus recorded=2220 (34 fewer, not regression).
  No baseline was rewritten or loosened.

## Remaining review and qualification

No implementation blocker remains in this assigned seam. The shared source is
still separately owned and is not copied into this worktree. Combine its reviewed
`8e7b828d5` preparation split with these changes, then independently review the
claim-to-private-envelope-to-live-view-to-proposal chain before a normal pin or
any live proof. The current direct successful action test stubs preparation; it
does **not** prove combined real speech settlement, Runtime producer acceptance,
requester outbox retry, or undo. Those remain the deferred frozen-counterpart
central-service proof, not evidence from this worker. No full/broad/live/pin
request was submitted and no shared dependencies were modified.
