# F-D22 installed identity review — 1647

## Final disposition

Independent readonly source review **PASS** for the partial fixture handback;
actual installed Remotion qualification **FAIL / not qualified**. The author
added the two authentic rendering carriers and preserved the original test
body and production guards. The non-Remotion neighbor pass is not evidence that
the actual Remotion environment is qualified.

The prior central D22 run remains authoritative: **108 passed, 1 failed**.
The failed selector was
`tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`.
Its retained trace reaches `_registry_origin` through `_registry_probe` and
reports `installed registry launch source binding is unavailable`. I did not
rerun that known failed body.

## Source and custody review

Only `tests/sdk/test_host_bootstrap_source_identity.py` changed in the author
commit. `_materialize_source_closure()` now copies the current checkout’s
authentic:

- `astrid/core/rendering/remotion_runtime.py`
- `astrid/core/rendering/_effect_registry.py`

The selected original test is AST-identical to its parent:

```text
AST SHA-256  8c72537c41c2bcb2b20c33439277a0844a22fcd77eab0c2e4d0b6d4a1245df20
body SHA-256 cc255d621ebcb0706dd124f52374f1eb9704892e0c2c68b3fda9bc732549728f
```

All four original assertions remain: three launches, `-I -m`, no
`PYTHONPATH`, and a cwd different from the temporary source. Parent/current
production guard hashes are equal:

```text
host_bootstrap.py       50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07
remotion_runtime.py     84a495de2139c74b22c001094a3bb4d9252803f11715d7803054ecc2f9cc617e
_registry_origin.py      47af6b12421f44d943a2c00621fc2b08a3d0f2d29fbd66b3c150a328bed88ca2
```

The source explains the remaining limit: the fixture carriers are present, but
the installed `-I` preflight requires the selected distribution’s package
search locations. The temporary fixture source root and the installed child
package root differ, so the existing guard rejects the binding. No guard waiver,
environment stripping, copied fake identity, or product repair is suggested.

## Commands and results

Bounded targeted execution, with Remotion disabled, using the historical
execution checkout `/home/user/work/wt/rt-pin-9ce4242b`:

```text
9 passed in 1.57s
```

This is the repaired selector plus four positive neighbors and five strict
missing/foreign/alias controls. The known Remotion-enabled failure was not
replayed.

Quality checks:

```text
env PY=/home/user/work/venv-agent/bin/python make ruff
Ruff findings: current=2149 baseline=2149

/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
Mypy findings: current=1912 baseline=1912

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
ok runtime.lock.json (matches producer manifest)

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current

git diff --check
pass
```

The author’s earlier Mypy attempt used the wrong `venv-agent` and was
environment-blocked; the required `venv-agent-typecheck-v2` check passed at
1912. `34eac004` is the official vendor producer; `9ce4242b` is the separate
execution checkout used for the bounded historical test recipe.

No full/109/113 suite, provisioning, lock/pin/generated-file change, guard
change, test weakening, or body replay was performed.

Worker report: `/home/user/work/wt/agt-F-D22-installed-identity-review-1647/report.md`.
