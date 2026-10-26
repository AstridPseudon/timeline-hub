# Validation

Read-only checks performed in this continuation:

- `id -u` — `0`.
- `/proc/self/uid_map` and `/proc/self/gid_map` — both `0 0 1`; UID65534 is unmapped.
- Static manifest/AST check — **exit 0**; all 11 immutable candidate names matched recorded mode and SHA256; AST parsing passed for the complete derivative, `run-final-delivery.py`, and `delivery_gate_build.py`.
- `jq empty` on the prior purpose map and immutable source manifest — **exit 0**.
- Static phase audit — source-owner checks precede caller stage-owner checks, and direct D68 stage controls are separate from caller `run_wrapper` controls.

No checker, staging, builder, installer, service, browser, socket, full suite,
or product test was run. No chown, privilege experiment, source edit, install,
canonical write, cleanup, or branch operation was performed.

Prior evidence, not rerun: Sol-1637 complete checker **exit 1** at UID65534
fixture setup after positive and stale-upstream PASS; same33 historical
production route retained actual PASS; Sol-1627 and whole-path-1627 retained.
