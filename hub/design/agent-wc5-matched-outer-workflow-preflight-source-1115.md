# WC5 matched outer voiceover workflow source/preflight

Date: 2026-10-21 UTC  
Worker: `agt-m2-wc5-matched-outer-workflow-preflight-source-1115`

## Result

**SOURCE/PREFLIGHT READY; REAL OUTER QUALIFICATION NOT CLAIMED.** The exact
current Agent source contains the independently approved dormant requester join
and the existing managed outer action. The normal PRIVATE017 Runtime source and
client origin are coherent and the relevant tests collect cleanly. There is no
supported fixture for a genuine outer Runtime admission through accepted
`authoring_proposal` history, so no new fake positive was added.

This task intentionally ran no test body, model, external service, HTTP/native
or outer execution, installation, render, or full suite.

## Exact source and origins

Current Agent source:

- commit `8a6f1024651b9ecb481e2a6cf5258c7598f65deb`
- tree `3d0c76ec570046036979b93794e517744a9a3301`
- worktree `/home/user/work/wt/agt-m2-wc5-matched-outer-workflow-preflight-source-1115`

The six feature blobs from approved source `f07d97715fbe4efcb80e2db40ef4597e81f75547`
are byte-identical in the current tree: `_action_context.py`, the managed
action runner, `pack.yaml`, `draft_voiceover.py`,
`settled_voiceover_input.py`, and `voiceover_requester.py`. The current source
also retains the f07 containing-entry route and the a4da custody source.

The a4da custody ACK is exact Agent commit
`a4da7cbe417aa4a3c0f90681020db6e5fd55b757`, tree
`f009d028cbeeb76dba954808db1ecea217afc3fa`; it approves source staging only,
not execution or settlement. Review1036 approves the current 8a6 source for
dormant staging only and names one genuine outer workflow as the remaining
prerequisite.

Normal PRIVATE017 Runtime/client origin:

- Runtime producer commit `42a7203f49bb89f299ec854cfbf2b1444e815a7c`
- Runtime producer tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`
- Runtime checkout `/home/user/work/wt/rt-pin-42a7203f`
- Agent `runtime.lock.json` source commit `42a7203f...`
- producer artifact version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`
- generated client origin: current Agent `astrid_runtime_client/`; runtime protocol origin: the exact 42a checkout

`vendor_lock.py check` matched all locked client/runtime bytes to the 42a
producer. Runtime `artifact_manifest.py --check` reported
`contract/artifacts.json is current`.

## Exact native route

The existing registered outer identity is
`video_editing.sync_draft_voiceover` (executor Python action), not
`generation.generate_speech`. The dormant private route is:

```text
_sync_draft_voiceover(requester_entry=True)
  -> _requester_sync_draft_voiceover
  -> _prepare_requester_speech_inputs
  -> existing generation.generate_speech per planned occurrence
  -> _read_authoritative_media_info
  -> one CAS settled_speech_input descriptor
  -> existing task admission for video_editing.sync_draft_voiceover
  -> observe the outer managed authoring_proposal
  -> build_producer_batch
  -> TimelineSession.queue_proposal
  -> TimelineSession.flush   [sole commit]
```

The requester carries one ordered descriptor in
`execution_request.inputs` and mirrors its object ID in `input_manifest`.
The JSON bundle root is only `{"entries": [...]}`; it carries no outer target,
producer identity, duration, media-selection authority, or commit identity.
The managed action receives the host-materialized file below the attempt root
and obtains its outer producer/target from the lifetime-fenced action context.

For each settled speech result, the existing authoritative reader selects the
exact five fields `asset`, `generation_id`, `variant_id`, `object_id`, and
`catalog_digest`, then reads Runtime verified media and the exact object bytes.
It requires `audio/wav`, positive verified size, matching SHA-256, and Runtime's
positive intrinsic `duration_seconds`. The requester bundle does not claim or
override that duration. Inner Speech task/run/attempt/output values remain
provenance/locators and never become outer producer identity.

The public wrapper has no `requester_entry=True` call. The only current
`requester_entry=True` references are the focused forwarding regression; there
are no live production callers. This preserves the public path and all
original22 expectations.

## Fixture dependency closure and exact gap

The existing supported coverage is sufficient for source inspection but not a
real outer qualification:

- `test_wc5_requester_source.py` uses a fake Speech result, fake CAS importer,
  and patched authoritative media reader. It proves descriptor shape,
  idempotency-key stability, ordered entries, and omission of claimant duration.
- `test_draft_voiceover_managed.py` uses a generated-client wire fixture and a
  patched Speech invocation. It proves exact Runtime media-selection/WAV
  custody, trusted outer identity, proposal shape, and no worker-side publish.
- `test_sync_draft_voiceover_action.py` uses the real action runner/context
  with a patched shared helper/proposal. It proves the registered action,
  action-context fences, output manifest, and optional file-port threading.
- `test_draft_voiceover.py` proves the existing private core forwards the
  candidate, scripts, four-field target, and outbox path; it does not admit an
  outer task.
- `test_recipe_native_voiceover.py` proves original/native lowering and timing;
  it has no outer Runtime task or requester outbox.

No current supported test provides all of the following in one normal42a
fixture: real outer `tasks.create` admission for
`video_editing.sync_draft_voiceover`, the actual outer task/run/attempt,
settled managed `authoring_proposal` read, and requester-owned
`queue_proposal`/`flush` acceptance against the admitted four-field base. There
is consequently no honest carrier for accepted outer history, lost-ack/restart
retry, or undo evidence. Adding a fake accepted history/proposal would violate
the qualification boundary, so no test was added.

The exact next carrier required is one isolated normal42a/private source/client
fixture or real qualification harness that supplies those Runtime admission,
managed-output, and accepted-history facts while keeping inner Speech identity
and outer identity distinct. It must use the existing action and
`queue_proposal`/`flush`; it must not add a Speech root, client duration,
alternate media selection, SQL/helper-only commit, or new Runtime route.

## Preflight evidence

Commands were run from the assigned worktree with shared dependencies read-only:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --collect-only \
  tests/packs/video_editing/test_wc5_requester_source.py \
  tests/packs/video_editing/test_draft_voiceover.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py \
  tests/core/execution/test_python_action_context.py
=> 121 tests collected in 1.85s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --collect-only tests/editing_conformance/test_recipe_native_voiceover.py
=> 9 tests collected in 1.07s
```

```text
/home/user/work/venv-agent/bin/python -m ruff check --no-cache \
  astrid/core/execution/executor/_action_context.py \
  astrid/packs/video_editing/actions/sync_draft_voiceover/run.py \
  astrid/packs/video_editing/shared/draft_voiceover.py \
  astrid/packs/video_editing/shared/settled_voiceover_input.py \
  astrid/packs/video_editing/shared/voiceover_requester.py \
  tests/core/execution/test_python_action_context.py \
  tests/packs/video_editing/test_draft_voiceover_managed.py \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py \
  tests/packs/video_editing/test_wc5_requester_source.py
=> All checks passed!
```

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B \
  scripts/vendor_lock.py check runtime.lock.json \
  --producer /home/user/work/wt/rt-pin-42a7203f
=> ok runtime.lock.json (matches producer manifest)

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B \
  /home/user/work/wt/rt-pin-42a7203f/scripts/artifact_manifest.py --check
=> contract/artifacts.json is current

git diff --quiet f07d97715fbe4efcb80e2db40ef4597e81f75547 HEAD -- \
  astrid/core/execution/executor/_action_context.py \
  astrid/packs/video_editing/actions/sync_draft_voiceover/run.py \
  astrid/packs/video_editing/pack.yaml \
  astrid/packs/video_editing/shared/draft_voiceover.py \
  astrid/packs/video_editing/shared/settled_voiceover_input.py \
  astrid/packs/video_editing/shared/voiceover_requester.py
=> identical

git diff --check HEAD^ HEAD
=> passed
```

No full suite was requested. No test body or workflow execution was run.
