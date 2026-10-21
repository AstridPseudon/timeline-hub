# WC5 current017 prerequisite-join review

## Verdict

**APPROVE** for dormant source staging only. This review does not approve
registration, activation, pin/public adoption, native or HTTP execution, or a
normal outer workflow claim.

Reviewed exact candidate:

- commit `8a6f1024651b9ecb481e2a6cf5258c7598f65deb`
- tree `3d0c76ec570046036979b93794e517744a9a3301`
- parent/current safety base `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`
  / tree `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`

## Source and custody findings

- The six feature production blobs are byte-identical to the independently
  approved f07/a4da lineage: `_action_context.py`, the action runner,
  `pack.yaml`, `draft_voiceover.py`, `settled_voiceover_input.py`, and
  `voiceover_requester.py`. The current source has no diff against the f07
  versions of these six files.
- `settled_speech_input` is an optional `type: file` action input. The
  requester builds one ordinary ordered descriptor and passes the same
  descriptor object ID in `execution_request.inputs[]` and the one-element
  `input_manifest`. Runtime/host materialization therefore remains the
  existing immutable CAS/attempt-input path; no path or new DTO is added.
- The consumer treats the bundle as a locator only. It checks the ordered
  occurrence/text/settings entries and H3 result digest, then selects the
  inner task from the result coordinates and re-reads task identity, project,
  capability, state, task inputs/result, exactly one managed speech output,
  exact output/attempt binding, and Runtime's existing five-field media
  selection. `_read_authoritative_media_info` supplies the verified WAV bytes,
  size, hash, media type, and intrinsic duration. None of those facts is
  accepted from the bundle as authority.
- The outer proposal uses only the lifetime-fenced `_ActionContext` producer
  and admitted-target values. Inner Speech task/attempt/output values remain
  provenance and are not copied into the outer producer guard. The requester
  reads the managed outer proposal, validates it, then is the sole committer
  through `TimelineSession.queue_proposal()` followed by `flush()`.
- The actual pack declaration and action runner agree on the optional file
  input and report/proposal outputs. The existing private containing seam is
  coherent: `_sync_draft_voiceover(..., requester_entry=True)` forwards the
  pinned candidate, scripts, four-field target, settings/selection choices,
  timing values, and outbox path to the requester. The public wrapper and
  managed action do not set `requester_entry`; `rg` found no live production
  caller, so default/live behavior is unchanged.

## Preservation checks

`git diff --name-only 6c1989adf..8a6f1024651b9ecb481e2a6cf5258c7598f65deb`
contains only the 11 assigned feature/test paths. The following are unchanged
from 6c: the canonical EditCommand schema, current-union fixtures,
`runtime.lock.json`, all generated Runtime client files, and all other
current-safety paths. The inherited PRIVATE017 controls remain the frozen
schema raw SHA-256 `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`
(65 definitions / 37 clauses), Runtime source `42a7203f49bb89f299ec854cfbf2b1444e815a7c`,
the 15 locked consumer files, and the 76-entry Runtime artifact manifest
(`sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`).

## Tests and limits

Current-tree targeted controls:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_wc5_requester_source.py tests/packs/video_editing/test_draft_voiceover.py tests/packs/video_editing/test_draft_voiceover_managed.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/core/execution/test_python_action_context.py
121 passed in 12.00s
```

```text
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/core/execution/executor/_action_context.py astrid/packs/video_editing/actions/sync_draft_voiceover/run.py astrid/packs/video_editing/shared/draft_voiceover.py astrid/packs/video_editing/shared/settled_voiceover_input.py astrid/packs/video_editing/shared/voiceover_requester.py tests/core/execution/test_python_action_context.py tests/packs/video_editing/test_draft_voiceover_managed.py tests/packs/video_editing/test_sync_draft_voiceover_action.py tests/packs/video_editing/test_wc5_requester_source.py
All checks passed!
git diff --check: passed
```

Reused independent controls remain valid because the reviewed source blobs are
unchanged: f07 containing-entry review `agt-review-wc5-containing-private-entry-1014`
reported 29 targeted voiceover tests and 92 neighboring requester/coordinator/
managed/action tests passing; the a4da custody review
`agt-review-wc5-existing-input-context-custody-0841` reported 23 + 7 + 9 + 24
focused tests and three compact custody negatives passing. No mocked test is
treated as a normal Runtime workflow proof.

The broader Ruff invocation over the compact legacy
`tests/packs/video_editing/test_draft_voiceover.py` reports 32 style findings;
the parent 6c version already reports 31, and no style cleanup was made.

Not run or claimed: full suites, HTTP/live sockets, native execution,
settlement, generation, renderer, browser, installation, pin/public adoption,
or the real outer requester -> managed proposal -> outbox commit/retry/undo
journey.

## Smallest remaining prerequisite

One genuine outer qualification on the exact matched Agent/Runtime PRIVATE017
pair: enter the existing private requester seam through a normal Runtime
admission, settle the real outer `authoring_proposal`, and demonstrate the
requester-owned `queue_proposal`/`flush` accepted commit plus lost-ack
restart/exact retry and undo. Keep the inner Speech selection/duration and the
outer producer/target guard distinct throughout. Until that node exists, this
is source APPROVE only and remains dormant.
