## Report

**Verdict: PASS — custody review**

- Finalized author branch matches exactly: `ed81088ed8`, tree `a75cebb9`.
- Frozen App/Agent/Runtime tuples, parents, Remotion tree, and clean worktrees all matched.
- Normal venv import origins and versions matched; `PYTHONPATH` was unset and no preload/import loader hook was active.
- Client contract `0.2.14`, schema digest, generated-client hashes, Runtime artifacts, Remotion provenance/package locks, and approved Composition artifact/80-file graph digest all passed.
- Runtime daemon, door, DataProvider, harness, and Agent callable targets were confirmed at the declared paths.
- Historical Remotion commit `079580…` exactly matched current `HEAD:remotion`; package and lock hashes also matched.
- No package installation, overlay, copied environment, service/backend/HTTP/browser/native execution, or Git mutation occurred.
- The recipe reports `qualified_existing_inputs_not_live`; live service identity remains unverified as intended.

Commands passed:

```text
env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python current-service-inputs.py
JSON parse and compile checks
git diff --check
```

Wrong-input negative controls were not run because the recipe exposes no argument interface; extra arguments are ignored and trigger the normal check.

No files were changed in the worktree. Required `commit-msg` and `DONE` markers were created.