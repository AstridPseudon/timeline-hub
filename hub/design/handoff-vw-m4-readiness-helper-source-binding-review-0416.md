# Handoff: readiness helper source-binding review

Candidate `d65c50d4b565bbfa7d63b6ff4e3a04f802ca3d13` versus base
`7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`: **REQUEST CHANGES**.

The extracted `_remotion_package.py` is executable validation authority, but
`remotion_runtime._runtime_inputs()` still binds only `Path(__file__)` for the
Agent validation source. The readiness artifact's probe-source digest covers
only `_schema_probe_source()`, and the consumer rechecks the same incomplete
input list. A private ephemeral-copy negative showed a helper-byte mutation
left the input fingerprint unchanged. Minimal repair: add the helper's trusted
source path to the existing `paths` list / `_file_binding()` loop and add the
stale-artifact negative; no new authority, store, or DTO.

Targeted package lane: **6 passed, 1 deselected**. No full suite run.
