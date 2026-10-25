# D139 validation

Result: finite no-eligible-candidate. This worker performed no cleanup, recycle, retirement request, process stop, deletion, source mutation, or test run.

Read-only witnesses:

- `date -u` at capture: `2026-10-25T21:56:57Z`.
- `df -B1 /home/user/work`: `/dev/vda`, available `5310427136` bytes; threshold `5905580032`; deficit `595152896`.
- Bounded `du -sx -B1` found the largest candidate-shaped directories, but no eligible one: bench-store `1620480000`, runtimes `1971752960`, f1012 `1054433280`, d22 `517910528`, venv-agent `675598336`.
- `git -C /home/user/work/{agent,runtime,app,composition} worktree list --porcelain` plus worker metadata found no clean non-KEEP finished worktree available to `bin/recycle`. `agt-G2-open-commit` is the sole non-KEEP finished worktree left in the direct scan; `git status --short` reports `M astrid/sdk/timeline/sync.py`, so the normal recycle guard refuses it. Its head `a086cc6d…` is already an ancestor of `tl/integration`; dirty state remains the binding condition.
- `agt-F-final-source-join-0816` has a KEEP marker and is retained source evidence despite its finished/recycled bookkeeping. All pin worktrees are KEEP-marked. No process cwd or fd referenced either worktree.
- `jq` of `/home/user/work/bench-store/index.json` found exactly two active child entries: `child-3b5cb98c…` (d40 tuple) and `child-3e16336b…` (d137 tuple). Both have retained owner/source/provision metadata. Exact process cwd/fd scans and exact bench lock-fd scans were clear, but that does not override registration, suite, age, or KEEP guards.
- d40 is referenced by `tests/suites.conf:173`; it is not a retirement candidate. d137 was provisioned at `2026-10-25T21:24:50Z` and is registered under the current old tuple; at capture it was about 22 minutes old, so the ordinary one-hour retirement guard is binding. The brief’s “old child 3e16336b superseded” note does not revoke that guard.
- d22 and f1012 were checked at their exact paths with `/proc/*/cwd` and limited `/proc/*/fd` reads; both were clear of process use but remain absolute protected targets and are not recommendations.
- Prior retirement refusal records were read without retry: `agent-remotion-main95bd`, `agent-remotion-published14-091aa23e`, `agent-remotion-0013`, and `venv-agent-child-f1012-installed` each state `target is referenced`; those targets remain STOPPED. No refusal was rerouted or transferred.
- `/tmp/.../queue/pending` and `/tmp/.../queue/running` were empty at capture; no manager lease note named any scanned worktree or bench. The existing sweep/compact result is not duplicated here.

Guard/source hashes are recorded in `audit.json`. No product or repository tests were run because this is an evidence-only operational audit and the brief forbids test/body execution.
