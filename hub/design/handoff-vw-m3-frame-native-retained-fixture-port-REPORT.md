# Native retained frame fixture port

## Result

Ported the existing frame-parity fixture onto a bounded native pre-start setup.
The original 640x360 / 30 fps source generation is unchanged: one gradient PNG,
the existing 45-frame marked VP8 WebM, and the existing 1-second 44.1 kHz WAV.
The canonical closure keeps the original image/video/audio clips, media registry,
occurrence duration, and output dimensions/frame sequence. It is prepared in a
new harness realm by the bounded helper, then accepted after daemon startup by
the ordinary authenticated `timeline.restore` commit route.

Changed App test infrastructure only:

- `tests/e2e/timeline/viewing-parity/native-fixture-helper.py` calls the native
  Runtime `TimelineCommitStore._validate_closure` and `_persist_closure` inside
  the existing store mutex/transaction. It does not write a head, history,
  command, certificate, capture reference, SQL, or compatibility publication.
- `fixture.ts` generates the existing media before startup, invokes the helper,
  restores through `/v1/.../commit`, and reuses the existing closure/media
  assertions.
- `DirectHarness.start` gained an optional `beforeRuntimeStart` callback and
  `seed: false`; the default M1 startup path is unchanged.
- Added one no-browser integration test for native bootstrap, ordinary restore,
  zero legacy composition writes, and a forged task request with zero object
  writes.

The native ShotPayload carries the required internal revision link inside the
payload. This is a native closure requirement; the legacy publication builder
only carried the same identity at the outer image level.

## Source and witness

- Runtime witness tuple: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Agent witness tuple: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Recovered prior witness: restore pass, capture positive pass, and four forged
  config/registry/digest/missing-media refusals before CAS/task writes. Its six
  stdout lines are preserved in the adjacent `-COMMAND.md`.

## Tests

- `npx eslint tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts` — 5 PASS.
- Central named suite `integration-viewing-native-retained-fixture` — 1 PASS; no browser or renderer. The successful run used `/home/user/work/agent` and `/home/user/work/runtime` as the central service's compatible source paths and the shared read-only Runtime/Agent virtualenvs.

The original browser four-case parity suite was not run here. Final browser/render qualification remains pending the approved App capability/public13 and Agent13 pair, as requested.
