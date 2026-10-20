# Agent transition peer repair review

## Verdict

**APPROVE — bounded Agent repair only.** The added correction in candidate
`5b3e41941b1263011f52f9f1291cbbc854563dbb` closes the two Runtime/App findings
against current Main and does not alter the settled carrier or schema.

This is not a sourcefreeze or activation approval. The Runtime and App peer
ACKs are still required; no sourcefreeze is claimed here.

## Exact candidate identity

- Parent: `eb115db81ac2c24b182fe6873fbd883da851571e`
- Commit: `5b3e41941b1263011f52f9f1291cbbc854563dbb`
- Committed tree: `705fc969ffcc2281d3b3e808e68e8a02467066bc`
- Schema path: `astrid/core/timeline/schema/edit-command.schema.json`
- Schema Git blob: `95d7f4eb90a3afe8b3b6c554f31ac2cce4300d44`
- Schema SHA-256: `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`

The schema is unchanged from the parent. No Runtime/App artifact, public pin,
DTO, generation path, freeze, or new API was added.

## Review findings

- `_transition_set` still writes the incoming transition and matching
  `elementRef` to the destination clip. It now requires exactly one recorded
  same-track predecessor, checks Main’s `abs(predecessor_end - target_start) <
  0.001` adjacency rule, and rejects a duration larger than the shorter pair
  using Main’s frame-fit tolerance. It does not clamp or strip fields.
- The selected-pack `clip.set` path now joins the existing accepted-history
  authority chain for same `(packId, id, kind)` references. A later revision
  or P2 pin is refused atomically for an ordinary same-reference update.
  Explicit `clip.set-element` remains the fresh reselection path, including P2;
  no latest-pin/catalog inference was introduced.
- The existing canonical incoming meaning, first-clip/gap/oversize playback,
  paired `transition` + `elementRef` removal, transition-only clear, exact
  introduced-pin inverse, old accepted retries, opaque values, and occurrence
  owner handling remain unchanged. Playback/compiler files are outside the
  candidate delta.

## Evidence

Current Main’s `element-adapter.ts` was checked directly: same-track adjacency
uses the 0.001 tolerance and transition duration must fit the shorter adjacent
clip. The candidate’s recorded predecessor selection and new checks match
those controls. The pre-existing selected-authority proofs were checked for
inverse pin identity, disjoint rebase/reload, ABA behavior, and explicit
reselection; the new resolver only extends that chain to `clip.set`.

Commands run from the candidate worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-transition-current-peer-repair-tests tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'private_transition or transition_only_clear or explicit_transition or transition_set_enforces' tests/sdk/test_timeline_transition_schema.py
```

Result: **7 passed, 136 deselected**.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-transition-current-peer-repair-authority-tests tests/sdk/test_timeline_selected_param_authority.py -k 'disjoint_peer_and_paginated_reload or inverse_consumed_pin or batch_reselection_changes_stage_authority or param_after_inverse or equal_selection_aba or param_cannot_reselect_pin_after_relevant_peer_selection'
```

Result: **7 passed, 20 deselected**.

The candidate’s bounded transition/P1 test lane was also run directly:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q tests/editing_conformance/test_recipe_clip_scalar_fields.py -k 'transition' tests/sdk/test_timeline_transition_schema.py
```

Result: **29 passed, 87 deselected**.

No full suite, browser, socket, live Runtime, generation, pin, or sourcefreeze
operation was run. The only worktree change made by this review is deletion of
the misplaced `ORCH/design/agent-transition-eb115-peer-reconciliation.md`;
the exact useful report is published at the real orchestration path.

## Next step

Obtain independent Runtime and App ACKs against this exact commit/tree/schema,
then coordinate any activation or sourcefreeze decision. Until those ACKs,
this approval is limited to the Agent repair.
