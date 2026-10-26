# D141l controller continuation

This packet is source preparation only. `check` never installs a row, calls
request-test, calls test-run, calls wait-test, submits a request, or starts a
body. `dispatch` is the later real controller action. It admits once at the
recorded 4,714,564,096-byte floor, installs one existing
`agent-core-full` row by atomic CAS, obtains the returned request directory,
captures the request bytes and native row, writes the own immutable brief and
dispatch receipt, then calls the existing `test-run` and `wait-test` route.

The two phases are serial. The original row is restored only after the phase's
terminal result, and the next phase CASes from that exact restored row. The
receipt contains the actual returned service ID and request/row/command/source
hashes. The terminal result is separate, so no request, row, or admission hash
cycle can cause an old row to execute.

The source-only checker runs the same dispatch function against private tiny
doubles of those three existing commands. It labels that result isolated and
never uses it as live admission.
