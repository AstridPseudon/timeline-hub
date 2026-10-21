# Agent private15 authoritative media read

## Result

Closed the managed voiceover proposal media-read gap in
`astrid/packs/video_editing/shared/draft_voiceover.py` without changing the
action, host, or Runtime source.

The private `_sync_draft_voiceover_proposal` path now:

- obtains the settled output binding from the existing managed output row;
- resolves the exact five-field selection through the existing Runtime
  `getProjectMediaSelection` generated-client operation;
- reads the matching authoritative media metadata through the existing
  verified-media (`MediaReads.selected`) operation, including MIME, byte size,
  and intrinsic duration;
- reads the selected object bytes and checks both SHA-256 identity and exact
  Runtime-reported size; and
- repeats the same authoritative read for the old selected voiceover media
  before native capture.

The private preparation call uses the Runtime duration for retiming and the
final capture re-read uses the Runtime duration again. No returned synthesizer
duration, selection, MIME, or size is used as authority. The existing public
`sync_draft_voiceover` path still uses its original preparation, validation,
CAS publication, receipt, and failure behavior. Managed proposals still use
`_require_action_context`, preserve the original revision/publication pair, do
not call `bound.publish`, and do not fabricate a receipt.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py
26 passed in 1.13s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py tests/editing_conformance/test_recipe_native_voiceover.py tests/editing_conformance/test_producer_guard.py tests/editing_conformance/test_settled_proposal_contract.py
136 passed in 8.90s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile astrid/packs/video_editing/shared/draft_voiceover.py tests/packs/video_editing/test_draft_voiceover.py
git diff --check
passed
```

The shared module passes Ruff. The touched test file retains pre-existing
style findings (31 E701/E702/E401/I001 findings); none was introduced by the
two new tests. No full, browser, live, Runtime, private-pin, requester-outbox,
or render qualification suite was run.

## Qualification boundary

The direct positive test uses a Runtime-read-shaped client double only to
exercise the Agent boundary. It is not a live Runtime qualification and does
not claim the normal private pin or requester outbox/retry/undo proof. Those
remain for the independently reviewed C3d Agent/Runtime pair. Runtime read
authorization failures are allowed to propagate as the normal API error; no
scope was broadened.
