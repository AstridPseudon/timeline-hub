# Native frame fixture frozen-pair requalification

## Result

APPROVE the bounded requalification of App fixture `dba11c8432cee8df6e8bced4eae4d82e79f2b652`.
The App change remains test infrastructure only. The follow-up delta touches only the
existing `native-fixture.integration.test.ts`; it archives the exact frozen Runtime and
Agent commits into an owned temporary directory, verifies their imports, runs the normal
HTTP `/v1` restore fixture, and verifies the archive manifests after teardown.

The existing default M1 `DirectHarness.start()` seed behavior, native three-media fixture,
ordinary restore route, zero legacy composition writes, and forged-capture zero-write
assertions remain unchanged. No App-owned core/authoring source, Runtime source, Agent
source, generator, pins, SQL, direct head/history writer, browser, renderer, or capture
writer was changed.

## Frozen source proof

| source | commit | tree | archive SHA-256 | files | full manifest SHA-256 |
|---|---|---|---|---:|---|
| Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` | `eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669` | 413 | `a6ec4c76dbc30bf37fd258f2267410ab591fd605181d21e7338a6dff2d6e3627` |
| Agent | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` | `91d4d82f4ee2a251ba6c3706d47efa80411d05e683c64c78a05414d4229b3add` | 3076 | `c436c9e648db306d59dbf728e3294f79d9b971d100ced69fbb1292c17206dada` |

The test output showed `astrid.__file__` under the frozen Agent archive and
`runtime_protocol.__file__` under the frozen Runtime archive. It validated the two archive
roots as the ordered explicit PYTHONPATH entries. After the HTTP run, both file counts and
full manifest hashes were identical to the pre-run values.

The older `2c4`/`d874` direct-service witness remains separate evidence and is not relabeled
as HTTP. This central HTTP proof is the only HTTP attribution used here; the central command
records moving checkout paths, while the test's own source proof records the frozen archives.

## Tests

- `npx eslint tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0 --no-cache` — PASS.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts` — 5 PASS.
- Central named suite `integration-viewing-native-retained-fixture` — 1 PASS, no browser/render/full suite. Successful request ID: `vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141813-18235`.

The first central attempt was rejected by the newly added guard because it incorrectly
included Python's normal empty script-directory entry in the expected PYTHONPATH slice.
That run did not start the Runtime or exercise the fixture. The guard was corrected and the
single fresh request above was made for the changed source tree; it passed. This is recorded
explicitly rather than waived or attributed to the failed attempt.

No browser, render, full suite, install, network, shared dependency/cache write, or moving
integration-ref qualification was performed.

