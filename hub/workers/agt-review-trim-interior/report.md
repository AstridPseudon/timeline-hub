Blocking case found: raw integer duration `9007199254740995` with an exact-end request writes `to=hold=9007199254740996.0`, exceeding the unrounded bound. The model also accepts an overrange request at that value.

Independent verification:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py -k 'portable_boundary_vectors or portable_golden or rational_fps or retrim or only_existing or replay_consumed or bad_closed_bounds'
```

**39 passed, 59 deselected**, including all 17 vectors. Additional probes reproduced the integer violation and confirmed 12 invalid native inputs refuse before writes. Reused the reported 281+168 neighbor passes; no full suite run.

The flat App contract and vectors exist and match the repository copies. Product code is unchanged.

[Verdict](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-trim-interior.md) · [Detailed report and commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-trim-interior/notes/report.md)

Review complete; `DONE` created. Recommend fixing integer bound preservation and adding this case before App qualification.