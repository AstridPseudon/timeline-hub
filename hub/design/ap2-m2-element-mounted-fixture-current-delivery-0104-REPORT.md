# Mounted fixture-only current delivery

## Result

Delivered the reviewed fixture-only `MountedForm` readiness hunk on the latest HOME tree. The production selected-parameter carrier is still the only carrier used. The fixture performs one local state refresh after the real command session has left `loading` while the real `clipParamsPort` has not yet appeared; it never manufactures or substitutes `clipParamsPort`.

The existing late-read, missing-carrier, and dirty-draft assertions remain unchanged. No product, shared-session, Provider, authority, pin, activation, or other source behavior was added.

## Current HOME handling

Prescribed attempt:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-element-mounted-fixture-current-delivery-0104 tl/integration
```

It failed before applying a merge because the shared Git worktree metadata is read-only:

```text
fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref 'ORIG_HEAD':
Unable to create '/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-element-mounted-fixture-current-delivery-0104/ORIG_HEAD.lock':
Read-only file system
rc=128
```

There were no conflicts. I reconstructed the current resolved tree through working files only. All eight non-fixture paths changed by latest HOME match `/home/user/work/app` byte-for-byte; the fixture file is latest HOME plus exactly the approved readiness hunk. No shared worktree, dependency, or cache was modified.

## Verification

- `TMPDIR=<worker-private-temp> node /home/user/work/app/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx -t 'uses the production selected carrier|refuses a mounted edit whose retained read completes after the command session is gone'` — **1 file, 2 tests passed**.
- `node /home/user/work/app/node_modules/eslint/bin/eslint.js src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx` — **passed**.
- `git diff --check` — **passed**.
- Approved hunk equivalence check against the source delivery commit — **passed**.
- No broad suite, browser, localhost, live socket, activation, pin, or new guard run.

The worker-private temporary directory was cleaned on exit.
