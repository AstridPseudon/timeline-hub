## Report — FAIL / HOLD

Reviewed `3d86dfc93` over `07b3f277a` (proof-only; no product edits, worktree clean).

Findings:

- **FAIL — validation-to-launch TOCTOU.** A bounded probe mutated the managed module inside the launch callback after inventory, symlink, digest, and admission checks. `spawn_task_scope` was still reached (`2/2` attack probes). No immutable capture or launch-time revalidation exists.
- **FAIL — incomplete collision guard.** `astrid` collision is rejected, but a top-level `runtime_protocol` package is not checked by `_verify_managed_pack_source`; the probe reached acceptance.
- **UNQUALIFIED — actual external positive.** Candidate tests only inspect captured argv/env. `-I` ignores the supplied `PYTHONPATH`, confirmed directly, so actual external-module loading is not proven.
- **UNQUALIFIED — Runtime provenance.** The host stores caller/CLI `source_inventory_identity` and compares it to locally re-read inventory; no independent authenticated Runtime-held capture provenance is established.
- Descendant module symlink, forged roots/digests, foreign admission, and installed `-I` argv controls passed. Parent-component symlink coverage remains incomplete.

Tests:

- Focused installed-root tests: **7 passed**.
- Neighbor security controls: **7 passed**.
- Source/inventory controls: **97 passed, 2 environment errors** (`runtime_protocol` unavailable under isolated helper).
- Qualified service `child-current-installed-proof-2250`: **3 passed, 3 setup errors** on D09 Remotion/profile guard; actual positive remains unqualified. Tuple verified: Agent `c36ca8c…`, Runtime `abd47e…`, child `c886…`.
- Ruff: **101 errors**, matching recorded parent baseline.
- Mypy: **140 errors vs parent 139**; one new test diagnostic at `test_installed_external_pack_roots.py:144`.
- Vendor lock: pass. Artifact manifest: pass. `git diff --check`: pass.
- Origins verified: Agent from this worktree; `runtime_protocol` from `rt-pin-8ea0766f`; `astrid_runtime_client` from this worktree.

No full suite was run. No merge or clean port is recommended until the TOCTOU, collision, provenance, and real installed-positive gaps are resolved and re-reviewed. `DONE` and the required commit message were created.