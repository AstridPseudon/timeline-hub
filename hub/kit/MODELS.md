# Models (owner rule, 2026-10-19). This applies to the orchestrator, area leads, managers and workers.

**Owner rule 2026-10-20, rev 2 (overrides the table below for workers):** effort is **high** everywhere. Nobody uses xhigh; it over-optimises and drives test bloat. Workers use `gpt-5.6-luna --effort high`. Sol (`gpt-6.1-sol --effort high`) is only for genuinely hard tasks (cross-repo contracts, undo/rebase semantics, a failure Luna already missed), and the brief must carry a first-lines `HARD: <reason>` line. bin/dispatch turns xhigh into high, turns Sol without a HARD: line into Luna, and logs both in $ORCH/model-downgrades.log. Reviews, test-only work, merge-forward and docs always use Luna. Managers and the 3-hourly audit (coordination, not code) stay on Sol high.

Prefer Codex models. Fall back to Claude models only when the Codex one is unavailable: login missing, rate-limited, or erroring repeatedly.

| Role | Codex (preferred) | Claude fallback |
|---|---|---|
| Managers and hard reasoning work | gpt-6.1-sol, effort high | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Normal workers | gpt-5.6-luna, effort high (xhigh only for hard tasks) | Haiku 5.5 (`claude-haiku-5-5`) |
| Second opinions and design reviews | gpt-6-astra, effort high | Opus 5.5 (`claude-opus-5-5`) |

How to fall back:
- A worker or manager run by the dispatcher: pass `--model claude-haiku-5-5` (or `claude-sonnet-5-5`) to `bin/request`. The dispatcher then runs `claude -p --model <m> --permission-mode acceptEdits` in the same worktree, with the same brief, COMMON.md rules and commit-msg mechanics, instead of `codex exec`. If that path isn't wired on a machine yet, the area lead runs the brief with the Claude Agent tool (model sonnet or haiku) in that worktree.
- Record every fallback in STATUS.md, with the reason. Switch back to Codex as soon as it works again.
- The Codex login is per machine. The owner signs each machine in. Credentials are never copied between machines by tools.
- Machine-wide switch (added 2026-10-20, after Codex hit its usage limit): create `$ORCH/CODEX_UNAVAILABLE` on a machine. bin/dispatch and bin/run-manager then map every gpt-* model automatically: Sol to claude-sonnet-5-5, Astra to claude-opus-5-5, everything else to claude-haiku-5-5. Restart the manager with `bin/run-manager <area> claude-sonnet-5-5`. Delete the file when Codex works again.
- The Claude CLI on these machines has no sandbox (bwrap is missing), so bin/claude-perms.sh gives claude -p a fixed allow list (the request and test tools, the venv pythons, node/npm/npx test commands, git, basic shell tools) and hard denies (git push/commit/reset/checkout/merge/rebase, rm, and Codex credentials).
- While on Claude, cap each area at 5 workers, because Claude usage is shared with the orchestrator and leads.
