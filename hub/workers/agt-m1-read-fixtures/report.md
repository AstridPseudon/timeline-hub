## Done

- Fixed `_Timelines.open_bundle` to carry the exact immutable `base_parent.revision_id`.
- Regenerated `cli-surface.json` and `artifacts.json`.
- No product code changed.

## Evidence

- `pytest ...`: **40 passed**
- `scripts/gen_cli_surface.py --check`: current
- `scripts/artifact_manifest.py --check`: current
- `git diff --check`: clean

No full/socket/browser suite was run. Commit message written to the requested worker paths.