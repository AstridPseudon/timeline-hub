## Report

Implemented D126’s exact fake-runtime contract line in the existing builder-consumed README and gate notes.

Evidence:

- Both files remain `0644`; each candidate is predecessor + exact sentence only.
- `git diff --check`: PASS.
- Real `delivery-build.render_readme()` with four-repo stub: PASS; placeholders resolved and fences balanced.
- Receipt JSON validation: PASS.
- No active builder before/after installation.
- No product tests/typecheck/lint/full suite run; docs-only task.

D1359’s historical `FAIL` was not promoted. D124/1414 sources and the D126 normal-home receipt were consumed.

Commit message and `DONE` marker created.