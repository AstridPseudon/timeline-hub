# PASS — R1 inherited reads integrated proof

Integrated Agent HEAD `1951ee928a377c61d13642677269c4f91f70f0f0` (tree
`22fb3ddf58161927ea993b46a7f82f12ea13cb9a`) is clean and has the expected
two-parent merge: V1 integration `ffcec5d33` plus reviewed R1 correction
`14b924d72` → `169293c92`. The retained V3 integration is in ancestry through
`fa2cf5b66`; the retained P1 provider corpus is in ancestry through
`52e9c0ea6`. The delta from the V1 parent is exactly five source lines in
`astrid/sdk/timeline/commands.py` and 111 proof lines in
`tests/editing_conformance/test_doc_patch_v2.py`.

The locked generated source is Runtime `691a9436ce3dbf2dcbfeaf959c85143c165fe4e2`;
`astrid_runtime_client/contract_metadata.py`, `generated.py`, and
`timeline_commit_types.py` are byte-identical to that source. No generated,
schema, pin, or unrelated baseline bytes changed.

Evidence on the exact integrated HEAD:

- `test_doc_patch_v2.py` + `test_p1_doc_patch_provider.py`: **119 passed**.
- Inherited-read selectors (`mixed_native_capture`, forged/missing native
  claims, replay, and dependency conflicts): **16 passed, 86 deselected**.
- The three author/review-0145 native guard selectors: **3 passed, 234
  deselected**.
- Scoped Ruff: **passed**; private declared mypy: **no issues**.
- Normal ratchets: Ruff **2151/2151**, mypy **1915/1915**.
- `git diff --exit-code` and `git diff --check HEAD`: **passed**.

This is a bounded offline Agent/provider R1 PASS. It does not claim Runtime
persisted-wire, native HTTP, authorization, idempotency/history, or full-wire
qualification; no full/browser/native-14 duplicate was run.
