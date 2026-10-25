Farm table for F-D77-render (held: NOT_READY per Runtime 22:28Z; waiting final inputs + finite footprint bound). Source: design/rt-D77-complete-inputs-2218-inputs.json (24 rows) and the 10-step stage order. Nothing was requested, fetched or run to make this table. Current tuple in that list is the D139 one: Agent 4c4ee35d / tree d50fd98f, Runtime ab1e4f61 / tree 7d8e77b2 (conditional). The old 91398e9d / 1daca2a3 tuple and child 717e53d7 are historical only.

A. Farm can do once the lead says go (normal Farm routes, no new authority)
- request-checkout for the exact D139 Agent and Runtime (farm manager may issue; read-only).
- PROGRAM_ROOT, DATA_ROOT, RUN_ROOT, RESULT_ROOT: private directories under Farm (create only at stage time, via a worker).
- Independent re-verification of the guard receipt (helper 5c821f9e, review cdbb9fd9) before any heavy phase. Scope is wrapper-only (18 controls); no live-stage claim.
- uv 0.11.32 and ffmpeg/ffprobe hashes: already verified by the lead read-only (match). Farm records the receipts.

B. Lead / control plane only
- request-runtime and request-child-venv for the D139 tuple (existing receipts are tied to the old tuple; the Runtime receipt also reused a build from Agent 8657e836).
- Approval for anything that needs it (e.g. running uv).
- Disposition of the finite peak bound and the D89 admission (start >= 6.0 GB + KNOWN footprint).

C. Only Runtime (or its published source) can supply
- ASTRID_RUN: the installed launcher built by installer.launcher.install, final D139.
- INSTALL_MANIFEST: authenticated manifest (schema v1, full SHAs, tool versions/checksums, VibeComfy pin 31f90bb0).
- Finite footprint bound: UNKNOWN_UNBOUNDED; 1,358,509,601 and 1,524,776,481 are planning sums, 1,623,728,128 a lower bound.
- Remotion lock for the current tuple (f4fc0a32 matches only the historical source).
- Browser provenance (required sha 85918a99); none is on Farm.

D. Produced only by the ordinary stage (cannot exist before it; never invent)
- seven-key bindings, installed profile / service declaration / source digest, PY, SITE, ASTRID_PACKS_PATH, Remotion node_modules, installed tool hashes, preflight and render receipts.

Rule: no piecemeal run; core child recipe/security has priority. D77 stays at step 0 until C is delivered and B decides the bound.
