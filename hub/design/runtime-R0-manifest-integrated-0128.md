## Report

R0 integrated qualification passed on:

- HEAD: `db11ea82978f...`
- Tree: `a92a576a8837...`
- Source tree `8a742b1...` matches exactly.
- Base-to-HEAD change: only `contract/artifacts.json`.
- Worktree clean; no tracked edits or deletions.

Manifest:

- 78 entries total; 1 changed, 77 unchanged.
- Producer unchanged: `astrid-runtime`.
- Package digest: `78a69901...9035e6` → `d095328f...09ecc2`.
- Manifest version: `d5f98db3...88a572` → `100eb485...cb4f61`.
- `DocPatchArgs` root identity and `__all__` export verified.
- Producer/schema/client/v2 request/reply surfaces byte-identical to base.
- Meta limits unchanged: 64 namespaces, 65,536-byte namespace value, 262,144-byte total, depth 32.

Checks:

- Exact pytest lane: `74 passed`.
- `scripts/artifact_manifest.py --check`: pass.
- `generators/generate.py --check`: pass.
- Independent canonical 78-entry rebuild: pass.
- `git diff --check`: pass.

No full/browser/gate/benchmark suite was run, so no final full-suite PASS is claimed. PLAN R0/F and C0 remain unchanged. Commit message and `DONE` marker recorded.