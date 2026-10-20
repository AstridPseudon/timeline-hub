# Trim interior source review — BLOCKING CASE

Reviewed Agent `e4bec724bec39865b9b6b73b8754abd82d4f4449` in the assigned
`agt-review-trim-interior` worktree. No product changes.

The ordinary binary64 fix and all 17 supplied vectors are correct. Approval
against the unrounded-bound requirement is blocked by a supported integer
registry duration above binary64's exact integer range:

```python
D = 9007199254740995             # int, finite, accepted by existing number/schema guards
args = {"in_s": 0, "out_s": D}   # exact raw file end
# Native capture + execute succeeds, authoring:
{"from": 0.0, "to": 9007199254740996.0, "hold": 9007199254740996.0}
# to > D: one source second outside the unrounded registry bound.
```

At `astrid/sdk/timeline/units.py:23`, the exact floor is computed correctly,
but integer division converts its result to binary64 and rounds upward again.
There is no final `applied_out <= limit` invariant. Native accepts this raw
integer duration without replacing it (`_trim_commands.py:64–77`).

The model additionally converts registry duration to float before its raw
range check (`model.py:424–439`): for the same D, both exact `out_s=D` and truly
overrange `out_s=D+1` succeed with `to=9007199254740996.0`. Native correctly
refuses D+1 before writes. These extreme-integer weaknesses also existed in
the preceding coercion/rounding paths; this is an unmet absolute requirement,
not a claim that the patch introduced their first occurrence. The task
explicitly requests large-value/int-float review and requires raw-bound safety.

Reproducer (exit 0 means it reproduced the stated current violations):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-trim-interior/notes/boundary_probe.py
```

It uses real native capture/execute and the real model source-duration lookup;
no patched duration lookup is needed. It also confirms 3 very large binary64
durations stay bounded, 12 native bad-type/nonfinite/overflow probes refuse
before writes, and native integer overrange refusal records no write.

Focused existing suite, independently run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py -k 'portable_boundary_vectors or portable_golden or rational_fps or retrim or only_existing or replay_consumed or bad_closed_bounds'
```

**39 passed, 59 deselected, exit 0.** The worker's **281 passed** native/media
neighbors and **168 passed / 17 deselected** model/helper/verb neighbors were
read in its report and reused, not rerun. No full or socket/browser suite.

Other findings: shared native/model helper, source-second hold, speed applied
once, rational fps, half-open boundaries, parent-only ownership, registry
timing reads, opaque/child pins, original claims, replay, guarded inverse and
unchanged golden are intact for the reviewed ordinary domain. No epsilon,
global rounding, new args/aliases, schema/pin edits or stored-film rewrite.
Legacy model argument coercions remain more permissive than native schema
validation; the patch does not add or change those coercions.

The App mirror contract is already present at the exact flat shared paths:

- `design/agent-trim-interior-rounding.md`
- `design/agent-trim-interior-rounding-vectors.json`

Both are byte-identical to the repo document/vectors. All three source blob
SHAs match HEAD. Original golden SHA-256 matches
`4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`.
No missing handoff path. However, the 17 vectors contain no integer beyond
2**53, and the binary64-only formula does not resolve this accepted input.

Recommended next step: repair raw integer bound preservation in both entry
paths and the final representable endpoint, add this counterexample to the
portable contract/vectors, and requalify that focused slice before App mirrors
it. This review is complete; no implementation or plan decision was changed.
Full commands, source findings and limitations are in
`workers/agt-review-trim-interior/notes/report.md`.
