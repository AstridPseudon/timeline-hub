# D10 source-owner landing follow-through — 2026-10-20

## Exact source state

- App consumer/source-copy deletion is landed at `e245a4791f9270177408a7745d8397ad7b6f81a1` (tree `dce13f17a6873e86af00e06dea25624d719d31ad`). Its normal refresh used real Astrid source `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1` and passed the no-preload central verifier: 146 vendor files, 11 Home public imports, exactly nine exclusions.
- Agent current integration is `f82da322077ed0ac0c58966a0815b5ffc02fc0cc` (tree `c585e729962883c25efd04742b750d2ecc1e1b6b`).
- Approved Agent D10 source candidate is `da9a5bd860f3a16563bc2b0b0ef55ab042183091` (tree `a9a78a0818dbe7e22147b522679a350a5c87fd22`), whose immediate source-policy ancestor is `e4d23250429d17f5262aeea126c19a6d324bcaf7` (tree `d81e3af7a4864a770e4b57cd00ab0579ed7b67f2`). The cumulative common ancestor used by the source gate is `0b2f662e32e1a6818d58f9cf12130f0a89fb5a3b` (tree `4b578bf70c0fb217ea80ad1f022f6bc3ef554c92`).
- `da9a5bd8` is not an ancestor of current Agent integration (`git merge-base da9a5bd8 f82da3` is `0b2f662e`), so it is pending Agent owner merge/merge-forward. No App vendor-refresh request is emitted yet; using the candidate SHA as an App checkout SHA would be false provenance.

## Approved D10 source scope

The candidate removes exactly the nine Agent wrapper/resource sources (six animations, `text-card`, and two transitions), retains the descriptors/custom overrides, obtains public membership from the existing Composition registry, and fails closed for unknown missing rendering components. It does not add a registry/API/metadata policy or remove custom source authority.

## Qualifying evidence

- Agent source gate at the exact candidate: 23 targeted tests passed; `scripts/gen_element_catalog.py --check`, Ruff, `py_compile`, `git diff --check`, private bundled registry generation, and TypeScript typecheck passed.
- The exact focused command set was:
  `PATH=<pinned-node-first> ASTRID_NODE_EXECUTABLE=<pinned-node> ASTRID_REMOTION_PROJECT_DIR=/home/user/work/app PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/gen_element_catalog.py --check`;
  `... python -m pytest -q -o addopts= tests/core/test_editor_element_catalog.py tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_effect_registry_target.py tests/packs/test_composition_elements.py`;
  Ruff, `py_compile`, `git diff --check`, `scripts/gen_effect_registry.py --bundled-only`, and `tsc -p remotion/tsconfig.json --noEmit`.
- Pinned Node was `v20.19.4`, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`. Composition public13 was 77 files, archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Normal root package qualification passed `npm run typecheck` and `npm run bundle -- --bundle-cache=false`; no browser/render/install/full suite was claimed.

## D10 row and replacing tests

Proposed row text for the manager-owned ledger (not edited here):

`D10 | APP COPIES DELETED; AGENT SOURCE OWNER MERGE PENDING | App e245a4791 is consumer-first complete with normal provenance. Agent da9a5bd8 is approved but not yet integrated onto current f82da322. After owner merge, refresh App from the real merged Agent checkout SHA and rerun the existing no-preload normal vendor verifier; do not mark the Agent source row deleted before that refresh.`

Use these focused replacements/controls for the source row: `RemotionElementGenerationTest.test_canonical_registry_winner_is_not_replaced_by_local_shadow`, `test_public_composition_supplies_source_less_builtin`, `test_public_membership_uses_composition_registry_api`, `test_missing_non_public_component_is_diagnostic`, `test_unknown_rendering_component_is_not_silently_omitted`, plus `tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current` and the existing App `publicCompositionElementRegistry.test.ts`, `vendoredTimelineCompositionAliases.test.ts`, `TimelineRenderer.public-host.qualification.test.tsx`, and no-preload `d10-final-central-without-preload.test.mjs`.

## Limits / next step

No product files were changed in this follow-through. The Agent owner must merge/merge-forward `da9a5bd8` onto current Agent integration, publish the resulting real checkout SHA, then App may perform the normal vendor refresh and rerun the existing verifier. Do not edit the manager ledger from this worker. No browser, render, install, network, or full suite was run here.
