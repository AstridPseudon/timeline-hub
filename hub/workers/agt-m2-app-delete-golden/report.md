## Result

Added the exact App `clip.delete` portable golden and conformance/provider coverage.

- Exact source bundle verified against `design/app-track-rename-fixture-request.json`.
- Tests cover scoped raw-ID deletion, both mirrors, opaque/registry/source-pin preservation, restoration/order, and retired-ID refusal.
- No product semantics or refusal tests weakened.

## Evidence

- Targeted: **69 passed, 91 deselected**
- Adjacent suites: **178 passed**
- Ruff: **passed**
- `git diff --check`: **passed**

Full/browser/network suites were not run.

Artifacts written:

- `/tmp/.../agt-m2-app-delete-golden/notes/report.md`
- `/tmp/.../agt-m2-app-delete-golden/commit-msg`