# Runtime handoff — OPS-child-provision final independent review/install

Result: PASS. The exact reviewed candidate is installed into MAIN ORCH only.

Installed main route:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`

```text
SHA-256 8a64606a89f0747ae28f3121b56e876d5a12624d294e1ad32fa778d62a278eba
mode 755, owner root:root, regular file, not a symlink
```

Candidate source is the author-reviewed file at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-return-1006/evidence/candidate/make-child-venv`

The predecessor `526e16145c3b014fb613618c27fe6d1a007857d769f31bfe5169ce423c71b52a`
was retained. Its exact diff to the installed candidate is only removal of
`--foreground` from the overall and stage GNU `timeout` wrappers, plus
explanatory comments. This fixes the mandatory descendant/FIFO-held witness
while preserving the existing API and dispatcher route.

Independent evidence passed:

- `bash -n` for live, candidate, retained stub harness, retained author
  descendant harness, and the independently authored descendant harness.
- retained offline success/timeout/Runtime-failure/import-failure/
  immutable/partial-recovery matrix: PASS.
- independently authored real-GNU-timeout descendant/FIFO witness: PASS,
  bounded return in 2 seconds, child gone, no final environment, following
  fake queue job responsive.
- retained author descendant/FIFO witness rerun: PASS, elapsed 3 seconds.
- ShellCheck unavailable; no full suite or product typecheck was applicable.

No real pip, network, source fetch, venv, package graph, dispatcher, daemon,
or D09 operation was run. Agent0958 owns the next single real existing
request and original installer/D09 qualification.

Installed state and kit publication are separate. The separately resolved
kit path `/home/user/timeline-hub/hub/kit/bin/make-child-venv` remains a
regular `755 root:root` file at the old SHA-256
`ea4a1f53722ddd9f943b217021b6b4ed4828f34d10de76bae7ddc71fa470d6bc`.
Normal existing publication has not been claimed; the publication owner must
propagate/ACK it and the manager must verify that state.
