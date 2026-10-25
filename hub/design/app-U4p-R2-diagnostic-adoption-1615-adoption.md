# U4p qualified R2 redo and diagnostic adoption

Adopted Runtime `ab1e4f6141987706132916e2da16477f5a019464` through the normal
client and installer tooling from clean checkout
`/home/user/work/wt/rt-pin-ab1e4f61`.

Changed only:

- `runtime.lock.json`: `source_commit` now points to `ab1e4f…`.
- `public/install-manifest.json`: `runtime.sha` now points to `ab1e4f…`.

Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, schema digest, producer version,
14 mappings, canonical 15, and App protected eight were preserved. The App
diff is exactly the two authorized pin files.

Runtime custody is exact: released tree `7d8e77b2…`, auth blob
`75c290…`, redo test blob `0cbf231…`, and clean checkout. The R2 home receipt
records genuine grouped inverse/redo `3 passed` and native provider `2 passed`;
the diagnostic parent `00ede8c…` is part of the released merge. D130 recovery
remains safety-held and was not adopted or retried.

The inherited D115 p2-tour hash was stale for this newer App base; the current
base and worktree hashes are equal, so protected-file preservation is `8/8`.

No package install, full suite, browser/service body, native repeat, tour,
collector, observer, or held-recovery test was run.
