Implemented F-D86 in [_commit_patch.py](/home/user/work/wt/agt-R1-asset-guard-sol-0317/astrid/sdk/timeline/_commit_patch.py:106).

- Asset collections now project to `registry.assets`, captured as an exact C0 field dependency. Missing containers retain their tagged absence.
- Native captures, selection/order guards, ABA scanning, atomic fallback and all protected tests remain unchanged.
- AST conservation and in-memory compilation passed.
- Scoped Ruff and mypy passed on parent and candidate with identical diagnostics; `git diff --check` passed. [Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-asset-guard-sol-0317/evidence/verification-commands.txt).

No behavioral tests or services ran, as required. The six outcomes remain unverified. No blockers or contract changes were needed.

Commit message and `DONE` written. Next: independent protected core review, then exact MAIN proof before normal merge.