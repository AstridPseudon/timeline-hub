## R2 actual-home qualification: PASS

- Reviewed blobs exact:
  - `_root_inverse.py`: `0b4be3a1…`
  - Regression test: `5f2b011b…`
- Agent: `200819d572`, tree `bfa91291…`; clean before/after.
- Runtime: `2c1bf087`, tree `b466ee33…`; includes popup successor `b318a8e`; clean before/after.
- Runtime lock remains `5c1a03f` provenance; expected identity lag, untouched.
- Protected hashes unchanged:
  - source-copy originals: `8a6e7a7c…`
  - inverse fork guard: `83028710…`
- All 15 canonical mappings unchanged.
- Production path confirmed: `apply_inverse` → `restore_root_baselines`.

Test command:

```text
PYTHONPATH=/home/user/work/agent:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=.../home.xml <two original selectors> tests/sdk/test_timeline_inverse_shared_root_baseline.py
```

Result: **10 passed in 22.09s**, no skips/errors.

Evidence retained in `/tmp/.../workers/agt-R2-sourcecopy-home-1715/evidence/`, including XML, log, exit, pre/post identities, origins, and hashes. No P4/full/browser qualification claimed. `DONE` and commit message created.