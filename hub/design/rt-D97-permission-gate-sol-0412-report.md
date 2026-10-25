Implemented D97 in the two allowed files. Memo reuse now requires protected DB/WAL/SHM files and directory, owned by root or the loaded Runtime package owner. Ineligible requests fully verify with one condition-specific diagnostic. Ownership/mode changes invalidate proofs, including across Runtime’s own commit.

Validation:

- Central six-file acceptance: **267 passed, 74 deselected**.
- Local five-file acceptance with `--timeout=45` and XML: **263 passed, 74 deselected**.
- Existing finite forward/warm control: **1 passed**. N=3–22 stays at **286 SQL statements, 11 decodes, one new-entry verification**; warm reads stay at **27 SQL statements, zero decodes/digests**.
- Ruff **11→10**, Pyright **74→54**, with **zero added diagnostic identities**. Compile and diff checks pass. Original test definitions remain unchanged.

Different-owner cases use controlled stat witnesses; actual chown is unverified. SHM/directory fingerprints track identity and protection because ordinary reads change SHM. DB/WAL retain all D94a checks. The central files-only service supplies neither custom timeout nor XML; local XML and original central logs are retained.

Exact identities:

- Tree: `e22cdd54b668acea9fe593e6724b34d1a56f7530`
- Store blob: `32eed5b11316a9cf647dc36ed87bce0d2bd9fa86`
- Test blob: `00fd477ee663775ec44c3562f8af00ebb68f919f`
- Final commit SHA awaits the harness; parent is `09a27efc6cac5a25fbcc63cffa7ca4e221336ee8`.

[Exact commands/results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D97-permission-gate-sol-0412/evidence/commands.txt) and [SHA-256 identities/origins](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D97-permission-gate-sol-0412/evidence/source-identities.json) are retained. Artifacts total **1.64 MiB**; commit message and `DONE` are written.

No implementation blocker remains. Next: independent review of this exact tree and curve. Merge/adoption remain held; original P4 under 45 seconds remains unproved.