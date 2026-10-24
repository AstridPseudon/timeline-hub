## R2r integrated proof report

- No source changes. Worker and home Runtime checkout are clean.
- HEAD: `2b49da8d6d8dbb8245a1a7cc8d7eee7d3bdaae65`
- Tree: `40eb05d5a51b8d7b31cbfad8a38afeb3318fbd44`
- Matches reviewed commit `2e96c68c…` exactly.
- Exact Agent source: commit `12701589…`, tree `efad939c…`; ambient Agent checkout was not used.

Tests:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_historical_image.py
13 passed in 11.90s

/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_inverse_occurrence_retirement.py \
  tests/test_timeline_inverse_stage_authentication.py \
  tests/test_timeline_commit_authentication.py \
  tests/test_timeline_history_authenticated_read.py \
  tests/test_timeline_source_duplicate_authority.py
243 passed, 74 deselected in 22.44s
```

Additional checks:

- Ruff: passed.
- Artifact manifest: current.
- `git diff --check`: passed.
- Protected paths: exactly 502, all byte-identical.
- Protected aggregate SHA-256: `75de7fb81b97ba2320751d61c6b0fa3da9cc8fb6c0a15552fc8e5ea95d26ce3e`.
- Independent review’s scoped Pyright: parent/final `0 / 0` diagnostics.
- Auth blob SHA-256: `4a0c8b03…`.
- New test SHA-256: `902343ec…`.

The standalone test exercises in-process origin/target before-and-after documents and captures the actual `auth.validate` redo packet. It verifies the authenticated root `internal-revision:authoring-timeline-revision-f910933b…`, owner `occurrence:return-owner/shot`, native range `[0,1]`, and effect range `[0,3]`.

Custody limits remain unchanged: the original 0339 packet, author’s temporary 61,298-byte capture, and 11 manifest artifacts are unavailable and were not reconstructed. No original-family, last-owner, HTTP, browser, full, benchmark, or broader duplicate suite was run.

Required `commit-msg` and empty `DONE` markers were created.