## agt-docs-out-of-repo: report

Four review/process docs are removed from the Agent repo's `design/`. Two product contracts stay, because tests reference them. The targeted tests that mention `design/` pass.

### Kept vs removed

| File | Decision | Reason |
|---|---|---|
| `agent-review-viewing-20261020.md` (122 lines) | **Removed** | Review note. No references. Orch copy is byte-identical. |
| `agent-review-viewing-20261020b.md` (64 lines) | **Removed** | Review note. No references. Orch copy is byte-identical. |
| `owner-film-differences.md` (83 lines) | **Removed** | Viewing review list. No references. The orch file of this name is a different, shorter document, so the repo version is saved as `orch/design/owner-film-differences.agent-repo.md`. |
| `m2-public10-adoption.md` (147 lines) | **Removed** | Status/process record. No references. The orch file of this name is a different document, so the repo version is saved as `orch/design/m2-public10-adoption.agent-repo.md`. |
| `audio-compile-contract.md` (136 lines) | **Kept** | Referenced by `tests/editing_conformance/test_compile_contracts.py`, `tests/editing_conformance/fixtures/audio_compile_contract.json`, and `tests/packs/rendering/test_normal_audio_source_phase.py`. |
| `visual-compile-contract.md` (110 lines) | **Kept** | Referenced by `tests/editing_conformance/test_compile_contracts.py` and `tests/editing_conformance/fixtures/visual_compile_contract.json`. |

Removed lines total 416. Kept lines total 246. The brief's "~664" was the whole directory (662 lines).

### Checks
- Grep over `astrid/`, `tests/` and `docs/` finds no references to the four removed basenames.
- Byte-compare: the two `agent-review-viewing-*` copies match orch exactly. The other two orch copies differ, as noted above. The two kept contracts' orch copies are stale: the repo versions are newer. I did not touch them.
- The `design/` removal goes through `git rm`, and the four deletions are staged in the worktree. The only other worktree change is `DONE`, which lives outside it.

### Tests
Command, run through the test service:
`/home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_recipe_text_binding_spike.py`

Result: **51 passed, 7 xfailed in 1.39s** (request `agt-docs-out-of-repo-targeted-1020063023-29979`, agent tree `2a2a1fc5`). No full suite was requested.

### Notes
- `tests/editing_conformance/test_recipe_text_binding_spike.py` cites `design/m2-text-binding-contract.md`. That file is not in the repo's `design/`, so the citation is already dangling. It predates this change; I left it alone.
- The commit message is at `orch/workers/agt-docs-out-of-repo/commit-msg`. `DONE` is created. Nothing was pushed or merged.
