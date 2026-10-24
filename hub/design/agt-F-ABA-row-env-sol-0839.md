Completed F-ABA-row-env. Changed only the staged candidate and request explanation.

- Preflight and pytest now share one qualified environment; `"$@"` forwards the service’s exact selector.
- Added `--noprofile --norc` after the synthetic control exposed Bash prepending Nix paths.
- Preserved all 23 preflight assertions, source/Runtime/composition hashes, and 59 original body assertions.

Validation commands:

```bash
python3 -I -c 'from pathlib import Path; p=Path("tests/suites.conf.candidate.request.md"); exec(compile(p.read_text().split("```python\n",1)[1].split("```",1)[0],str(p),"exec"))'
git diff --check
```

Both exited **0**. Controls prove the old row loses the environment, the repaired row preserves every assignment in both commands, the selector round-trips, and preflight failure prevents pytest execution.

No actual preflight, original test, Runtime, realm, child, bench or full-suite execution occurred. The live registry remains unchanged.

Commit message and `DONE` marker written. Next: independent read-only review PASS, then manager installation and the authorized exact-selector service run.