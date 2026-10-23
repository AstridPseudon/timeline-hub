# Runtime handoff — OPS-child-provision independent review

Result: FAIL; conditional install was refused safely.

The author candidate remains staged at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-provision-0955/evidence/candidate/make-child-venv`

Candidate SHA-256 is `526e16145c3b014fb613618c27fe6d1a007857d769f31bfe5169ce423c71b52a`, mode 755. The live main route was rechecked immediately after review as SHA-256 `ea4a1f53722ddd9f943b217021b6b4ed4828f34d10de76bae7ddc71fa470d6bc`, mode 755, owner root:root; it was not replaced.

Independent checks passed `bash -n` for live and candidate, the retained
offline harness (success, timeout, Runtime failure, -I import failure,
immutable existing, partial recovery), and `git diff --check`. ShellCheck was
unavailable. No real install, network, venv, D09, daemon, full suite, or
product test was run.

The blocking issue is process bounding: candidate lines 46 and 82 use GNU
`timeout --foreground`. GNU timeout documents that children are not timed out
in this mode. The independent descendant probe demonstrated the risk, so the
candidate cannot be called PASS under the brief’s all-descendant finite-wall-
time requirement. A corrected candidate must use a process-group-safe timeout
strategy compatible with the existing inline dispatcher, and then repeat the
offline and descendant probes before any publication. Do not install the
current candidate or invoke the real provisioner as a workaround.

