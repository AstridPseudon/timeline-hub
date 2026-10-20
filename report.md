# Composition M4 clean-main delivery proof

## Handoff

The current Composition tree `ac918bb645d2ee4e8e36bbb98df02fb732176475` applies cleanly to fresh `origin/main` `67b8aa3d0d6831d3e3504a340ff583c3da253707`. The patch reproduces every current tracked path, mode, and blob byte.

Artifacts:

- [Patch](/home/user/work/wt/vw-m4-composition-ac918-delivery-proof-refresh/composition-origin-main-to-ac918bb64.patch) — SHA-256 `60a82dff67e7516cb17439910d7e44fe70122218add4bc8a72452aa6c0f6c26b`
- [Patch checksum](/home/user/work/wt/vw-m4-composition-ac918-delivery-proof-refresh/composition-origin-main-to-ac918bb64.patch.sha256)
- [Git bundle](/home/user/work/wt/vw-m4-composition-ac918-delivery-proof-refresh/composition-origin-main-to-ac918bb64.bundle) — SHA-256 `c49d2638b3118aa9d2c0b7584a72151cc7e3c8a7303f6acdecff404d95861532`
- [Bundle checksum](/home/user/work/wt/vw-m4-composition-ac918-delivery-proof-refresh/composition-origin-main-to-ac918bb64.bundle.sha256)

The immutable public 0.0.13 archive was not changed: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 members, 58,477 bytes. It is below the 50 MB handoff limit.

## Proof results

- Patch `--check` and application: PASS.
- Fresh `origin/main` archive: 29 expected, 29 found, no missing or extra paths, mode mismatches, or blob mismatches.
- Fresh archive after patch: 113 expected, 113 found, no missing or extra paths, mode mismatches, or blob mismatches.
- Fresh `HEAD` archive: 113 expected, 113 found, with the same clean result.
- Patched archive equals the current `HEAD` tree: PASS.
- `origin/main` is an ancestor of `HEAD`: PASS; merge-base is `67b8aa3d0d6831d3e3504a340ff583c3da253707`.
- Bundle verification: PASS; it contains `HEAD ac918bb645d2ee4e8e36bbb98df02fb732176475` and requires the stated main commit.
- `git diff --check origin/main HEAD`: PASS.

The central result `composition-full-1020223241-16395` is reused as instructed: PASSED, 78 passed, 0 failed, 0 skipped. No full suite was rerun. No product tests, build, package, pin, release, or design archive was changed by this worker.

## Decisions and cleanup

The first private staging attempt was nested inside the Git worktree; Git resolved `git apply` against the enclosing repository and skipped the patch. I discarded that private stage and repeated the proof with a validated `/tmp/timeline-composition-proof.*` directory outside any repository. The corrected application and byte comparison passed. That temporary directory was removed after verification. Only the four delivery artifacts, this report, and the command log remain in the worker tree.

Whole-repository delivery assembly, macOS validation, and owner-film review remain outside this worker's scope and are unverified here.
