**BLOCKED — no product or test changes.**

Runtime `6634a17f` requires `scope,parent,[]` for the captured asset-collection read. Agent `4dcb/b415` emits a registry-assets field dependency, which cannot cover that scope. Adding the scope restores the original disjoint-parent rebase conflict. The independent whole-path investigation confirmed this contradiction.

All six parent cases share this seam. Exact failed capture arrays remain **UNKNOWN**; the two word cases remain out of scope.

Static checks passed:

- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py`
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-b2e8d9f08f/mypy-parent astrid/sdk/timeline/_commit_patch.py`
- The same mypy command with `mypy-candidate`: identical diagnostics.
- AST/input conservation, in-memory compilation, and `git diff --check`.

No behavioral execution occurred. [Source trace and proposed controls](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-parent-read-union-sol-0425/evidence/source-trace.md>) and [exact verification commands](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-parent-read-union-sol-0425/evidence/verification-commands.txt>) are preserved.

Recommend resolving the permitted encoding/seam before another correction, followed by one independent protected review and exact MAIN six proof. Candidate remains held. `commit-msg` and `BLOCKED` written.