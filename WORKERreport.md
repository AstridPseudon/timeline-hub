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

## Independent bounded review (ap2-P4-two-port-service-review-0658)

Result: **PASS for source qualification and the terminal ops-row review.**
This is not a live HTTP/body qualification.

Source identities:

- Resolved current integration base: `9df06d16de5270c449dea938175123942ad00a8b`, tree `39193b28f71e832d85ff01d6eec893ebdff8f1ea`.
- Candidate HEAD: `a809764ae56f9fc13845464138c9ad4cd56e2575`, tree `15b155b7872b24e640b82fb93382970eb6e837c4`.
- `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`: exact reviewed blob `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`; byte comparison to `tl/ap2-P4-ten-current-review-0621` passed.
- `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`: exact reviewed blob `cbd332db227ecb9c6254e8ced0af72c3de91821e`; byte comparison to `tl/ap2-P4-http-conflict-rerun-review-0647` passed.
- Candidate code diff against the resolved base is exactly those two test paths; no product/helper/fixture/schema/generated/pin change or donor ancestry was introduced.

The tests retain the existing production caller (`test_native_batch_ingress.runtime`,
`timeline.open`, public `commit`, and the generated client path) and the required
full-v2 request/reply assertions: scope and base pair, commands, label, steps
patch/reads, merge/reads, dry-run, idempotency key, accepted/merged canonical
document/head/digest/receipt/effects/bindings/step dependencies/history, and
conflict/invalid details. The original shared seed, ten notes, per-step undo and
redo, real note-04 peer conflict, bounded callback rerun, remaining notes,
closure, show/history, restart, and authored-field preservation assertions are
present unchanged in the exact donor blobs.

Retained normal boundary identities:

- `runtime.lock.json` source commit is `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Vendored client files compare byte-for-byte with Runtime 34eac004.
- `astrid_runtime_client/generated.py` SHA-256 is `9b5686c388347108898956c3475b16960e2434d64adcefcc71a26fc269cdd904`.
- `astrid/core/timeline/schema/edit-command.schema.json` SHA-256 is the retained d106 digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
- These normal/d106 files are byte-identical between the resolved base and candidate.

Source checks passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-34eac004" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004 /home/user/work/venv-app2-native/bin/python -m pytest --collect-only -p no:cacheprovider -q -m integration tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
2 tests collected (pytest warning: unknown config option timeout)
/root/.local/bin/ruff check --config pyproject.toml tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
All checks passed
/root/.local/bin/mypy --config-file pyproject.toml --platform linux --no-incremental --cache-dir /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-two-port-service-review-0658/mypy-cache-0658 tests/editing_conformance/test_p4_ten_note_v2_runtime.py tests/editing_conformance/test_p4_note_rerun_v2_runtime.py
Success: no issues found in 2 source files (three annotation-unchecked notes)
git diff --check 9df06d16de5270c449dea938175123942ad00a8b..HEAD
passed
```

Ops-row review after terminal completion:

- Ops worker `ap2-P4-service-gain-execution-0655` has `DONE`, exit `0`, and a
  checkout receipt at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-runtime-1cf5562f8d2eddb6ee26cbec5155f94098e057b8`.
- Kept checkout is clean at HEAD
  `1cf5562f8d2eddb6ee26cbec5155f94098e057b8`, tree
  `f74b016ea837f8148db4a602c972073a226ed177`.
- Exactly one `p4-v2-http-nodes` row exists. Recorded config bytes are
  `89540 -> 90710`; target-row bytes `209 -> 1379`; target-row SHA-256
  `d3be1fa1385fb003fe395ec84704f10ef14d6e5feb9b6340fa5ac60c4160ac96 ->
  2ff0bb94d75defeee99267b073369406f3069726728704ea135453b4234f7cc0`.
  Outside-row bytes remain `89331` and outside-row SHA-256 remains
  `d9591c5ece20def0e0c77dbb1f61169dcd221413c55bfa100c634c79397fa5e3`.
- Independent post-change audit found the exact 1cf SHA/tree/clean guards, both
  Runtime and Agent import-origin guards, the unchanged normal 34e client
  boundary, and the original `/home/user/work/venv-app2-native/bin/python -m
  pytest -q -m integration` suffix. No new launcher, suite, pin, or client
  modification is present.

Limits: no HTTP, body, socket, service, browser, full-suite, or build execution
was run. The manager must run the original ten-note node once, then the distinct
rerun node once, only after this PASS and the retained Runtime independent /
integrated PASS. No merge or execution PASS is claimed here.
