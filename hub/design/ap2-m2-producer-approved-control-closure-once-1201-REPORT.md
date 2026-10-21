# Producer approved control closure — 1201

## Disposition

**BLOCKED after the one authorized preflight.** The archived report manifest was restored exactly and all 44 entries in the existing checksum manifest pass. The parent test was waited on, the local browser lock is clear, and the 1132 closure is intact. The preflight reached and passed all 11 public13 checks, then failed at the existing TSX module-format probe because Node could not create its IPC pipe in the sandbox (`EPERM`). Per the task boundary, this first new failure stopped the run: no retry and no five-control execution occurred.

No product source, test, pin, guard, specification, `.gitignore`, shared dependency, or original evidence file was changed.

## Exact report restoration

Source archive (read-only):

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132-closure.tar.gz
sha256: fff1e47ee33684b4cf6acda9b3f72d703700ff2691a5dc7001e16bd10662528e
size: 988676 bytes; members: 44
```

The exact `REPORT.md` member was restored to:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132/REPORT.md
size: 33875 bytes
sha256: ce0ed96342c3a77ce5ef71ffeb754f6885606a387971222f085de964878b53f4
```

`MANIFEST.json` records that member’s identical source as `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132-REPORT.md`. The archive and the existing `SHA256SUMS` were not rewritten. The exact verification command was:

```text
(cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132 && sha256sum -c SHA256SUMS)
```

Result: **44/44 OK**, including `REPORT.md: OK`; the restored report hash independently matched the archived member. The accidentally attempted parent-directory extraction was removed immediately; that path is absent.

## Unchanged source and closure hashes

The authorized keeper remains clean at the exact source pin:

```text
keeper: /home/user/work/wt/app-pin-5863411a
HEAD: 5863411a8c2400db719b5385002b05af0a2b3891
tree: 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
status: empty
node_modules -> /home/user/work/app/node_modules
```

The recorded source ancestry remains `5863411a -> b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7 -> 17d2518c341c47a2d8634047b400399886da3a2a`; no source or pin was rebound. The original harness and stub are unchanged (`outer-controls-run.py` `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234`; `launch-tool-stub.py` `4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7`). The approved phase-corrected sidecar remains `a4b3f89d9f15f9fbd095e5b6b658605807f7b0099e8337f0cb4dea11ebdf662e` and was not edited.

The eight retained positive artifacts remain byte-stable at the hashes in `P/SHA256SUMS`:

| Artifact | SHA-256 |
|---|---|
| `producer-physical-keeper-gate-0717-owned.sh` | `d9ecc3ade14746c559c46c68046eec3f71ecac5c37f9218cb575a9e2057a6238` |
| `producer-public13-runner-0717-owned.sh` | `b21d9ccd1dfc31b81d38e2e19c78ca4d53ca3a3a7a5c74f82c7bffb533fe9d13` |
| `producer-retain-failure-artifacts-0753.sh` | `dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75` |
| `producer-runner-0717-owned.sh` | `84031e301827518c2b981c585e812c5a5ad3d00727105c1b8515a6e1209a54fa` |
| `producer-startup-custody-gate-0717-owned.sh` | `02d831e05094586d3771424ac43cacb602799c691ec40423fb370891ba1cb16e` |
| `producer-startup-module-format-probe-0717-owned.mts` | `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3` |
| `producer-startup-only-gate-0717-owned.sh` | `4ce9e7f4fc0eb6c6a7b32b784cd3ea64f598b4169fa49ba2a99126237dc4a5df` |
| `producer-startup-only-probe-0717-owned.mts` | `a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f` |

## Parent slot and prerequisite checks

The existing parent result was waited on exactly once using:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-parent-build-heap-corrected-one-central-1145-ap2-m2-parent-build-heap-corrected-one-central-1145-e2e-integration-1021114743-590 2
```

It completed `fail exit=1` after its own browser phase. Its result was not used as producer control qualification and its body was not analyzed. Post-parent checks passed:

- `flock -n /home/user/work/.app-m1-browser.lock true`: **CLEAR**.
- Parent `/tmp/tl-pv-parent-1145-central`: **absent**.
- Disk free on `/tmp` and P filesystem: **13,796,012 KiB** at check time.
- P had no prior `controls`, `evidence`, `run_root`, or `node-modules` copy; the old recorded `/tmp/w-af90d07e5e` path was absent.
- P’s full SHA manifest and `python3 P/validate-syntax.py`: **PASS**.
- Keeper status and source identity: **PASS** as recorded above.

## One authorized preflight

The exact next-preflight operation was run once from the pinned keeper, with a fresh physical private `TMPDIR` `/tmp/p1201-5or4Tn` (realpath identical), and a cleanup trap:

```text
cd /home/user/work/wt/app-pin-5863411a
TMPDIR=/tmp/p1201-5or4Tn sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132/artifacts/producer-startup-custody-gate-0717-owned.sh preflight
```

Observed result:

```text
public13 hosted-build resolver PASS version=0.0.13 ... tarball_sha256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
public13 preflight PASS checks=11 source=agent:8130a401bf44a518d5a40ae274d398b8c560be55 runtime:2c4ac180c2220bdad966bc01e95ad230e99ce26a graph=public13 isolation=private
Error: listen EPERM: operation not permitted /tmp/p1201-5or4Tn/tsx-0/344.pipe
exit 1
```

This is the first new failure: the real TSX launcher attempted to create its IPC pipe while executing the authorized format probe. No build, browser, localhost server, startup probe, list mode, final run, socket service, install, or actual test was run by this worker. The temporary roots `/tmp/p1201-5or4Tn` and `/tmp/tla-wEpCER` were absent after the exit; no `dist`, evidence packet, or P control directory was left behind.

## Five-control reachability

The approved sidecar `P/outer-controls-run.phase-corrected-1150.py` was **not invoked** after the preflight failure. Counts are therefore:

| Case | Reached | Result/evidence |
|---|---:|---|
| `before` | no | no dispatch or output |
| `after` | no | no dispatch or output |
| `absent-output` | no | no dispatch or output |
| `copy-failure` | no | no dispatch or output |
| `success` | no | no dispatch or output |
| **Total** | **0/5** | **not qualified** |

The positive-case assertions, failure-retention checks, cleanup checks, and required 5/5 status are all **unreached**. No second attempt was made. Manager/orchestrator authorization is required after the sandbox IPC restriction is resolved; this report does not claim preflight or control qualification.

## Source colophon

This packet is tied to App source `5863411a8c2400db719b5385002b05af0a2b3891` / tree `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`, the original eight positive artifacts and launch stub, the phase-corrected sidecar `a4b3f89d…`, and the preserved original archive/evidence bytes. No repo worktree files changed. Commit message and blocked status are recorded beside this worker packet. The manager separately decides whether any future actual run is authorized.
