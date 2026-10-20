# Runtime raw014 / 7d1 final narrow review

**Decision: APPROVE**

Review target: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`, tree
`ac693097189637d3bd0fc3a39299d9b166758853`.

## Exact review basis

- First parent: `6798c6986d85601450a3d8dc25d10befeb1e92c7`.
- Second parent / approved base-fix reference: `dcac221296ef2c73e02d30534effb2a09d9a91bd`.
- The merge delta from `6798` is exactly two files:
  `runtime_protocol/timeline_commit_port.py` and
  `tests/test_timeline_raw_audio_port.py`.
- Both file patches and both resulting blobs are byte-identical to the
  corresponding `dcac` patch/blobs. No public contract, private carrier,
  API/DTO/table, schema, release/version, or generated artifact path changed.

The `media_info` guard validates the exact two-field pin, requires recursive
declaration, resolves `self.__request["base_revision_id"]` through the
authenticated original-base closure, requires base-manifest membership, and
only then consults the memo or `MediaReads.media_info`. The source-order probe
found no latest-head, observed-head, candidate, or caller-publication authority
in this path. Acceptance-time consumed-media recheck and execution
coordinator ledger-first replay lookup are unchanged.

## Identity and handoff boundary

- Reviewed Runtime server candidate: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`,
  tree `ac693097189637d3bd0fc3a39299d9b166758853`.
- Immutable ordinary014 artifact/client producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Frozen Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.
- Frozen Agent raw schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime wire digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Counts remain 75 artifacts, 55 definitions, and 29 operations.

The candidate is **REVIEWED CANDIDATE / NOT CURRENT**. The public 0.2.13
tuple is not mutated. Agent qualification may use the stable KEEP checkout
`rt-pin-7d1cfa6b` for the one actual pair, through the normal health/door/
provider-authenticated path; no bypass is authorized. Native legacy-trim
qualification remains open pending its result.

## Evidence

Inherited exact-candidate evidence from the compose worker:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py tests/test_timeline_commit_port.py tests/test_timeline_commit_contract.py tests/test_timeline_commit_acceptance.py
131 passed, 1 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_raw_audio_port.py
8 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python generators/generate.py --check
passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
contract/artifacts.json is current

git diff --check
passed
```

Independent final checks performed here:

- exact patch/blob comparison against `dcac`: passed;
- merge changed-path guard: exactly the two paths above;
- source-order AST probe for pin/declaration/original-base/membership/memo/
   reader: passed;
- acceptance recheck and ledger-first source probes: passed.

No full suite, live HTTP/socket journey, Agent native pair, or native
legacy-trim qualification was run in this review. Shared dependencies were
not modified, and the assigned Runtime worktree remains source-clean.
