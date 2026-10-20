# Runtime insertion handoff

The exact approved owner scanner is ready at:

`payload/owner_film_cliplook_scan-v1.0.8.zip`

It is 12,221 bytes, has SHA-256
`204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`, and
contains exactly `README.md` (7,033 bytes) and
`owner_film_cliplook_scan.py` (38,074 bytes). The current instruction payload
is the byte-identical copy of the authoritative
`/home/user/timeline-hub/hub/design/owner-film-differences.md` at
`payload/owner-film-differences.md` (10,519 bytes, SHA-256
`969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`).

Read-only inspection found no existing extras/input carrier in
`/home/user/timeline-hub/hub/kit/bin/delivery-build`; it only stages the four
repo patch/bundle outputs, generated README and `SHA256SUMS` before creating
the ZIP. `delivery-build-owner-scanner-extra.unapplied.patch` adds one
repeatable `--extra DESTINATION=SOURCE` input to that existing staging flow.
It accepts only regular non-symlink source files and relative POSIX
destinations below the staging root, rejects traversal/absolute destinations,
copies before the existing `SHA256SUMS`, and does not add a ZIP framework.

The exact apply/build/owner commands are in `COMMAND`. The patch is UNAPPLIED;
the Runtime-owned script and four repo source worktrees were not changed.
