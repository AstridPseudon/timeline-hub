## Report

- Migrated the D66 test to the requester-owned v2 route via `publish_authoring_proposal`.
- Preserved single publication, producer custody, renderer, result, and no-save/invoke assertions.
- Only changed the assigned function in [test_runtime_publication_chain.py](/home/user/work/wt/rt-D72-generic-host-1717/tests/packs/video_editing/test_runtime_publication_chain.py:1030).
- No product source or legacy alias added.

Tests/checks:

- Target: `1 passed`
- Bounded neighboring tests: `3 passed`
- Ruff: passed
- Compile: passed
- `git diff --check`: passed
- Mypy baseline: blocked by unavailable `venv-agent-typecheck-v2`; fallback environments lack YAML stubs and reject installed NumPy stubs.

Evidence is in the durable worker evidence directory. Independent protected review remains for the orchestrator’s queue workflow.