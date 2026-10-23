# Sourced by bin/dispatch and bin/run-manager for the MODELS.md Claude fallback (claude -p has no sandbox here: bwrap is not installed).
# 2026-10-23T15:30Z OWNER approved (in the orchestrator session) whatever the farm workers need: ln/tar, npm ci/install, npx (Playwright),
# ruff/pyright, venv and runtime binaries, and git checkout (scratch clones). push/commit/reset/merge/rebase/rm and Codex credentials stay denied.
# CLAUDE_PERMS = --allowedTools/--disallowedTools args: the commands a manager or worker needs, plus hard denies (no push/commit/history edits, no rm, no Codex credentials).
# codex_fallback MODEL -> prints the Claude model to use when $O/CODEX_UNAVAILABLE exists (owner rule: Sol->Sonnet, Luna->Haiku, Astra->Opus), else MODEL unchanged.
codex_fallback() { local m=$1; if [ -f $O/CODEX_UNAVAILABLE ]; then case $m in gpt-6.1-sol*|gpt-6-sol*) m=claude-sonnet-5-5;; gpt-6-astra*) m=claude-opus-5-5;; gpt-*) m=claude-haiku-5-5;; esac; fi; echo $m; }
CLAUDE_PERMS=(--allowedTools Read Edit Write Glob Grep
  "Bash($O/bin/request:*)" "Bash($O/bin/request-checkout:*)" "Bash($O/bin/request-child-venv:*)" "Bash($O/bin/request-runtime:*)" "Bash($O/bin/request-retire-venv:*)" "Bash($O/bin/request-test:*)" "Bash($O/bin/wait-test:*)" "Bash($O/bin/request-merge:*)" "Bash($O/bin/request-merge-remote:*)"
  "Bash($O/bin/digest:*)" "Bash($O/bin/workers:*)" "Bash($O/bin/ledger-index:*)" "Bash($O/bin/merge-forward:*)" "Bash($O/bin/rm-own:*)" "Bash(python3:*)"
  "Bash(/home/user/work/venv-agent/bin/python:*)" "Bash(/home/user/work/venv-runtime/bin/python:*)"
  "Bash(npx vitest:*)" "Bash(npx tsc:*)" "Bash(npm test:*)" "Bash(npm run:*)" "Bash(node:*)"
  "Bash(git:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(grep:*)" "Bash(rg:*)" "Bash(head:*)" "Bash(tail:*)" "Bash(wc:*)" "Bash(find:*)"
  "Bash(sed:*)" "Bash(awk:*)" "Bash(diff:*)" "Bash(sort:*)" "Bash(uniq:*)" "Bash(cut:*)" "Bash(date:*)" "Bash(sleep:*)" "Bash(jq:*)"
  "Bash(ln:*)" "Bash(tar:*)" "Bash(npm ci:*)" "Bash(npm install:*)" "Bash(npx:*)" "Bash(ruff:*)" "Bash(pyright:*)"
  "Bash(/home/user/work/venv-:*)" "Bash(/home/user/work/runtimes/:*)"
  "Bash(mkdir:*)" "Bash(cp:*)" "Bash(mv:*)" "Bash(echo:*)" "Bash(test:*)" "Bash(stat:*)" "Bash(du:*)" "Bash(df:*)" "Bash(touch:*)" "Bash(pwd)"
  --disallowedTools "Bash(git push:*)" "Bash(git * push *)" "Bash(git commit:*)" "Bash(git * commit *)"
  "Bash(git reset:*)" "Bash(git * reset *)" "Bash(git merge:*)" "Bash(git * merge *)"
  "Bash(git rebase:*)" "Bash(git * rebase *)" "Bash(git * branch -D *)" "Bash(git * worktree remove *)" "Bash(git * worktree prune*)" "Bash(git * push*)" "Bash(git * commit*)"
  "Bash(rm:*)" "Bash(* .codex*)" "Read(/root/.codex/**)")
