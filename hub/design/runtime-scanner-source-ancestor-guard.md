# Runtime scanner carrier — source-ancestor guard candidate

2026-10-20 23:34 UTC. This is a revised unpublished candidate; the installed
carrier was not changed.

Viewing’s current installed-script distinction is important: the installed
`delivery-build` is the independently reviewed carrier at SHA-256
`9808c9225aa3d4dff8ee81b3c7fa218173e9130edf43c553cad6e89a078ac3b5`. It is
not the original rejected proposal and it is not the earlier Viewing
replacement patch. Its destination `README.md`/`SHA256SUMS`/collision checks,
intermediate destination checks, cleanup, and atomic final ZIP rename remain
in place.

Against that exact installed script, a regular leaf reached through a
symlinked parent was accepted and copied. The leaf itself was not a symlink,
so the existing leaf check did not see the ancestor. The installed hash stayed
`9808c9225aa3d4dff8ee81b3c7fa218173e9130edf43c553cad6e89a078ac3b5`.

The candidate changes only `_open_extra_source`: it opens `.` or `/`, walks
the lexical source ancestors by directory fd with `O_DIRECTORY|O_NOFOLLOW`,
opens the leaf relative to the final directory fd with `O_NOFOLLOW`, validates
that same opened leaf fd as regular, closes intermediate descriptors, and
returns the leaf fd to the existing copy loop. It does not call `realpath` or
silently remove the ancestor evidence. The candidate and exact diff are
durably kept in the worker folder:

- `candidate-delivery-build` SHA-256
  `3dfd5c28a9be9ab809e6c1fe1e9a83fbf8417ea888afc1b10eec5f751023e990`
- `delivery-build-source-ancestor.patch` SHA-256
  `96d5cf2a2a25ee0de656b6685cfcafcf42cdb6f24a751c91b1e502db37e43e71`

Checks completed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -B installed-source-ancestor-repro.py`:
  finding reproduced; installed hash unchanged.
- Candidate compile and `--help`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B source-ancestor-check.py`: PASS —
  one synthetic symlinked-parent negative, no output on refusal, descriptor
  count unchanged, and exact frozen scanner/instructions payload controls
  copied with hashes `204a7aac78177824219954574f67fcaf4c56ac81620d533ecb376030340c93ee`
  and `969fe3034ca1e7b7aab061ff16575fe7f7d973d9c9ec1f81c347464c4d9da220`.
- Existing private delivery fixture copied into this worker folder and run
  with `DELIVERY_TEST_SCRIPT=candidate-delivery-build`: 11/11 passed.

No install, product/contract/scanner source change, final ZIP, four-repo dry
run, owner scan, or owner-data operation was performed. Independent review is
still required before any installation.
