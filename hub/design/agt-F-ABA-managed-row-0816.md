Implemented staged candidate row: [tests/suites.conf.candidate](/home/user/work/wt/agt-F-ABA-managed-row-0816/tests/suites.conf.candidate).

- 4,564 bytes; SHA-256 `290bd2bf…899b41a`
- Binds Agent tree `4ce9de…`, Runtime `becfe6db…` / tree `7edc08…`
- Guards repaired auth blob `979225ab…`
- Preserves original oracle `e55be12f…` and source archive `a0dca…`
- Preserves Node 20.19.4, Remotion `819acf`, full import/profile origins
- Live suite registry and test body unchanged
- Exact selector: `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`

Checks passed:

- Shell syntax
- Candidate serialization
- Source-identity guard
- `git diff --check`

The original test body was not executed. Commit message and `DONE` marker are prepared.