## Report

Completed finite R2 safe handback. No product/source changes; worktree is clean.

- Evidence: [per-id-summary.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-restore-safe-export-0550/evidence/per-id-summary.md)
- Inventory: [byteexact-inventory.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-restore-safe-export-0550/evidence/byteexact-inventory.tsv)
- Provenance: [source-provenance.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-restore-safe-export-0550/evidence/source-provenance.txt)

Results preserved:

- Old-RED `31475`: 1 failed, 3 passed, 1 setup error.
- Candidate `30269`: 4 passed, 1 setup error.
- Historical setup error remains `CommandError` at `_doc_patch.py:300`, wrapped by `DocumentPatchError` at `emitter.py:304`.
- Whole proof remains blocked; candidate PASS does not establish full GREEN.

Verification:

- `cmp` of exported IDs against originals: PASS.
- SHA-256 inventory verification: PASS.
- Raw XML/log/command exports present: none.
- `git status --short --branch`: clean.
- No tests rerun; this was read-only evidence export.

Commit message written; empty `DONE` marker created.