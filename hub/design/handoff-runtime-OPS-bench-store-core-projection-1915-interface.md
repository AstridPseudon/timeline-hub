# Core projection 1915: compatible API (early, source-only)

Accepted creator field: `report: str`, optional, absent/empty means no projection. Exact strict UTF-8 bytes, maximum 1 MiB, no `{bench_path}` substitution. Only derived destination `tests/provision/<validated registration name>.txt`; no report path input. Existing ensure signature/callback timing and callers without report unchanged. Creator reads actual fully verified `.provision-report` after verify; core owns projection with suite/env in existing recoverable transaction, validates hash before mutation, rolls creation back and eviction forward, and removes only owned report. Metadata holds exact text/digest. Creator receipt fields/verification remain creator1912 ownership.

Confirmed lease1910 finding: genuine existing unmanaged suite rows conservatively acquire ALL registered managed dependencies. No shell parsing or string path authority. Missing/tampered managed rows still refuse. Legacy unknown benches never become eviction targets.

Readonly publication/deletion algorithm unchanged; EACCES stop persists. No combined creator/host/test service/readonly fixture permitted. Final source/tests/manifest follow under this unique prefix.

## Final source contract

Nonempty `report` must exactly equal the regular, owned, single-link `.provision-report` at the already verified final entry path. Core reads bounded raw bytes and strictly decodes UTF-8. The registration stores both exact text and `report_sha256`, covered by the registration hash. Reuse must supply identical registration. Empty/absent report stores the original metadata shape and neither claims nor checks unrelated same-name files in provision/. No path argument and no interpolation of report text exists.

The provision parent must be a physical directory owned by the current UID; core creates it privately only when applying the first actual report projection. File UID, regular type, single link, size, exact bytes and SHA256 are validated before changes. Creation rollback removes its report; durable eviction rolls forward all dependent registrations and their exact owned reports. Recovery accepts only the exact journal baseline/target bytes; tamper leaves pending refusal. Unchanged owned reports are checked before recovery writes as well. Empty provision directories may remain; no unrelated report is deleted. UTF-8 reads/writes preserve newline bytes, including unrelated CRLF suite rows.

No change to ensure signature, verifier ordering, publication rename, deletion algorithm, lock identities/inheritance or latest-two-plus-held retention. A genuine existing unmanaged row must match its current exact repo/suite/command; fallback returns all registered names for normal `acquire`. Missing, ambiguous, tampered or retired managed rows refuse.

Production creator1912 source already calls ensure with `report`, verifies persisted bytes, and emits its receipt fields. Existing production test-run calls names_for_suite then acquire; the exact unchanged exported lease seam is exercised by our custom-row test. These are source wiring checks and a tiny writable private caller exercise, not permission to run the combined child fixture or any live service.
