# Gate 6 runner lifecycle cause repair

## Result

Materialized one corrected successor packet at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739`

No central suite or central/physical request was registered by this task. The
packet is ready for one independent custody review followed by the existing
central preflight and, only if that passes, the one physical executor.

The repaired cause was the 0730 lifecycle collision: `run.sh --preflight`
created the same fresh physical namespace that the later normal invocation
required to be absent. The successor reserves the fresh physical namespace
`gate6-20261021T0739` for normal mode only. Diagnostic mode creates a bounded
unique `diagnostic-XXXXXX/run` root, routes every `RUN_DIR` and output
reference through it, leaves the physical namespace absent, and removes only
that owned diagnostic scratch on exit. `evidence/preflight-*` and invocation
logs remain.

The browser lock is now one standard kernel lock per `run.sh` invocation:
`run.sh` opens and exclusively holds `/tmp/timeline-viewing-browser.lock` on
fd 9; `preflight.sh` verifies and inherits fd 9 rather than opening a second
lock. The inherited descriptor remains live through issue/controller,
Playwright, export, and cleanup, and closes only when the parent invocation
exits. `issue.mjs` accepts only the fresh physical `RUN_DIR` beneath this
worker.

## Packet changes

Only the runner lifecycle files changed from the 0730 packet:

- `run.sh`: diagnostic-vs-physical namespace routing, explicit `RUN_DIR`
  export, parent-owned fd 9 lock, invocation logs, and combined cleanup trap.
- `preflight.sh`: consumes caller `RUN_DIR` and verifies inherited fd 9.
- `issue.mjs`: consumes and validates `RUN_DIR` instead of a stale fixed path.

`prepare.mjs`, `dist-availability.mjs`, and
`prepare-validation-diagnostic.py` retain their frozen source/graph/dist/tool,
clean-environment, byte, ancestry, space, authority, and cleanup guards.
There are no product, API, DTO, store, controller, package, pin, fixture,
threshold, assertion, graph, shared dependency, or protected-cleanup changes.

## Checks run

The final static checks were run from a unique empty foreign `/tmp` cwd:

```text
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/run.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/preflight.sh                         PASS
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/prepare.mjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/issue.mjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/dist-availability.mjs PASS
/home/user/work/venv-agent/bin/python -B - /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/prepare-validation-diagnostic.py <ast-check> PASS
(cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739 && sha256sum -c /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/SHA256SUMS) PASS
```

The final packet diagnostic was run as:

```text
(cd /tmp/gate6-foreign-run-XXXXXX && bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-runner-lifecycle-cause-repair-0739/run.sh --preflight)
```

It passed static checks, printed both fd-9 lock-lifetime lines, and reached
the pinned Python child probe. The sandbox then returned
`spawnSync /home/user/work/venv-runtime/bin/python EPERM`, after reporting the
expected Runtime/Agent import origins. This is a sandbox limitation, not
central evidence; no actual preflight pass is claimed. After the failure, the
physical namespace, source tuple, grant, marker, and Playwright output were
absent, diagnostic scratch was clean, and the invocation log was retained.
Two final-packet local attempts reached this same EPERM boundary; one earlier
draft attempt is also retained in its invocation log and caught the missing
`RUN_DIR` export before the final fix.

A private temporary copy, with no product or intended physical namespace, ran
normal mode once. It reached the same validation boundary and exited 1 at the
sandbox EPERM before `issue.mjs`; no source tuple, grant, marker, or physical
output was created. This proves mode routing and exit propagation under narrow
nonphysical controls only. It does not mock graph validation and does not
qualify preflight or physical execution.

The lock lifetime probe passed: a parent-held fd 9 was inherited by a child,
and a competitor could not acquire the lock until child cleanup. No lock path
was deleted or replaced.

Current free space was `11,423,010,816` bytes versus the unchanged known
threshold `11,320,247,244` and floor `10,737,418,240`.

No Composition product files were changed; `git status --short` is clean. No
full suite, central diagnostic, physical run, browser, Runtime, helper,
export, marker, or authority was started.

## Packet hashes

```text
run.sh                              593659a7d5591f45f9eec96ae28ab5468c455392ab19f456397c7462812d2da3
preflight.sh                        04291181ea001d664997d92a1ecae5da1b8c79a6739408ac296dbf13efbd812a
prepare.mjs                         7ad93869a27ff241319559881ade5207c65005f1b1bf9cdb7eb5641a713fd074
issue.mjs                           0912be05ad1fd15767966eedc296975bb1501b18891b1501a025c06aae324c2b
dist-availability.mjs               fb7632d2c69da10c65db04052f0b04ede1b6e72064817fdc600098135ea50dfd
prepare-validation-diagnostic.py    24be3f3479faafb0676e6a7d18b055e7f1079fa5436802ad0cba7a81124b0c59
SHA256SUMS                          9f969e97e423316d25ed4f2b867985d63198e133ab90f1b8e59a0060219c4073
COMMAND                             10db30029c8a95d92de29b6fabebfbce00e84166fec88299fe8c47d7539f1d33
PACKET-DIFF.md                      c7650f2a5354e321bae4bd8489c421ab355c4f4c56c80b49b2d6ea4c332633ea
PACKET-DIFF.patch                   caac9a1efd8ceaabb3b1a3d835aaa5c34e6a1ecece701fc9a8971ddd341f9134
```

Exact commands are in `COMMAND`; the complete executable diff is in
`PACKET-DIFF.md` and the exact unified patch is in `PACKET-DIFF.patch`.
No central request should be made until independent custody review accepts
this packet and its explicit local limitations.
