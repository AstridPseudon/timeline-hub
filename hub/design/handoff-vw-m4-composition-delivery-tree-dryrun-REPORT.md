# Composition M4 delivery handoff

## Result

Prepared one linearized, binary-capable Git patch from the observed local
`origin/main` to `tl/integration`, and one Git bundle for `tl/integration`.
The patch was applied to fresh archives of the observed main tree outside the
product repository. The resulting tracked file set, modes, Git blob IDs, and
symlink status exactly match target tree `13e375534fffd704305eced5686699d2c8c9c948`.

This is a composition delivery artifact only. It does not claim the M4
foundation or the overall ZIP gate.

## Observed refs

- Observed local `origin/main` commit: `67b8aa3d0d6831d3e3504a340ff583c3da253707`
- Observed local `origin/main` tree: `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`
- Target `tl/integration` commit: `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`
- Target `tl/integration` tree: `13e375534fffd704305eced5686699d2c8c9c948`

No network fetch was performed, and no latest-main claim is made.

## Patch

`handoff-vw-m4-composition-delivery-tree-dryrun-composition.patch` is one
`git diff --binary --full-index --no-ext-diff --no-renames` tree diff, not a
format-patch series or merge-history replay.

- 463,276 bytes
- SHA-256: `ffcde5f77a2b10fc34a101e838c8ef24cf2ac2cb106089c3b5d8a8061cb39206`
- 109 changed paths; 7,674 added lines and 773 deleted lines

## Fresh-archive proof

Two independent fresh `git archive origin/main` extractions were made under
the worker's private staging directory, outside the product repository. On
each archive, `git apply --binary --check` passed, `git apply --binary` passed,
and the normalized manifest comparison passed.

The target contains 113 tracked files: 113 mode `100644`, zero executable
files, and zero symlinks. The target manifest uses each target path's exact
mode and Git blob object ID; the applied archive's file bytes were hashed with
the same Git path-aware hashing and matched exactly.

The first archive was also checked against the observed main manifest before
application. The normalized target manifest SHA-256 is
`919b30bc07bc5f7cf2329b28760d7945db6d376a5d330b160c0981ff42f6ca9b`.

One redundant post-application `git apply --check` against the already-patched
first archive was refused, as expected for a non-idempotent patch. It was not
treated as delivery evidence; the second fresh-archive check above is the
correct recheck.

## Bundle

The single bundle is held in the worker output directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-composition-delivery-tree-dryrun/handoff-vw-m4-composition-delivery-tree-dryrun-composition.bundle`

`git bundle verify` passed. It reports a complete history and the exact head
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8 refs/heads/tl/integration`.

- 239,217 bytes
- SHA-256: `f0395412890441d45956abcb1a4eb41caef0c250ffe1da9c214c28797d2f4461`
- The flat handoff `...-bundle.sha256` contains this bare SHA-256.

## Tests and limits

No product test, build, browser, npm, or full-suite command was run. The task
requested delivery mechanics only and records prior build/full evidence at
this exact tree without rerunning it. The checks above are delivery proof,
not product qualification.

The composition worktree remained clean throughout. No commit, merge, rebase,
reset, push, ref mutation, dependency installation, or shared-install write
was performed.
