Implemented D118 host-bootstrap14:

- Sanitized copied child environments by removing proven forbidden `PYTHONNOUSERSITE`.
- Preserved strict rejection of `NODE_OPTIONS`/`PYTHONHOME`, caller environment, and launch provenance.
- Added three additive environment regression tests.
- Protected source-identity test remains byteexact (SHA256 unchanged).

Validation:

- Additive pytest: `3 passed`
- Ruff: passed
- Mypy: passed
- Pycompile: passed
- `git diff --check`: passed

The protected 14-node selector was not run because no genuine local Remotion profile/environment was available; no substitute was used. Commit message and evidence are written under the assigned worker directory.