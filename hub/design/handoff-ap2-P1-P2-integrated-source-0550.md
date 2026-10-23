# Handoff: P1/P2 integrated source proof — 2026-10-23

PASS — bounded read-only source proof on exact App head
`cffa91c93e80717cec1a4e740fae67140394eb88`, tree
`8eb4d915848663c5cd1ea9ee2eabb8c14404f411`.

## Exact source result

`18354adfa..cffa91c93` has exactly the three permitted paths:

```text
tests/e2e/local/support/astrid.ts
tests/e2e/local/three-products.p1-chain.spec.ts
tests/e2e/local/three-products.p2-tour.spec.ts
```

Integrated blobs equal the reviewed donors:

```text
support/astrid.ts                  6bc055e90ba47be204acd2c943e8eed4e8cad0c6 == 38fbbc993 donor
three-products.p1-chain.spec.ts   f59f3f4e1964c1f2a38ccfcb8869b176cb0ff6b2 == 5c5794718 donor
three-products.p2-tour.spec.ts    45a8088fafd72a462409e444c0294e8a35682a0f == 67eda1803 donor
```

Outside-path guard passed. Production `src`, normal/frozen Runtime 34e source,
generated client, exact Composition archive, schema/lock/launcher/suite/body
files are unchanged. Runtime lock source is `34eac0041b0891e9011966b39bcbd26053fde5bc`;
the exact archive SHA-256 is
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

## Exact checks

Passed: App and Node tsconfig typechecks; P1 list exactly 2; P2 list exactly 3;
scoped ESLint for the three paths; `git diff --check`; offline import of
`astrid`, `astrid.sdk`, `astrid_runtime_client`, and `runtime_protocol`
using the pinned Agent/Runtime checkouts; private graph integrity (80 files,
package 0.0.14, generated exports resolve only from `dist/`).

No full/browser/build/HTTP/socket/live-service/body run was performed.

## Reused evidence and limits

Independent reviewed behavior evidence is reused because the integrated blobs
are exact donor matches. It remains source evidence only. The known P1 body
readiness failure (23041) remains; P2/P3 remain blocked on mounted Undo/move
production callers. No H3 GO, tour/body credit, or scenario-DONE claim follows.

See the worker report at
`/home/user/work/wt/ap2-P1-P2-integrated-source-0550/report.md`.

