# Report — F D141 installation review

**FAIL — `FAIL_CUSTODY_LIMIT`**

- Canonical targets match accepted candidates exactly:
  - README: `48013c…f9fc02`
  - gate-results: `506e44…63a55`
- Backups match declared preimages; all files are regular, non-symlink `0644`.
- `delivery-build.render_readme` was inspected and invoked function-only with four controlled repo inputs. Placeholders, fences, disclosure count, and all 32 IDs passed.
- Current delivery inventory contains exactly 568 genuine outside files and matches the retained manifest maps.
- Genuine pre/post outside-file conservation is unobservable: the installer lost its in-memory pre-install map after CAS when an over-strict fallback assertion failed; the follow-up serialized the current map as both before and after.
- Separate review disk sampler: 3 durable 5-second samples, minimum 5,708,038,144 bytes, above 4GB floor; PID 9, exit/wait 0, reaped. Installer sampler lifecycle remains unobservable.

No product tests, builds, ZIPs, source repairs, or installation actions were performed. Evidence written to the requested seven files; `DONE` marker and commit message created. Worktree is clean.