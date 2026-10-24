Completed the R1-D41 candidate backport on exact `079580ca46af77e0292d49dc34386b25c8391f99`.

- Applied only the 18-line intermediate-root retention hunk from `4f6c85ddc6`; no semantic changes to that hunk.
- Added its 18-case regression test byte-for-byte unchanged.
- SHA-256 inventories confirm all **3,418 protected tracked files** remain unchanged, including clients, schemas, types, lockfiles and existing tests.
- Retained the full source comparison for independent review. Unrelated repair-tip inverse/history changes were excluded.

Validation:

| Check | Original079 | Backport |
|---|---:|---:|
| New regression cases | 14 passed, 4 failed | **18 passed** |
| Exact App donor through production `RuntimeCommitService.commit()` | Accepted passes; merge fails `binding_changed` | **Both pass** |
| Requested five-file lane | 151 passed, 20 failed | 155 passed, 16 failed |

All 16 remaining failures reproduce on original079 with `nested inverse ranges differ from accepted history`; no new failures. Scoped Ruff, qualified mypy for both changed files, and `git diff --check` pass.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-popup-079-backport-sol-0943/evidence/validation-commands.txt) and [qualification/hash details](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-popup-079-backport-sol-0943/evidence/qualification.json) are retained with raw logs, XML and donor packets, totaling approximately 3.2 MB.

The donor harness preserves the exact request; its historical detached port defaults omitted rationale to null and spells merged acceptance `rebased`. Receipts/history remain test doubles. No Runtime service, browser, full-suite or gate qualification was performed.

No pin, App, integration or git writes. Commit message and `DONE` are ready for the harness. Next: independent review and source qualification before normal App adoption.