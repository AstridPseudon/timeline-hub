# agt-G3-normal-commit-frontdoor-1548

Implemented the normal `timelines commit` CLI frontdoor in the Agent worktree. It routes detached documents through the existing authenticated public TimelineSession/G2 commit path and G3 document emitter, preserving exact base revision/publication scope, full Runtime v2 request/receipt data, dry-run behavior, structured refusal errors, and durable-history idempotent retries.

Verification: six focused document-commit tests passed; new implementation/test Ruff passed; `cli_native.py` private mypy passed; parser census found 34 commands including `commit`; `git diff --check` passed. Full touched-file Ruff and parser-inclusive mypy retain pre-existing baseline findings documented in the worker report. No full suite was run.
