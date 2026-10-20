Wrote [suffix-basis.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/suffix-basis.md) and [isolated specification tests](/home/user/work/wt/agt-m0-suffix-basis/tests/m0_suffix/test_suffix_basis.py).

Proposed `base_view: "original-result"` plus retained original-request context. The executable ABA counterexample shows why unchanged guards and a relabeled accepted base are insufficient.

Validation:

- `python3 -B -m unittest discover -s tests/m0_suffix -v` — **14 passed**.
- `PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/m0_suffix` — **14 passed**.
- `/home/user/work/venv-agent/bin/ruff check --isolated tests/m0_suffix` — passed.
- `git diff --check` — passed.

These are specification experiments using the real R4 `EditCommand` structure, not production proof. Full product gates were not run. No blockers or product-code changes; temporary output was removed and the commit message written.

Next: managers reconcile the field and retention requirements, then prove the cases through the real recorder, Runtime persistence and App restart journey.