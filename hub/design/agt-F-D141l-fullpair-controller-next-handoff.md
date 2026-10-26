# F D141l full-pair handoff

Status: `MEASUREMENT_RECORDED`, not qualification.

The existing reviewed controller dispatched the cut member and then the
pristine member serially through the normal `request-test` → dispatcher-owned
`wait-test` route. Cut returned native service
`agent-agent-core-full-1026100428-24814`, status `fail`, exit `1`; pristine
returned `agent-agent-core-full-1026103030-25513`, status `fail`, exit `1`.
The actual cut failure was retained while the controller proceeded to
pristine. The final controller exit was `1`.

The controller floor witness was `6479253504` bytes. Native service traces
showed minima of `6542942208` (cut) and `7407423488` (pristine), both above
the continuous 4 GB stop. The exact native and body traces, raw stdout/logs,
JUnit XML, request/summary/status/exit/snapshot files, manifests,
runmanifests, source-before/after origins, CAS backups, row readbacks and
KEEP markers remain retained at the absolute paths recorded in `result.json`.

The sole owned row was restored after each member; the outside-row digest was
unchanged. No mismatch was found, so the supported withdraw route was not
needed. No REG, gate, candidate, product, or full-suite credit is inferred.

The wrapper's own continuous sampler had an arithmetic-format error and is
marked `UNREADABLE` in `disk-trace.txt`; exact native traces are appended and
the limitation is disclosed in `validation.md`. This must not be described
as a fresh wrapper available-byte witness.
