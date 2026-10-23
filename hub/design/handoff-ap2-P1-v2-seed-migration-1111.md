# Handoff: P1 v2 seed migration

Worker `ap2-P1-v2-seed-migration-1111` completed the test-only seed migration
on base `537040f505e49f2122867ba671d06778f77c3f5a`.

Changed file: `tests/e2e/local/three-products.p1-chain.spec.ts` only.

`seedOneClip` now creates a fresh Runtime timeline through public empty-shell
creation, reads the Runtime-owned head pair, imports and verifies the existing
seed video through Runtime media APIs, and submits the original P1 payload via
the existing Agent SDK native/lossless commit path. The final payload equality
guard includes `name`, `slug`, config, registry, clips, occurrences, opaque
data, nulls, and exact field absence. No shared harness or P3 source was
changed; no production App/outbox/provider code was changed.

Static evidence passed:

- exact Playwright `--list`: 2 P1 tests;
- scoped ESLint;
- embedded Python `compile`;
- `tsconfig.app.json` and `tsconfig.node.json` no-emit typechecks;
- `git diff --check` and one-file diff scope.

No browser/HTTP/body/full/service/request-test/native-14 run was authorized in
this slice, so live current-R5 seeding and the original P1 bodies remain for
the next independent review/current-port qualification.
