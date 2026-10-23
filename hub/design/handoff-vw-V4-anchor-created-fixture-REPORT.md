# V4 anchor-created fixture report

## Change

Added the canonical native creation claim to the initial `track.create` request
in `tests/editing_conformance/native_word_anchor_fixture.py`:

```json
"created": ["parent/track:initial"]
```

This is the existing native capture contract form. No tests, recipes, provider,
Runtime, generated files, pins, or manifests were changed.

## Evidence

- Required integration command: **7 failed, 47 passed in 49.04s**.
- Captured-output rerun for durable trace: **7 failed, 47 passed in 48.47s**;
  see `targeted-test.log`.
- `git diff --check`: PASS.
- Ruff on the single changed fixture: PASS (`All checks passed!`).
- Typecheck: N/A; the change adds only a literal command metadata field.

The original 54 setup errors are gone: the real Agent provider and pinned
Runtime now accept the initial native creation and execute the anchor cases.

Protected source blobs equal Agent base `f894c3c9d`:

- `test_native_word_anchor.py`: `d1ca4b79922d78d7c39a0e64fd8e479dfe725df0de5d348550b54f1f8399a717`
- `word_binding_recipe.py`: `5f22b3f0c8d9a81a5bd5cc520fc5295c3049ab89c9c9f46f565dd1c87f55307c`
- `test_word_binding_recipe.py`: `4722227e6e347778bb491f4f660e0a8d049ee074026b23e43de939a65d47142a`

Pinned compatibility checks: Runtime `ad823e0a0f5be4a7acf1d3006df6f794709da63d`,
official client source `34eac0041b0891e9011966b39bcbd26053fde5bc`, artifact
manifest SHA-256
`7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`, and all
15 `runtime.lock.json` mappings matched.

## Remaining blockers

Per the task instruction, no repair was attempted after the first non-setup
failures appeared. The seven failures are:

1. Two review-source counterexample cases report `details.status == "invalid"`
   instead of the preserved expected `"refused"`.
2. Two equal-text undo cases refuse with `intervening publication wrote a
   guarded address`.
3. The retained-source rebase case refuses with `provider dependency union
   omits a captured read`.
4. The half-open acceptance case reports `"invalid"` instead of `"refused"`.
5. The stale-anchor window case reports `"conflict"` instead of `"refused"`.

All failures are in existing semantic/status/dependency behavior; no test
expectations were changed. The required all-54 PASS source-candidate proof and
the independent integrated-home proof remain unverified.
