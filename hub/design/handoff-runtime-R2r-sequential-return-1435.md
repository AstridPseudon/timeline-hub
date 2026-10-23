# Runtime R2r sequential-return handoff

Base: `c8c9094e37f3b723dae58337d672bbf9095e6dcf` (integration leaf).

## Implementation

- Original-side sequential validation now authenticates each command at its own input boundary, including staged aliases and command outputs.
- Capture documents, heads, records, command/step metadata, image digests, and projections are closed-shape validated with structured refusals.
- Source-to-landing physical bindings must be complete, unique, consumed exactly once, and tied to authenticated images and owners.
- Replay maps enforce existing patch/read shapes, strict integer ordinals (booleans rejected), complete coverage, and per-node source-step ordering, transitions, owners, images, and original/landing correspondence.
- Added a regression test proving boolean command ordinals are rejected without a write.

Changed product files: `runtime_protocol/timeline_commit_auth.py` and `tests/test_timeline_commit_sequential_verifier.py`. No contract, schema, generator, client, pin, lock, or baseline files changed. `git diff --check` passes.

## Evidence

The required single real Agent run was performed once with the pinned Agent checkout `2dcae8d598201270a127ee865989d6af5c783fcc`. It returned `4 failed, 5 passed in 8.62s`: all four positive cases failed and all five strict-negative controls passed. The first failure exposed an over-strict generated-record command comparison; that comparison was removed and the verifier was subsequently corrected offline. Per the run rule, the Agent body was not rerun, so the four positive cases are not qualified by a fresh post-fix run.

The observer captured four full attempts before validation, including request/context, prepared candidate, source/base/history, replay map, module origins, and no-write evidence:

```
a0dc79b1716b5bdb5a31c17f1af08ccf6bfbe21ddb2f7317529a2a5040d80ec7  capture-0.json
26b34cec169b56ba8e5650a1becb2a1009f82889b112c67c885dd06d8acca354  capture-1.json
4b08a3bba6f0b53f79953de71066f9158d128c3bc4be4fab5a819db9c58b91e7  capture-2.json
b0d73b1ed85d8c81823952f37f91614f397c7ffa119a138782e4364c29cd9d0f  capture-3.json
59e329b65a9b83c38f257ae5b87157072e30d71e63e0506b8b6908aa89231619  retained R1 packet
```

The retained four-capture packet passes `validate_sequential_capture` for all four cases offline after the fixes. This is causal/offline evidence only and does not replace the failed single real Agent qualification run.

Runtime verification:

```
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py
315 passed in 75.72s

PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_sequential_verifier.py
6 passed in 2.05s

/root/.local/bin/ruff check runtime_protocol/timeline_commit_auth.py tests/test_timeline_commit_sequential_verifier.py
All checks passed!

/root/.local/bin/pyright runtime_protocol/timeline_commit_auth.py tests/test_timeline_commit_sequential_verifier.py
0 errors, 0 warnings, 0 informations
```

The frozen contract/schema/generator paths are unchanged (`git diff --quiet -- contract generators runtime_protocol/schemas runtime_protocol/contract_metadata.py`). No full suite was run.

## Qualification status

Implementation and Runtime evidence are complete, but Agent qualification is blocked by the mandatory one-run stop: the only new real Agent run failed all four positives before the post-run fixes. A later manager-directed Agent run is required to claim the requested 4-positive/5-negative qualification.
