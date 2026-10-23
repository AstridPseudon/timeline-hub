# FAIL — V1 Agent resume review

Found one remaining defect: `_collect_media` and `authoring_media_inventory` globally skip any key named `meta`, excluding valid component-parameter media at `params.meta.media_id`. The real `open_authoring_bundle → compile_authoring_candidate` witness reproduces this.

Evidence passed:

- Required tests: 54 passed, 2 subtests.
- Expanded tests: 168 passed, 3 deselected, 2 subtests.
- Ruff passed.
- Mypy: 24 identical baseline errors, no new errors.
- `git diff --check` passed.
- No product changes made.

Full report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V1-agent-resume-review/report.md)