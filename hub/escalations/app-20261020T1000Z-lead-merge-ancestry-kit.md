# App lead: two-parent merge for refresh-main needs a kit path (re app-20261020T0956Z)
2026-10-20 10:00 UTC. From: App lead.

Problem: bin/merge-forward can't work from inside a worker. The worker's .git is read-only (it fails with exit 128 on ORIG_HEAD.lock), so a worker can never produce MERGE_HEAD. As a result, the harness commit in bin/dispatch (line 37, `git add -A && git commit -F commit-msg`) makes a single-parent commit. The manager rightly says a single-parent copied tree is not an acceptable upstream merge.

Worker app-m2-refresh-main-current (base 18becfbed) is hand-resolving the merged tree with upstream 44f0b9ca9d0247d909f86f56955a04ef6c18a2aa (fetched; present in the shared object store).

What I tried: writing MERGE_HEAD=44f0b9ca9 (plus MERGE_MSG/MERGE_MODE) into that worker's gitdir, so that dispatch's own final commit records both parents. This machine's permission policy blocked writing shared .git state from the lead, so it was NOT done. Nothing in git was changed.

Proposed kit fix (yours to make; I don't patch bin/):
- bin/dispatch honours an optional `merge_parent=<sha>` line in workers/<w>/meta.
- At the final commit, if it is set, dispatch first writes MERGE_HEAD into `$(git -C $WT rev-parse --git-dir)`, then commits as now. The result is a TRUE merge with parents HEAD and merge_parent, and the worker's reviewed tree.
- Alternatively, bin/merge-forward could run on the dispatcher side before the worker starts, as a `premerge=<ref>` meta.

Interim if you prefer: let the worker finish. Then the lead creates the merge commit with `git commit-tree <worker tree> -p 18becfbed -p 44f0b9ca9` and points tl/app-m2-refresh-main-current at it. That needs your explicit go-ahead, and also an owner permission change on this machine.

Ask: (1) ship the kit change, or approve the interim; (2) confirm that the worker should keep resolving meanwhile, with integration NOT merged until ancestry is verified, as the manager says.
