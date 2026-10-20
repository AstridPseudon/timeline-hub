# Runtime parent ownership strict marker

## Contract item

The current public-013 Runtime schema does not admit the bounded Agent parent
`clip.swap-media` carrier. Its `Intent.ownership` enum is exactly
`['shared', 'occurrence']`; `parent` is refused during ordinary commit-request
validation before provider execution.

The test contract is intentionally split into two named cases:

- `tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema`
  constructs the real native request and asserts the current-013
  `ValidationError` naming the ownership enum.
- `tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media`
  retains the full parent-swap acceptance body and is marked
  `pytest.mark.xfail(strict=True, raises=ValidationError, reason="needs schema 0.2.14 parent ownership; ledger D04")`.

The acceptance body remains intact: it uses real project-owned imported media,
the actual Agent provider, normal Runtime commit acceptance, and its accepted
status and canonical parent payload assertions. It must not be converted to an
imperative or non-strict skip. When the qualified 0.2.14 schema/provider cohort
is adopted, running this test with `--runxfail` is expected to turn the marker
red (XPASS) until the marker is removed in that adoption change.

## Evidence and boundary

The current-013 case reaches `runtime_protocol.timeline_commit_port.validate_request`
and fails on the normal schema validator with:

```text
invalid CommitRequest: 'parent' is not one of ['shared', 'occurrence']
```

The matching frozen Agent 310 provider and Runtime 0.2.14 candidate have
already passed the same full acceptance case under `--runxfail` on a normal
owned ephemeral realm (`1 passed`). That is qualification evidence for the
future cohort only; it does not authorize changing the public-013 schema or
removing this marker. No Runtime product/schema/DTO change is part of this
contract item.
