# D118d own9 commands and results

- `git status --short --branch` — PASS; worktree clean on `tl/app-D118d-projection-own9-resume-1630`.
- `sha256sum tests/sdk/test_timeline_capture_projection.py` — PASS; `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436`.
- `git diff --no-ext-diff --quiet d05975c7d6a0ab9eeea2db0f1c6e97ccbe136b6b -- tests/sdk/test_timeline_capture_projection.py` — PASS; empty.
- `git diff --no-ext-diff --quiet d05975c7d6a0ab9eeea2db0f1c6e97ccbe136b6b` — PASS; whole-tree diff empty.
- `git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD` — `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.
- `git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD^{tree}` — `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Runtime pin status — PASS; clean.
- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py` — PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir <private tmp>/mypy --follow-imports=skip tests/sdk/test_timeline_capture_projection.py` — PASS (`Success: no issues found in 1 source file`).
- `PYTHONPYCACHEPREFIX=<private tmp>/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py` — PASS.
- `git diff --check` — PASS.
- Fresh `df -B1 /tmp` immediately before own9 admission — `4,991,860,736` bytes available; mandatory floor `5,000,000,000`; exact shortfall `8,139,264` bytes.
- Exact own9 command — NOTRUN by admission rule. No test body executed, no XML test results, and no first failure/node/frame exist.

The exact nine authorized node IDs are recorded in `facts.json`. No whole-file, family, full, browser, service, or replacement run was attempted. No code or test input was edited.
