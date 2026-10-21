# App pin 0d432391 graph clone readiness — HELD

The requested private regular-directory graph was not materialized. Source
graph allocation is `555,896,832` bytes; required free before copy is
`11,876,144,076` bytes (`11,320,247,244` staging threshold plus source
allocation); final observed free is `10,926,952,448` bytes. Exact
**STORAGE NEED: 949,191,628 bytes (0.884003591 GiB)**. Predicted post-copy
free would be `10,371,055,616` bytes, below both the threshold and the
10-GiB floor. No margin was invented and no guard was lowered.

The exact `0930` symlink from
`/home/user/work/wt/app-pin-0d432391/node_modules` to the read-only source
`/home/user/work/wt/app-pin-d00a6613/node_modules` was verified by `readlink`
and `realpath`, then removed with `unlink`; the source graph remains the same
real directory, inode `65024:3574084`, graph `8bdc…/32393`.
The pin and source graph remain retained/leased for eventual physical
preparation; no worker recycle dependency was introduced.

Static checks passed for the exact App pin/tree, source graph, Runtime graph
`4913…/21455`, public13 artifact `9412…` with 77 regular members, React/
Remotion versions, tsx and all packet loader/tool paths, and retained d00
dist (339 files, index hash `aeb5d833…e257b`). The unchanged graph guard
rejected the former symlink with `private dependency graph must be a real
directory`.

No copy, install, network, hardlink, central/physical request, grant, marker,
browser, helper, Runtime, socket, render, or full suite was run. Central
preflight still owns Python import origins, retained dist availability, exact
destination graph/inode proof, source tuple/ancestry classification, and the
five-case admission checks. Prior local Python `spawnSync ... EPERM` remains a
sandbox boundary only.

Worker evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-physical-graph-clone-readiness-0934/REPORT.md`.
