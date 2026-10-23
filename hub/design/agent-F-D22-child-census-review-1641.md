# F-D22 child census review 1641

## Verdict

Review **PASS** for the report's bounded evidence, while retaining the actual
service result **FAIL (108 passed, 1 failed)**. The sole failure is fixture-
owned, not a product regression; no repair was made in this readonly review.

## Independent checks

- Sole D22 inventory SHA-256:
  `cc8b7d96dadaa6f9022a064fcd5a5db3d72f008b1565afc1f63c72e4adbcc397`.
- Target groups are 17 + 87 + 9 = 113 distinct nodes; no overlap.
- Durable `D22_REPORT_ALL` has 113 body records, 109 unique selected IDs, and
  exactly the four exclusions listed in the worker report. Selected IDs equal
  target-minus-exclusions exactly. All current/installed-8c body hashes match.
- The service summary is authoritative: 109 collected, 108 passed, 1 failed,
  1266.10s, request exit 1. No body replay was performed.
- The raw service log contains two identical D22 JSON records. The original
  selector manifest and `d22-state.json` were absent from the author temp
  area; the retained JSONL is explicitly reconstructed from those durable raw
  lines, with lost original artifact hashes disclosed.
- 246 product-relevant source hashes independently match both the 98ef Git
  tree and installed 8c site-packages (246 read, zero mismatch).
- Read-only installed metadata confirms Agent 8c, Runtime checkout 9ce/tree
  92ab, Node 20.19.4, Composition 0.0.14, PEP 610 direct URLs, `-I`, absent
  `PYTHONNOUSERSITE`, and the recorded profile lock/archive hashes.

## Failure classification

The failed selector is
`tests/sdk/test_host_bootstrap_source_identity.py::test_installed_profile_launch_preserves_identity_and_uses_isolated_interpreter`.
Its trace ends at `_registry_probe` with
`installed registry launch source binding is unavailable`. The complete mock
fixture creates no `astrid/core/rendering/remotion_runtime.py`; installed mode
passes that temporary source root to `_registry_origin.installed_argv`, whose
`canonical_file` correctly refuses the missing/aliased carrier. The guard is
working. This is an exact small-fixture owner handback, not evidence of a
production regression. The failure remains visible and unqualified.

Historical full-10679 remains terminal FAIL and UNCONFIRMED; existing 4/9/1
proofs and prohibited suites were not rerun.

Evidence and raw-log hashes are retained under the worker evidence directory;
the worker report contains the full command/result/limit record.
