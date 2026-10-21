# Gate 6 staging budget handoff

For the retained App909 source, the test-service recipe (`git commit-tree` → `git worktree add` → resolved `node_modules` symlink) produces a measured next-snapshot peak of **314,671,104 allocated bytes** (**300,535,487 apparent bytes**). The exact safe free-space budget before staging is:

```text
10,737,418,240 bytes (10 GiB floor)
+ 314,671,104 bytes (measured staging peak)
= 11,052,089,344 bytes free before staging
```

The snapshot excludes ignored `dist/` and private `node_modules/`; `node_modules` is a 32-byte symlink with zero allocated blocks. The direct duplicate is the tracked App checkout, dominated by tracked `public/` media (225,226,752 allocated bytes). The retained App root's full `dist/` (285,278,208 allocated) and `node_modules/` (555,896,832 allocated) are baseline kept payloads, not duplicated by the service snapshot, and neither is safe to release for this frozen Gate 6 tuple.

The central failure-time `bavail` was not emitted and remains unknown. No retry or cleanup was performed.
