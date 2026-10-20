# Current Agent Remotion smoke schema snapshot

## Result

Updated only `remotion/__smoke__/bundle.mjs` so its `_ASSET_ENTRY_ALLOWED` snapshot matches the current generated public10 schema. The three additions are `derivedFrom`, `media_id`, and `origin`, in the generator's sorted order.

## Contract check

This is an expectation repair, not a schema relaxation. `SharedAssetEntry` in `astrid/core/timeline/banodoco_schema.py` declares all three fields; the canonical `_ASSET_ENTRY_ALLOWED` contains them; `scripts/gen_remotion_types.py` serializes that allowlist in sorted order; and `astrid/core/timeline/validators/registry.py` validates the same closed field set and distinct nested/value behavior. No generator, schema, compiler, runtime, provider, pin, fixture, or readiness behavior changed.

## Evidence

- Red-before offline probe: actual generated Root bundling passed, then the old 12-field expectation failed against the actual 15-field generated `_ASSET_ENTRY_ALLOWED`; observed additions were `derivedFrom`, `media_id`, `origin`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/gen_remotion_types.py /tmp/vw-m3-current-root-smoke-schema-types.generated.ts` followed by `cmp -s /tmp/vw-m3-current-root-smoke-schema-types.generated.ts remotion/src/types.generated.ts`: passed (`GENERATOR_PARITY=0`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/vw-m3-current-root-smoke-schema-pytest tests/timeline/test_asset_registry_contract.py tests/timeline/test_timeline_roundtrip_fixture.py`: **31 passed, 2 subtests passed**.
- `/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check remotion/__smoke__/bundle.mjs`: passed.
- After offline probe using Node `v20.19.4`, borrowed read-only Remotion graph, actual generated Root bundling, and exact 15-field check: **passed**, bundle output `/tmp/remotion-webpack-bundle-XwVAaz`.
- `git diff --check`: passed; product diff is one file, three insertions.

## Not run

The full `remotion/__smoke__/bundle.mjs` was not invoked because its `selectComposition` phase requires the prohibited localhost/browser path and manager final-SHA grant. No browser, renderer, socket, install, network, export, full suite, codec, or fixture run is claimed.

## Decision / next step

No escalation or source bug found. The harness can commit this one-file smoke expectation repair. A manager-authorized full smoke may be run later under the exact pinned Node/browser controller when that grant exists.
