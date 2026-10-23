**PASS for the provider migration. App consumer remains unwired.**

Added `clip.duplicate-media` through the existing extensible carrier. All six original parent-media functions remain AST-identical to c36. Ordinary fully authored `clip.add-media` requests remain unchanged, including sibling placement.

Interface for App:

- `schema_version: 1`, `op: "clip.duplicate-media"`, `version: "1"`.
- `select: "parent/clip:<source>"`.
- `args: {id, old_media, media}`; both selections contain exactly `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`, resolved through `port.selected_media`.
- `intent: {ownership: "parent"}`.
- `created`: new asset reference when absent, followed by `parent/clip:<id>`.
- Witness batch read: parent `["config","clips"]`, with sorted membership and original order.
- Step: `{id,label,intent,tags,command_ordinals:[0],patch:[],reads:[...]}`; its field read captures the complete source row at `["config","clips","id:<source>"]`.
- Retain the full V2 request and reply envelopes, including full V2 undo.

The recipe clones normalized metadata and transition, starts at source end, applies the `.05` duration floor, ripples later same-row clips, and preserves unrelated rows.

Validation:

- Focused pytest: **190 passed, 1 integration deselected**:
  ```bash
  env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-8ea0766f" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/editing_conformance/test_prepared_video_birth.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_occurrence_media.py
  ```
- Central suite `agt-G4-video-sol-2250-managed-video`: **1 passed**, using Runtime `8ea0766f`, tree `6047ac3033c3594b8f83db3afd8bb2c47cafa6d6`. Preview, accept, exact retry, structured refusals without writes, and full V2 undo passed. [Durable requests, origins, and results]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G4-video-sol-2250-agt-G4-video-sol-2250-managed-video-1023230035-9608/log.txt) total 236 KB.
- Frozen `34eac004` and execution Runtime schemas validate the exact new request.
- Scoped Ruff passed; private mypy passed for four files, with zero baseline/new diagnostics.
- Vendor lock, artifact manifest, and both c36 diff checks passed. Pins unchanged. No full suite requested.

Earlier witness attempts exposed setup errors, unstructured media failures, and a legacy-envelope inverse refusal. The final witness uses the required full V2 envelope; no inverse core changes were made.

Next: independent review, then App wiring to this interface. Mounted App parity and merged replies were not exercised. Commit message and `DONE` written.