## Result: FAIL for current-integration freeze readiness

The exact-795 U1c draft itself remains PASS, but it is not integrated.

- Draft: `40427e8b5d658ecc0eb117d576b2a4e9de6c6d59`
- Tree: `34ca7af13426512ab6ce3584a65582e393fe8675`
- Parents: reviewed `0138e3af...`, upstream `795379a67...`
- `795379a67...` is an ancestor: PASS.
- Current integration `1d9ddba...` is not descended from the draft; merge-base is `abd47e68...`.

Candidate delta remains exactly:

- `runtime_protocol/service.py`
- `tests/test_managed_output_export.py`

Protected evidence for the draft:

- 69 protected blobs: byte-identical versus reviewed `0138e3af...` and integration base `abd47e68...`.
- Schema digest: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`
- Producer digest: `sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572`
- Current integration has five protected-path changes from D39/R0 and producer digest `sha256:6eb9b835...`; schema digest is unchanged.

Remaining merge seams:

1. Current integration reverts U1c’s default `~/Downloads/Astrid exports` behavior to “export root is not configured.” Reapply `_ensure_export_root` and the associated test while preserving current integration behavior.
2. Readiness changes also touch `service.py`, but in the separate timeline-history hunk (`_read_history`); preserve that change.
3. D39/R0 contract and generated-client changes must remain; do not wholesale restore the draft’s protected blobs.
4. D40 source admission, headless, and occupancy changes are disjoint from the U1c hunks, but require current-integration qualification after reapplication.

Mounted caller verified: `runtime_protocol/server.py:990-992` routes authenticated export POSTs to `RuntimeService.export_managed_output`; the draft calls `_ensure_export_root` and `_materialize_export`. C0 v2 request/reply fields and guards remain unchanged.

Evidence reused from exact 0056 source bytes:

- Targeted pytest: 224 passed.
- Ruff: 78 baseline diagnostics, 0 new.
- Pyright: 375 baseline/current diagnostics, 0 new.
- Compilation and candidate `git diff --check`: passed.

Recheck-only commands run:

- `git merge-base --is-ancestor ...`: passed.
- In-memory compilation of both candidate files: passed.
- Worktree status: clean.
- No full, integration, browser, or gate suite run.

No product files were modified. External live-tip freshness is not claimed; this report targets exact upstream `795379a67...`.