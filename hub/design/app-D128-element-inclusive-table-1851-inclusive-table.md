# D128(4) inclusive function table

Verdict: `EXACTMISSING/full requestedtable NOTDERIVABLE`.

The only input was the published safe profile at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D127-element-profile-controller-1840-safe-profile.json`. Its exact size is 3557 bytes and its SHA-256 is `7ea986113ce80436d873739e2406dfed56308f4f6ed1577c99dc946e752cc756`. The source bytes were unchanged during this read-only derivation.

The request is the top 10 functions under `_timeline_commit` by inclusive samples for existing actual element `32016`, with call counts only when explicit real counters exist. The safe projection retains five inclusive rows, all at 828 of 828 samples, but they are outer routing wrappers plus the `_timeline_commit` anchor. It retains no child stack membership or inclusive child counters below `_timeline_commit`; therefore there are zero rankable descendant rows and no invented ranks.

| Rank | Classification | File | Function | Line | Inclusive samples | Sample total | Call count |
|---|---|---|---|---:|---:|---:|---|
| — | outer routing wrapper | `<runtime>/server.py` | `_dispatch` | 1229 | 828 | 828 | UNKNOWN |
| — | outer routing wrapper | `<runtime>/server.py` | `_route` | 547 | 828 | 828 | UNKNOWN |
| — | requested anchor, not child | `<runtime>/server.py` | `_timeline_commit` | 332 | 828 | 828 | UNKNOWN |
| — | outer routing wrapper | `<runtime>/server.py` | `do_POST` | 1264 | 828 | 828 | UNKNOWN |
| — | service wrapper | `<runtime>/service.py` | `wrapped` | 438 | 828 | 828 | UNKNOWN |

These are retained wrapper/anchor rows, not the requested descendant top 10. The four retained leaf rows are `copy.deepcopy` at lines 125 and 119 with 39 and 33 samples, and `timeline_commit_validation.reuse` at lines 120 and 116 with 27 and 24 samples. Leaf counts do not substitute for inclusive counts or prove call chains.

Line entries cannot be safely summed into invocation or exclusive-cost counts: membership is at most once per safe frame identity per sample, but line samples are not necessarily disjoint, and recursion/sample overlap can occur. No explicit real call counters, per-function duration, child stack membership, or exclusive wall time are present. The current safe projection cannot justify a Runtime or Agent cost author and does not identify a product author.

Missing for a complete table: inclusive child identities and counters below `_timeline_commit`, per-sample parent/child stack membership, explicit invocation counters, and per-function timing. The existing safe-profile producer/helper is the owner of that projection; this task adds no collector or extraction design.
