# D116 report

- Evidence fidelity: **PASS**
- Functional result: **FAIL** — retained exact NEW4 run: `3 failed, 1 error in 28.85s`, 0 passes; admission `5,005,950,976` bytes.
- Source custody verified at Agent `795608e1...f522`, Runtime `5e9ad1c...fd344`, clean worktrees, registered provider/module origins intact.
- Three cases fail at `native_word_anchor.py:100` (wrapped at line 381): exact transcript pin refusal. D107 owner remains **UNKNOWN**; missing record remains **EXACTMISSING**.
- Gate3 independently fails during setup at fixture line 90: `parent.occurrences` membership requires semantic commands. No legitimate companion-only correction is established.
- No source edits, retries, pytest, collection, or behavior reruns.

Checks passed:

```text
Python 3.11 py_compile: PASS
Scoped Ruff: PASS
git diff --check: PASS
JSON validation: PASS
Agent/Runtime no-change checks: PASS
```

Safe evidence written under `evidence/`; commit message and empty `DONE` marker created.