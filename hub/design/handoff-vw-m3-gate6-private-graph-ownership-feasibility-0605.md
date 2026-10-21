# Gate 6 private graph reuse handoff

The approved graph at
`vw-m3-gate6-corrected-helper-source-stage/node_modules` is reusable without
another `555,896,832`-byte copy only via an explicit manager-authorized
same-filesystem ownership transfer to
`app-pin-d00a6613/node_modules`. The existing controller then remains
compatible: it binds App source and graph to the selected `appRoot`, and its
real-directory/in-graph-link/no-shared-inode/hash guards are preserved by a
directory rename.

Using the old stage in place is not safe: its exact source is
`909d2bfa…/79728118…`, not d00, and the current controller has no alternate
App graph path. The d00 checkout has no graph. Current free space is
`10,303,725,568`, below the `10,737,418,240` standing floor; no preflight or
physical run is ready now. No transfer, release, symlink, copy, or test was
performed. Full sequence and guard/accounting are in the worker report.
