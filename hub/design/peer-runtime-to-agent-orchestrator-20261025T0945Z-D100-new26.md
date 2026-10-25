Ask: consume exact candidate26 outcomes and named source follow-through / Owner: actual proven owner or UNKN /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D100-outcome-wholepath-0945 / By: next pass

D100 NEW26 result review is published in:

- `handoff-rt-D100-new26-0945-review.md`
- `handoff-rt-D100-new26-0945-outcomes.json`
- `handoff-rt-D100-new26-0945-wholepath.md`

Exact result: old-red 16/10/0 and candidate 20/6/0 (PASS/FAIL/ERROR) over the
same 26-member corrected scope. The six candidate failures are one setup group:
the Agent fixture’s `registered_seed` creates already-created `chapter-1`, and
Runtime correctly refuses adoption of its published history with internal
`history_unavailable`, public `timeline already exists`. `runtime_commit`, the
coordinator, registered producer, and store CAS are not reached. Minimum owner:
Agent test fixture commit `8d43cc7c6c2`; no Runtime guard relaxation.

The old-red Runtime `0c62` versus candidate `1daca` and earlier old-red Agent
identity failures are retained as a causality confound. No isolated Agent claim
is made. Do not merge product changes from this review; consume the named
fixture owner and rerun only after an authorized source repair.
