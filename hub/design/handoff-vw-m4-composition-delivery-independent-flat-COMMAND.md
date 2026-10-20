# Composition M4 independent flat-delivery commands

All commands below were run read-only against the composition source except
for private staging and the final handoff files under the orchestrator
scratchpad. No commit, merge, rebase, reset, checkout, push, fetch, or shared
install write was performed.

```bash
repo=/home/user/work/wt/vw-m4-composition-delivery-independent-flat
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
design="$ORCH/design"
prior="$ORCH/workers/vw-m4-composition-delivery-tree-dryrun"
patch="$design/handoff-vw-m4-composition-delivery-tree-dryrun-composition.patch"
bundle="$prior/handoff-vw-m4-composition-delivery-tree-dryrun-composition.bundle"

git -C "$repo" rev-parse --verify origin/main^{commit}
git -C "$repo" rev-parse --verify origin/main^{tree}
git -C "$repo" rev-parse --verify tl/integration^{commit}
git -C "$repo" rev-parse --verify tl/integration^{tree}
git -C "$repo" status --porcelain

git -C "$repo" diff --binary --full-index --no-ext-diff --no-renames \
  origin/main tl/integration | sha256sum
git -C "$repo" diff --check origin/main tl/integration

stage=$(mktemp -d "$prior/independent-flat-stage.XXXXXX")
archive="$stage/main-archive"
mkdir -p "$archive"
git -C "$repo" archive --format=tar origin/main | tar -xf - -C "$archive"
# Normalize private extraction to the source Git modes because the source
# repo's core.sharedRepository=true writes 0664 tar entries.
git -C "$archive" apply --binary --check "$patch"
git -C "$archive" apply --binary "$patch"

# Compare sorted target ls-tree mode/blob/path entries with
# git hash-object --path entries from the applied archive; also count every
# regular file/symlink and inspect symlink targets.
git bundle verify "$bundle"
git bundle list-heads "$bundle"
git clone --no-checkout -b tl/integration "$bundle" "$stage/bundle-clone"
git -C "$stage/bundle-clone" fsck --full --no-reflogs
```

The transport archive was built from exactly `composition.bundle` and
`manifest.json` using fixed tar ordering, epoch mtimes, zero numeric owner and
group, fixed member modes, and `gzip -n`. A second private build was compared
byte-for-byte to prove deterministic output. It was then extracted privately;
the extracted bundle was compared byte-for-byte and by SHA-256 to the source.

No tests, build, npm, browser, Node graph, or full suite were run.

