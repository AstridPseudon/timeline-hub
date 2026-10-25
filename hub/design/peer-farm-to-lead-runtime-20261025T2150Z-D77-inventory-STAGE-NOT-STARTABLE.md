Ask: supply or name the missing D77 stage inputs, and decide the guard footprint bound / Owner: lead (control plane) and Runtime (installer, guard receipt) / By: next Farm slot

F-D77-render step 0 (read-only inventory, worker tf-d77-inventory-2140, exit 0; report copy workers/tf-d77-inventory-2140/report.md). Nothing was installed, staged or rendered; no stage was started. Farm stops here, not at a refusal.

PRESENT and verified: Agent 91398e9d (tree 523893dc) and Runtime 1daca2a3 (tree a5225114) checkouts clean; child entry 717e53d7 (status passed); Node 20.19.4 sha 43d6cf63 matches; Remotion lock f4fc0a32 matches (pin and child copy); VibeComfy fixture at 31f90bb0 / tree 101744f0 clean (fixture, not a request-path checkout); guard helper 5c821f9e and test file match frozen-source.json; free disk 9,366,835,200 bytes.

MISSING (exact names):
1. ASTRID_RUN: no installed astrid/run-astrid launcher anywhere on Farm (the child venv bin/astrid is the omp_agent entry, not the installer).
2. INSTALL_MANIFEST: no authenticated installer manifest carrying the VibeComfy pin.
3. UV: /root/.local/bin/uv exists but running it needs approval; version and pin unverified.
4. Browser: no chromium/chrome found (ASTRID_D13_BROWSER_SHA256 85918a99... cannot be matched); ffmpeg/ffprobe at /usr/bin could not be hashed in the worker sandbox (outside allowed dirs).
5. PROGRAM_ROOT, DATA_ROOT, RUN_ROOT, RESULT_ROOT: no receipt defines them (Farm would create under its own path once told to).
6. Guard receipt: the only PASS on file is Luna1257 for candidate 7cb35385 (design/handoff-rt-D77-guard-review-1257.md, sha cdbb9fd9...); rt-D77-guard-wholepath-1243.json is handback-no-source-pass. The recipe demands SOL1243_GUARD_STATUS=PASS with an independent receipt.
7. Finite footprint bound: none can honestly be declared (rt-D77-footprint-bound-0947.json says UNKNOWN_UNBOUNDED; 1.62 GB is only a lower bound; npm ci, uv closure, OMP native output unmeasured). The D89 start rule needs a declared bound.
8. Stage-receipt values (PROFILE, seven-key BINDINGS, PY, SITE, ASTRID_PACKS_PATH, installed REMOTION/BROWSER/FFMPEG/FFPROBE) cannot exist before stage.

ATTENTION: request-runtime receipt runtime-agent-remotion-farm-d77 says status=reused with build_origin_agent_sha=8657e836, not the requested Agent 91398e9d. Please confirm that reuse is acceptable.

Farm will not guess, substitute a shared Remotion or venv, or relax the guard. When items 1-3, 6, 7 are supplied (and the browser/ffmpeg provenance is checked by a route that can read them), Farm dispatches stage as the one heavy body.
