# Composition M4 independent flat-delivery review

## Result

The prior composition delivery handoff was independently checked against the
actual local source tuple. One fresh private archive of observed
`origin/main` accepted the prior binary patch, and its complete tracked file
set matched `tl/integration` exactly by path, Git mode, Git blob ID, bytes,
and symlink status.

This is one composition delivery artifact only. It does not claim the M4
foundation, the overall ZIP gate, or an all-repository exit.

## Source tuple

- Worktree: `/home/user/work/wt/vw-m4-composition-delivery-independent-flat`
- `origin/main`: `67b8aa3d0d6831d3e3504a340ff583c3da253707`
- `origin/main` tree: `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`
- `tl/integration`: `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`
- `tl/integration` tree: `13e375534fffd704305eced5686699d2c8c9c948`
- Worktree status: clean
- Network fetch/latest-main claim: none

The current source-generated patch SHA-256 is
`ffcde5f77a2b10fc34a101e838c8ef24cf2ac2cb106089c3b5d8a8061cb39206`, equal
to the prior handoff patch. The patch is a single binary-capable tree diff,
not a format-patch series.

## Fresh archive proof

- `git archive origin/main`: PASS, one fresh private staging archive.
- `git apply --binary --check`: PASS.
- `git apply --binary`: PASS.
- Target manifest: 113 tracked files, all mode `100644`, zero symlinks.
- Applied manifest: 113 entries, all mode `100644`, zero symlinks.
- Exact sorted mode/blob/path comparison: PASS.
- Git path-aware blob hashes and file bytes: PASS.

The composition repository has `core.sharedRepository=true`; its archive tar
entries materialize as `0664` under the shared umask. The private archive was
normalized to the source Git modes (`0644`) before applying the patch. This
changes no bytes and makes the mode comparison test the Git tree modes.

## Bundle proof

- Bundle: prior worker handoff bundle, 239,217 bytes.
- SHA-256: `f0395412890441d45956abcb1a4eb41caef0c250ffe1da9c214c28797d2f4461`.
- `git bundle verify`: PASS; complete history and no prerequisites.
- `git bundle list-heads`: exact `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8 refs/heads/tl/integration`.
- Private clone from the bundle by `-b tl/integration`: PASS.
- Bundle ref/tree: exact target commit/tree above.
- Private clone `git fsck --full --no-reflogs`: PASS.

## Flat transport

The new deterministic transport is
`handoff-vw-m4-composition-delivery-independent-flat-composition-delivery.tgz`.
It contains exactly two members:

- `composition.bundle`: the verified bundle bytes above.
- `manifest.json`: the scoped independent-review manifest.

The archive uses sorted member order, fixed epoch mtimes, numeric zero
ownership, fixed `0644` member modes, and gzip with no timestamp/name. It was
re-extracted privately; the bundle bytes and SHA-256 matched the source.

- Size: 237,957 bytes.
- SHA-256: `99048bbbeebea85b574568a1dd4e8ddcb41d6560444b7f790593197d5caeae61`.
- A second private build compared byte-for-byte: PASS.

## Tests and limits

No product test, build, browser, npm, Node graph, or full-suite command was
run. The manifest records prior historical composition evidence of `76 pass /
0 fail / 0 skip` on this exact target tree only; that evidence was not rerun
here and is not a foundation, ZIP, or all-repository claim.

The filesystem reported 9,434,896 KiB available after private proof cleanup,
below the requested 10 GiB floor. The generated transport is small (under
1 MiB); no large operation was attempted. This pre-existing capacity shortfall
should be resolved before any heavy follow-on work.

