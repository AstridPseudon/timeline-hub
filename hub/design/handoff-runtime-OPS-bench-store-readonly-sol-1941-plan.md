# D27 API/order plan

Add optional `seal=None` as the last Store.ensure argument. For new entries only: build movable staging; retain owner/node and sync checks; rename into final entries; call the bounded creator seal callback on the final path; then run the unchanged final custody verifier before registration/projection/index or lease exposure. Reuse still runs the same final verifier and never reseals. Child final readonly moves out of staging build into final seal; runtime gets an explicit final readonly seal too.

Owned removal will validate entry identity/path, stable lease inode and owner/node marker before fd-based owner-write restoration on owned directories. Never follow or chmod symlinks; compare opened inode to observed inode and recheck directory names before restoration/removal. Recovery takes exclusive creation lock as well as eviction locks. Existing report/index transaction, latest-two-plus-leased policy, source and final-path custody assertions remain intact.

All source/tests export under the new unique flat 1941 prefix; historical packets remain unchanged. Fresh complete queued creator fixtures and lifecycle/regression suites run only in this run own TMPDIR, allocated <=20 MiB. Author qualification only, no installation or production eviction claim.
