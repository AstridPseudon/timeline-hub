# Agent WC5 voiceover proposal cut

## Exact caller cut

- Migrated the only in-scope producer caller, `astrid/packs/video_editing/shared/draft_voiceover.py` (the former `bound.publish(...)` call at the ledger's `:475`), to proposal capture.
- Removed `TargetBoundAuthoringBundle.publish` and `_transport_idempotency_key` from `astrid/sdk/authoring_remote.py`.
- Preserved `open`, `compile`, `validate`, `diff`, `preview`, and the read-only target closure checks.
- No producer-side Runtime publication, candidate writer, generic apply/root-diff path, task fence, or producer guard is used.

## Proposal and approval binding

`TargetBoundAuthoringBundle.proposal(...)` validates the pinned project/timeline/base revision, compiles the candidate locally, validates every registered `EditCommand`, and returns a direct proposal containing:

- `kind: edit-proposal`, schema version, producer identity, admitted target, native commands, and rationale;
- `proposal_digest`, calculated over the canonical proposal body;
- `approval_binding.proposal_digest`, bound to that exact digest.

If the command set becomes complete, `_commit_voiceover_proposal` uses the existing `TimelineSession.commit_many` durable outbox with an idempotency key derived from the proposal digest and a `via` value carrying the digest. It does not call `queue_proposal`, so direct requests do not receive invented task fences.

## Captures

- Text capture only occurs when the pinned script exposes one exact descriptor: `object_id == digest`, bounded UTF-8 size, and `text/plain; charset=utf-8`; the candidate already contains the same `voiceover_script` occurrence row, so existing row order, pin identity, and word-anchor state are not invented or rewritten.
- The generated media identity and generated clip timing remain known producer intent, but the current native command registry accepts only image/video media selectors and has no registered audio-source/duration command. The producer therefore emits an open proposal with an exact per-occurrence dependency instead of silently dropping audio or timing edits.
- Existing positive/opaque/timing/approval assertions remain in the original direct voiceover tests. The new direct assertion checks `proposal_open`, digest binding, and the generated-audio/timing gap.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py
23 passed in 0.84s
```

Also passed syntax and whitespace checks:

```text
python3 -m py_compile astrid/sdk/authoring_remote.py astrid/packs/video_editing/shared/draft_voiceover.py
git diff --check
```

No full, live-runtime, browser, or localhost suite was requested.

## Gaps / held-open dependencies

- Real provider/Runtime durable-outbox acceptance of a completed voiceover command batch is not claimed: the current registered commands cannot express generated audio media plus its timing. This remains the bounded OPEN dependency required by WC5.
- The proposal carries the approval digest binding and the outbox request source carries that digest; there is no separate approval endpoint or DTO in the existing direct-request path, so none was invented here.
- The existing out-of-scope legacy `tests/timeline/test_authoring_feedback.py` still directly calls the removed `TargetBoundAuthoringBundle.publish` API. It was not edited because WC5 restricts changes to `authoring_remote.py` and the specific voiceover producer/direct tests; that suite was not run.
- The ledger remains HELD until the integration merge supplies the Runtime/native audio-media and timing capability and migrates any remaining legacy caller tests.
