# D135 reviewed delivery-build installation validation

## Result

The exact reviewed candidate from commit `d45e07dfb305c41d588fe168a2518d5ffa1c4954`,
tree `92401b1abc84a0a6a23d5b0d9b9bfebeb41638a2`, was installed once at the authorized
entrypoint. The source and installed SHA-256 is
`ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`, mode `0755`.
The exact predecessor was `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`,
retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build.20261025T201050.398733Z.bak`

The backup is regular, single-link, mode `0755`, and has the exact predecessor hash.

## Preflight and installation checks

- Source physical check: PASS — regular, single-link, mode `0755`, exact candidate hash.
- Target physical check: PASS — regular, single-link, mode `0755`, exact predecessor hash.
- Reviewed source identity: PASS — commit/tree exactly as above; worktree clean.
- Active builder check: PASS — no `delivery-build` executable process before or after.
- Normal delivery test-service status check: PASS — no active delivery status; observed records were terminal (`pass`, `fail`, or `withdrawn`).
- Host process probe: not run, as required.
- Candidate staging: PASS — same-directory temporary, exact hash/mode verified.
- Atomic replacement: PASS — `os.replace` followed by directory fsync.
- Installed read-back: PASS — exact candidate hash/mode/regular single-link.
- Backup read-back: PASS — exact predecessor hash/mode/regular single-link.
- Neighbor/protected-input check: PASS — all pre-existing direct `bin` neighbors were unchanged; the only new live artifact is the authorized predecessor backup.
- Source/test preservation: PASS — source hash `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`; focused test hash `c00401bb11401ffaa8929f887c4ccf69600bcf6f312c81ba41d4d54c9e3286bf`.

The first post-install verifier returned nonzero because its comparison did not exclude the newly authorized backup from the neighbor set. This was a verifier-scope false alarm after the replacement had completed; read-only verification confirmed the expected backup and no pre-existing neighbor drift. No second install or fallback was performed.

## Installed smoke and focused caller controls

- `TIMELINE_DELIVERY_SCRIPT_SHA=ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --help` — PASS.
- In-memory `compile()` of installed bytes — PASS.
- The same eight focused unittest controls were executed with a private in-memory test substitution so the caller used the installed path and the exact candidate SHA environment. Result: **8 passed**. This includes ancestry refusal before staging writes and invalid relative/symlink private inputs returning exit 2 without traceback or output writes.
- No production positive preflight, real build, ZIP, fresh clone, network, package/venv/Store/child, hub write, or full suite was run.

## Review findings and decision boundaries

D135-REV-1 remains independently fixed and reverified. D135-REV-2 is resolved by this Codex installer. D135-REV-3 is resolved in the derivative source manifest and receipt by naming the actual reviewed tree; the candidate script was not changed. Positive delivery remains D59-gated.
