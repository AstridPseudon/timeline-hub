# P4 cache-boundary correction handoff

Only `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` changed from
`5108aaf1438b52be17d5346e04f3dcb590a892b7`. Outside that path, all blobs match
reviewed `246f92507f15ac16c3bb559b7ce1576a608c86d8`; Runtime pin and all product,
schema, generated/client/helper/fixture/launcher/suite files are untouched.

The test now asserts exact cache absence on the raw source, ordinary session
read and direct executed candidate, and exact cache presence on accepted and
authenticated publication reads. Execution preserves the input cache boundary.
It compares the complete accepted document with the exporter result from the
real authenticated original base plus full recorded request/evaluated head,
then requires the complete digest, steps, recorder (including physical bindings
and refs), receipt, head and stored closure. Original authored and CLI/sheet
request/show/history requirements are preserved. No conditional dropping,
forged expected pins, mutable-latest lookup or raw-source normalization.

Independent source review: **PASS** before the one central run, and **PASS**
again after correcting the exact caller wrapper. Final one-node collection,
Ruff, private-cache mypy, diff check and offline production cache/export witness
all **PASS**.

**HTTP remains FAIL/unverified.** Exactly one central service request was made:
`ap2-P4-runtime-cache-sol-0455-p4-v2-http-nodes-1023045756-24992`.
Result: **1 failed, 1 warning in 3.77s**, exit 1, snapshot tree
`453114eb91242a0d6fd9ba32fbb0f2044cbdc05b`.
The run passed the original authored comparisons and the new authenticated
cache/complete-document/digest/steps comparisons. It failed my newly added
receipt equality because `TimelineSession._flush` adds exactly
`accepted_publication_id` and `show_command` to caller data. Final source
requires the complete receipt result plus those two exact production fields.
The final correction was reviewed and statically checked, but has not had an
HTTP run. Downstream show/history/recorder/stored-readback assertions were not
reached. No completion credit, full suite or second service attempt is claimed.

Recommended next step: orchestrator separately authorizes one run of the same
single node on the final committed tree. No product blocker or plan deviation
was found; proof is incomplete because this task's single attempt was consumed.

Exact commands/results and production-boundary rationale:
[/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-runtime-cache-sol-0455/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P4-runtime-cache-sol-0455/report.md)

Service log:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P4-runtime-cache-sol-0455-p4-v2-http-nodes-1023045756-24992/log.txt`
