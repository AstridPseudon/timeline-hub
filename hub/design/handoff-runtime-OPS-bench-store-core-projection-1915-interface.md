# Core projection 1915: compatible API (early, source-only)

Accepted creator field: `report: str`, optional, absent/empty means no projection. Exact strict UTF-8 bytes, maximum 1 MiB, no `{bench_path}` substitution. Only derived destination `tests/provision/<validated registration name>.txt`; no report path input. Existing ensure signature/callback timing and callers without report unchanged. Creator reads actual fully verified `.provision-report` after verify; core owns projection with suite/env in existing recoverable transaction, validates hash before mutation, rolls creation back and eviction forward, and removes only owned report. Metadata holds exact text/digest. Creator receipt fields/verification remain creator1912 ownership.

Confirmed lease1910 finding: genuine existing unmanaged suite rows conservatively acquire ALL registered managed dependencies. No shell parsing or string path authority. Missing/tampered managed rows still refuse. Legacy unknown benches never become eviction targets.

Readonly publication/deletion algorithm unchanged; EACCES stop persists. No combined creator/host/test service/readonly fixture permitted. Final source/tests/manifest follow under this unique prefix.
