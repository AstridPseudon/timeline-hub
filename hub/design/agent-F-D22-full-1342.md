# Agent F D22 full requalification

Status: **RUNNING** — the single authorized real-runner service owns the full
body. No local full execution was performed.

## Service handoff

Requested exactly once through the production test service:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-F-D22-full-1342 full-current-v3-1229
```

Service ID/result directory:

```text
agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679/
```

Initial state at handoff: `queued`; it entered `running` on the retained
snapshot. At the worker's 30-minute limit (2026-10-23 14:10:01 UTC), it was
still `running`, with the raw pytest progress at approximately 71% and
`log.txt` size 14,970 bytes. The retained snapshot must be checked from
`status`, `summary`, `log.txt`, and `snap`; do not stop or duplicate this
service.

## Preflight result

The uniquely named report-all preflight was run through the same service:

```text
agt-F-D22-full-1342-D22-report-all-preflight-1342-1023134418-16182
```

Result: **PASS**, exit 0; eight report-all groups passed and the xdist child
origin probe passed `6 passed in 1.91s`.

The real-runner snapshot was synthetic commit
`c711594fecd6cecf4fc87b93c647145f3a8dcf21`, parent
`8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree
`c4d72b065d6e68c92e4335120cc016cadf53b06a`. The preflight locked the Agent
source/test/pyproject tree, Runtime3b checkout, installed profile, imports,
toolchain, D09 supported environment, and full-row identity in one pass.

## Hash lock and exact recipe

- Agent requested input: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, tree
  `c4d72b065d6e68c92e4335120cc016cadf53b06a`; worktree clean.
- Full row `agent full-current-v3-1229` occurs once and retains SHA-256
  `9035bd9672c7186c440e4e3aaee15ae3dfbeaeb0192864f0a68b9f68cc212879`.
- Runtime: commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree
  `b794170504544b259781e50d7ca4d61b6729e67c`, protocol import SHA-256
  `4e4064e1d9b80c6637576490150f44f3c710fabc520af1e640abf2493dcbb0d2`, clean.
- Profile: `/home/user/work/runtimes/agent-remotion-v3-819acf-1110`, lock
  SHA-256 `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`,
  selected archive SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`,
  installed Composition `0.0.14`; custody check found 21,501 read-only
  regular files and 33 in-profile symlinks.
- Toolchain: Python `3.13.16`, pytest `9.0.2`, xdist `3.8.0`, Node
  `v20.19.4`; the profile receipt SHA-256 is
  `8e86a46fe6388975909e94ff28b2ea335a2095935ba4f898ff8a2ee854df801a`.
- D09 fixture source is locked at blob
  `ce4fb6c08ee5c682d3163eb0ab3eda856b59df59` and file SHA-256
  `03d79f9ea17c6c3c899aa1268a3b9ee4f8bd21681063a2f5be018d86eb887417`;
  its isolated profile/runtime/schema supported-environment bindings were
  present. No D09 body was rerun.

The newer 859 environment/profile is not claimed. No source, test, generated,
pin, dependency, contract, guard, or suite recipe was changed; the only ORCH
changes are this handoff, the uniquely named preflight row/script/probe, and
the retained service evidence.

## Terminal result

**Pending service completion.** No terminal `summary`, exit code, or complete
failure inventory exists at the worker handoff. The visible progress included
`F`, `E`, `s`, and `u` markers, but none is classified here. After the service
reaches a terminal state, preserve every failing node, skip/deselection/xfail
inventory, and classify each failure as source, fixture, or environment.
Historic 4249 classifications are not current causality evidence. Do not
rerun or broadly repeat any node before that classification.
