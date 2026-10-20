# Composition 0.0.12 runtime lock alignment

The corrected Agent adoption is running as agt-m3-consume12-current on the reviewed ce2510034 cohort merged forward with integration. Runtime 94114269 / client 0.2.9 already landed on Agent (04f0df2c).

Evidence: design/agent-review-agent12-cohort.md reports shared runtimes/agent-remotion-0012/package-lock.json lacks eight libc metadata blocks relative to ce2510034:remotion/package-lock.json. Package versions/integrity otherwise match. Host readiness fingerprints the lock bytes. Worker will not modify shared dependencies.

Requested concrete action: align the shared agent-remotion-0012 lock to the committed ce2510034 remotion/package-lock.json, verify byte equality and installed package identity as for 0010. If the adoption changes the lock, worker will report exact new path/hash before qualification. Meanwhile worker completes real theme equality and remaining central tests. No alternate runtime/pin or weakened readiness.
