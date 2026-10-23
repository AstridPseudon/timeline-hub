# Runtime OPS-D21b Remotion reuse — independent final review

Status: **FAIL; do not install, merge, or publish.**

Reviewed the exact flat `return-1811` scripts and patches after independent
`review-1802` FAIL. The flat hash manifest and cmp claims pass, and a fresh
private matrix against the exact flat scripts passes the source-custody,
toolchain, reuse, registration, changed-tree, requester-shape, and refusal
guards. The assigned Runtime worktree is clean at Base Runtime
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

Blocking finding: flat `request-runtime` lines 7–9 require
`RUNTIME_ORCH_ROOT`, and flat `make-runtime` lines 15–17 require it too. The
existing production requester instead defaults its ORCH root internally, and
the existing production dispatcher invokes `make-runtime` without this
variable. Fresh `env -i PATH=/usr/bin:/bin` invocations of both exact flat
scripts exit 2 with `REFUSED: RUNTIME_ORCH_ROOT must name the private ORCH
root`. The normal production `request-runtime -> dispatcher -> make-runtime`
entry is therefore refused before queue processing.

Fresh private evidence and full exact commands/exits are in:

`workers/rt-OPS-remotion-reuse-finalreview-1818/report.md`

The old real-layout graphs remain unmarked/future-only. No host dispatcher,
daemon, provisioner, installed script, production queue, real graph, network,
package installation, or C0v2 product proof was run. The prior author
intermediate private npm failure was not repeated.

This is the second Luna failure. Route the next repair/review decision to
manager Sol; do not install or waive the root guard.
