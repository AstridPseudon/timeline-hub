# V1 integrated proof — PASS

Source verified at Agent HEAD `ffcec5d330732a25c4d2b4050618ea18339e5148` (tree `04b7324fb68a68a71857c9c877aca15cc49ecf79`), the requested `tl/integration` base with reviewed `25991306f`, metadata repair `838431382`, and review `b23e95872` merged. Worktree remained clean.

The requested lane passed exactly: `64 passed, 163 subtests passed` for `test_timeline_roundtrip_fixture.py`, `test_timeline_selected_schema.py`, `test_meta_validator.py`, and `test_timeline_characterization.py`. Artifact freshness passed (`scripts/artifact_manifest.py --check`, plus 9 artifact/schema tests). `vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-691a9436` passed.

All 15 locked files are byte/hash exact against producer checkout `691a9436ce3dbf2dcbfeaf959c85143c165fe4e2`; canonical top/clip/track `meta` passes production compiled-schema validation and Agent read/write round-trip. Production caller imports the generated client and v2 DTOs. Scoped Ruff passed; normal baselines are unchanged at Ruff `2151/2151` and mypy `1915/1915`.

Current V3 package, R1, P1, and V4 commits are preserved as HEAD ancestors. The `ae68a1bea` metadata reload seam remains separate/unmerged. This is V1-only evidence: do not claim R0/R2r/U4v2 or actual Runtime provider reload/wire acceptance from producer `691a9436`.

No product/test changes, regeneration, pin mutation, shared dependency writes, or full/browser/farm suites were performed.
