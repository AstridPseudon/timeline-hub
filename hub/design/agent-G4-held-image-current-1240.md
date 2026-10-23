# G4 held-image current-source port and bounded qualification

## Result

Implemented the a3450e08f source/recipe hold-image port on current Agent
d1fa6c133, plus a new bounded current-Runtime qualification fixture. The
source admits literal `clipType: hold` only when the authenticated media kind
is image; video hold remains refused. No Runtime, schema, provider, pin,
contract, App, or shared fixture files changed.

The new fixture owns one `RuntimeService` per test, performs public project and
timeline genesis before provider registration, imports real image media, reads
the exact public selection and verified-media pair, and uses the current Agent
provider through Runtime 9345cb58fe8c54f114d666929e167bbeb5899c6c. It covers
real image ADD and SWAP acceptance, dry-run no-write, canonical equality,
literal/raw/opaque/null/absent fields, exact selection and physical ownership,
retained media, local authenticated inverse restoration, and a Runtime-level
video-hold refusal with unchanged history/database. The full accepted request,
prepared candidate, input/output canonical documents, history, records,
bindings, effects, and module origins are retained at:

- `workers/agt-G4-held-image-current-1240/evidence/current-held-image-add.json`
- `workers/agt-G4-held-image-current-1240/evidence/current-held-image-swap.json`

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-9345cb58 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9345cb58 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py` — **66 passed**.
- Same environment, `tests/editing_conformance/test_occurrence_hold_current_runtime.py` — **4 passed** (image ADD, image SWAP, two video-hold refusal controls).
- Scoped Ruff — **passed**.
- `make PY=/home/user/work/venv-agent/bin/python ruff` — **2149/2149**.
- `TMPDIR=/tmp/agt-G4-held-image-current-1240 MYPY_CACHE_DIR=/tmp/agt-G4-held-image-current-1240/mypy-cache make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **1912/1912**.
- `scripts/artifact_manifest.py --check` — **passed**.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **passed**.
- `git diff --check` — **passed**.

## Classification / handoff

The accepted ADD/SWAP qualification is meaningful current-Runtime evidence.
An exploratory Runtime inverse submission after each accepted edit was
refused with the existing exact 422 `invalid_records` cause:
`inverse stage native writes do not cover its authenticated effect image`.
This was not waived or rewritten as a pass, and no Runtime code was changed;
the test asserts the Agent-owned authenticated local inverse restoration and
the report preserves the Runtime refusal classification. Independent review
is still required before integration completion. No P2/P3 or whole-suite pass
is claimed, and no full suite was run.
