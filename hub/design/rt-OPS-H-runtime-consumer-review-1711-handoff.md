# H3 handoff

The current Runtime `full` route for `base=tl/one-head` resolves Agent `88a9dfe9856344ade53d88d7dd4ec9883bd7a38c` and rewrites `ASTRID_CHECKOUT` to `/home/user/work/wt-int/agent-88a9dfe98563`. `external=agent=2d7b…` is generated from the configured command before rewriting and is dependency/cache metadata; it is not the provider source path.

The original H run is best attributed to the matching `88a9…` Agent source based on the pre-request 14:13 runner backup, worker base, ref resolution, and Runtime import bootstrap. Preserve the qualification that this is a source-backed inference: the original summary was recovered after runner death, the runner log includes line 470/477 errors, and no effective command or module-origin capture survives. The Runtime fixture selects the checkout via `sys.path`; it does not directly assert the provider module's `__file__`.

Keep the original result attached to Runtime `d3969a86e62f5f8761533499e7d2e3f97195932b` + Agent `88a9…` as the strongest supported pairing: **7,385 passed, 75 failed, 25 errors, 26 skipped, 13 xfailed**. It is a failed suite. This review closes only the metadata/source-routing diagnosis; it does not claim all-target pass or PHASE H qualification. H owns the final full-suite classification and any phase-gate rerun. Do not retry or retarget this original proof.
