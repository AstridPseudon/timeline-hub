## Report — FAIL

Read-only whole-path review completed; no App source/tests/registries/repairs changed.

Authority map:

- App: `be98aac54e27`, tree `2839c7e...`, exact parents recorded; target ref `tl/app-P2-P3-e68-current-pure-target-1409`.
- Agent: `68e82c0c...`, tree `aa62e96...`.
- Runtime: `e68cf231...`, tree `a2cbedd...`.
- P1 body: blob `5a2029d...`, SHA256 `50960dd...`; both original case titles remain.
- Historical `18792` remains historical only: App `f8b15af`, Agent `7873804`, Runtime `2a9e347`; 2/2 passed. It is not relabeled or reused.

Findings:

1. `assert_locks()` validates the App lock from `HERE` rather than authenticated `/home/user/work/app` (`p1-current-caller.py:180`). The emitted shell uses App correctly, but source-only admission can falsely pass.
2. `ASTRID_REMOTION_PROJECT_DIR` consumes an unbound bench path. The Composition graph/artifact hash is validated separately; the actual Remotion project is not authenticated.
3. `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` is hardcoded to the venv. Its origin and digest are not checked against the authenticated vendored/runtime schema.
4. Served `dist` has no source/build digest or provenance binding. Ambient `ASTRID_APP_DIRECT_DIST` is not scrubbed; App global setup may reuse an unpinned build.
5. Additional boundary: the C0 wire registry lists the full closure, but production decoding does not validate all reply identity/metadata fields (base/previous/accepted publication IDs, `rebased_onto`, publisher, dependencies/history/guarded-undo). Current P1 evidence leaves invalid/dry-run and several metadata fields unverified.

Checks passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile p1-current-caller.py`
- `python3 -m json.tool p1-current-caller-facts.json`
- Generated shell plus `bash -n`
- All 15 negative controls refused as expected
- `git diff --check`
- Worktree clean

No service, browser, HTTP, native, backend, package acquisition, or full suite was run. Minimal guidance: repair the four consumed-path bindings above, then repeat this independent review before executing the emitted caller.