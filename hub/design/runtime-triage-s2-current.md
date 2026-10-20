# Runtime M2 S2 current triage gate

## Result

APPROVED four-file triage `9abc5c65de784d8d04bc5af2284fbc365ca625fa` was ported onto final published current `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, preserving current S2 storage estimation and seam behavior. Final central snapshot tree: `7c6c5fbace46dc447e2b65fa7f7bde31c25675c8`.

The port changes exactly these four repository files:

- `runtime_protocol/store.py`
- `tests/test_render_historical_admission.py`
- `tests/test_spec_reference.py`
- `tests/test_timeline_pack_inputs.py`

The Runtime change is narrow: a historical replay with an earlier Runtime render admission converts only the exact retained snapshot-object `NotFoundError` (`timeline snapshot reference object is missing or corrupt`) into the established `ConflictError` with `reason=render_revision_integrity` and the Runtime-built snapshot digest. The later replay check is likewise narrowed so unrelated `ConflictError`/`NotFoundError` causes retain their original refusal.

The three fixture changes retain real behavior coverage: Agent provider startup registration and acceptance-boundary parent seeding; archive state setup without the retired archive API; real Agent projection plus isolated retained-row corruption; and a real media import adapter through Runtime ingestion. The current actual Agent host additionally requires `project_id` and `timeline_id` in capture authority, so those two identity fields were added to the visualize fixture after the first final-tree marked run exposed `verified source project_id differs from admitted authority`. No Runtime policy, Agent source, xfail, skip, overlay, receipt fabrication, or behavior-to-denial change was made.

The renamed `test_real_retained_legacy_publication_uses_verified_source` remains positive retained-publication coverage, but its acceptance fixture is not evidence that the retired legacy publication branch still runs.

## Source inventory and preservation check

- Current base: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Approved source: `9abc5c65de784d8d04bc5af2284fbc365ca625fa` / tree `0c4887d04467f1b269570255d80283fed9667967`.
- Final service snapshot: tree `7c6c5fbace46dc447e2b65fa7f7bde31c25675c8`.
- Worktree diff: 4 files, 84 insertions, 27 deletions. The one extra insertion over the approved 83/27 candidate diff is the two-field actual-Agent capture-authority compatibility repair described above.
- Comparing the final `store.py` to the approved source shows only the current S2 storage safety-factor/materialization estimate and seam diagnostic comment; those current changes were intentionally retained.
- No xfail/skip/skipif markers were added to the four files.

## Commands and evidence

Direct ordinary lane:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m 'not integration' tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py
```

Final result: **76 passed, 59 deselected in 47.07s**.

Central service final-tree requests:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_render_historical_admission.py tests/test_spec_reference.py tests/test_timeline_pack_inputs.py tests/test_canonical_render_admission.py
```

Final result: **59 passed in 50.94s**, result `rt-m2-triage-s2-current-gate-marked-integration-1020114812-13890`.

```sh
/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_canonical_render_admission.py tests/test_snapshot_authority_refusal.py tests/test_snapshot_preflight.py
```

Final result: **115 passed in 85.23s**, result `rt-m2-triage-s2-current-gate-targeted-1020114812-20872`. The review described this lane as 113 tests; the current composed tree collected 115.

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py
```

Final result: **9 passed in 10.93s**, result `rt-m2-triage-s2-current-gate-commit-integration-1020114812-4850`.

Cheap checks:

```sh
git diff --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python - <<'PY'
import ast
from pathlib import Path
for name in ('runtime_protocol/store.py', 'tests/test_render_historical_admission.py', 'tests/test_spec_reference.py', 'tests/test_timeline_pack_inputs.py'):
    ast.parse(Path(name).read_text(), filename=name)
print('4 files parse')
PY
```

Both passed. No full, broad, browser, live-socket, or default suite without `--files` was run.

## Limits and next step

The central integration commands used the actual shared Agent checkout `/home/user/work/agent`, as requested. No merge, publish, pin, activation/custody fix, keyed-view client change, or other repository was touched. The orchestrator may now review and merge this worker branch through the normal queue.
