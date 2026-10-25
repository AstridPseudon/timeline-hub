## Report — F-final D94a

Updated private evidence candidate only:

- Accepts complete shallow existing clones.
- Reports exact missing tip/tree/blob object IDs for lead-owned fetches.
- Preserves receipt, identity, cleanliness, approved-root, gate, and no-acquisition guards.
- Expanded synthetic controls for shallow-valid, missing-tip/blob, stale, dirty, and wrong-root cases.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-worktree-receipt-return-0358/evidence/candidate/`

Hashes:

```text
9a0bea08e932e9a0f0e6f6c48e8e1f800a92c1af949bb6d46b10b74d9c04d6a8  run-final-delivery.py
2f22d994f18c78699f6e1c706cab10ed404caeecb7b7f36dca2031428c912037  source_view_controls.py
179765fbbece51925cd9db62babfc027523f092532c952c1e4c0cb1eb0fef5da  source-acquisition-checklist.md
```

Tests passed:

- AST parsing
- `python3 -m py_compile`
- Private receipt controls
- `ruff check`
- `bash -n scripts/check-before-push`
- `git diff --check`

No fetch, clone, Git write, install, build, rehearsal, or full suite was run. Runtime worktree remains clean. `commit-msg` and empty `DONE` marker are present.