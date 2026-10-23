# R2 current-only port — agt-R2-current-port-1831

Status: PASS for the mechanical port. No merge request or source-approval call was made.

## Scope and exact source

Base/current HEAD: `78738040d72ce74c42ddf7731221aecb06f9246d`
Source: `0b735c13710d74600cc51bf55e4963b54163087e`
HEAD tree before edits: `e77ea239789dd8ae9103c68fef79b49329cf2c6e`

Only these five paths were carried, and each current git blob equals the source blob exactly:

| Path | Blob |
|---|---|
| `astrid/sdk/timeline/_step_undo.py` | `b5b99cc87743b2e37695d9ca4856c5cb35f5ce18` |
| `astrid/sdk/timeline/inverse.py` | `1b551173ebdf7a31a012573a92a02190918218ca` |
| `tests/editing_conformance/test_nested_parent_mirror_ranges.py` | `d8ccb0d5db11e8645768ed683494f270292a55aa` |
| `tests/editing_conformance/test_nested_inverse_order.py` | `264a0b336a67e21afacb1d4f93f81e482589638d` |
| `tests/editing_conformance/test_nested_native_aggregate_partition.py` | `7bff6baef0e5c1559a401a4e812dc50756b07fae` |

The cumulative source commit also changes these outside paths; none were carried:
`astrid/sdk/timeline/_commit_patch.py`, `astrid/sdk/timeline/commit.py`, `astrid/sdk/timeline/store.py`, `tests/editing_conformance/test_a4_track_doc_patch_witness.py`, `tests/editing_conformance/test_a4_transcript_doc_patch_witness.py`, `tests/editing_conformance/test_commit_document_input_capture.py`, and `tests/editing_conformance/test_current_pair_reader.py`.

Protected current modules remained unchanged, including `_collections.py`, `_commit_patch.py`, `_root_inverse.py`, `commit.py`, and `store.py`. The transient-root test/body and `_root_inverse.py` were not touched.

## Validation

Exact joined command used the author Runtime pin `/home/user/work/wt/rt-pin-2a9e347f`, `/home/user/work/venv-agent/bin/python`, `PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f`, `-o addopts= -p no:cacheprovider --tb=short`, four full focused files, five explicit split node IDs, and fourteen explicit original node IDs.

Result: **129 passed in 60.72s** (110 focused + 5 split + 14 original).

Additional checks:

- Scoped Ruff over all five paths: passed.
- Scoped mypy over all five paths: no issues.
- `scripts/vendor_lock.py check runtime.lock.json`: `ok runtime.lock.json`.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check`: passed.
- Credential scan over permanent evidence: no credential patterns found.
- Source author quality evidence was reused only because all eligible source blobs are exact and no dependency/pin files changed: Ruff baseline `2149/2149`, mypy baseline `1912/1912`. Current scoped Ruff/mypy were rerun above.

Permanent evidence, including before-validation bodies, source bodies, module origins, selected node list/body hashes, provenance, logs, hashes, and credential scan:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-current-port-1831/evidence`

The independent cumulative review and the separate transient-root owner remain separate; this report does not claim either.

