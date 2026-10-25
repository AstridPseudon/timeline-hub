# F/D134 progress

- Prepared the conditional measurement and preflight recipes without invoking
  a suite preflight body, request-test, collection, provider, control, or test
  body.
- Verified the required frozen tuple read-only: Agent `a4e016b6`, Runtime
  `5e9ad1c6`, App `d8a1cd40`, Composition `635f4de0`; all four paths are clean
  and have the expected origins, trees, and parents.
- Verified static Runtime lock binding, schema-copy equality, pinned profile
  hashes/version, and Node `v20.19.4`. Free space observed was `6669877248`
  bytes, above the `4700000000` start floor and above the `4000000000` stop
  floor; this is not body admission or ship credit.
- Recorded module origins as expected-but-unverified because the existing
  venv may only be used after MAIN's ordinary preflight accepts it.
- Recorded `EXACTMISSING` for the exact-tuple D73 manifest/evidence and all four
  genuine MAIN positive/poison control bindings. The available D73 manifest is
  stale and was not reused.
- Preserved D128's terminal ordinary child-maker refusal and the unchanged
  production suite row. Existing `30693` remains reference-only with no
  deduction or ship credit.
- At 20:00Z, only a MAIN-gated existing-environment run with custody E2E
  `NOT_GREEN` may proceed. Any green custody verdict, missing binding, or real
  safety/classifier/permission/preflight refusal stops the action.
