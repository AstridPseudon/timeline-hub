## G2/P4 read-only report

**SOURCE-CAUSE: PASS. Body remains FAILED.**

Cause is the unconditional publication hydration added in `astrid/sdk/timeline/sync.py:199-205` by `d05fcc0766`.

Path:

1. `TimelineSession._bundle()` always passes `publication_id`.
2. `fetch_bundle()` calls `open_bundle()` with the exact revision/publication pair.
3. `_remote_timeline.open_bundle()` authenticates that pair and attaches `_runtime_document`.
4. `NativeSheet.export()` receives the already-cached bundle.
5. The assertion fails before sheet mutation or HTTP application.

The earlier passing scope (`d05fcc0766^`) only passed `publication_id` for `doc.patch` commands. The smallest source seam is restoring that conditional selection. Sol1639 owns any correction; none was made here.

Authority constraints remain valid: outbox scope/base identity, exact publication-history matching, canonical closure verification, and accepted conversion through `bundle_from_document()`.

The fixture is not causal: `source["source_mapping"]` is cache-free, and the failure occurs before mutation. Accepted canonical output is correctly expected to contain `_runtime_document`.

Evidence:

- Retained XML/log 30725: original test failed at line 113 in 4.12s.
- Retained command: targeted P4 selector, one failure.
- `python3` AST parse of 7 relevant files: **PASS**.
- `git diff --check`: **PASS**.
- Worktree: clean; no product/test/HTTP rerun performed.

Control-doc limitation: the named frozen `docs/projects/timeline-r4` path was absent; current Runtime `contract/commit-v2.md` was used instead.

Commit message and `DONE` marker written.