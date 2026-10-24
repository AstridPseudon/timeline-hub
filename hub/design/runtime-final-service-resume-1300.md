Completed validation without changing source. Branch `tl/rt-F-final-service-resume-sol-1300` retains WIP `15f78c995bcd75dcf68f7c1d24393fe59d320c49` from `tl/rt-F-final-service-sol-1244`.

All three candidate commands resolve after worktree recycling. Controlled execution reproduced the original relative-path failure and passed all three absolute launchers from an unrelated cwd after renaming my simulated worktree.

Durable directory, unchanged:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-final-service-sol-1244`

| Artifact | SHA256 |
|---|---|
| `install-final-services.py` | `4164eaa4bc963f6e1d4b23d28684f50e8e5ac402f378af29722433ffc646f16f` |
| `run-final-services.py` | `3ff01eabcd30b60664f29302f28d1d6505c80ee922de56b1f0caeccc83441837` |
| `runtime-final-service-rows.txt` | `ede1bc59bdc999a23cacf27befd264935fa17108f38c3d0e99bbef68466fb070` |

Validation commands, with `O` denoting the absolute ORCH directory above `workers` and `A=$O/workers/rt-F-final-service-sol-1244`:

- `PYTHONDONTWRITEBYTECODE=1 python3 "$TMPDIR/check-final-services.py"` — **22 passed**, recovered from retained author commands. Covers tuple/source drift, synthetic snapshot compatibility, real import origins, environment propagation, TMPDIR cleanup/sentinels, exit handling, registry guards, inventory, Python compilation and shell syntax.
- `PYTHONDONTWRITEBYTECODE=1 python3 "$A/install-final-services.py" --registry "$O/tests/suites.conf" --candidate "$A/runtime-final-service-rows.txt" --builder "$O/bin/delivery-build"` — **PASS**, without final tuple or installation.
- `git diff --check` and `git diff 1e1f32dd0 --check` — **PASS**.
- Byte/hash comparisons — committed source, current source and retained artifacts match. Builder remains `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`; registry unchanged.

No additional design decision or source fix was needed. The 77 timeline files, four support files and TypeScript command remain preserved; product tests and TypeScript checking were not executed. No live installation, core/gate/full suite, build or ZIP ran.

Final tuple remains pending data. Next: independent custody review of this exact candidate, then tuple binding when available. Commit message and `DONE` written.