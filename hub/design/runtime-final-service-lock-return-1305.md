Completed on `tl/rt-F-final-service-lock-return-sol-1305`, based on `15f78c995bcd75dcf68f7c1d24393fe59d320c49`.

The runner now validates Agent’s actual lock, exact Runtime producer SHA, all 15 canonical mappings, and normal vendor checks before and after execution. The installer rejects symlink candidates and any candidate-byte changes, including trailing whitespace. No blanket mode restriction was added.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-6b90659fe0/controls.py` — **15 passed**, including old-RED/new-GREEN lock/map/client/symlink controls, all three durable launchers after simulated recycling, synthetic snapshots, environment propagation, TMPDIR cleanup, and failure propagation.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /home/user/work/agent/scripts/vendor_lock.py check /home/user/work/agent/runtime.lock.json --producer /home/user/work/runtime` — **PASS**.
- Python compilation, shell syntax, `git diff --check`, and unchanged 77+4 test inventory/TypeScript command — **PASS**.
- Retained source bytes exactly match worktree source. The 1244 artifacts and live registry remain unchanged.

Corrected artifacts are retained under this exact directory, replacing the same filenames under predecessor `rt-F-final-service-sol-1244`:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-service-lock-return-sol-1305/
```

| File | SHA256 |
|---|---|
| `install-final-services.py` | `c9b755609221d38748fe6d641a69965ae10b16f3baa352bf64075b82b7b3a1fb` |
| `run-final-services.py` | `2611b13745e5b6ecd1f2f2ba4346743093c5f150cae89384f2024f10fa4a98de` |
| `runtime-final-service-rows.txt` | `23b2cdf81202c70a3aa5f6e6fcbd3dfc3c1afa23e5524284d97e5af7b1be0497` |

Builder hash remains `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`.

Every candidate launcher resolves after simulated recycling. Actual execution remains pending the real D59 tuple. No installation, product suite, build, provider execution, or ZIP ran. Next step: independent delta custody review.

`commit-msg` and empty `DONE` are written; no Git writes performed.