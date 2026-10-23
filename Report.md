# V1 meta allowlist/container repair

## Result

Completed the interrupted V1 repair from base `25991306f`.

- Admitted canonical `meta` at timeline, clip, and track locations.
- Added the bounded validator for namespace names, object-root values, finite
  JSON descendants, depth, per-namespace bytes, total bytes, and namespace
  count.
- Reused `astrid.core.receipts.canonical.canonical_bytes` for canonical UTF-8
  sizing; did not add SDK `commit.py` metadata validation.
- Preserved opaque values through the existing `Timeline` load/save path by
  removing only the known `meta` fields from the strict shared-render view.
- Kept unknown top-level refusal, `params.meta` behavior, generated schema
  files, Runtime pins, and SDK provider code unchanged.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/timeline/test_timeline_roundtrip_fixture.py tests/sdk/test_timeline_selected_schema.py tests/timeline/test_meta_validator.py`
  — **42 passed, 2 subtests passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/timeline/test_timeline_characterization.py tests/timeline/test_meta_validator.py`
  — **27 passed, 161 subtests passed**.
- Final combined rerun of both lanes plus the selected-schema lane — **64
  passed, 163 subtests passed**.
- Scoped `ruff check` on all six touched source/test paths — **passed**.
- `make ruff PY=/home/user/work/venv-agent/bin/python` — **2151 current,
  2151 baseline; passed**.
- `make mypy PY=/tmp/astrid-u2-typecheck/bin/python` — **1915 current,
  1915 baseline; passed**.
- `git diff --check` — **passed**.

The direct private mypy command on only the four source modules reports eight
existing diagnostics from the shared-schema/timeline baseline; the repository
ratchet is the authoritative check and remained exactly unchanged.

## Review and decisions

The independent V1 copy audit identified the exact parity failure: canonical
top/clip/track `meta` was present in the Runtime-vendored schema but absent
from Agent allowlists. A final repair review checked that the diff is limited
to those allowlists, the local validator, the strict-render projection, and
direct regressions. The characterization test also caught an initial public
`__all__` expansion; those exports were removed so the pinned public surface
remains unchanged.

No full, browser, Runtime, or generated-artifact suite was run; those were out
of scope for this first incoming-copy repair.

## Next step

Run the orchestrator’s independent merge review, then merge this narrow Agent
repair. Broader parent/shot/registry meta placement remains a separate seam and
is intentionally not claimed here.
