# App M2 producer exact-source startup finish — 0606

## Result

BLOCKED at the required source preflight. No startup suite was requested, and
no Runtime health, teardown, or producer body execution occurred; body count is
0. No App/source/guard/probe/dependency files were changed.

## Source and test custody

- Source target: `ap2-m2-producer-realm-physical-path-diagnosis-0538`
- App source HEAD/tree: `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` /
  `fd16d32fd3487e56c9fe1ff16582dba240f63b77`
- Existing preflight suite: `ap2-m2-producer-startup-final-registration-resume-0600-preflight`
- Existing queued result ID: `ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-final-registration-resume-0600-preflight-1021060628-16814`
- Central result: `fail`, exit `1`, before gate execution.
- Required startup suite name was confirmed in `suites.conf` as
  `ap2-m2-producer-startup-final-registration-resume-0600`, but it was not
  requested because preflight failed.

## Exact first cause

The first failing assertion in the hash-bound custody chain is:

```text
realpath "$TSX_BIN" = "$TSX_CLI"
```

Actual: `/home/user/work/app/node_modules/tsx/dist/cli.mjs`

Expected by the gate:
`/home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545/node_modules/tsx/dist/cli.mjs`

The keeper's `node_modules` is the required read-only symlink to
`/home/user/work/app/node_modules`; all prior bound hashes, refs, tree checks,
clean checks, probe hash, and wrapper hash passed. No retry or gate/probe edit
was made.

## Bound hashes

- Custody gate: `0e39303a1deebadeaeeaf1b7336e71c2ee9f55107452d86094ed74b2a2678282`
- Wrapper: `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`
- Probe: `4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6`
- tsx executable/CLI: `8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8`
- tsx loader: `0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1`
- tsx package: `6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2`

## Remaining prerequisite

The custody gate must be reconciled with the required shared-node_modules
symlink layout, then the same source preflight must pass. Only then may exactly
one startup suite run against this source target.

