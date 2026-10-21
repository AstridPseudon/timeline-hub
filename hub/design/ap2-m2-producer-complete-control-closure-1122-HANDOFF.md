# App2 producer control-closure handoff — 1122

Status: **BLOCKED before controls**. This is a source-only, no-browser handoff.

## Durable packet

- Report: `ap2-m2-producer-complete-control-closure-1122-REPORT.md`
- Recovered 1113 report: `ap2-m2-producer-new-topology-main-binding-1113-REPORT.md`
- Recovered 1113 handoff: `run-on-main-app2-producer-current.md`
- Command closure: `ap2-m2-producer-complete-control-closure-1122-command.tar.gz`
- Closure SHA-256: `6983e1f08fe9207faacefe79494300a6ded3c55272a36f85363deeb95c6645d5`

Extracted closure contents are the existing `outer-controls-run.py`, exact
0935/0945 `launch-tool-stub.py`, and the eight rebound 1113 chain artifacts.
No product source or App documentation was changed.

## Source and guards

```text
App source  5863411a8c2400db719b5385002b05af0a2b3891
tree        31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
parent      b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
baseline    17d2518c341c47a2d8634047b400399886da3a2a
Agent       8130a401bf44a518d5a40ae274d398b8c560be55
Runtime     2c4ac180c2220bdad966bc01e95ad230e99ce26a
version     0.0.13
guards      51 hash / 20 path / 1 version
```

The exact stub SHA-256 is
`4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7`, mode
`0755`, and matches the originals in both the 0935 and 0945 records.

## Run state

The one authorized command was run once:

```sh
cd /home/user/work/wt/app-pin-5863411a && \
  sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-control-closure-1122/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

It exited `1` before emitting output. The first ordered mismatch is the
existing custody gate at line 66: `/home/user/work/wt/app-pin-5863411a/node_modules`
is absent, so the required symlink to `/home/user/work/app/node_modules` cannot
be verified. The five controls were not started (`0/5`, no result claim).

Do not retry from this packet. MAIN must restore the approved keeper symlink
without installing or mutating shared dependencies, then authorize the single
remaining preflight/control attempt. Current shell Node is `v22.22.0`; Node
`20.19.4` on MAIN remains unverified.
