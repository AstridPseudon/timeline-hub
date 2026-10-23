# Runtime handoff: R0 public-trim independent review

**Disposition: qualified facts; Runtime R0/C0 provenance PASS, App normal pure preflight FAIL due stale historical `95bd` tuple. Evidence-only; no product change.**

## Canonical normal profile

The independently verified supported normal profile is:

```text
producer=astrid-runtime
producer_version=sha256:d5f98db3213e91d96d4a7f5b184e17bf5268357b37dc06eaa5b568c4b788a572
source_commit=34eac0041b0891e9011966b39bcbd26053fde5bc
source_tree=9853574865f25e08284e82ffb26c0bdecaa16a30
manifest=contract/artifacts.json
manifest_sha256=7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d
artifact_count=78
timeline_schema_sha256=sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd
contract_version=0.2.14
protocol=workspace.v1
component_manifest_sha256=sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
runtime_schema_digest=sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c
```

Independent finite-JSON/hash/`git show` checks matched all 78 official artifact
entries. App `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` has exactly 13 lock
mappings; all 13 actual consumer files match both their lock digests and the
official frozen `34e` source blobs.

## C0/R0 wire-shape result

Frozen `34e` schema and generated client audit passed unchanged for the complete
C0 v2 surface: `api_version`, project/timeline scope, exact base pair, commands,
label, steps (`command_ordinals`, patch, reads), merge mode, request reads,
`dry_run`, and HTTP `Idempotency-Key`; accepted/merged `{data, receipt}`;
conflict/refused/invalid reason/current-head/code/path/hint/suggested-command;
and preview `would_status` with a null receipt. No Runtime wire/schema/client
change is indicated.

## App-owned stale tuple

Current App `tests/e2e/local/support/public-trim-preflight.ts` and its pure test
still assert historical `95bd`:

```text
commit=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
tree=d3a290b407fa61e6ab2d476f50c068073f70df00
producer_version=sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
schema_artifact=sha256:f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
artifact_count=76
```

The historical App lock at `4301732b6a3cfddd80d8878524bddf337b2d951d` is
consistent with that old tuple. The current normal App lock is consistent with
`34e`; the narrow pure test therefore fails causally at producer-version
comparison (`d5f98…` actual versus `54205…` expected), before source comparison.

The minimal recommendation is App-owned: point normal preflight at exact `34e`
values, or isolate the `95bd` values as a named historical fixture. Preserve
valid, wrong-producer, forged-digest (manifest/vendor-lock authority), mismatched
source/path, and extra-entry negatives. The helper’s digest regex is syntax-only,
not forged-content verification. Do not retire a guard, authorize regeneration or
adoption, create a new tuple, or claim a standalone helper as production proof.

The real fixture calls the preflight before its journey, while the normal caller
uses the generated App `commitTimeline` path and App `runtime.lock.json`; no live
caller/browser/socket execution was run in this review.

## Verification limits

No product/App/Runtime/test/schema/generated/pin/lock write, regeneration,
daemon, install, cleanup, full suite, browser, socket, or live production run was
performed. Runtime `git diff --check` and worktree cleanliness passed. The narrow
pure App preflight was run only to establish the stale-tuple first cause.
