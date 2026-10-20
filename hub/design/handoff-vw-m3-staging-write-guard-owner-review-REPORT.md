# vw-m3-staging-write-guard-owner-review

## Verdict: APPROVE

The Agent-owned patch is safe for the owner gate and is ready for Agent to
apply. No source files were changed in this Composition worktree.

## Review

- The historical f816 culprit was the deleted inline double-glob command. The
  current surviving equivalent is the peer staging in Agent's
  `tests/packs/rendering/test_presenter_scene_capability.py:47-49`; Composition
  has no staging builder. The patch changes that live call site to use
  `_stage_private_node_modules`.
- The helper iterates `peers.iterdir()` once, and each scoped peer's
  `peer.iterdir()` once. It has no duplicate `*`/`@*` scope enumeration.
- Before every `mkdir` or leaf link, it resolves the destination parent and
  rejects any parent resolving into the borrowed graph. Existing scope
  parents must be real directories; a linked scope parent into the borrowed
  graph is rejected before leaf writes.
- Leaf links use `ln -sfnT`, so an existing destination leaf symlink is
  replaced as a leaf and cannot be followed into a borrowed package. Source
  leaves are resolved strictly for the link target, but are never written.
- The helper is not unused theater: the patch imports it at the surviving
  presenter staging call site. The private regression file imports the same
  helper and exercises the actual helper implementation.
- The positive regression proves real scope directories, ordinary unscoped
  staging, private `@banodoco` package-byte preservation, borrowed-graph
  preservation, and idempotent repeat staging. The negative regression proves
  a linked destination scope parent is refused before writing.

## Evidence

1. `git -C /home/user/work/agent apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-staging-realpath-write-guard/staging-realpath-write-guard.patch`
   — PASS (exit 0), against Agent `tl/integration` at `a8a40afd3`.
2. Applied the exact patch to a private copy of the two Agent fixture files,
   then ran:
   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$review_tmp" pytest -q --basetemp="$review_tmp/pytest-tmp" "$review_tmp/tests/packs/rendering/test_private_node_modules_staging.py"`
   — PASS: `2 passed in 0.21s`. The private graph was under `/tmp`; no shared
   graph or shared dependency path was written.
3. Ran a separate private fake-graph probe with existing scoped and unscoped
   destination leaf symlinks pointing into the borrowed graph:
   `PYTHONDONTWRITEBYTECODE=1 python - <<'PY' ... PY`
   — PASS: `existing-leaf-symlink-replacement=PASS`; borrowed package bytes
   were unchanged and no nested `leaf/leaf` or `plain/plain` link appeared.
4. `rg -n '_stage_private_node_modules|for peer in peers\\.iterdir|symlink_to\\(peer' /home/user/work/agent/tests/packs/rendering/test_presenter_scene_capability.py /home/user/work/agent/tests/packs/rendering/_helpers.py`
   — PASS for the expected pre-apply state: the old inline loop is the sole
   current call site, and the patch replaces it with the helper import/call.

The source worker also reported Ruff passing on the changed helper and new
regression file. I did not run Agent or Composition full suites, installs,
browser/render, live sockets, or any real shared-graph write.

## Owner-gate handoff

The flat Agent patch, this report, and the file list are exported through the
existing orchestration peer channel:

- `design/handoff-vw-m3-staging-write-guard-owner-review.patch`
- `design/handoff-vw-m3-staging-write-guard-owner-review-REPORT.md`
- `design/handoff-vw-m3-staging-write-guard-owner-review.filelist`

No Composition merge, source-repo Git mutation, push, or fake source commit
was performed.
