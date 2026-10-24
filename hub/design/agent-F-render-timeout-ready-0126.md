## Report

- Added runner: [tools/run-render-timeout-ready-0126.sh](/home/user/work/wt/agt-F-render-timeout-ready-0126/tools/run-render-timeout-ready-0126.sh)
- Records source hashes, revisions, Node/profile provenance, import origins, and child admission.
- Target row:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
```

Validation:

- `bash -n ...` — passed.
- Preflight — correctly blocked without a current immutable child.
- Source-profile probe — failed before validation with `ModuleNotFoundError: No module named 'runtime_protocol'`.
- Original 45-second test — not executed.
- `git diff --check` — passed.

Current provenance: Agent `2b2c1a02`, Runtime `8ea0766f`, Node `v20.19.4`, profile `819acf`; validator SHA256 `361f759e...9686`.

Manager must request the normal child using the tuple recorded in `BLOCKED`; requirements are `requirements/proof.lock`, SHA256 `236d5be9...c778`. Existing `c886` is stale Agent `c36ca8c9` and is unsuitable.

Commit message written to the requested path. `BLOCKED` marker created.