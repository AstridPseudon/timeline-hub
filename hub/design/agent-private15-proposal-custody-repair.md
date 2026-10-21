# Agent private15 proposal custody repair

## Result

Repaired the shared voiceover helper without changing action, runner, host, or
pack declaration files.

- Restored `sync_draft_voiceover` as the existing public path: it retains the
  original preparation, validation, CAS publication, receipt, and failure
  behavior.
- Added the separate private `_sync_draft_voiceover_proposal` entry, reusing
  the same implementation with a managed-proposal mode. The managed path
  never calls `bound.publish` and never fabricates a receipt.
- Replaced the caller-settable `client.trusted_execution_context` lookup with
  the private `_require_action_context()` accessor from the trusted-host
  worker's source. Producer identity and the exact four-field admitted target
  are copied from that context and compared against the proposal target.
- Managed head checking preserves and rechecks the original
  `(head_revision_id, head_publication_id)` pair.
- Restored the original public sync-positive assertions one-to-one and added
  a forged-selection refusal.

## Blocking finding

The current Agent checkout has no existing callable Runtime read boundary for
the exact five-field `MediaSelection` plus authoritative intrinsic duration
and byte/source proof. The available pre-commit surfaces are the detached
authoring target and raw managed-byte reads; `port.selected_media` is only the
commit-time Runtime acceptance boundary. The current synthesizer output rows
are therefore not authoritative selections.

The private managed path fails closed with:

> Managed voiceover proposal requires the existing Runtime authoritative
> media-selection read boundary; synthesizer output claims are not sufficient

No proposal-ready positive, managed output settlement, requester outbox,
lost-ack retry, or guarded undo is claimed. Those require the authoritative
Runtime read and the independent host/action integration review.

## Verification

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py
24 passed in 0.97s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py
134 passed in 6.61s

/home/user/work/venv-agent/bin/python -m ruff check astrid/packs/video_editing/shared/draft_voiceover.py
All checks passed!

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile astrid/packs/video_editing/shared/draft_voiceover.py tests/packs/video_editing/test_draft_voiceover.py
git diff --check
passed
```

Not run: full, live, browser, Runtime, private-pin, or requester-outbox
qualification suites.
