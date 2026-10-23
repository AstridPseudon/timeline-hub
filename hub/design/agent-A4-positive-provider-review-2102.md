## Result

**FAIL — faithful replay, no provider defect shown.**

The four App packets replay exactly, but all are refused by the registered Agent provider with:

`dependency_changed: patch references media outside Runtime-verified inputs`

Cause: the synthetic base has `dependency_manifest.media: []`; each `doc.patch` adds a new registry `media_id`, while the request contains no authenticated media selection or verified-input authority.

The provider guard is contract-faithful. The v2 contract requires new media to already be Runtime-verified. The immediate test limitation is incomplete synthetic authority; the production-level owner is App A2/A3 (with Runtime coordination), because the captured App request is not authority-complete for adding prepared media. No evidence supports changing the Agent guard.

## Lossless evidence

All four matched the original packet exactly:

- Request JSON and serialized bytes
- Length and SHA-256
- Canonical base closure
- Source pins
- Production caller binding

Hashes:

- Missing hold: `38afc047…c66c738a1`
- Explicit null hold: `a422aaf9…e268269f1`
- Subminimum duration: `99cf8093…603f17f5`
- Incoming transition: `e1f05b38…35f602825`

The App report’s accepted response is mock transport/client-adoption evidence only, not Runtime or provider acceptance.

## Verification

- Author-retained combined targeted lane: `4 failed, 16 passed`; all four failures were the same provider guard, with no realm writes. I did not rerun the known-failed bodies.
- Collection, with and without `ORCH`:

  `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_a4_after_positive_doc_patch_witness.py`

  Result: `4 tests collected`.

- Ruff: passed.
- Mypy: passed.
- Vendor lock: `ok runtime.lock.json`.
- Artifact manifest: `artifacts.json is current`.
- `git diff --check`: passed.
- Base-to-HEAD changed path: only `tests/editing_conformance/test_a4_after_positive_doc_patch_witness.py`.
- Worktree clean; no product, schema, pin, generated, environment, or existing-test changes.

Runtime provenance:

- Execution pin: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`
- Lock producer: `34eac0041b0891e9011966b39bcbd26053fde5bc`
- Runtime origin: `https://github.com/banodoco/banodoco-workspace-runtime`

## Unverified behavior

Because the provider fails before candidate completion, these remain unproven:

- accepted versus v2 `merged` response semantics;
- canonical response and full receipt schema;
- complete records, bindings, effects, dependencies, history, and undo steps;
- full mirror scope;
- provider-derived step effects;
- preview/null receipt and structured error envelopes;
- canonical acceptance of the subminimum and incoming-transition cases.

The witness also uses `get(..., [])` for reads checks, so it does not distinguish omitted `reads` from explicit `reads: []`; the packet itself omits the field.

## Smallest next step

Provide authentic Runtime-verified media authority for each prepared asset through an existing semantic media-selection path or an equivalent Runtime verification hook. Do not fabricate `dependency_manifest.media`, raw media info, or read declarations. Primary owner: App A2/A3, with Runtime boundary support if required.