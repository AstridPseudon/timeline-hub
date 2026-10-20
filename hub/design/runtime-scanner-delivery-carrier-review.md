# Runtime scanner delivery-carrier review

## Verdict

**REQUEST CHANGES — do not apply the exact patch.**

The existing staging seam is sufficient and is the right smallest mechanism:
copy extras after the generated `README.md` and before the existing
`SHA256SUMS`, then let the normal ZIP path include them. No new ZIP framework
or scanner release is needed. The proposed 65-line patch is close, but its
path and failure guards do not yet meet the bounded-carrier requirements.

## Identities

- Installed packer: `/home/user/timeline-hub/hub/kit/bin/delivery-build`,
  SHA-256 `a3e7ab2ba9cd051cc64d5fd3806b4b49b2eb1909f5063968282970ccc91fa34e`.
- Unapplied proposal:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-unapplied.patch`,
  SHA-256 `5a0600658e4a2f538c81f16b6855846f4e335bd6ebe9ed70fee90d5539a51d16`.
- Scanner ZIP:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-scanner-v1.0.8.zip`,
  12,221 bytes, SHA-256
  `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`.
  It contains exactly `README.md` (7,033 uncompressed bytes) and
  `owner_film_cliplook_scan.py` (38,074 uncompressed bytes), both regular
  stored ZIP members with no owner-film data.
- Owner instructions:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-owner-scanner-delivery-payload-owner-film-differences.md`,
  10,519 bytes, SHA-256
  `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`;
  `cmp` passed against `/home/user/timeline-hub/hub/design/owner-film-differences.md`.

## Findings

1. `parse_extra` and the direct `lexists(target)` check correctly reject the
   tested `..`/absolute/backslash destinations, source symlinks, and direct
   destination collisions. However, `add_extras` creates/uses every parent
   directory with ordinary path traversal. If an intermediate destination
   component is a symlink, `shutil.copyfile` follows it and writes outside the
   staging root. The synthetic control `redirect/escaped.bin=source` reproduced
   this exact escape.

2. Only `ValueError` is caught around `add_extras`. A non-directory parent
   produces an uncaught `FileExistsError`; a source disappearing or a copy/mkdir
   error can likewise leave a partially populated staging directory and a
   traceback. The normal output is not published in that case, but the failure
   is not cleanly atomic/fail-closed.

3. The existing final `zipfile.ZipFile(zip_path, "w", ...)` writes directly to
   the destination. If the requested atomic-failure requirement includes the
   published ZIP itself, the next bounded patch must write a private temporary
   ZIP, close/verify it, and atomically install it without overwriting an
   existing destination. This is a small delivery-path hardening, not a new ZIP
   framework; it should not be silently claimed as fixed by the proposed
   `--extra` staging change.

## Required next unit

Keep the existing seam and `--extra DESTINATION=SOURCE` interface, then add
small controls that:

- preflight all extras and reject duplicate/occupied destinations;
- reject symlinks in every destination parent and create/copy without following
  destination symlinks (dirfd/`O_NOFOLLOW` or an equivalent bounded check);
- catch copy and directory-creation failures, remove the private staging tree,
  and report one clean argument/build error with no ZIP output; and
- if final-artifact atomicity is in scope, publish the ZIP through a private
  temporary path plus atomic replace/refusal of an existing output.

Then rerun only the supplied small synthetic help/compile/traversal,
intermediate-symlink, collision, and injected-copy-failure controls. Do not
apply/install the carrier, build a four-repo ZIP, run the owner scanner, or
make an owner-film claim in this unit.

## Review evidence

- `(cd /home/user/timeline-hub/hub/kit && patch --dry-run --verbose -p0 < <proposal>)` — **PASS**; all hunks apply cleanly, with no file changed.
- In-memory compile of the exact proposed helper insertion — **PASS**.
- Synthetic controls — **PASS** for valid regular-file copy, traversal,
  absolute path, backslash, source-symlink, and direct-collision refusals;
  **EXPECTED GAP** for intermediate destination-symlink escape and uncaught
  parent `FileExistsError` as described above.
- `python3 /home/user/timeline-hub/hub/kit/bin/delivery-build --help` against
  the installed a3e7 packer — **PASS** baseline; it correctly has no `--extra`
  because the proposal remains unapplied.

No Runtime worktree/product file, shared packer, ZIP, owner input, or release
artifact was changed. No full suite, four-repo dry run, owner-film scan,
renderer, macOS, or release claim was performed.
