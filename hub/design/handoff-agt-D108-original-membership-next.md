# F-D108 original metric membership recovery

Status: **SOURCE_ONLY_EXACT_MEMBERSHIP_RECOVERED**.

The D108b full body was already terminal before this worker started:
`agt-F-D108b-core-local-0811-agent-core-full-1025081835-2016`, exit 1,
`8763 passed / 159 failed / 347 errors / 86 warnings / 173 subtests`.
This worker did not rerun it.

## Exact replay

I replayed the authentic original parser source
(`f8a000977ee880cefb4e1d8313157049acc667549a88351d3547b03b5e4c8c96`) with
only the unavailable manifest path replaced by the authentic local manifest
(`37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`). The
parser semantics remain the original: Git-object reads, `ast.parse`,
top-level/class-member `test*` functions, complete-function SHA-256,
attribute-free assertion-expression AST fingerprints, Counter subtraction,
and operator/decorator deltas.

Authentic source tuple:

- Agent: upstream `08e6b905114a3ee2b05c3e7980421f26b4abf15c`, captured
  `d6294843286c18e57af3c1874cf1996be42212d2`.
- Runtime: upstream `d4f496ec4fbcae7a1f3a51d47ed5147c561117ad`, captured
  `1daca2a33f6d7b10053e07c539a54843e3984e19`.

The exact Agent result is:

`2536 upstream / 4893 captured / 104 missing / 2461 added / 129 changed bodies / 113 removed assertion fingerprints / 287 added assertion fingerprints / Eq -3 / In +17 / no skip-xfail or parametrization delta.`

The Runtime replay independently reproduced `113 / 72 / 205` for changed,
removed, and added, respectively.

The complete per-function/fingerprint membership, old/new actual Git blob,
line, body hash, and multiplicity records are in
[`original-membership.json`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-original-membership-next/evidence/original-membership.json)
(SHA-256 `1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`).
The handoff JSON contains the same source identity, arithmetic, and ownership
record in machine-readable form.

One manifest metadata discrepancy is retained explicitly: its
`upstream_blob` for Agent `tests/test_installer_platforms.py` (and the
non-test `astrid/installer/service.py`) is not the blob at fresh `08e6`; the
replay uses the actual `git show 08e6:path` blob as required by the original
parser and records both values. Captured source blobs match the captured ref.

## Disjoint review ownership

The recovered 129/113/287 set is source membership, not clearance. Existing
approvals clear only an exact relevant predicate/body with its cited decision;
operator counts and lexical similarity clear nothing.

The remaining review work is kept disjoint and owned by its existing receipts:

| Group | Scope | Disposition |
|---|---|---|
| D108 original membership | 129 Agent changed bodies; 113 removed and 287 added fingerprints | Exact membership recovered; predicate review remains unresolved. |
| D07/b943 | Three timing/ripple predicates in `tests/test_timeline_editing_helpers.py` | Retain D07 source/proof ownership; no D108 edit or clearance. |
| Windows/d0ec | `test_register_scheduled_task_accepts_rendered_xml_string` | Retain Windows source/proof ownership; source-qualified only. |
| D107/2e3331ee | Exact original M1-baseline ten | Retain D107 ownership; original ten unchanged and behavior-pending. |
| D18 | Generic-host child-bridge retention predicate | Retain D18 ownership; excluded from D108 citation mapping. |

Named receipts are recorded in the handoff JSON, including
`handoff-agt-D108-D07-source-0724.md`,
`handoff-agt-D108-D07-source-receipt-0743.md`,
`handoff-agt-U2-D108-windows-review-0745.md`,
`handoff-agt-D107-source-receipt-0721.md`, and
`agent-F-D18-node-return-1049.md`.

The direct-tuple `added=289` examples and the finite fallback `189/310/119`
were not substituted. No retirement, semantic policy, product/test/body,
import, collection, probe, or live-request change was made.

## Checks

- JSON parse and in-memory compile: PASS.
- Exact parser replay and target aggregate arithmetic: PASS.
- Actual Git blob/path receipts: PASS for replayed refs; manifest-versus-Git
  metadata discrepancy retained as above.
- `git diff --check`: PASS (composition worktree unchanged).
- Product tests, typecheck, and lint: N/A for this read-only source task.
