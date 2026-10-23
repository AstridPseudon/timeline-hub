FAIL — helper-level tests pass, but the production reload witness fails:

`commit.bundle_from_document()` raises `AuthoringBundleError: missing media dependency` because `_verify_document` still calls `_collect_media` without opaque-meta filtering.

Evidence: 169 tests passed, Ruff passed, mypy baseline unchanged (24 errors; authoring file 2), diff checks passed. No product edits made.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V1-agent-media-review/report.md)  
`DONE` marker and commit message were written.