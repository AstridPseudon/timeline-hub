## D52 report

PASS. Read-only qualification completed on actual Agent home:

- Agent: `cba425b619` / tree `d19ce2e55c`
- Runtime: `becfe6db88b2` / tree `7edc08e3fe`
- Both worktrees clean.
- Protected native ASTs match `aff339`; structure migration retains approved canonical v2 fields.
- Census reconstruction matches lock exactly: 108 current labels, 109 historical labels, 114 executor IDs; `music.duck` retained with all prior IDs.
- Production caller confirmed: `duck_timeline → client.invoke_result("music.duck", ...)`.

Exact twelve-selector command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
-p no:cacheprovider --timeout=45 --tb=short [12 exact selectors] \
--junitxml=/tmp/.../evidence/twelve.xml
```

Result: **12 passed in 60.20s**, 0 failures/errors/skips. JUnit evidence: [twelve.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-native-census-home-1242/evidence/twelve.xml).

Additional checks passed:

- `vendor_lock.py check ... --producer /home/user/work/runtime`: 15/15 mappings
- `artifact_manifest.py --check`
- Ruff on four native files
- Qualified mypy on four native files
- `git diff --check`

No source, test, generated lock, pin, environment, or package edits. No full/gate/ABA/child suite was run; this is not a full-suite claim.

Commit message and `DONE` marker created.