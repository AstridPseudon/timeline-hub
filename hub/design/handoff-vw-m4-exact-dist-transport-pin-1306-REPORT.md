# Exact App dist transport report

## Result

The d00 App dist was archived as a deterministic regular-file-only tarball and
verified by round-trip extraction. The archive is **244,690,962 bytes**, above
the 50 MB design-sync limit, so it remains in this worker folder and was not
published into `orch/design/`.

Retained artifacts:

- Archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-exact-dist-transport-pin-1306/app-dist-d00a6613.tar.gz`
  - SHA-256: `669b8d13050da29094da9f54d919961566012353fa7ef2e6d808ef6352b98b6b`
- Per-file manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-exact-dist-transport-pin-1306/app-dist-d00a6613.manifest`
  - SHA-256: `8a2de62bf07e933bdc6a8bb47f4ae6b65fd2c5f77f813f3b8023f2cfa1bb5d99`
- Checksum file: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-exact-dist-transport-pin-1306/app-dist-d00a6613.SHA256SUMS`

Source was `/home/user/work/wt/app-pin-d00a6613/dist`, with 339 regular files,
284,372,591 source bytes, and original `dist/index.html` SHA-256
`aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`.
All source files were mode 0644. The archive has 339 regular entries and zero
non-regular entries; archive metadata was normalized for deterministic output
while preserving file modes.

## Safety disposition

- **KEEP d00**: the archive cannot use the normal under-50-MB design transport;
  no independent farm-local dist materialization is available. The READY farm
  request still needs the dist at `/home/user/work/wt/app-pin-d00a6613/dist`.
  Its KEEP marker was not changed.
- **KEEP 0d43**: its source/graph freeze and current Gate6 leases remain active.
  Its actual checkout currently has 37 symlinks, all resolving within the 0d43
  root; its `node_modules` is a separate real directory from d00. The active
  leases are still blockers and were not altered.
- **3ee remains released** by the prior pin-release worker; this worker did not
  touch that marker.

The request’s dist prerequisite was updated only in
`design/run-on-farm-viewing-gate6-1209.md`: it records the retained archive,
manifest, hashes, size limit failure, and materialization destination
`/home/user/work/wt/app-pin-d00a6613/dist`. No command, script, source identity,
or frozen 0d43/C13 tuple was changed.

## Verification commands and results

- Source inventory with `find`, `du`, `sha256sum`, and `stat`: **PASS** — 339
  files, 284,372,591 bytes, required index SHA, all mode 0644.
- Deterministic archive creation with GNU `tar` using sorted file names,
  normalized owner/group/time metadata, and gzip: **PASS**.
- `tar -tzf` / `tar -tvzf`: **PASS** — 339 entries, all regular files, zero
  non-regular entries.
- Private extraction under a worker-local temporary root followed by `cmp`
  and mode checks for every path: **PASS** — all 339 paths/bytes/modes matched;
  index SHA matched. Temporary root was cleaned.
- Actual protected-graph alias scan with `find -type l` and `realpath`: **PASS**
  — 37 internal symlinks, zero resolving outside 0d43.
- Process scan (`ps`) for Gate6/farm/browser/Runtime/Vite/Remotion/test
  processes: **none found**.
- Dispatcher worker status: relevant pin workers are done; no active Gate6
  worker was shown. Unrelated d09 workers were left untouched.
- d00 and 0d43 identity/status checks: **PASS** — exact expected HEAD/tree and
  clean checkouts.

No tests, builds, browsers, farm runs, installs, full suites, or shared
dependency writes were run. The only produced payload is the retained exact
dist transport artifact; the Composition worktree is clean.

## Recommended next step

Keep d00 and 0d43 protected. The farm lead must provide an approved transport
for the 244,690,962-byte archive (or materialize the exact dist independently)
before d00’s KEEP can be released; then re-check the active 0d43 leases before
any pin recycling.
