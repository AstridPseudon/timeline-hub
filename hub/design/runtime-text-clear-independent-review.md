# Runtime text clear independent review

**REJECT** `bfec49af4e2bcb82ae2beed922dda99a977b7d72` against
`8609333456b9537339ee1a5dfc7ffd9609242de8` as the complete clear implementation.
The existing-stream presence representation is sound; the implementation still
refuses authentic retained legacy text on clear and exact inverse restoration.
No representation redesign is needed.

## Blocking finding: retained legacy MIME is treated as a new selection

`runtime_protocol/timeline_commit_store.py:755–760` passes both clear's current
descriptor and inverse's restored descriptor to `verify_text_object`.
`runtime_protocol/timeline_commit_port.py:584–590` permits only
`text/plain; charset=utf-8`. Main's original writer materializes `text/plain`.

Private probes use unchanged writer methods from main
`29d0954b6d78a7d7937d81bc36567b6dee7ca976` on a private candidate realm, then
the existing real acceptance fixture. They establish the original object,
registered event, and retained canonical descriptor without fabricated SQL or
history. Clearing that binding fails; replacing it with canonical text succeeds,
but restoring its exact retained descriptor fails. Both failures are
`ValidationError: text selection requires object_id == digest, size within 1 MiB
and text/plain; charset=utf-8`, with whole-SQL equality after rollback.

This is an explicit compatibility gap, not silent corruption. The strict
selection helper and legacy inverse limitation already exist in the base;
the new clear path also inherits that limitation. The prior report's separate
legacy-MIME debt remains real. Its legacy-event test uses canonical MIME, so it
does not qualify legacy-MIME restoration.

Recommended correction: distinguish verified retained binding/history inputs
from newly selected text at the existing internal validation seam. Preserve the
exact original descriptor and MIME, with ownership, digest, size, UTF-8 and
ancestry checks. Keep first-use selection strict. Do not normalize old objects,
accept arbitrary MIME, or add caller-supplied authority or public API/schema.
The Runtime projection check itself needs correction; an Agent-only adjustment
cannot make its unconditional strict verifier accept the retained descriptor.

## Verified and bounded

- The row remains the existing stream/retention anchor. Clear/resurrection append
  `shot.text_binding.rebound`; original birth remains `created`. Missing state
  means present. Added state is covered by the existing event hash.
- Live GET/list observe absence. Current inspection/Markdown follow authored
  membership; historical inspection retains old text. Immutable shot and accepted
  closure reads retain the old descriptors. Empty UTF-8 remains present until
  explicitly cleared and can be resurrected as present.
- Recorded birth reversal and clear reversal preserve append-only history,
  retry identity, authored order and descriptor metadata in acceptance-fixture
  tests. These are not native Agent inverse proofs.
- Missing first/head events and un-rehashed payload/state changes refuse on all
  five tested readers (GET, list, projection, service pin, baseline pin), without
  writes. Absent selected heads refuse; earlier present pins validate.
- Candidate tests prove old V1 pins/bytes after V2, clear, restart, structured
  export, backup/restore and deep CAS checking. Existing registered objects are
  retention roots. No destructive GC was run or claimed.
- No schema, endpoint, table, journal, DTO or caller-authority addition appears
  in the five-file diff. The original positive clear expectation is preserved;
  only its strict-xfail marker/comment is removed.

The private anchor-only corruption probe exposes an existing reader asymmetry:
baseline pin validation accepts a valid historical pin/chain after only the
live anchor digest is changed; the other four readers refuse. This does not
authorize an absent event or different historical bytes, and is not a new
corrupt-chain regression from this patch. Do not claim every authority integrity
check is identical across those readers.

## Evidence and remaining gates

Independent candidate text tests: **52 passed**. Private probes: **25 passed**
(20 chain-damage cases, four anchor guards, one opaque descriptor/order reversal);
one baseline anchor-only discrepancy. Corrected legacy probes: **two positive
expectations fail at the strict MIME verifier**. Inspection/Markdown probes:
**two passed**. Exact commands, setup correction and limits are in
`workers/rt-m2-text-clear-independent-review/DetailedReport.md`.

Agent representation ACK is required and was located at
`design/agent-text-binding-clear-ack.md` (2026-10-20 10:58 UTC), SHA-256
`0c0e8e6903ff0eb255ba0f1872772439de5c0acfb20e5e9ca50b4eac20768a8a`.
It matches this representation and supersedes the prior Report.md's pending-ACK
wording. It does not satisfy native qualification.

Native Agent paired acceptance/inverses using the full S2-superset schema and
normal generation remain **REQUIRED and unverified by this review**, including
group ordering/metadata, first-birth undo, EMPTY, and exact legacy restoration.
No public tuple promotion, writer retirement, App cutover or overall completion
is approved. No full, socket/browser or central-service suite was run.
