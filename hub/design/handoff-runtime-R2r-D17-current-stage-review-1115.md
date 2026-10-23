# R2r/D17 current-stage independent review — PASS

Date: 2026-10-23

## Result

**PASS for Runtime candidate `5768a3a63076195a7ecc251fcf3830ab8d821702`
(tree `b794170504544b259781e50d7ca4d61b6729e67c`) against exact base
`49ce53289bc37d9387a7d9e6b9c9b16072162181` (tree
`364380ae064c512c0a0d2b8903a599b7026642f4`).** The candidate’s stage-boundary
normalization is authenticated and narrow. Integrated D17 is still **FAIL / not
qualified** because Agent’s two repeated-source-copy inverses omit required
physical `commit.effect` bindings; Runtime correctly refuses them.

## What was verified

The only candidate diff is `runtime_protocol/timeline_commit_auth.py` plus
appended tests in `tests/test_timeline_inverse_stage_authentication.py`.
`runtime_protocol/timeline_commit_store.py` is byte-identical to base. The
normalization applies only to empty-path `shot:<id>` and `occurrence:<id>` root
writes. It resolves shots through a unique authenticated physical shot image
and exact internal image, observes occurrences from the authenticated parent,
and compares representation-normalized authored values. Sequential native
writes, physical effect images, stage ranges, source publication/step/ordinal,
history membership, input/output documents, digests, and effect bindings remain
strict. Missing roots are authenticated absent states, null remains present,
managed-link edges must correspond to authenticated physical images, and
ambiguous aliases refuse. There is no broad inverse exemption, dropped native
record, new executor, or binding waiver.

The new source-copy adversarial controls and retained stage suite cover forged
before/path/ref, omitted/extra writes, missing effect metadata, forged effect
digest, raw/mirror topology, immutable publication/step/range/order/history,
and no-durable-write behavior.

## Exact evidence

Runtime targeted commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py
137 passed in 48.27s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_inputs.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_port.py
101 passed in 13.75s
```

Exact four Agent nodes, candidate Runtime first on `PYTHONPATH`, immutable Agent
`ce1d1cca87379029924b0be6f98564f556597107` / tree
`68dee9124ab8f4026ac4119f816eceec654f0bba`:

```text
2 failed, 2 passed in 36.99s
```

Exact command:

`TMPDIR=/tmp/w-05c57a6ad5 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-R2r-D17-current-stage-review-1115:/tmp/w-05c57a6ad5/agent-ce1:/tmp/w-05c57a6ad5 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-R2r-D17-current-stage-review-1115 D17_OBSERVATION_LOG=/tmp/w-05c57a6ad5/exact-four-origins-history.jsonl /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o addopts= -p no:cacheprovider -p observe_d17 --timeout=45 tests/editing_conformance/test_commit_runtime_source_copy.py::test_source_copy_real_port_receipts_preview_undo_redo tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[False] tests/editing_conformance/test_commit_runtime_source_copy.py::test_repeated_source_copy_real_port_idempotency_and_guarded_inverse[True] tests/editing_conformance/test_source_copy_retained_inputs_whole_undo_redo`.

The failures are both `provider inverse effect bindings do not cover its stage
image`; the two other nodes pass. Origin/history capture recorded 8 before/after
origin snapshots, 39 candidate Runtime modules, 389 auth calls, and 2 strict
auth exceptions. The actual source history for the failing calls contained only
the accepted source publication.

The one retained REALSTORE witness independently passed forward and inverse
Runtime auth using exact accepted `store.history_entry` provenance: source step
`split`, ordinal `[0]`, created `parent/clip:music-right`; inverse publication
excluded. Missing, forged-step, and extra-history probes refused. The witness
metadata has stale hard-coded commit labels; the actual candidate origin is
`runtime_protocol/timeline_commit_auth.py`, SHA256
`a8a0b00025f99ace48e0fee989fe3e11c948c3f1e2fa47a33621791e91252756`.

Ruff identity comparison is 11 vs 11 with 0 added/removed diagnostics. Pyright
is 76 vs 76 with 0 added/removed. AST/compile and diff-check pass. The existing
stage-test prefix is byte-identical (34,547 bytes), the store is unchanged, and
the retained original repro remains SHA256
`47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a`.

## Owner action / limits

Agent must restore complete physical effect bindings for ordinary session
undo/redo, or submit a properly bound v2 request. The four ABI-1-style requests
missing `commit.effect` must remain refused; this is not permission to waive
request/effect binding or relabel the old Runtime 1365 result as current.
After Agent repair, rerun the exact four nodes once. No full/native14/original20,
browser/HTTP/P4/Agent58/broad281 duplicate or live-daemon suite was run.
