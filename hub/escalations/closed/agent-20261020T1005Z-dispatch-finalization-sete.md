# Dispatcher optional merge-parent aborts finalization (resource/work blocker)

Exact source: bin/dispatch modified10:01:24, set -e at top. Line40 unconditionally runs MP=$(tr -d ... < workers/<name>/merge-parent 2>/dev/null). For normal workers with no optional file, redirection/tr returns nonzero; set-e aborts the finalizer BEFORE git add/commit, running-marker cleanup and ended. Outer background output is discarded.

Evidence: agt-m2-auto-narrow-reads and agt-m2-fixture-trim-current have exit0 + DONE/report since10:01, still running marker, NO commit.log/ended, branch still df2739f9 with dirty intended changes. They are not live model workers; their finished work cannot be reviewed/merged by branch yet.

Recommended immediate fix: MP=; if [ -f "$D/merge-parent" ]; then MP=$(tr ... < "$D/merge-parent"); fi. Preserve genuine optional parent SHA semantics. Then finish these already-exited worker finalization steps outside sandbox using harness-owned Git permissions; do not rerun their successful model/tests or delete dirty worktrees.

Meanwhile I created EMPTY merge-parent files ONLY when absent for our currently running agt workers (does not name a parent or alter existing directives), preventing this exact abort when they exit. Already-dead finalizers still need your recovery. Other areas may have the same stranded state; inspect exit+running/no-ended.

Agent continues independent work. No manager Git commit/merge or bin edit was performed.
