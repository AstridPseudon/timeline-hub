# Validation

## Read-only source checks

- `git -C /home/user/work/runtime status --short --branch`: clean Runtime worktree.
- Exact refs, trees, frozen R4 ref, and computed merge-base: PASS.
- `git -C /home/user/work/runtime merge-tree --trivial-merge d4f496ec4fbcae7a1f3a51d47ed5147c561117ad e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9 dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f`: 71,105 bytes; recomputed SHA-256 `2d341b37bafebc1feb09d4e69971bcde5ed12b729dcdc6e1c041838e7142540e`.
- JSON/crosswalk comparison: PASS for 10 paths, 22 hunk records, all base/ours/upstream blobs and source-side hunk arrays.
- `git cat-file --batch-check` for all recorded source blobs: PASS, 30/30 are exact `blob` objects.
- Class partition: PASS, 3 textual + 2 context-only + 17 semantic.
- Semantic question count: 17 present; 14 exact merge-tree anchors and 3 incorrect anchors documented in `findings.md`.

## Proposed patch checks

Exact upstream blob files were materialized only under the worker-owned scratch
path `/tmp/w-98eb673119/runtime-conflict-review-agtF/upstream-blobs`.

- `git -C /tmp/w-98eb673119/runtime-conflict-review-agtF/upstream-blobs apply --check --verbose --unsafe-paths /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-F-tail-Runtime-conflicts-1902-trivial-resolutions.patch`: PASS, exit 0.
- Same check with `--whitespace=error`: PASS, exit 0.
- Patch paths: exactly `.github/workflows/ci.yml` and `docs/runtime-portability-testing.md`.
- `git diff --check` in this review worktree: PASS, exit 0.

The delivery builder was inspected read-only: it creates a format-patch and
re-applies with `git am -q`; no `--whitespace=error` flag is present. No actual
ZIP/build/apply service was run.

## Tests

No pytest, typecheck, lint, live service, browser, or full suite was run. This
task is an independent source review and explicitly forbids product/body
execution.
