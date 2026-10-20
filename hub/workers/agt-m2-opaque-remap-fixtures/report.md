## Report: agt-m2-opaque-remap-fixtures

**Result:** one shared fixture file is now the authority for the opaque item-reference remap, the contract doc is written, and the targeted tests pass. Changes are uncommitted in `/home/user/work/wt/agt-m2-opaque-remap-fixtures`; the commit message is at `workers/agt-m2-opaque-remap-fixtures/commit-msg`, and `DONE` is created.

### What changed
- **`tests/editing_conformance/fixtures/opaque_remap.json`** (new, schema `opaque-remap/v1`): a top-level `opaque` block (the `org.example.notes/v1` namespace) and 8 cases, each with `item_ids`, `payload` and a hand-written `expected`. Cases cover:
  - `item_id` and `id` codecs, including equal mirrors and a mismatched `id`.
  - metadata vs root source-link descriptors, and a non-mapping `metadata` falling back to the item.
  - unmapped ids.
  - unknown namespaces and selectors left byte-identical.
  - `0` and `0.0` left untouched.
- **`tests/timeline/test_opaque_remap_fixture.py`** (new): runs every case and compares canonical JSON bytes, not Python `==`, so `0` and `0.0` stay distinct. It also has the one permanent test, `test_prototype_keys_round_trip_as_plain_own_data`, which round-trips `__proto__`, `constructor` and `prototype` through set, get, encode, digest and the inverse remap. It passed with no fix needed.
- **`tests/timeline/test_authoring_bundle.py`**: the end-to-end test now takes its opaque block from the fixture instead of an inline copy. Its expectations are unchanged.
- **`design/opaque-remap-contract.md`** (new): the exact allowed fields, the byte-for-byte rule, the source path and the fixture path.

### Tests run
- Targeted, via `request-test` → `wait-test` (ID `agt-m2-opaque-remap-fixtures-targeted-1020035228-18581`): `tests/timeline/test_opaque_remap_fixture.py tests/timeline/test_authoring_bundle.py tests/editing_conformance/test_recipe_m1_commands.py`. Result: **pass, 100 passed, 1 deselected** (the deselected test is outside my change). Agent tree `1c062c71c0b430f94d229197e73ffbb0157e5093`.
- No full suite was requested.

### Decisions and notes
- **Test-running rule conflict.** The orchestrator rule says run targeted tests directly. The brief says "targeted via request-test only". I followed the brief.
- **The fixture is a pure unit fixture**, not an end-to-end one, because the real remap IDs are hashes of project, timeline, occurrence and shot. Hardcoding them would have made the fixture brittle. The end-to-end test still covers the real identities through the fixture's `opaque` block.
- **The `_remap_known_item_references` code was left as is.** It already matches the M1 decision (explicit codec, equal mirrors, descriptor fallback). No product change was needed.
- **Caveat for App:** `JSON.parse` does not distinguish `0` from `0.0`. The TS `remapItems` test cannot check the integer/float rule from parsed values alone. The contract says to compare canonical text, so App needs its own canonical encoder or a text-level check for the numeric cases.
- **Not verified:** I did not mutation-test the new cases against a broken remap. They were checked only by the passing run.

### Recommended next steps
- The orchestrator merges with the Agent branch. App's `authoringBundle.ts` should load `tests/editing_conformance/fixtures/opaque_remap.json` via hub-sync and follow the contract's canonical-text rule for numerics.
