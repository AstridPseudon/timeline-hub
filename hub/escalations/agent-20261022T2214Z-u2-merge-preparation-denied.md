# U2 merge preparation permission denial — Agent
Owner: orchestrator / agent lead infrastructure.
U2 Codex Luna worker agt-U2-upstream is running from tl/integration a086cc6db.
Supported bin/merge-forward agt-U2-upstream 9ec1eae349affda35da8b1dc6b5d37e12627f37e failed before preparing the merge:
fatal: update_ref failed for ref ORIG_HEAD: cannot lock ref ORIG_HEAD: Unable to create /home/user/peteromallet/astrid-agent/.git/worktrees/agt-U2-upstream/ORIG_HEAD.lock: Read-only file system.
Please provide a dispatcher-owned Codex merge-preparation path with rerere, or prepare the merge for this worker outside its read-only Git metadata sandbox under the approved Codex merge mechanics. Manager will not run git merge/commit/rebase/reset or bypass sandbox restrictions. Worker must resolve and validate the actual upstream merge tree before ancestry is recorded.
The harness currently has a merge-parent file from the dispatched request; do not land an ancestry-only merge if the worker exits blocked. Manager will refuse review/merge without resolved-tree proof.
Also noted: hub-sync re-imported archived v1 inbox content at 22:11Z into the new lane inbox. Manager ignores it under v2.1; old ready items were refused without launching.

Update 22:14Z: harness finalized 8a2677cd7 (parents a086cc6db + 9ec1eae34) despite author BLOCKED and no DONE. This is unreviewed and must NOT be merged. Independent Luna review agt-U2-review is queued to record the failure and targeted baseline checks. Recovery must start from tl/integration a086cc6db, not the ancestry-only branch, after approved merge preparation is available.
