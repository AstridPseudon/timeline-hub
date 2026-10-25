# D135 installation plan

Candidate: `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca` (`0755`).
Protected installed reference: `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`
(`0755`, unchanged). Harness labels: `D135`, `D135-REV-1`, `PASS_WITH_FINDING`,
`Luna/high/default180`.

1. Independent reviewer checks the immutable source/test artifact and verifies the candidate hash against `source-manifest.json`.
2. Manager supplies a concrete successor D59 tuple when Agent forward integration is complete. The tuple must name the actual Agent-home integration root and exact commit/tree; no proof-pin or local stale `tl/integration` substitution is allowed.
3. Manager installs `ops-delivery-d135/delivery-build` as the production `bin/delivery-build` caller with `TIMELINE_DELIVERY_SCRIPT_SHA` set to the reviewed candidate hash.
4. Manager invokes the caller with private `--delivery-root`, `--work-root`, `--template`, `--gate-results`, and the successor `--source-tuple` plus tuple SHA. The caller must first pass all-repository ancestry preflight.
5. Only after the actual production-main control passes should the manager run the independent exact-CAS kit installation/publish. This worker does not merge, publish, write live roots, or make the ZIP.

Review disposition: reuse substantive independent review `1949` as PASS_WITH_FINDING; perform one
bounded independent **finding-only** review next, limited to this caller boundary and its no-write
exit-2 controls. Do not expand it into a build, ZIP, clone, network, install, or provider review.

The current committed tuple is a historical D59 capture and is included for custody/evidence only; it is not a positive production input because the recorded Agent/Runtime/App tips are not descendants of their current upstream-main refs.
