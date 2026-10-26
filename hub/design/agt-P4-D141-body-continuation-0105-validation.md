# P4 D141c body continuation validation

- Source gate: `PASS_OPERATIONAL_SOURCE` from independent review 0106; prior 0101 `FAIL` and historical 1347 zero-selector failure remain preserved.
- Admission: dispatch witness `5,169,483,776` bytes; current admission above `4,700,000,000`; continuous stop floor `4,000,000,000`; no other live Agent heavy body observed.
- CAS install: existing `tools/install_p4_launcher.py` only; preimage/outside-row equality are recorded in `registration.json`; installed row equals reviewed candidate SHA `21f407285a7f1476e9507add8d8d54e723776d6ce5074ac7cbbe8be5773c2f0b`.
- Readback: input manifest SHA `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f`; materialized normal manifest has the same SHA; request ID `p4-d141c-normal`; body destination is separate.
- Exact request: `bin/request-test integration:agent p4-current-becfe-http-3legs --no-cache` — submitted once; service `agent-p4-current-becfe-http-3legs-1026011042-10086` reached terminal `PASS`, exit `0`.
- Actual body command retained with `run -- -m pytest`, three unchanged selectors, cleared addopts, disabled cache provider, timeout `45`, later `-m integration`, and JUnit under the preserved 0055 body-evidence path.
- JUnit actual artifact: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-P4-D141-operational-return-0055/evidence/body-evidence/p4-d141c.xml` SHA `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`; 3 tests, 3 passed, 0 failed, 0 errors, 0 skipped.
- Per-ID results and hashes are in `result.json`; raw service/body logs remain private and retained at their actual paths.
- Product typecheck/lint: not applicable; no executable product delta.
- Body evidence only. App owns cumulative P4 verdict; source/body PASS is not GO or ship credit.
