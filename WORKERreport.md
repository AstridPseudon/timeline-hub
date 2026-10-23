# P4 current two-HTTP-port source qualification

## Scope

Ported only the two reviewed final test blobs onto the current Agent integration
base. No product, helper, report, fixture, pin, schema, generated, suite, or
launcher files were changed.

- Base / HEAD before edits: `9df06d16de5270c449dea938175123942ad00a8b`
  (`tl/integration`)
- HEAD tree before edits: `39193b28f71e832d85ff01d6eec893ebdff8f1ea`
- Ten-note blob:
  `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`
  `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`
- Conflict-rerun blob:
  `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`
  `cbd332db227ecb9c6254e8ced0af72c3de91821e`

Both files compare byte-for-byte with their reviewed donor blobs. The source
reviews 0621 and 0647 remain PASS; this is source qualification only.

## Checks

Passed:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q -m integration tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
    # 2 tests collected; one environment warning: pytest config option timeout is unknown

    /root/.local/bin/ruff check --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
    # All checks passed

    /root/.local/bin/mypy --config-file pyproject.toml --platform linux --no-incremental --cache-dir <private-temp> tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
    # Success: no issues found in 2 source files

    git diff --check
    # passed

The app2-native venv did not contain Ruff or mypy; the approved host tools were
used with private temporary caches. No HTTP/body/socket/service/browser/full
execution was run, as required by the task.

## Handoff

The manager should verify the eventual harness commit contains exactly these
two paths and these two blob IDs before any remote Agent request. Runtime
execution remains manager-owned after the corrected execution review/proof;
manager owns the two separate original-node observations. No premature merge
claim is made here.
