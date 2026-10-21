# App M2 producer keeper residue first cause — 0641

## Result

The protected 0545 keeper was restored to its exact clean source prerequisite
without changing tracked bytes, shared dependencies, or another active worker.
The residue was proved inactive worker-created startup scratch and was moved
losslessly to this worker's durable record. The required 0626 source preflight
was then executed once on the exact target, but failed in the immutable 0626
custody artifact before the ESM module probe could run. The startup smoke was
not run, as required by stop-on-first-failure. No producer case/body was run.

## Residue origin and safe disposition

Residue:
`/home/user/work/wt/ap2-m2-producer-physical-keeper-startup-preflight-0545/.public13-effective-ordinary/`

Evidence of origin:

- Worker `ap2-m2-producer-physical-keeper-startup-preflight-0545` was finalized
  as `done`, exit `143`, with STOPPED reason “orphan finalized by request”; its
  `KEEP` marker remained a deliberate lease for the protected keeper.
- The 0617 startup test was terminal (`fail`, exit 1) before this task began.
  Its gate binds the 0545 keeper/startup gate at lines 4–7. The 0545 startup
  gate sets `SHORT_APP_ROOT` to `.../a`, symlinks that path to the keeper at
  line 41, then creates `RUN_ROOT=$SHORT_APP_ROOT/.public13-effective-ordinary`
  and `agent`/`runtime` at lines 38–43. Those mkdir/clone operations therefore
  planted the untracked tree in the keeper. Its cleanup only deleted the
  physical short root and did not remove the symlink target.
- Residue timestamps were 2026-10-21 06:22:07–06:22:09, matching the 0617
  startup result requested at 06:21:52 and ending at 06:22:09. The residue
  contained only the private Agent/Runtime clones and empty run/cache dirs:
  3,547 files, 736 directories, 0 symlinks, 114,964,896 bytes (121 MiB).
- No `running` test marker existed; both relevant central results were
  terminal. A `/proc` cwd/fd scan found no live process using the residue.
  The producing scripts and all active-test/lease checks were read before the
  move. No shared node_modules/venv path was inside the residue.

Safe disposition:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/
  scratchpad/orch/workers/ap2-m2-producer-keeper-residue-first-cause-0641/
  residue-archive/public13-effective-ordinary/
```

The move used `mv`, not deletion or copying. Relative metadata and file-hash
manifests compare byte-for-byte before/after:

```text
pre/post metadata sha256: 256671b516b88e862ac498204296cbbd5984929b1d4c120fd149f43fa229cb93
pre/post file-hash sha256: 927eb0a49f9331e2765f46849279e4028618aa6ac7840c61440b3fcb9afdd94a
LOSSLESS_MOVE=PASS
```

The manifests are `residue-archive/pre-move-*` and `residue-archive/post-move-*`
in this worker record. The protected keeper now has no untracked files.

## Final source and artifact identity

Keeper and exact target both remain:

```text
App HEAD: b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7
App tree: fd16d32fd3487e56c9fe1ff16582dba240f63b77
keeper status: clean
KEEP: present
keeper node_modules: /home/user/work/app/node_modules
```

Matched source pins:

```text
Agent:   8130a401bf44a518d5a40ae274d398b8c560be55 / tree 236c3e57e0265c52b81ba8085de3193026176bff
Runtime: 2c4ac180c2220bdad966bc01e95ad230e99ce26a / tree 7ab412cc4bcbe517efcfa806e092336390312e18
wrapper: 329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
```

The immutable 0626 artifacts were not edited and retain these hashes:

```text
producer-startup-only-probe.mts:       4beb7c22dfa06e04d28253dbab02f76ff2a9953f0accd4b12247514e4f0608f6
producer-startup-module-format-probe.mts:
                                        d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
producer-startup-only-gate.sh:          dbd346763a431c2ae69de4e0fff523511b8c170c13a5a78c58458abb4bbf4d9a
producer-startup-custody-gate.sh:       e218b82a8288d4a9a6f29e6dbbfe082f85e7cd7e8bed9d646aad8b621850cd1b
0545 source gate:                       c365641bdeca10b9d740d5968c9a1161db7b18f8bf49e9d8bd46f14aae60cfab
0545 startup gate:                      8f3be0c8fcb18ab474b8d5b31c8b6a17b1cdc3d02324b4159d184c266357013c
tsx executable/CLI:                     8729ecfb90d9d568939e4190e6f1d3317c946583b7d37a776e0c23a21c021cf8
tsx loader:                             0b1c5b86192772fe9257710e739959cee5947c11ae1f93b61abfaa9b80c6def1
tsx package:                            6e764b21991c21595441f82387c1451ccd10a3e7a3f0973cc5e3649a12dea7d2
spec:                                   d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
helper:                                 50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016
config:                                 5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0
```

## Central command and result

The exact target was `ap2-m2-producer-realm-physical-path-diagnosis-0538`.
The cached lookup was not treated as evidence; the one real run used
`--no-cache` after cleanup:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-producer-realm-physical-path-diagnosis-0538 \
  ap2-m2-producer-startup-esm-entry-fix-0626-preflight --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-esm-entry-fix-0626-preflight-1021064401-23664
```

Result: **FAIL**, exit `2`, result ID
`ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-startup-esm-entry-fix-0626-preflight-1021064401-23664`.
The existing public13 source preflight passed its 10 checks, then the exact
immutable custody script failed at line 81:

```text
producer-startup-custody-gate.sh: 81: SERVICE_ROOT: parameter not set
```

The 0626 custody artifact uses `SERVICE_ROOT` at line 81 but never defines it;
the 0545 startup gate defines it at line 20, which does not make it available
to the 0626 custody process. Consequently the owned `.mts` format probe did
not execute and no daemon health/teardown result exists.

The 0626 startup command was not requested after this first new failure. No
producer body/case, browser, Vite, build, install, local socket, full suite, or
shared dependency mutation was run.

## Exact next prerequisite

Obtain an independently reviewed correction to the 0626 custody invocation
that defines the service-root carrier before line 81, recalculate the custody
artifact hash and its suite literal, and then run exactly one fresh central
preflight on target
`ap2-m2-producer-realm-physical-path-diagnosis-0538`. Only if it passes may
the existing 0626 startup smoke be run exactly once on that same target.
Do not run startup or producer actuals against the current `e218b82a…` artifact.
