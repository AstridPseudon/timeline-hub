# Handoff: P1/P3 operations bench binding

Updated only the existing ap2-P1-chain-h6 and ap2-P3-gate5-h6-0348 rows in
scratchpad/orch/tests/suites.conf.

- Child: venv-agent-child-ap2-p1-f611-1343
- Remotion planned name: agent-remotion-ap2-p1-f611-1346
- Tuple: App 4282d776497f651bce3870d1d9e6a37a5eaa2030, Agent
  f6116e1b658514021cbbf08d5a6f16a240523f1a, Runtime
  8592822fd11275540f596562f43c715676f2bc0f
- Child receipt/marker: success, 92 pins, installed/import/CLI/freeze/read-only
  validation; multiline import-origin marker accepted by the smallest
  validation-only predicate fix.
- Remotion receipt/artifact: absent; both rows intentionally report
  NOTREADY and dependent stages NOTRUN.
- P1 --list: exactly 2 selectors (accepted 1, refused 1).
- P3 --list: exactly 1 Gate-5 selector.
- P1 body SHA256:
  f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133
- Gate-5 body SHA256:
  0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14
- Row SHA256: P3
  2118e19fa1a259cf790d75001555395d451bd8643bd8024a5e56a2ac0f485e17;
  P1 899b9087db06b980e9af90d3f8d76ff715332b6e8f0fd81ec8eed1756241ee56.
- Outside-target-rows SHA256:
  a692019e830e965c198eabc747e1d3ef3424df487db6292975f0b36760c13e3e

Do not run the original body, build, browser, service, global setup, seed,
or full suite from this worker. Request the normal Remotion dispatcher bench,
then use the central serialized test service.
