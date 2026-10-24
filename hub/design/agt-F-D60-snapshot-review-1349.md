## D30 Report — agt-F-D60-snapshot-review-1349

Status: PASS for the new installed source delta. Ready for one meaningful baseline full run.

- Installed row: `agent full-upstream-final-9244377`
- Row SHA256: `29bf758c29248e50e3d588f0f46702577c6e6dab548f29c2d87f667d852e3eb5`
- Outside-row SHA256: `6a047fa39f78f516bb31047c382b63707307bfca12e1a5a4f35091c3824920ba`
- Source: `92443771676ef2bbb547d0a103d708fa8bec4c63`
- Tree: `a81a8c7f262e4416dcdefc0720fd760e026d766b`
- Current `agent full` row SHA256: `41a1ffc60cdb7b6f78b16877984e347a78bcc5d8f954ac5ac6ab9b8cd6ca5f9d`, matching its prior pre/post hash.

Guard cases:

```json
{
  "existing_direct_924": true,
  "legitimate_one_parent_snapshot_924": true,
  "wrong_parent": false,
  "wrong_tree": false,
  "extra_parents": false,
  "dirty_snapshot": false,
  "import_origin_overlay": false
}
```

Checks passed:

- Parsed installed command with `/bin/sh -n`.
- Verified exact 924 history/tree, Runtime `becfe`, Node 20.19.4, profile and module-origin guards remain present.
- Verified absolute JUnit argument targets author-owned `agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml`.
- Evidence directory exists and is writable; XML is absent as expected before the actual body.
- No pytest body, service request, full suite, source mutation, or registry mutation was performed.
- Worktree is clean.

Caveat: author evidence records `10d8…` for “current full row”; that hash belongs to the distinct `full-current-v3-1229` row. The actual `agent full` row is `41a1…`, independently confirmed unchanged.

Created required `commit-msg` and `DONE` markers.