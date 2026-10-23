# G5 c271 cause-return reconciliation

**PASS — causal reconciliation complete; c271/G5 remains FAIL / DRAFT / P1-gated.**

The predecessor's Agent-emission attribution is retracted. The exact offline
validation regenerated the captured Agent candidate, ten native writes, and
step records byte-for-byte, then reproduced Runtime's HTTP 422
`validation_error` / `invalid_records` refusal:

```text
inverse stage native writes do not cover its authenticated effect image
```

Exact call:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-effect-sol-2013/evidence/replay.py
```

Runtime's authenticated collection normalizer validates each physical pin and
then strips `shot_revision_id` for the authored comparison
(`timeline_commit_auth.py:817-864`). Its ordinary projection of native write 6
(`parent`, `occurrences`) copies the authored-only permutation into the
physical image (`:1188-1201`). The trace shows all three pins present before
projection and all three missing after it. Recursive native/effect comparison
differs only at:

```text
parent.occurrences[0..2].shot_revision_id
```

Native/effect root-key sets are identical, and all other payload bytes match.
The Agent intentionally models `parent/occurrences` as authored placements and
requires an exact row-preserving permutation (`_command_state.py:291-292,
370-377`). The accepted source has occurrence native writes, so its
materialization helper correctly emits no `commit.materialization` bindings
(`_commit_patch.py:632-649`). Adding physical pins or speculative turnover
bindings would not fix this comparison and would violate the representation.

Precise owner: **Runtime normalization**, preserving each already-authenticated
physical pin while applying the authenticated authored-row permutation, with
strict membership/order/owner/identity checks. No source or product repair was
attempted. Full immutable archive, source-history constraints, hashes,
credential scan (0), exact trace, limits, and command results are in the own
report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-c271-cause-return-2017/report.md`
