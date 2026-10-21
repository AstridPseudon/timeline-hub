# AP2 M2 producer recreated-source environment diagnosis

## Result

The prior actual `28181` failed for the recreated source keeper's missing
ignored `node_modules` symlink, before the runner, build, browser, or producer
body. I reproduced the unchanged wrapper refusal locally, provisioned only the
normal existing App dependency symlink on that private keeper, and ran the same
hash-guarded central preflight once.

- Missing-link proof: `sh .../run-producer-public13-list.sh <source> preflight`
  with no source link returned exit 1 and exactly `producer preflight FAIL` /
  `- isolation`.
- Setup command:

  ```text
  ln -s /home/user/work/app/node_modules /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/node_modules
  ```

  The target was verified first as the existing directory
  `/home/user/work/app/node_modules`; no install or shared-dependency write was
  performed.
- Final preflight: `ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-preflight-1021042625-4648`
  — PASS, exit 0, `public13 hosted-build resolver PASS`, `public13 preflight
  PASS checks=10`, private isolation.
- No actual, build, browser, producer, full suite, or product edit was run.
- Changed live callers: none.

## Exact custody and hashes

- Source keeper: `/home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416`
- Source commit: `97187ce3c1576559239f869067a9cef8ffb5f357`
- Source tree: `4acab858b0f12a1878fc231a33f3d06af9b0bdc0`
- Source parent: `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- Source parent’s parent: `70dec48e88ea036bf160539b58b68bb64c38f3b3`
- Baseline: `4ef89267f00d193273441ff6dbb955f30d27d708`; source diff is only
  `scripts/testing/run-producer-public13-list.sh`.
- Wrapper SHA-256:
  `3069891ce3c1f56fd66d138ccd5be2960bfb0158b368209704fc215ed3761b48`
- Existing runner SHA-256:
  `be59b3da5c01e0df22ec556cc84cd25a2a1a4304cf4542035829003eecb2e75b`
- Body commit/tree:
  `36dd91257fd13dcad0d58b48c790caa5063b4c8c` /
  `d908845dbc8e5ebf96698d08621557e904f20c52`
- Body spec SHA-256:
  `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`
- Body helper SHA-256:
  `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`
- Config SHA-256:
  `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`
- Locked graph archive SHA-256:
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Locked graph Composition package SHA-256:
  `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`
- Locked graph evaluation SHA-256:
  `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`
- Composition tarball SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

The source keeper is clean and retained with
`workers/ap2-m2-producer-final-external-hash-binding-0416/KEEP`. The existing
precise lease remains at
`managers/app2/notes/producer-exact-source-keeper.lease` and names the exact
source path. The source link remains
`node_modules -> /home/user/work/app/node_modules` with that target's existing
package-lock hash unchanged.

## Lifecycle diagnosis and cleanup

`bin/test-run` recreates a missing worker worktree detached from `tl/<worker>`.
It links dependencies onto the temporary test snapshot, but the registered
command passes the absolute source keeper path to the wrapper. The wrapper's
`check_isolation` therefore checks the recreated keeper itself. The normal
`bin/dispatch` App setup supplies `node_modules -> /home/user/work/app/node_modules`,
but the test-service recreation path did not.

Smallest normal environment fix: mirror that existing App-worker symlink setup
when `test-run` recreates an App worker, before executing commands that receive
the worker path. Do not relax `check_isolation` or alter the hash guard.

The preflight's child path was
`.public13-effective-ordinary/node-modules/...`; its resolver and private graph
checks passed, and cleanup removed `.public13-effective-ordinary`, the central
`.test-*` snapshot, and all other temporary child paths. No stale mutable copy,
new source authority, wrapper, or live caller was created.

## Commands and results

```text
TMPDIR=<private-temp> sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416/scripts/testing/run-producer-public13-list.sh /home/user/work/wt/ap2-m2-producer-final-external-hash-binding-0416 preflight
# exit 1; producer preflight FAIL; - isolation (link intentionally absent)

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-final-external-hash-binding-0416 ap2-m2-producer-existing-graph-command-preflight --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-final-external-hash-binding-0416-ap2-m2-producer-existing-graph-command-preflight-1021042625-4648
# PASS; exit 0; preflight checks=10
```

