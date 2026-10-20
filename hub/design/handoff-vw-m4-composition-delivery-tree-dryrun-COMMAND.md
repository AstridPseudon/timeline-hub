# Composition M4 delivery commands

These are the commands used from the clean composition worktree. `$ORCH` is
the existing orchestrator scratch path; all generated delivery artifacts are
outside the product repository.

```bash
repo=/home/user/work/wt/vw-m4-composition-delivery-tree-dryrun
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
worker="$ORCH/workers/vw-m4-composition-delivery-tree-dryrun"
design="$ORCH/design"
patch="$design/handoff-vw-m4-composition-delivery-tree-dryrun-composition.patch"
stage=$(mktemp -d "$worker/delivery-stage.XXXXXX")
archive="$stage/main-archive"
mkdir -p "$archive"

git -C "$repo" rev-parse --verify origin/main
git -C "$repo" rev-parse --verify tl/integration
git -C "$repo" rev-parse --verify 'origin/main^{tree}'
git -C "$repo" rev-parse --verify 'tl/integration^{tree}'

git -C "$repo" diff --binary --full-index --no-ext-diff --no-renames \
  origin/main tl/integration > "$patch"

git -C "$repo" archive --format=tar origin/main | tar -xf - -C "$archive"
git -C "$archive" apply --binary --check "$patch"
git -C "$archive" apply --binary "$patch"
```

The exact proof normalized `git ls-tree -r --full-tree tl/integration` to
`mode blob-id<TAB>path`, then recursively hashed every regular file or
symlink in the applied archive with:

```bash
git -C "$archive" hash-object --path="$relative_path" "$relative_path"
```

It compared the sorted normalized manifests with `diff -u`, including mode
and path. A second fresh archive repeated `git apply --binary --check`,
`git apply --binary`, and the exact manifest comparison.

The bundle command was:

```bash
bundle="$worker/handoff-vw-m4-composition-delivery-tree-dryrun-composition.bundle"
git -C "$repo" bundle create "$bundle" tl/integration
git -C "$repo" bundle verify "$bundle"
git -C "$repo" bundle list-heads "$bundle"
sha256sum "$bundle"
```

No test/build/browser/npm/full-suite command was run. No network fetch was
performed. The first redundant `git apply --check` issued after the first
archive had already been patched was rejected because the patch is not
idempotent; the independent second fresh archive is the recorded recheck.
