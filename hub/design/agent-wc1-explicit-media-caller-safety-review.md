# Agent WC1 explicit-media caller safety review

Date: 2026-10-21 UTC  
Verdict: **HOLD / do not promote**

## Exact provenance and scope

- Proposal: `2aa627af22c8087022101b23aeeb93eca1b2b1a6`
- Proposal tree: `2a936f4d77417ccb14605808d1ae5260c970a451`
- Actual proposal parent/base: `a08a500077c7551fa8455b936d82adc2aae08f41`
- Parent tree: `9a64fb0a08627c4b218d9ea4b8e044a39830da78`
- Direct proposal delta: exactly `astrid/sdk/timeline_media_replacement.py` and
  `tests/test_timeline_clip_replacement.py` (`334 insertions`, `67 deletions`).

The assigned worktree was independently at `de36e302e3ee6e950e22aed5c02c02163f7cf5c8`
(tree `3cafb9450b3633fc7b974a7e0d761fe489badf39`). I reviewed the named proposal
from Git objects and did not treat the unrelated `tests/sdk/test_scene_real_public_summary_rle.py`
change visible when comparing against the current integration merge as part of this proposal.

## What is safe in the source cut

The selected branch does use the pinned native operations: `clip.swap-media` for
the raw parent owner and `occurrence.swap-media` for an explicit occurrence.
It captures from the authored bundle, passes the exact five-field old/new
selections (`asset`, `generation_id`, `variant_id`, `object_id`,
`catalog_digest`) through Runtime verified-media reads, preserves the authored
old alias, and supplies the original revision/publication pair to
`TimelineSession.open`. The idempotency key is passed to the initial flush and
the persisted flight is retried without recapturing. No snapshot inference,
fabricated producer/selection, active private-v2 route, or silent publication
fallback was introduced in the changed source. The existing digest-only branch
remains present.

## Blocking data-loss finding

`astrid/sdk/timeline_media_replacement.py:63-71` matches a pending command only
by `select`, `op`, and `args.old_media`/`args.media`. It does not bind the
persisted new object to the caller's `source_object_id` on retry, and it does
not compare the command's native `intent` or other exact command metadata.
At `:154-162`, a restarted call with omitted `old_media`/`media` can therefore
flush a matching pending command even when the new `source_object_id` supplied
by the caller differs. The current retry test uses the same source identity and
does not cover this mismatch. This violates exact outbox retry safety and is a
promotion blocker; add a strict refusal/no-flush regression for a changed
source object and compare the complete native command identity.

## Test/assertion review

The original full-closure positive, retired-route/grammar positive, CLI mapping
positive, and invalid/incomplete-selection refusal remain in the changed test
file. No opaque or draft test outside the two-file proposal delta was removed.

The original selected positive was not preserved one-to-one. Its direct
commit-door assertions were removed: captured `(project, timeline, body, key)`
identity, `base_revision_id`, `base_publication_id`, the final
`len(transport.committed) == 2`, and the real `commit_timeline` path. They were
replaced by assertions over a fake `TimelineSession`/`Outbox`/`flush` object and
local `execute()` replay. The fake ignores the `TimelineSession.open` arguments
and does not exercise an actual provider or HTTP transport. The replacement
does retain command `select`/`op`/old-new args, no whole-closure publication,
local asset replacement, and same-key lost-ack retry assertions, but it is not
equivalent acceptance evidence.

## Evidence

Focused proposal-tree run, using a private archive of the exact proposal and
the shared Runtime checkout (no worktree source edits):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  "$TMP/tests/test_timeline_clip_replacement.py"
```

Result: **7 passed in 1.40s**.

Smallest adjacent actual-provider node run against the same private proposal
archive:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP:/home/user/work/runtime" \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
  -p no:cacheprovider -m integration \
  "$TMP/tests/editing_conformance/test_commit_runtime_parent_media_swap.py::test_selected_swap_capture_accepted_reload_restart_retry_undo_and_redo"
```

Result: **2 failed** (`image`, `video`) at the SDK-caller tail before Runtime
acceptance: the test transport has no authenticated `_last_handshake`. This is
evidence that the existing provider test was not migrated to the new native
caller; it is not native HTTP acceptance evidence.

`git diff --check` on the exact proposal delta passed. No full suite, rerender,
browser, or live normal-HTTP run was performed. The proposal has no smallest
normal-HTTP selected-media caller case, so that gate remains outstanding and
must be run on a matched published-014 Agent/Runtime pair after the retry
identity and provider-test corrections.

## Required next step

Keep the proposal held. Correct complete pending-command identity matching,
repair the real provider caller test, then run the smallest normal-HTTP parent
and occurrence selected-swap acceptance/restart/exact-retry case with the
published-014 Runtime. Recheck that the digest-only path remains reachable only
for its explicit legacy input shape and that all original positive/refusal
assertions remain present.
