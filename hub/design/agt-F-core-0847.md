# agt-F-core-0847 handoff

F-core repaired the three exact production boundary failures from base
`e837e18c5156e762eca05e6d9bb15779cf847b60`.

Source delta:

- `astrid/core/rendering/_effect_registry.py`: use the canonical env catalog
  for `ASTRID_REMOTION_PROJECT_DIR` and `ASTRID_NODE_EXECUTABLE`; remove the
  direct Remotion backend import from `main()`.
- `astrid/core/rendering/remotion_runtime.py`: expose the used,
  inherited-lock-aware `remotion_render_lock()` server-owned boundary so the
  installed generator carrier retains the original lock behavior.
- `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py`:
  use `runtime_protocol.platform.current_user()` in the existing ownership
  proof instead of `os.getuid()`.

Exact reproduction before repair: the three named nodes failed (`3 failed in
9.58s`). Exact named group after repair: `3 passed in 10.81s`.

Adjacent targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_remotion_locking.py tests/packs/rendering/test_remotion_attempt_temp.py tests/core/rendering/test_effect_registry_carrier.py
```

Result: `13 passed in 7.61s`.

Quality: `make ruff PY=/home/user/work/venv-agent/bin/python` PASS at
2149/2149; mypy baseline PASS at 1912/1912; vendor lock PASS; artifact
manifest PASS; `git diff --check` PASS. Direct whole-file ruff reports six
pre-existing unrelated findings in `remotion_runtime.py`; no changed line is
reported. No full suite was run or requested.

Limits/owners: this is the single bounded repair slice. The terminal full run
remains broadly red and unqualified outside these exact nodes; environment
provisioning remains with `agt-F-environment-0840`, and independent Luna review
is required before merge. No upstream-preexisting claim, D14/H9 credit, or
full-green claim is made.
