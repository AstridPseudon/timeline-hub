# Independent handoff: exact-seven retired registrations review

Status: **independent PASS for proposal scope; NO-GO for live operation**.

This review independently validates `ap2-OPS-retired-registrations-1841` against
PLAN §3 P1/P3 and BOARD-HEADER D21a/D21b as an exact proposal for seven
historical generated `agent-remotion-*-nodes`
registrations at `tests/suites.conf` lines 162–168 and their seven matching
env files. It does not authorize deletion, runtime retirement, retry, guard
waiver, process/daemon/socket inspection, provisioning, or source/product
changes.

## Decision

- **PASS:** target identity, authored provenance, exact row/env hashes, bounded active-use classification, private patch scope, protected-input preservation, and flat evidence publication.
- **UNKNOWN by design:** whole-host process/daemon/lease-service idleness. Sandbox metadata and bounded runtime-marker checks cannot certify host idle; no PID view was used for that claim.
- **NO-GO:** any live lifecycle operation. Runtime must apply its existing guarded retire lifecycle only after its own normal guard/activity recheck, and must retain/reject any target whose current use becomes unknown.

The current live orchestration source is not the authored full baseline: SHA-256
`b53dde1222f2625f4c5b81c45a126277dbdfde022cbf87b043092a161b6d7c95` (140,648
bytes) versus the authored evidence SHA-256
`07dfac86a0a63b3449a5d3393327ea95cc5688c342413fe1d9e323f3cfd9a330` (140,559
bytes). Independent diffing found exactly the concurrent P3 OPS 1845 row update
at line 36; target rows 162–168 and protected row 169 remained unchanged. The
proposal patch applies cleanly to a private copy of the current source while
preserving that P3 row; the live source was not overwritten.

## Evidence and verification

- Patch: SHA-256 `5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`, 23,163 bytes; one suite hunk plus seven exact env Delete File hunks.
- Source manifest: SHA-256 `acb5cf9d2e4f989650e9dfd6eba98f53e89d45db835eeafad1f693091f777678`, 16,778 bytes.
- Private author-baseline `patch --dry-run`/apply: PASS.
- Private current-source `patch --dry-run`/apply: PASS.
- Each private result: exactly seven target rows and seven target env files absent; outside-target suite bytes and every non-target env byte unchanged; current 1743, P1/P2/P3/F, and general inputs protected.
- Seven Agent and seven Runtime provenance commit objects resolve in the frozen repositories.
- Exact target matches in pending queue, active worker metadata, pending provisioning, replay/debug paths, and bounded runtime lease markers: 0. Historical receipts, refused retirement records, and completed test summaries were retained and classified as historical.
- No product tests/typecheck/lint or live operation was run because source/product inputs were unchanged and the task is proposal-only.

## Flat source publication

The author evidence directory was not COMMS-flat. The eight unchanged original
files were exported to uniquely named flat files at `design/` and verified with
byte-for-byte `cmp`. See [the flat mapping manifest](handoff-ap2-OPS-retired-registrations-1841-evidence-flat-manifest.json), which records each old path, new path, SHA-256, byte count, line count, and review links. No denied report 1536 was copied. The narrow publication scan found no configured secret markers.

## Runtime handoff

Runtime may use this independent packet for its lifecycle assessment against
D21a, together with the [author packet](handoff-ap2-OPS-retired-registrations-1841.md), [exact patch](handoff-ap2-OPS-retired-registrations-1841.patch), [source manifest](handoff-ap2-OPS-retired-registrations-1841-manifest.json), [author report](../workers/ap2-OPS-retired-registrations-1841/report.md), and [Runtime peer disposition](peer-runtime-to-app2-20261023T1834-runtime-reference-disposition.md). The existing guarded production caller and full v2 request/reply shape are unchanged. This review authorizes no live action.
