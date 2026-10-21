# APPROVE — staged inverse correction

Review target: committed `1ee4561a5` (`tl/agt-m2-group-new-parent-track-existing-batch`),
limited to `astrid/sdk/timeline/_recording.py` and
`astrid/sdk/timeline/inverse.py`. No product files were changed by this review.

## Decision

**APPROVE.** The correction preserves the existing strict inverse, ABA,
intervening-write, created-reservation, later-dependent, owner, and order
guards. The only deferred claims are `track.create` claims with an absent
member and `lane.members` claims whose owner is absent while the grouped
inverse is being installed. The deferred claims are materialized after the
same inverse writes and ordering restoration, with `ctx.input_state` disabled;
they therefore describe the restored state and cannot be satisfied by a
refreshed read, a caller-declared ID, an unrelated absent lane, or another
request.

## Source proof

- `_recording.py:295-305` starts from the immutable inverse input claim. It
  switches to the post-reversal `self.state` only for the two named structural
  queries and only when the exact accepted owner/member identity is absent
  from that input. It does not broaden reads or invent IDs.
- `inverse.py:401-447` still checks complete intervening history, staged
  earlier-batch writes, coalesced final writes, collection membership/order,
  each reverse-stage guard, surviving track dependents, and `_validate_inputs`
  before public claim capture.
- `inverse.py:451-469` defers only the absent `track.create` member or absent
  `lane.members` owner. `inverse.py:470-501` then performs the exact grouped
  reverse writes, collection ordering, and root restoration. At
  `inverse.py:502-510`, deferred selections are selected against that restored
  state with `input_state=None`; no unrelated request or mutable refresh is
  consulted.
- The accepted target record is exact: the first command records
  `created=[{'ref':'parent/track:V3','kind':'track','owner':'parent'}]` and an
  absent-to-present `parent/track:V3` write; the second command binds the
  accepted `parent/track:V3` and records the grouped move. The positive test
  also reloads the accepted bundle, reverses the same two records, redoes the
  resulting accepted inverse record, and checks exact document equality.

## Adversarial evidence

The existing committed tests cover the valid grouped restoration and later
V3-dependent clip refusal. Additional bounded checks were run in a temporary
Python harness (no source/test edits):

- changed and same-value intervening writes both raised `intervening_write`
  and left the head byte-for-byte unchanged;
- a later clip using V3 raised the existing intervening/dependency refusal and
  left the head unchanged;
- a foreign absent lane injected into the accepted structural selection
  refused with `identity_conflict` and left the head unchanged;
- corrupted V3 restoration mappings (row ID, write ref, created ref, and row
  value) refused with `history_unavailable` or `inverse_conflict`, atomically;
- caller-declared foreign IDs added to inverse selections, `created`, or
  bindings refused during authoritative claim verification, atomically;
- the unmodified accepted records succeeded through inverse and redo, restoring
  the exact original and target documents.

## Tests

- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_group_new_parent_track.py tests/editing_conformance/test_recipe_m2_group_move.py tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_group_read_view.py` — **82 passed**.
- `PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_group_new_parent_track.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_grouped_clip_cache_inverse.py` — **139 passed**.
- `/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_recording.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_recipe_m2_group_new_parent_track.py` — **passed**.
- `git diff --check` — **passed**.

No full, browser, render, Runtime, public activation/pin/generation, or
private44 replay was run or requested. No blocker or source change remains.
