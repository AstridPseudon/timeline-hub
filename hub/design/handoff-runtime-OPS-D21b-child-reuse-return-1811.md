# Runtime OPS-D21b child-reuse first return — 1811

## Return status

Independent security controls are repaired in a private, non-installing
staged packet. Qualification and host integration remain pending one exact
orchestrator decision.

## Exact decision request

The 1802 review is decisive: the normal maker installs the Runtime backend,
imports `astrid_runtime` and `runtime_protocol`, and runs Runtime CLIs,
including `python -I -m astrid_runtime`. The backend SHA is therefore real
installed source custody. Do not silently waive it to force an Agent-SHA plus
generated-client-only reuse key.

Choose one:

* **A:** retain the existing full maker and key a full installed bench by
  Agent SHA + Runtime backend SHA + generated-client tuple; or
* **B:** separately redesign a genuinely client-only reusable component, with
  truthful independent Runtime-backend custody and binding.

No component redesign, host install, or production change was made while this
decision is pending. The minimum approved security change for either path is
the installed-byte/RECORD/read-only authentication in the packet below.

## Current dependency graph

```text
request-child-venv
  -> ORCH/queue/pending/childvenv-NAME (CHILDVENV ...)
  -> dispatcher-daemon CHILDVENV branch
  -> make-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH]
  -> installs Agent + Runtime, imports both, runs Runtime CLIs/-I, publishes RO bench
```

The existing fourth argument remains the Remotion graph. No Runtime argument
was invented. The real dispatcher is not run because it hardcodes the shared
ORCH and the task forbids actual queue/provision/install/daemon activity.

## Independent fixes and fresh evidence

The requester now requires explicit absolute private roots, compares installed
canonical `astrid_runtime_client` bytes to the exact Runtime source tuple,
requires those rows in the Agent-owned `astrid` RECORD (and rejects Runtime
ownership), validates RECORD digests/shape, rejects symlinks and write bits
throughout the retained bench, and preserves marker/origin/noneditable,
partial, dirty-source, and ambiguity guards.

Fresh private actual-layout fixtures pass for positive Agent RECORD ownership,
unchanged-marker client-byte mutation, writable-root negative, wrong RECORD
owner, missing/partial identity, ambiguity, omitted roots, and normal plus
`env -i` request execution. No real artifact was mutated.

Packet and report:

* Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-reuse-return-1811/report.md`
* Flat packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-reuse-return-1811/evidence/`

Final evidence: all staged `bash -n` checks passed; private nested and flat
fixtures passed; `sha256sum -c hashmanifest.sha256` was 8/8 OK; `cmp.txt` was
4/4 PASS; `git diff --check` passed; Runtime source checkout was clean. No
full suite or real dispatcher/maker was run by design.
