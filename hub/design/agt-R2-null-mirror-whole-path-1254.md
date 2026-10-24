## Report

Investigated current cumulative join `e5fa8aac0e` read-only. The named join worktree was absent, so files were inspected via `git show`.

Finding: genuine Agent source bug in `astrid/sdk/timeline/_commit_patch.py`.

Path:

`test_remove_last_clip...` → `recorded_removal` → production `clip.delete` → `commands.execute` → `CommitPatch.finish` → `effect_diff` → `logical_parent`.

Both failures occur before accepted history:

- `null-payload`
- `null-config`

`logical_parent` rejects a list/null mirror pair as contradictory. However, `_verify_document` admits these explicit-null shapes, `State` selects the list side as the authoritative collection, and the original positive tests predate the strict guard. List/list and registry contradictions must remain rejected.

Unapplied source hunk for the future Agent source owner:

```diff
             if mirror in config and not equal(present(config[mirror]), present(value)):
-                raise CommandError('contradictory parent mirrors', kind='capture_mismatch',
-                                   ref='parent', path=['config', mirror])
+                other = config[mirror]
+                if mirror != 'clips' or isinstance(other, list) == isinstance(value, list):
+                    raise CommandError('contradictory parent mirrors', kind='capture_mismatch',
+                                       ref='parent', path=['config', mirror])
+                value = other if isinstance(other, list) else value
```

This preserves raw null/absent shape while retaining all other mirror and admission guards.

Evidence:

- Retained M1 run: `124 passed, 2 failed`; exact ten: `10 passed`.
- R2 cohort: `336 passed`; neighbor lane: `203 passed`.
- No tests rerun, no product/test edits, no full/gate/child suite.
- Assigned worktree clean; `git diff --check` passed.
- Join commit: `e5fa8aac0eea52d7e5cedae49cafe81e5c03b810`.
- Join `_commit_patch.py` blob: `620ced06c6bf161b3f58877ec5ca9b0ef5b3cd52`.

Commit message and `DONE` marker written.