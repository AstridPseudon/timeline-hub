## Report — U4a D88b

Implemented the authorized provenance-only adoption. Only `runtime.lock.json` changed:

- `source_commit`: `a3cd1a…` → `6634a17f3ffd885567ba3c91b6c7a560df7375a4`
- Before hash: `850d761e…`
- After hash: `d66e7f2b…`
- 15 mappings verified; schema `867f…` and config `4d74…` unchanged.
- Runtime HEAD/tree: `6634a17f…` / `47b37671…`

Checks:

- `refresh_runtime_client.py`: exit 0
- `vendor_lock.py check ... --producer /home/user/work/runtime`: exit 0
- `artifact_manifest.py --check`: exit 0
- `git diff --check`: exit 0

No tests run, per adopter instructions.

Merge was requested, but the receipt incorrectly merged `tl/agt-D86-publication-0127`; Agent home remains at `258d2ccc…` / `45ab160f…` with the old `a3cd1a…` provenance. Marked `BLOCKED`; re-request should occur after this worker’s harness commit.