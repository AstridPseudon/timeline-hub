## D52/G4 sourcewholepath review — PASS with limits

Reviewed `tl/agt-F-D52-import-whole-path-1203` at:

- Commit: `d411f439acce0c6bc2fa50f77a7f92c103773d5d`
- Tree: `b8218b65149cba8b16c2895fc3c58078be957539`

Findings:

- The bounded 15 bootstrap cases, 4 retained generic-child cases, and 14 retained rendering cases each trace to missing `runtime_protocol` in the child interpreter. This supports the same cause for these exact 33 retained subsets only.
- The claim does not extend to the remaining unknown/summary-only D52 rows.
- Production callers are real: `ensure_pack_host`/Remotion validation, `GenericPackHost` child launch, and `CommandTransport.run`.
- The actual transport path is `astrid/core/rendering/transport.py:_build_environment()` → `build_child_subprocess_env()`. Installed profiles remove `PYTHONPATH`; source variants admit only selected checkout/dependency roots. No arbitrary Runtime checkout overlay is justified.
- `generic_host.py`, `remotion_runtime.py`, `publication.py`, and `host_bootstrap.py` use Runtime platform/custody APIs. Lazy-import arguments do not excuse the missing Runtime dependency.
- Agent `pyproject.toml` omits `astrid-runtime`. Runtime metadata identifies the separate `astrid-runtime` distribution as owner of `runtime_protocol` and `astrid_runtime`.
- Existing passing installed-child evidence is a different qualified tuple: Agent `ba8f0bc8` + Runtime `f3208b26` in child `3b5c`. It does not qualify the failing D52 `venv-agent` tuple or establish install-fix readiness.
- A metadata-only dependency proposal is architectural guidance only: it can express that independently installed Agent environments require a compatible Runtime distribution, but it does not provision existing child venvs, authorize source substitution, or create a new trust carrier.

Limits remain: the 10:16 schema/child-admission hold; no current environment qualification, installation, acquisition, overlay, subprocess, network, or source execution was performed.

Checks:

- `git status --short --branch` — clean.
- `git diff --check` — pass.
- Source identity matched the target branch.
- No tests/full/gate suite run, per task scope.

Required commit message and `DONE` marker were created.