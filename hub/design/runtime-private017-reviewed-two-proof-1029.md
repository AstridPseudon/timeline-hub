# Runtime PRIVATE017 reviewed two-proof execution

Date: 2026-10-21 UTC

## Reviewed bytes

- Runtime base: `8ad62e4dce83ab3df7f3778dec2a449100e585d1`.
- Runtime artifact producer: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Normal Agent: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`, at
  `/home/user/work/wt/agt-pin-6c1989ad`.
- Runtime worktree source/artifact comparison against `42a7203f` found exactly
  one changed path: `tests/test_timeline_owned_reference_integration.py`.
  No other source or artifact path differs.
- Final reviewed test SHA256, checked immediately before each request and after
  each result:
  `28583b4adda23d464207a43c71b3f134ff960363050908b51187fab646705b13`.
- The only test edit is the approved RT03 media-manifest comment/assertion
  hunk. The ordered helper/body and every other assertion remain from `8ad`.
- The copied RT03 diagnosis at
  `design/runtime-rt03-manifest-order-diagnosis-1019.md` is byte-identical to
  `42a03d324af6e7916923fe7c152aa1fcccf996d4` and hashes to
  `2ba5ced993c193fac08a7f1ecc5fbf338720998d6252a581648bb9e58492c405`.

## Fresh preflight

Passed read-only checks:

- Frozen Agent ed5 schema source: raw
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions and 37 `EditCommand.allOf` clauses.
- Runtime artifact manifest: 76 entries, version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent lock: 15 entries, all matching the producer manifest; source commit
  and producer version match the exact 42a tuple.
- Client package `0.2.17`; Runtime/Agent/client imports resolved to the
  requested Runtime worktree, Agent pin, and Agent client respectively;
  `load_timeline_commit_provider("astrid")` loaded successfully.
- Healthy private Runtime probe returned status `ok` and schema digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
- Agent venv imports passed for pytest, jsonschema, referencing, filelock,
  Pillow, and PyYAML.
- Exact two-node collection passed: 2 tests collected. Exact `--setup-plan`
  showed complete closure for each node: `tmp_path_factory`, `tmp_path`,
  `film`, `monkeypatch`, `astrid_importable`, and `agent`; no tests ran during
  setup planning.
- Worktrees were direct realpaths, producer and Agent pins were clean, and
  `/home/user/work` had 10,558,156 KiB available at the source preflight.

## Central executions

The named suite was `private017-agent6c-integration`. Each selector was
submitted once with the exact `--files` argument. The central service snapshot
reported Runtime tree `ab5a6548c8d158e1952961cc681af737ff211ce0`, which
includes the uncommitted reviewed test hunk.

### Ordered project-data proof

Selector:

```text
tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

Result ID:
`rt-m2-private017-reviewed-two-proof-1029-private017-agent6c-integration-1021103142-12634`

Result: **1 failed in 1.76s**. The test reached semantic body and failed at
the inverse commit (`tests/test_timeline_owned_reference_integration.py:328`):

```text
RuntimeErrorBase: media inverse records differ from accepted history
```

This is the first unchanged cause. No retry was made.

### Original owned/unplaced reference proof

Selector:

```text
tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

Result ID:
`rt-m2-private017-reviewed-two-proof-1029-private017-agent6c-integration-1021103216-543`

Result: **1 failed in 1.23s**. The test reached semantic body and failed at
the unchanged same-key mutation status assertion (`:193`): expected `409`,
received `422`, with:

```text
ValidationError: 'source' was expected
```

This is independent of the ordered proof. No retry was made.

The test SHA256 remained the required value after both results. No collection
pass was counted as proof; both outcomes reached direct Runtime/provider
semantics.

## Limits and disposition

No source chase, assertion weakening, body retry, full suite, old44/186 lane,
Agent materialization lane, HTTP/socket/browser/render/install/generation/pin
operation, marker conversion, integration/release/adoption, or public
qualification action was performed. Shared dependencies remained read-only.

Both independent proofs are recorded as failed with their first causes. The
requested evidence is complete, but neither proof is a pass or qualification
claim.
