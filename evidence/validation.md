# Validation

This is source/dry preparation only. No launcher, preflight control, body,
test, provider, browser, socket, render, package, profile, or service command
was executed.

Read-only source facts used by the candidate:

- `tools/p4-d73-pinned-launch.sh:128` and `:149` export
  `PYTHONNOUSERSITE=1`; `:132` and `:153` export the Remotion project.
- `host_bootstrap.py:1651` calls `_prepare_render_validation`; `:836` calls
  `prepare_remotion_validation`; `:813-814` only takes the no-Remotion return
  when the project variable is absent.
- `remotion_runtime.py:214-216` includes `PYTHONNOUSERSITE` in
  `_UNSUPPORTED_PYTHON_STARTUP`; `:234-236` raises before host launch.
- The launcher preflight checks exact manifest keys, four SHA/tree/clean
  states, parent guards, original P4 test hash, Python/Node/profile/schema
  bindings, module origins, lock and registry hashes, and writes report-all
  evidence before the body. Those guards are unchanged in the candidate.

Commands run after editing:

```text
bash -n evidence/next-core-command.sh                         PASS
python3 -m json.tool evidence/environment-contract.json        PASS
python3 -m json.tool evidence/source-manifest.json             PASS
git diff --check                                               PASS
```

Additional read-only checks:

```text
sha256sum tools/p4-d73-pinned-launch.sh                        PASS: cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1
git -C /home/user/work/wt/agt-pin-a4e016b6 rev-parse HEAD HEAD^{tree} PASS: a4e016b6 / 60d45288
python3 AST-parse of host_bootstrap.py, remotion_runtime.py,
  subprocess_env.py                                             PASS (read-only)
static recipe comparison                                            PASS: 22 roots, -n 3, empty addopts, no cache, timeout 45
static full-body comparison                                        PASS: command/body copied from 1909; only outer PYTHONNOUSERSITE omitted
```

The corrected candidate is not evidence that the current launcher can admit
the environment: the two launcher-owned exports are the exact finite blocker.
An independent review must verify any authorized launcher correction before a
meaningful own-14 or ship-grade/full-core run.
