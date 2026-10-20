# App machine disk: proposed durable fix (follows app-20261020T0448Z-lead-disk-steady-state)
Opus second-opinion findings (read-only, verified):
- 70% of each App worktree is dead weight for most workers: public/ is 215 MB, of which ~203 MB is 28 tracked media files over 1 MB (mostly .mp4, e.g. a 43 MB hero background). Only Home-page components use them; no test reads them.
- Review does NOT need the worktree: for recycled app-m2-edge-current-qualify, `git -C /home/user/work/app log -1 tl/app-m2-edge-current-qualify` and `git -C /home/user/work/app diff tl/<w>~1..tl/<w>` (85 files) still work from the main repo. Diffs between commits never touch .git writes, so this works from the manager's read-only sandbox.
- Not usable: reflinks (ext4 refuses them); hardlinks between writable worktrees; worktree-local caches (none present).
Recommended decision, ranked:
1. RECYCLE ON FINISH: when a worker exits with a clean tree and its commit is on tl/<w>, the lead removes the worktree right away (branch and report kept; never --force; never KEEP, leased, ACTIVE or queued/running-test targets). The manager reviews and merges by branch (`git -C /home/user/work/app diff <base_sha>..tl/<w>`, `bin/merge` already merges by branch) instead of `git -C wt/<w> diff`. This needs: manager agreement, and the orchestrator (MANAGER-COMMON) to stop assuming wt/<w> exists after a worker finishes. Effect: finished worktrees go from ~18 GB to ~0.
2. Optional, needs the owner of the reigh-app repo config: sparse checkout without public/**/*.mp4 for non-UI, non-e2e workers (~300 MB -> ~95 MB). This turns on extensions.worktreeConfig in the shared repo config, a one-time change.
3. Optional: recycle the 8 finished cross-repo agent/runtime worktrees (~0.9 GB) unless they are leased.
Meanwhile: the lead only recycles listed and merged workers.
