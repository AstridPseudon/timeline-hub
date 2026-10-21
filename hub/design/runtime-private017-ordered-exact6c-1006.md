# Runtime PRIVATE017 ordered exact6c result

Date: 2026-10-21 UTC

## Scope and exact pair

This was the one bounded Gate2/Gate4 direct-provider proof requested for
Runtime base `aa0c26e0dafc6a749a1c8aae5ccfe971a1ce27d4`, with the approved
PRIVATE017 artifact counterpart Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c`
(tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`) and the approved normal
Agent6c checkout `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79` (tree
`cc0a8dd1360324a1b440ba7d318a083e7f8814cc`). The required Agent checkout
completion marker was present, and both exact artifact approvals plus the
`agent-private017-completed6c-current-pin-final-0948.md` current-safety APPROVE
were read. The Agent and Runtime checkouts were clean.

## Preflight

The single read-only preflight passed:

- frozen Agent `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` schema provenance;
  raw SHA-256 `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical SHA-256 `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions and 37 `EditCommand.allOf` clauses;
- Runtime artifact manifest version `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`,
  all 76 producer artifact bytes, and all 15 consumer lock bytes;
- package/health metadata `0.2.17` and schema digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`;
- imports from the expected Runtime and Agent roots, `authoring_profile=astrid`,
  and the existing Agent virtualenv dependencies (`pytest`, `jsonschema`,
  `referencing`, `filelock`, `Pillow`, `PyYAML`);
- exact collection command: `1 test collected`;
- direct, clean shared paths, removed private temporary directory, and
  `10,590,552 KiB` available on `/home/user/work`.

No schema, metadata, public014, c964, shared dependency, or live caller was
overridden or modified.

## One execution result

The central named suite was requested exactly once:

```text
private017-agent6c-integration --files tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

It failed during pytest fixture setup, before the test body ran:

```text
fixture 'film' not found
tests/test_timeline_commit_integration.py:58
```

The `agent(film, astrid_importable, monkeypatch)` fixture could not be built;
the central run reported `1 error in 0.44s`. Result log:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-private017-ordered-exact6c-1006-private017-agent6c-integration-1021100753-27437/log.txt`.

Therefore this run provides no body evidence for `insertion_order`, actual
provider acceptance, lost-ACK restart retry, duplicate prevention, inverse,
redo, null/absence/opaque preservation, or no-partial-write behavior. The
existing test remains unchanged. No retry, fixture rewrite, marker, assertion
removal, full suite, HTTP/browser/socket/render/install/generation/pin lane, or
public adoption/activation/release action was performed.

## Disposition

Bounded qualification is blocked by the missing `film` fixture in the central
named-suite environment. The next step is for the Runtime manager/orchestrator
to repair or authorize the appropriate test-service fixture environment, then
decide whether to rerun this exact selector. This report makes no qualification
or adoption claim.
