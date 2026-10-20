# Runtime fresh-bootstrap scope preflight — review candidate

The qualified corrupt-state finding is closed in this source candidate. A provider-backed fresh create now calls the existing strict `timeline_scope_is_empty(conn, timeline_id, project_id=project["id"])` after exact create replay and existing-row adoption, before the first timeline INSERT, snapshot, event, receipt or bootstrap publication. Failure uses the existing `headless_content_not_empty` conflict. The new product delta over approved b748 is two lines in `runtime_protocol/service.py:1676`.

This is explicitly a corrupt-state boundary: there is no timeline row, but an injected same-project reserved `timeline:<id>` document contains plain authored data or duplicate-hidden data. Current document APIs reject reserved IDs; this work does not demonstrate a normal-current-API exploit. Refusal prevents allocating empty canonical authority; the original raw recovery bytes were not being deleted by the old behavior.

## Source

- Assigned Runtime base: `129493b2aff614560d9b7ac2577957e799cf30ec`.
- Approved shell base ported: `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, including strict reader `ff9d5c17bc75fb12b3293690a8d9acd8eded0db2`. All four files in that approved delta are byte-identical to b748; current fixes are preserved.
- Final central source tree: `708df14c75ef739a2c6130ca39f9e67b2758a571`.
- Real Agent qualification: clean `/home/user/work/agent` at `4ef1391c2c104d5d11b3a27265035c51be296045`, checked before and after the central run.
- Source: `/home/user/work/wt/rt-m2-fresh-bootstrap-scope-preflight/runtime_protocol/service.py:1658` and `runtime_protocol/timeline_commit_store.py:55`.
- Permanent probes: `/home/user/work/wt/rt-m2-fresh-bootstrap-scope-preflight/tests/test_timeline_fresh_bootstrap_scope.py`.

## Scope and behavior

The provider condition preserves no-provider Main creation. Exact replay remains before any new state check. The document query is scoped to the requested project, so a foreign project's same-ID orphan document does not prevent fresh creation. Unrelated ordinary documents and ingested media also remain valid and unchanged. Fresh creation, canonical empty legacy bytes and distinct opaque empty keys still install the existing exact empty bootstrap.

No shared helper policy, JSON normalizer, migration, overwrite, writer, endpoint, schema, table or DTO was added. The helper's existing timeline-keyed row checks are unchanged. Timeline IDs are realm-global; this is not a change to cross-project ID ownership or a general repair of arbitrary corrupt relational rows. A foreign timeline row continues through the existing same-ID conflict path. Baseline adoption of an already accepted immutable publication is unchanged; this preflight applies only to new empty authority.

All new positive authority is created through Runtime APIs. SQL in the new tests inserts only the explicit orphan document after proving the timeline row absent. Existing approved shell tests retain their historical negative fixtures.

## Evidence

- Both retained raw inputs (`{"clips":[{"id":"keep"}]}` and `{"clips":[{"id":"keep"}],"clips":[]}`) fail the new refusal expectation on verified ff9: **2 failed**, both `DID NOT RAISE ConflictError`.
- Candidate targeted new controls plus existing headless/shell/baseline cases: **124 passed**.
- Final new controls plus unchanged original audit orphan probe and original reviewer probes: **13 passed, 1 deselected** (real-provider integration reserved for central).
- Central bounded real-provider lane: **14 passed, 7 deselected**: nine original commit integration cases, four absent/null-head repair cases, one new fresh-create bootstrap case. Request `rt-m2-fresh-bootstrap-scope-preflight-commit-integration-1020131338-753`.
- Negative attempts are repeated; each compares whole SQL dump, complete CAS/staging file and directory trees, raw bytes and SQLite `total_changes`. No persistence writes, including rolled-back SQL writes, occur.
- Changed helper/tests lint passes. `service.py` has exactly its existing 77 lint diagnostics, verified equal to HEAD; no new diagnostic. `git diff --check` passes.

No full suite, schema generation, pin, publication, merge, commit, browser/App or macOS qualification. No passing behavior expectation was removed, weakened or converted to refusal. Shared dependencies and caches were not modified. The approved private-init central launcher is ported unchanged but was not invoked; it targets another worker's private overlay.

This branch is source-reviewable only. Owner classification of the corrupt-state boundary remains pending; no integration/publication approval is implied. Recommended next step: review the two-line delta against the already merged shell base, decide whether the qualified boundary is required, and integrate only through the orchestrator if accepted. No implementation blocker.

[Detailed report and exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-fresh-bootstrap-scope-preflight/DetailedReport.md).
