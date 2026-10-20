## agt-qual-d06 report: D06 (core extensions deletion) qualified, row set to DELETED

**Result:** The deletion holds on the current tree. I marked D06 DELETED in `design/deletion-ledger.agent.md` (the orch copy at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.agent.md`). The status is conditional on the deletion branch landing on integration.

### What I did
- **Merge not performed.** Merging `tl/integration` (4a75f68f) into the branch needs a `.git` write, which is read-only to me. Instead I checked the delta: since the base `fc324e83`, integration changed 11 files (718+/41−), and none of them is under `astrid/core/extensions`, `tests/core/extensions`, or the replacing test files. The merge should therefore be clean. The manager's merge queue needs to do the actual merge and re-run the targeted set on the merged tree.
- **No code changes in the worktree.** `git status` is clean. The deletion is already commit 6c5b616a.
- **Importers and references:** `git grep` on the worktree finds no remaining `core.extensions`, `core/extensions`, `ExtensionRegistry`, `ExtensionPoint`, `parse_contribution`, `extensions/schema`, `contribution.json`, `point.json`, or `sidecar.py`/`scopes.py` references. The only leftovers are a stale cache entry in `tests/.test_durations` and one docs line (below).

### Commands and results
- Targeted pytest, run directly (not via the test service):
  `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/test_pack_discovery_v3.py tests/test_editor_extension_catalog.py tests/packs/test_pack_discovery.py tests/packs/test_pack_resolver.py tests/packs/test_pack_rendering_extensions.py tests/packs/test_pack_layout_contract.py tests/packs/test_pack_yaml_schema.py tests/test_sdk_public_surface.py tests/core/test_elements_registry.py tests/core/test_element_kind_registry.py`
  → **255 passed, 7 subtests passed** (about 10 minutes).
- `python -m scripts.reshape.compare_structure_baseline` → **current=14, new=0, fixed=0** (was 15 before the deletion).
- `python scripts/reshape/check_doc_references.py` → **0 errors, 0 warnings**.
- All named replacement tests exist in the tree (checked by grep).
- Cleanup: removed the ignored `__pycache__` directories my test runs created (`git clean -fdX`). The worktree now has no changes and no ignored files.
- The full suite was not requested, and I did not run one.

### Decisions
- **Status DELETED, not held.** The deletion is proven on the branch, and its replacements pass. The "proof on the merged tree" still depends on the merge, so the row says so.
- **Replacing tests** (kept from the original row): `test_pack_discovery_v3.py::test_external_broken_hidden_and_duplicate_roots_are_isolated` and `test_editor_extension_catalog.py::test_editor_entry_discovery_rejects_paths_outside_pack`. The full old-test mapping is in `workers/agt-m2-review-retirements/notes/report.md`. I checked that the named tests exist and pass; I did not re-audit each mapping line.
- **Commit message:** written to `.../orch/workers/agt-qual-d06/commit-msg`. I left out model names, per the brief. I kept only the Claude-Session trailer.

### Follow-ups (not done; outside the ledger scope)
1. `docs/development/testing-plan.md:282` still says "15 distinct violations"; it is now 14. Recommend a two-line docs fix and a bullet removal in the agent area.
2. `tests/.test_durations` still has stale `tests/core/extensions/*` entries. Harmless, but the cache could be regenerated.
3. Some legacy behaviours have no one-to-one replacement: the sidecar symlink-escape cases, the disabled-ID policy, and the mtime cache. The mapping treats them as belonging to a dormant second registry with no caller, and the plan already cuts them. Live-discovery symlink confinement is not separately re-verified here.

### Unverified / blocked
- Not verified: the merged tree itself (integration plus deletion). That needs the actual merge.
- Scratch cleanup: my attempt to delete `scratchpad/integration.tar` (106 MB) and an empty `scratchpad/merged/` was denied. They sit in my scratchpad, not the worktree, and need manual removal.
- `DONE` created; no `BLOCKED`.
