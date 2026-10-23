# R1/A3 current-port independent review — PASS

Approval is for the actual fresh target commit
`1f418aea45c70bff3d8517b506c72cf8b230060e`, based directly on integration
`bf40d6bb5923210a3f5d210414c9ad737b40403d`. It is not approval of old
`dc00a764c` ancestry.

## Identity and exact port

- `git log bf40d6bb5..1f418aea4`: one commit only,
  `feat(timeline): port R1-A3 occurrence fork`.
- `git diff --name-only --no-renames bf40d6bb5 1f418aea4`: exactly the 13
  requested Agent provider/conformance paths.
- Every target blob equals the corresponding reviewed `dc00a764c` blob.
- Every pre-existing target baseline equals the reviewed `9cf0fde2` source
  baseline; no novel composition was found.
- Manifest source-set SHA256 is
  `e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830`.
- Manifest has ten source files and matches the call manifest exactly.
- Schema digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`
  is unchanged; no schema/generated/pin/artifact/runtime/app/composition path
  changed.

## Functional review

The production Agent operation registry contains
`'occurrence.fork': Operation(FORK_PARAMETERS, occurrence_fork, OCCURRENCE_INTENT, True)`.
The real RuntimeService test passes through provider registration, schema
validation, normal bootstrap, disjoint-head merge, selected occurrence
ownership replacement, sibling preservation, public undo, explicit-created
redo, selected-child edit, and surviving-consumer undo refusal.

The focused provider/recipe tests cover shared and distinct physical sources,
exact source/row/order/opaque preservation, stale and ABA refusal, forged
created/reads/bindings/expect capture refusal, closed arguments, authenticated
AcceptedRecords inverse recovery, and native undo/redo. Existing v2 request,
receipt, metadata, effects, steps, dependencies, preview and historical
`rebased` behavior remains in the exercised neighbor lane. No tests were
skipped, xfailed, deleted, or weakened.

Runtime import provenance was explicit: `runtime_protocol` and `service` came
from `/tmp/w-4f3d8d00b5/runtime-be584`; that archive was checked byte-for-byte
against Runtime `be5848e17fbf68100286114883f5820fe4755911` (465 tracked files,
zero missing/mismatched/extra files). Agent and fork imports came from the
review worktree.

## Evidence summary

- Focused fork/provider/recipe: **25 passed in 4.63s**.
- Real RuntimeService integration: **1 passed in 4.25s**.
- Source/neighbour lane: **244 passed in 20.48s**.
- Scoped Ruff: **PASS**.
- Normal Ruff ratchet: **2150/2150**.
- Scoped mypy using persistent `/home/user/work/venv-agent-typecheck-v2/bin/python`:
  **10 files, no issues**.
- Normal mypy ratchet using the same persistent interpreter: **1915/1915**.
- Vendor lock: **PASS**.
- Artifact manifest: **current**.
- Diff/whitespace and exact scope checks: **PASS**.

The existing Runtime inverse-created equality issue remains separately owned
and is not waived. Mounted App caller proof remains outside this Agent commit
and is not claimed. The actual target commit is approved for the home queue on
the evidence above.

