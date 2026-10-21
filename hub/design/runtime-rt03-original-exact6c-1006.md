# RT03 exact6c original unplaced owned-raw proof

Date: 2026-10-21 UTC

## Result

The single authorized named-suite run was attempted once and failed during
fixture setup before entering the target test body. The RT03 semantic proof is
therefore **not qualified**. No assertion, Runtime commit, CAS reference, or
database mutation from this proof ran.

First cause: the central named-suite `--files` filter isolated the target test
module but did not make the `film` fixture from
`tests/test_timeline_commit_integration.py` available. Pytest reported
`fixture 'film' not found` while resolving the target's `agent` fixture.
This is a test-service/suite dependency issue, not a product-behaviour result.
Per the brief, I did not rerun, change the fixture/test, add a marker, or use a
different selector.

## Exact identities and approvals

- Runtime base: `aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4`, tree
  `09699414ff8ca79f3e9146b44b5713a10b8ef132`, clean.
- Producer Runtime: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`, detached clean checkout
  `/home/user/work/wt/rt-pin-42a7203f`.
- Agent consumer: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`, detached clean KEEP checkout
  `/home/user/work/wt/agt-pin-6c1989ad`.
- Checkout done records were present for both immutable pins.
- `runtime-private017-42a-independent-review.md`: exact producer artifact
  APPROVE.
- `agent-private017-completed6c-current-pin-final-0948.md`: exact6c current
  safety EXACTAPPROVE.
- `agent-owned-raw-reference-source-review.md`: source compatibility APPROVE.
- The orchestrator disposition
  `peer-runtime-to-agent-app-app2-20261021T1007-private017-exact6c-owned-proofs.md`
  accepts this exact bounded pair and keeps public adoption/activation out of
  scope.

## Fresh preflight

All requested prerequisites were checked before the body run:

- Schema raw SHA-256: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`.
- Schema canonical SHA-256: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`.
- Schema shape: 65 definitions / 37 `EditCommand.allOf` clauses. The `ed5fd33c4a7fa9956178f9b24eb127415eaca9e` schema provenance exists.
- Producer artifact manifest: 76 entries; manifest file SHA-256
  `0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`;
  version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent lock: 15 entries, source commit exactly `42a7203f…`; the exact command
  below passed with all locked bytes matching the producer manifest:

  `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B /home/user/work/wt/agt-pin-6c1989ad/scripts/vendor_lock.py check /home/user/work/wt/agt-pin-6c1989ad/runtime.lock.json --producer /home/user/work/wt/rt-pin-42a7203f`

- Runtime client metadata: version `0.2.17`, health/schema digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
- Import origins under the intended environment were the Runtime worktree,
  exact Agent checkout, and Agent-vendored `astrid_runtime_client`; provider
  profile `astrid` loaded as `astrid-v1`, interface 1, with the same digest.
- Agent venv imports for `pytest`, `jsonschema`, `referencing`, `yaml`,
  `filelock`, and `PIL` all resolved under `/home/user/work/venv-agent`.
- A private `0700` temporary directory was created and removed by the probe.
  Shared realpaths were `/home/user/work/venv-agent` and
  `/home/user/work/app/node_modules`; neither was modified. Available disk was
  10,590,516 KiB on `/home/user/work` and `/tmp`, above the 5 GB floor.
- No schema/health override, c964 checkout, public014 checkout, install,
  generation, renderer, browser, HTTP, full-suite, or sibling ordered-proof
  operation was used.

## Authorized execution

Request command, exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-rt03-original-exact6c-1006 private017-agent6c-integration --files "tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract"
```

Central service command:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

Result: exit 1, one setup error in 0.44s; no test count was reported. The
target body and all original assertions remain unchanged and unexecuted.

## Next step

The test service needs a dependency-aware exact-selector run that includes the
fixture module while still collecting only this one target. The orchestrator
must authorize any later retry; this worker made no product or test change and
makes no completion claim for RT03.
