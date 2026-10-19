# Models (owner rule, 2026-10-19). This applies to the orchestrator, area leads, managers and workers.

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
