# Handoff: P2 D21 OPS snapshot guard repair

P2 is ready for the farm’s authorized actual run. The only edit is the existing
`app full-e2e-three-products` row in ORCH `tests/suites.conf`: it now accepts
direct App411/exact-tree or the test-service synthetic single-parent App411
snapshot with the same exact tree. Clean, receipt, Agent/Runtime, artifact,
all-three-body, and selector-8 guards remain in place.

Evidence:

- row syntax: `bash -n` PASS;
- bounded pre-global P2 prefix against direct App411/tree: PASS;
- offline controls: direct source ACCEPT, exact-tree synthetic single-parent
  App411 ACCEPT, wrong parent/source ref/tree/dirty/body REFUSE;
- P2 row SHA-256:
  `8fd8f5b39a25f5572efc1d31993a8ff84659cc2b92e6448edc9f9dee09a2a2ef`;
- current P3 row SHA-256:
  `53118de6a2a88b3d21496f47049b01bb188870c253cc990b2defda265b021d7d`.

Farm limits: run only the authorized P2 actual 8-tour after host readiness.
This worker did not run browser/global setup/build/native boot/HTTP/service/full
or duplicate body suites. No synthetic commit was manufactured and no shared
install or Git ref was changed.
