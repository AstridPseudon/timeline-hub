# Runtime Main infrastructure touched for M4 disclosure

The unpublished Main-merged Runtime candidate carries Main’s health and
service declarations/observations, the matching generated `/v1` client
surface, and the existing `runtime_protocol.platform.durable_replace` helper
used by durable file publication. It does not add a second door, relay, or
timeline writer. The candidate’s source tuple and qualification boundary are
in the [current Main-merged source packet](runtime-mainmerged014-paired-candidate.md);
Runtime deletions and retained paths remain in the [Runtime deletion ledger](deletion-ledger.runtime.md).

The retained safety invariants are concrete: a bootstrap abort or readiness
failure before ready remains a failure; a stop after readiness remains orderly;
health identity is checked before accepting the owner; and durable replacement
keeps the POSIX parent-directory flush behavior. Existing coverage includes
`tests/test_schema_validation.py::test_health_schema_has_exact_closed_runtime_identity_contract`,
the generated-client health identity checks in `tests/test_generated_client.py`,
`tests/test_profile_services.py::test_immediate_exit_service_never_reports_running_and_marks_startup_failure`,
the startup/ready-stop cases in `tests/test_foreground.py`, installed lifecycle
coverage in `tests/test_portable_lifecycle.py`, and
`tests/test_platform.py::test_posix_durable_replace_fsyncs_both_parent_directories`.
Copied-fixture freshness/timestamp repairs are test setup only; they do not
change product expiry semantics.

Evidence is Linux-only. The latest Main014 full `29693` remains RED, and any
later full remains pending until its real result is recorded. Public013 remains
the immutable published Runtime 0.2.13; Main014 is the separate unpublished
Main-merged 0.2.14 candidate and is not a consumer pin or release. The current
Composition delivery piece is `e7ef7a`, not `ac918`; the reviewed scanner
insertion is installed, but there is no final ZIP. No owner-film, macOS,
all-writer, or M4-completion claim follows.
