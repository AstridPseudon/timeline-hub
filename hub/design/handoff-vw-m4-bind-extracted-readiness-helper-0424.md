# Handoff: extracted readiness helper source binding

Candidate `d65c50d4b565bbfa7d63b6ff4e3a04f802ca3d13` now has the requested
minimal correction in worker `vw-m4-bind-extracted-readiness-helper-0424`:
`_runtime_inputs()` binds `Path(_remotion_package.__file__)` through its
existing `_file_binding()` loop. A direct-validation regression uses an owned
ephemeral helper copy, creates and validates the normal readiness artifact,
mutates only that copy, and rejects the stale validated context.

The source-binding patch is intentionally not self-approved. The worker report
contains the exact base tree, flat diff hash, test commands/results, and the
unfiltered-lane environment blocker for the same independent reviewer.
