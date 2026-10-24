## Report — F-helper-originals

- Qualified 13 eligible exact-original selectors: **13 passed**, 0 failed, 0 skipped, 73.955s.
- Intentionally did not rerun `test_cut_nudge_restart_merges_other_cut["second"]`; it remains source-only due the known missing authenticated word binding.
- Preserved all original assertions and refusal predicates. No files in the worktree changed.
- Agent modules resolved from this worktree; Runtime modules from `/home/user/work/runtime` at `1d9ddba...`.
- Pre/post source, body, and AST hashes were identical. `git diff --check` passed.
- JUnit evidence: [helper-originals-eligible.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-helper-originals-0622/helper-originals-eligible.xml)
- Commit message written to the requested path; `DONE` marker created.

Test command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
[13 exact assigned selectors] \
--junitxml=.../helper-originals-eligible.xml
```

Recommended next step: record the 13 named receipts and retain the `["second"]` row as an explicit unqualified source gap.