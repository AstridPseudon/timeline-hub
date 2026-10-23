# Handoff: ap2-P4-current-two-http-port-0655

## Source qualification

The worker started at the current integration base:

- base and pre-edit HEAD: `9df06d16de5270c449dea938175123942ad00a8b`
- pre-edit HEAD tree: `39193b28f71e832d85ff01d6eec893ebdff8f1ea`

Only these reviewed final test blobs were ported:

| Path | Exact blob |
|---|---|
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | `cdb186d001fe8bd7476c2a059ee65e9a312dbec5` |
| `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` | `cbd332db227ecb9c6254e8ced0af72c3de91821e` |

The files compare byte-for-byte with the donor blobs. No donor product,
helper, report, fixture, pin, or ancestry was imported. Independent source
reviews 0621 and 0647 remain PASS.

## Evidence

- Exact two-test collection passed: 2 tests collected.
- Scoped Ruff passed.
- Scoped private mypy passed with a Linux platform override because the
  repository Darwin-target configuration causes the installed mypy build to
  raise an internal error on this host.
- `git diff --check` passed.
- Changed-path inspection showed exactly the two named test paths.

This handoff is source qualification only. Per the task, no HTTP/body/socket/
service/browser/full test execution was run. The manager must perform the
commit-log/path/blob check before requesting remote Agent execution, and owns
the two separate original-node observations after Runtime gain corrected
execution review/proof. This is not a premature merge or runtime-pass claim.
