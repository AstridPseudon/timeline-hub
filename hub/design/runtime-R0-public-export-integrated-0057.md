# PASS — R0 integrated qualification

- Integrated HEAD: `458595850c354f4403dabc58a72b98bebbc2c3a3`
- Tree: `703b1aac733ad3c977399e67cd4e23d6ae85e7bb`
- Clean before/after; tree equals reviewed `cf74f3e…`.
- `cf74f3e…` is an ancestor. Both reviewed blobs match exactly:
  - generator: `0a6c7cc7…`
  - package `__init__.py`: `9b4dc2a3…`
- Integrated diff contains exactly those two files.

Checks:

- Targeted pytest command: `144 passed in 16.25s`
- Full-v2 `WorkspaceClient` wire probe: `7 passed, 68 deselected`
- `generate.py --check`: passed
- Ruff: passed
- In-memory compilation: passed
- `git diff --check`: passed
- Root `DocPatchArgs`: exact DTO identity, constructible, listed in `__all__`.
- Generated outputs: only allowed package `__init__.py` changed.
- Schema digest unchanged: `sha256:35c2d9c5…`
- Producer metadata unchanged: `astrid-runtime`, version `sha256:d5f98db3…`
- Reviewed Pyright comparison reused: six existing diagnostics, zero changes.

Imported source origins resolved to this worktree; key hashes: generated client `9b5686c3…`, DTO `88c67d9e…`, Runtime commit modules recorded and unchanged.

No full suite, browser journey, or P1 claim made. No tracked edits or commit created.