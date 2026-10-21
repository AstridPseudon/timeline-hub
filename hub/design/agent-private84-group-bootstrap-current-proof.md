# Agent private84 group bootstrap current proof

Date: 2026-10-21 UTC

## Result

The trusted group bootstrap fixture gap is closed for the exact private pair:

- Agent `4d4535882f1e028805c3da178bf9a7fa53696da8`, tree
  `f18245ced9c231ddf8f6f2ee64405a84d3517921`, schema
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
- Runtime `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`, tree
  `f3ae49d38454ce73a9c91a954bb530b3ce51c122`.

The Agent test-only lane is `tests/sdk/test_timeline_group_migration_runtime.py`.
It uses Runtime c3 for the in-process service and the existing Runtime private
trusted-persistence helper at `54db299d6ebb9ec98649895760a4cd37cee6c147`.
That helper records explicit `command.created: []` before request hashing and
uses whole-closure `timeline` RootPins, so it does not manufacture accepted
history, alter Agent reservations, or write SQL. The helper is loaded through
the existing immutable checkout locator and is used only in each test's own
temporary realm.

The original golden and opaque migration positives now pass through actual
Runtime storage acceptance and the Agent canonical provider: accepted
migration, retained source/document pins, canonical reload, source-v2 update,
restart, exact inverse, same-ID redo, and integrity all pass. The test also
keeps the rational-fps public-seed refusal and detached transcript refusal.
The two schema checks use the existing in-process `plan_for()` output because
this current Agent source does not carry the historical generated JSON
fixture; no fixture or generated artifact was added.

## Evidence

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-c3d26567 \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration \
--basetemp=/tmp/agt-m2-private84-group-bootstrap-current-proof-pytest4 \
tests/sdk/test_timeline_group_migration_runtime.py
```

Result: **9 passed** in 4.81s.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
--basetemp=/tmp/agt-m2-private84-group-bootstrap-current-proof-pure2 \
tests/editing_conformance/test_current_group_slice.py \
tests/editing_conformance/test_group_read_view.py \
tests/editing_conformance/test_recipe_m2_group_migration.py \
tests/editing_conformance/test_recipe_m2_group_move.py \
tests/sdk/test_timeline_materialization_schema_union.py
```

Result: **107 passed** in 9.40s.

`ruff check tests/sdk/test_timeline_group_migration_runtime.py` and
`git diff --check` both pass. No full suite, HTTP, browser, native, render,
pin adoption, schema generation, or release qualification was run or claimed.

## Boundary preserved

No Agent product/provider code, public API, schema, pin, created-ID
reservation, SQL, acceptance override, or history rewrite changed. The old
raw-parent helper shape and its `value.occurrences` mismatch were not
normalized in Agent; the corrected existing Runtime helper supplies the
trusted setup boundary. Ordinary segment transcript data remains present and
bound before the legacy parent setup. The rational `30000/1001` parent is
retained, and opaque/null/order assertions remain live.

Next step is coordinated private readiness/native work only after the normal
private pin/readiness gate; this handoff is not evidence for HTTP/native or
App qualification.
