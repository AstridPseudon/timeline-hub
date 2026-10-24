## Report

- Updated only `tests/timeline/test_authoring_media.py`:
  - nested selector requested;
  - exact `working_before == raw_before`;
  - hold guard derives from authenticated baseline.
- No production code or other tests changed.
- Offline fixture/current-code checks confirmed raw hold `0.9` and canonical patch `0.9 → 0.75`.
- Targeted static checks passed: Ruff, vendor lock, artifact manifest, `git diff --check`.
- Exact selector run failed as warned:

```text
...test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
1 failed in 6.10s
KeyError: checkout_shot['internal_timeline']['revision_id']
```

The checkout serialization omits that nested field. Publication had already been accepted with hold before-value `0.9`; no subsequent test writes occurred. No alternate selector or canonical-shape rewrite was made.

`BLOCKED` marker and commit message were written.