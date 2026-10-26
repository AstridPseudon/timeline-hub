# F D141l handoff

Status: `SOURCE_ONLY; CURRENT_BINDING_MISSING`.

The six 0731 findings remain valid as source defects against 0718, except that
the historical statement about the live `agent-core-full` row must be read as
the 0718 snapshot: the current central config now has generic Agent `full`,
`targeted`, and `conformance` rows and no current `agent-core-full` row. That
absence is expected because this worker did not install or mutate rows. The
real blocker is that 0718 has no producer for the future binding: it accepts a
caller-authored JSON file instead of obtaining the native request ID, row,
result directory, terminal status, receipt, and brief from the existing
request-test/test-run path.

The next controller must use the existing owned row-CAS mechanism, then run
the two same-suite phases serially with genuine pristine Agent/Runtime source:

1. CAS the exact cut row against the live registry preimage and capture
   before/after/outside-row hashes.
2. Check the one-time `4,714,564,096` dispatch floor and write the immutable
   witness/brief; call normal `request-test`, capture its actual request ID and
   request bytes, then follow that ID through `test-run` and `wait-test`.
3. Bind native row, request, tuple, command, distinct command/source manifest,
   service/result, receipt and brief hashes from that same invocation, then
   wait for terminal status and reap body/sampler processes.
4. CAS-replace only the owned row with the pristine comparator and repeat
   serially. Preserve the 5-GB light floor, 4.7-GB `agent-core-full` floor,
   4-GB continuous stop, and D89d `4,714,564,096` paired dispatch floor.

No current pair, body, REG, gate, or ship credit is claimed. Historical 0249
and 0321 artifacts are retained as named historical inputs only. The later App
`82e9e13...` catch-up is recorded separately in `source-map.json`; it does not
rewrite the existing `4de54db...` controller facts.
