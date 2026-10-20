# vw-m4-build-staging-guard-custody-review

Decision: APPROVE

Source SHA: `96eb54b509b35ffe1e076b20c78a264bff77627d`

Reviewed only:

- `tests/packs/rendering/_helpers.py`
- `tests/packs/rendering/test_presenter_scene_capability.py`
- `tests/packs/rendering/test_private_node_modules_staging.py`
- corrected historical helper `f816-root-build-safe.sh` in the source worker record

The live fixture now calls the reusable extraction and node-module staging
helpers. Scope traversal is one top-level iteration; scopes are real private
directories and only package leaves are links made with `ln -sfnT`. Realpath
and linked-ancestor guards protect directory and leaf writes. Focused tests
cover idempotent scope staging, linked-scope refusal, tar-through-scope
refusal, and unchanged borrowed graph entries. The presenter assertions remain
intact; the diff only replaces inline staging calls. No product edits were
made.

Evidence and limits are recorded in the worker `report.md` and `COMMAND`.

