# Agent PRIVATE017 normal current-preserving pin staging

Status: **staged only**. This is the exact normal Agent consumer staging for
Runtime PRIVATE017. It is not an integration adoption, public qualification,
native/HTTP/lifecycle qualification, all-current qualification, or final ZIP.
The complete document repair remains unmerged; the current document safety
stopgap remains in the staged tree.

## Flat identities

- Agent base commit: `4c98d5043e2ac7f301326a3fe31f9b1d72b8b5a0`
- Agent base tree: `a8e4bc44e00dcea9f546622677d0026473e47c0c`
- Agent base parents: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` and `7c9ef2ed5e70da1a13e89278496c74321453955a`
- Current preservation reference: `f777b04d1c90c189ee2565a0d68060692cb24287`
- Prospective worktree tree, including untracked files: `0215154fd47dbbabdc2020cc8b48627ce8aade38`
- Harness commit SHA: pending; no commit/merge/rebase/checkout was run by this worker.
- Runtime producer path: `/home/user/work/wt/rt-pin-42a7203f`
- Runtime producer commit: `42a7203f49bb89f299ec854cfbf2b1444e815a7c`
- Runtime producer tree: `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`
- Runtime producer parent: `da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406`
- Runtime package: `0.2.17`
- Runtime health/schema digest: `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`
- Runtime raw timeline bundle: `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f`
- Runtime artifact manifest: 76 entries, file `sha256:0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f`
- Runtime artifact version: `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`
- Agent source commit/tree: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` / `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`
- Agent schema raw SHA-256: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`
- Agent schema canonical SHA-256: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`
- Agent schema shape: 65 definitions / 37 `EditCommand` clauses

## Generated consumer byte diff

- `astrid_runtime_client/__init__.py`: old `4069c15e93b72d504cc882b18dbae119fcd9e7a5186f3c06238bad304276a206`; new `7e602716931ca03930e1801596e098b83aa7344b7c54fe34b26e2308f82f15b2`; exact producer artifact.
- `astrid_runtime_client/contract_metadata.py`: old `40d329430bf40c36876b12adc08c6c59f2a4b7e980da8b963305b6b375a43aea`; new `e6d8286ca342bbb7a7d6554bb37357548b95bf2df123e7d46f60d6fce8fe53b1`; exact producer artifact.
- `astrid_runtime_client/generated.py`: old `61b55a2e14127a9cc360054a67f6c0b6259ff7eb75bcf58e9c788da344c234ca`; new `e58f0fbe652b2baf8a3cd113def468dde3b32d1522f946a733c2b2a3b8461350`; exact producer artifact.
- `astrid_runtime_client/timeline_commit_types.py`: old `f33a509da59352fed877d2c0ccc5e2e150d17494a0a28e4de811d2c268382644`; new `af295393450db831c43e6559eb0aa8f645e6cd0e79f4beb078df949bdb58e0d3`; exact producer artifact.
- `runtime.lock.json`: normal selector/version/file-hash update to Runtime `42a7203f...` / artifact version `a0dc430a...`; no hand-generated client edit.
- The other 11 locked consumer artifacts remain byte-identical to the base and match the producer manifest. All 15 lock entries match producer bytes.
- Runtime generated Python carrier is `AgentWrite.insertion_order: NotRequired[list[str]]`; Runtime generated TypeScript carrier is `insertion_order?: Array<string>`. The field is optional and absent-key-compatible; null and non-string values remain refused by the source schema/validator.

## Current preservation

- Applied the `7c9ef2ed5..f777b04d1` current-parent delta onto the ordered stage.
- Current transcript/source hydration, sheet frontend, document architecture, and current tests are retained byte-for-byte on non-overlapping paths.
- Restored the current parent’s `TimelineSession.commit/commit_many(..., verified_media=())` API and forwarding through the ordered-aware execution call after overlap review found the ordered stage had dropped it.
- `native_checkout.py` and `sync.py` retain both current source hydration and the ordered carrier/ack validation. No later position, producer, effects, caption, raw-init, or occurrence-trim proposal was added.
- No native caller, HTTP route, lifecycle body, outer execution, private body, renderer, install, build, browser, or render lane was run.

## Exact commands and results

Passed:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout runtime 42a7203f49bb89f299ec854cfbf2b1444e815a7c 'PRIVATE017 normal Agent vendor pin exact immutable producer'
=> exact detached checkout created at /home/user/work/wt/rt-pin-42a7203f

(cd /home/user/work/wt/rt-pin-42a7203f && python3 generators/generate.py --check)
=> passed

(cd /home/user/work/wt/rt-pin-42a7203f && python3 scripts/artifact_manifest.py --check)
=> contract/artifacts.json is current

git -C /home/user/work/wt/rt-pin-42a7203f diff --check da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406 42a7203f49bb89f299ec854cfbf2b1444e815a7c
=> passed

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py update runtime.lock.json --producer /home/user/work/wt/rt-pin-42a7203f
=> updated from exact Runtime 42a7203f49bb

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-42a7203f
=> ok; all locked bytes match producer manifest

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_vendor_lock.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py
=> 82 passed in 204.74s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py
=> 23 passed in 0.97s

custom producer/lock proof: all 76 producer artifact hashes and all 15 locked consumer hashes exact
custom source proof: raw/canonical schema hashes and 65/37 shape exact
custom carrier proof: Runtime generated Python/TypeScript optional insertion_order and health digest exact
custom source parity: six non-overlapping current-parent paths byte-identical to f777b04d1
changed Python compile() syntax check: passed
git diff --check: passed
```

One attempted mixed targeted command also included the existing provider test
file:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_vendor_lock.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_commit_provider.py
=> 196 passed, 1 failed in 227.16s; the failure was the existing subprocess
   test test_move_reload_and_inverse_import_no_renderer, which did not inherit
   ASTRID_RUNTIME_CHECKOUT and therefore failed before provider setup while
   looking only at default Runtime paths. It was not used as pin evidence.
```

No full suite was requested. No install/build/browser/render/HTTP/native/live
lifecycle/outer/private-body execution was requested or claimed. The missing
`venv-runtime` path was not recreated or modified; the exact immutable Runtime
checkout was used through `PYTHONPATH` for bounded Agent imports.

## Decision and next step

The only judgment call was the overlap restoration of `verified_media`: it is
an existing current integration safety/custody argument in `f777b04d1`, so it
was retained while preserving the ordered source changes. The candidate is
ready for independent review of the prospective tree and harness commit; do
not treat it as all-current qualification or activate it before the Runtime
owner’s separate ordered lifecycle node.
