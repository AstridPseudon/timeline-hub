Completed source-only analysis. **No product or test files changed.**

- **23 selected failures share `m1.film`:** it duplicates the historical declaration into a fresh, empty destination. The destination has no baseline child clip, so rejection does not require any source-metadata inequality.
- **Word IDs 99 and 101 change the bound source:** one replaces the referenced transcript descriptor; the other removes it. The native setter also removes its derived `binding_id`.
- Canonical materialization can change revision metadata, but the published packets lack actual baseline/candidate snapshots isolating a metadata-only defect. Those exact deltas remain **UNKNOWN**.

No safe `validation.py` repair or faithful setup-only correction was proven. Broadening historical acceptance would weaken the required declaration/source protections.

Checks:

- In-memory AST parse/compile: **PASS**, 17 current files and 14 HEAD counterparts; no module execution.
- Source/input conservation: **14/14 unchanged** against HEAD and both actual-run trees.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/validation.py`: **PASS**.
- `/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir /tmp/w-00fe139748/mypy-r1-legacy-basis astrid/sdk/timeline/validation.py`: **PASS**.
- `git diff --check`: **PASS**; worktree clean.

No functional tests ran, as required. Next steps belong to the common M1 fixture owner and word fixture/source owner; the report specifies the existing safe evidence needed before another repair or rerun.

[Detailed call trace and per-ID findings](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-legacy-basis-sol-0338/evidence/source-findings.md)

F-D86 commit message and empty `DONE` marker created.