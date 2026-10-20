# Runtime parent-route marker final review

**Decision: APPROVE**

Reviewed exact tree:

- commit: `d05e6383f4ccaf7541698a65b2737fbc5f3f0fbb`
- tree: `dbebdc779d3b87486871c2613897c2d1d592040b`
- reviewed against: `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`
- diff scope: `tests/test_timeline_clip_replacement.py` only

The corrected refusal test calls `RuntimeService.commit_timeline` through
`_native_commit`; it does not call `validate_request` directly. The actual
service method detaches the body and calls `validate_request` before entering
`_execute_timeline_commit`, so the parent-ownership refusal is exercised at the
Runtime service boundary. The current commit schema permits only `shared` or
`occurrence` ownership for this route, and the test asserts the exact resulting
`ValidationError` message.

The positive parent replacement test remains intact and all of its acceptance
assertions are preserved. It is now marked with `@pytest.mark.xfail(strict=True,
raises=ValidationError, ...)`, so the current schema gap is explicit and the
test will become a required pass when parent ownership is added. There is no
imperative `pytest.xfail`, broadened exception catch, extra marker, schema
change, or product/source change.

Evidence:

```text
python -m pytest -q tests/test_timeline_clip_replacement.py -m integration -k 'parent_clip_swap_route_refuses_parent_ownership_on_current_schema or parent_clip_swap_route_replaces_parent_media'
1 passed, 23 deselected, 1 xfailed, 1 warning in 2.08s
```

The warning was pytest's existing unknown `timeout` config option. No broad or
full suite was run, per the review brief. `git diff --check 6ab3243..HEAD`
passed. Manager may merge this review target.
