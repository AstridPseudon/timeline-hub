## Done

- Exact published reads use the loaded immutable revision, never stale head labels or drafts.
- Added Runtime commit-history support preserving publication ancestry and same-content edges.
- Added regression tests and coordination notes.

## Evidence

`91 passed`:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q --basetemp=/tmp/agt-m1-readback-basetemp \
  tests/sdk/test_timeline_revisions.py tests/sdk/test_timeline_show_views.py \
  tests/sdk/test_timeline_cuts.py tests/packs/timeline/test_cli_history.py \
  tests/packs/timeline/test_verbs_working_copy.py \
  tests/packs/timeline/test_show_clip_working_copy.py
```

Ruff and `git diff --check` passed.

Product diff: 305 additions, 33 deletions. Full/live Runtime suites were not run.

Commit message written to the requested harness path.