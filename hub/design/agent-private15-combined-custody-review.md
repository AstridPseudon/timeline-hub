# Agent private15 combined custody review

Decision: **APPROVE FOR ONE NATIVE REQUESTER PROOF**.

Reviewed exact source candidate:

- Agent commit `6a8dfb2286659dd67c108a230d24f14ba4599344`
- Agent tree `5f5449a2b668c96a9bc816cea1dd73eacc04f7ab`
- Parent `8444290337e2f7cb22e39b995834a80cb1cc1ef2`
- Runtime producer `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`, tree
  `f3ae49d38454ce73a9c91a954bb530b3ce51c122`

## Custody disposition

The combined source closes the earlier `8e7b828d` and `5869c0cb` rejection
findings without adding a new authority or wire path.

- The trusted outer producer context is created only by the existing host
  dispatch after the live task/attempt/executor/fence/runtime-epoch claim and
  immutable admitted target agree. `_ActionContext` is read-only, tied to the
  runtime request and exact attempt output directory, and expires on return or
  failure. PID/thread, nesting, copied-context, symlink, directory replacement,
  source, definition, and public-bypass controls are present and pass.
- The private action receives a `_PreparationClient` view. It does not copy
  caller identity, and its target wrapper refuses `publish`. The action settles
  either the existing six-key `timeline/authoring-proposal` or the existing
  successful `planned`/`unchanged` report; it does not publish, mint a receipt,
  or create a worker-owned writer.
- Media authority is fixed to the concrete normal `AstridClient` ->
  `RemoteAstridClient` -> `WorkspaceClient` chain and direct class-method
  dispatch. Caller-installed methods and lookalike clients are refused. The
  normal WorkspaceClient performs the exact Runtime selection read, verified
  metadata read, and object read. The exact five-field selection, `audio/wav`,
  positive size, finite positive Runtime duration, exact byte length, and
  SHA-256 CAS identity are all required.
- Repeated claims are fail-closed before success. Conflicting project,
  generation, variant, asset, object/digest, catalog, association, or version
  values—including nested source/scope/selector/lifecycle claims and boolean
  versions—are refused. Both association and legacy selector claims are
  compared with the authoritative Runtime result; no preferred form silently
  discards the other. Authored old-media claims are also checked against the
  Runtime selection and bytes.
- The original admitted `(base_revision_id, base_publication_id)` is checked
  before preparation and the complete pair is rechecked after synthesis. The
  proposal retains that original pair; changed head/publication cases refuse
  rather than refresh or rebase the proposal.
- The public helper remains on its original bound-client publication path. The
  copied parent public controls pass unchanged (22/22). The private changed
  path lowers through the existing native capture and proposal validator; the
  eventual requester, not the worker, owns `TimelineSession.queue_proposal`,
  durable flush/retry/restart, and guarded undo. Those requester/native/live
  steps are intentionally not claimed by this review.

## Declaration and closure

The action declaration retains the original eight inputs, `network: false`,
and the two explicit file outputs. The four declared action resources exist:
entrypoint `__init__.py`, `run.py`, shared helper, and `STAGE.md`. The whole
tool catalog's empty resource list is not represented as the action's complete
SDK/host closure. Generated catalog/artifact identities are updated only for
the changed pack/catalog, and the source/import closure checks pass; no copied
host, helper, or shadow context module is present.

`runtime.lock.json` is byte-identical to the parent and matches the exact C3d
producer. The protected edit-command schema remains byte-identical with SHA256
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.

## Evidence

All checks used the candidate tree, dependency-only shared environments, and
private `/tmp` test roots. No full suite, browser, localhost/live workflow,
renderer, or native requester execution was run.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-m2-review-private15-combined-custody-246 tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover.py tests/packs/video_editing/test_draft_voiceover_managed.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py tests/sdk/test_workspace_client_timeline_commit.py tests/test_artifact_manifest.py tests/test_tool_catalog_v3.py
246 passed in 21.78s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-m2-review-private15-combined-custody-public /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-private15-combined-executable-source/test_public_baseline.py
22 passed in 0.17s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache astrid/core/execution/executor/_action_context.py astrid/packs/video_editing/actions/sync_draft_voiceover/run.py astrid/packs/video_editing/shared/draft_voiceover.py tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_draft_voiceover_managed.py --output-format=concise
All checks passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/gen_tool_catalog.py --check
passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-c3d26567
ok runtime.lock.json (matches producer manifest)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-c3d26567" /home/user/work/venv-agent/bin/python -B -m scripts.reshape.compare_structure_baseline
Structure violations: current=13 new=0 fixed=0

git diff --check 844429033 6a8dfb228
passed
```

The broader ad hoc Ruff invocation including the giant pre-existing
`generic_host.py` and `runner.py` reported 103 repository baseline diagnostics;
it was not used as a new-source gate. No candidate worktree files were left
modified by review checks.

## Next step

Manager owns execution; no further custody approval is required. Run one
centrally managed native requester proof with this exact Agent/C3d pair. It
must use the real credentials and managed interfaces, genuine speech
settlement, the original proposal/base pair, and the existing requester
queue/flush/restart-retry/guarded-undo path. Do not publish from the worker,
broaden scopes, refresh the proposal base, or relabel an older C3d result.

