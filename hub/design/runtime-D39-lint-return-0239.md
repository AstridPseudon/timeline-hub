Restored only six pre-existing `# noqa: E402` import lines to their exact `45c3a7f47` form. No behavior, assertions, contracts, clients, metadata, schemas, or pins changed.

Checks:

- `/home/user/work/venv-agent/bin/ruff check --no-cache scripts/record_responses.py tests/test_client_parity.py` — passed.
- Requested Runtime `python -m ruff check …` — passed with read-only Agent Ruff paths supplied through `PYTHONPATH` and `PYTHONUSERBASE`; Runtime alone lacks Ruff.
- `git diff --check` — passed.
- Python AST comparison against reviewed HEAD — identical, excluding source locations.
- Complete-diff verification — exactly six parent-form import restorations.

Reused independent evidence without rerunning tests: **137 authority/recording passes; 25 declaration/schema passes; 211 passes plus 3 visible freeze deferrals; Pyright 4431 errors/3 warnings, zero new normalized identities.**

Base commit: `9d2fdf1ae794dea05888a3db22df03b22e7b9cfe`  
Final worktree tree: `93b13f978128e1055b4f439a29f6556b07481d5e` (computed without Git writes).

Commit message and `DONE` written. Final commit SHA awaits harness commit. No source blocker; next: independent narrow review, then normal merge.