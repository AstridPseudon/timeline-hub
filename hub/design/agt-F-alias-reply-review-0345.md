## Review report

Source-only result: **PASS**. Overall behavior remains **HOLD**, not full PASS.

Reviewed `4b79850b51`:

- `parent_revision_id` derives from authoritative `accepted_revision_id`.
- Canonical document, receipt, steps, identity mapping, and accepted reply remain intact.
- No wire/API/schema/client/Runtime changes.
- Production paths traced through `publish_authoring_candidate → authoring_commit_request → commit_timeline`, and `TimelineSession.commit_many → flush`.
- Trusted-seed fixture preserves the original 11 predicates; original body hash and AST remain identical.

Tests:

- Alias/publication controls: **24 passed**
- Publication neighbors: **18 passed**
- Complete-reply regression: **1 passed**
- First media round-trip: **1 passed**
- Scoped Ruff: passed
- Private mypy: passed
- Vendor lock, artifact manifest, `git diff --check`: passed

The retained original integration remains unresolved: after the prior `KeyError` was cleared, its unchanged fixture expects the pre-fork candidate shot ID, while the authoritative alias path persists an `authoring-fork-*` ID. I did not weaken or rerun that original body, nor the ABA body.

Worktree is clean; no source edits made. Recommended next step: separate fork-ID owner resolves the fixture/source continuation.