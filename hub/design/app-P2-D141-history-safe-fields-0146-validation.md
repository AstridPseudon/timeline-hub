# D141 finite validation

Status: PASS for finite evidence extraction.

The retained 3118 diff is a strict `assertNativeHistoryEntry` comparison at
`tests/e2e/local/three-products.p2-elements-assets.spec.ts:757`. Its actual-only
additions are two `records.commands[*].bindings[*]` objects. The flat key/path
list is in `extra-fields.json`; no field values, identifiers from the diff,
request payloads, images, or raw diff text are copied there.

The exact earlier automatic-placement case is the PASS case at line 1214 in
the retained original 15203 run. The overall run is correctly recorded as
FAIL (exit 1; 2 PASS, 2 FAIL, 1 ERROR, 3 NOTRUN), while the placement case is
recorded as PASS with its complete history/reload/native-Undo tail.

Source provenance was checked with `git ls-tree`/`git show` against the
recorded App commits. Both recorded App commits resolve the source file to
blob `b6a0ebb2597177c9719f0b23fbc3d135ecdcc019`; the source content hash is
`7cca78274f96c9466d82bea3108f6f8a447462c9cd722c078ab958bc3578d637`.

No tests, browser runs, lint, typecheck, imports, source repair, collector,
semantic investigation, retry, or new request were performed.
