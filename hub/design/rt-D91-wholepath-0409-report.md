# D91 read-only investigation report

Found earliest divergence: the D91 fixture’s mixed setup commands are submitted with one `edit` step whose `patch` is empty (`runtime/tests/test_timeline_commit_integration.py:126-136`). Agent validation then rejects the real `doc.patch` changes at `_commit_patch.py:71-85`, before prepared-commit construction (`commit.py:1429`) or Runtime acceptance.

Actual central proof `17648` confirms:

- `10 errors`, all `step patch omits doc.patch changes`
- `original-third`, step `edit`, command ordinal `0`
- Missing claim: `ref=parent`, path `occurrences/occurrence_id:occurrence-3/duration_ms`, `1800 → 2000`

The `39fcc` physical placement correction is present and is distinct from the earlier omission. For `authored-first`, source ordering puts the first physical patch at command ordinal `2`; private records were not expanded.

Passing patterns were found:

- Mixed step: aggregate all `doc.patch` changes (`test_commit_runtime_parent_media.py:33-40`)
- Per-command steps: attach each patch to its own ordinal (`tests/timeline/test_authoring_media.py:672-675`)

Minimal owner handoff: Sol’s D91 test-file correction should populate step patches using one of these existing patterns. No Runtime/provider fix is indicated.

Checks:

- Candidate AST parse/compile: PASS
- Scoped `git diff --check`: PASS
- Worktree unchanged
- No pytest, collection, fixtures, services, browsers, builds, or repros run

Evidence: [wholepath-findings.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-wholepath-0409/evidence/wholepath-findings.md)

Required `commit-msg` and `DONE` markers created.