# OPS-retire-venv-1512 — guarded child-venv retirement kit

## Final result

**PASS for authoring and isolated qualification; not installed.** The exact three-file packet is staged at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-1512/evidence/kit/`

Files:

- `request-retire-venv`
- `dispatcher-daemon`
- `retire-child-venv`

The packet patch, file list, hashes, and isolated output are in the worker evidence directory as `packet.patch`, `files.txt`, `hashmanifest.txt`, and `isolated-tests.log`. No live ORCH/bin file, product repository, manager state, venv, daemon, or branch was modified.

## API and invariants

Supported request:

```text
request-retire-venv venv-agent-child-<suffix>
```

The request writer accepts exactly one strict name, writes `RETIREVENV NAME` with a no-clobber queue write, and reports the normal `queue/done/retire-venv-NAME` result path. The dispatcher addition is one branch only: it probes 11 bytes for `RETIREVENV `, invokes `retire-child-venv` with one quoted argument, and leaves FIFO, refusal, done, stop, merge, bench, and self-reload handling unchanged.

The handler fails closed unless all of these hold:

- strict `venv-agent-child-[a-z0-9][a-z0-9-]*` name; exact direct child of the production `/home/user/work` root; canonical containment; no root/target symlink;
- target is a directory older than strictly more than 3600 seconds;
- both existing provisioner identity markers, `.astrid-source-commit` and `.astrid-runtime-source-commit`, are readable regular files containing a 40–64 character lowercase hex identity;
- no partial/active-builder sibling exists;
- no literal name or canonical target path occurs in current `tests/suites.conf`, `tests/*.env`, or other pending queue guards;
- no running worker marker has an unreadable metadata/brief/env inspection or a target reference;
- no inspectable live process has the target in argv, executable, cwd, or open FD (including Linux `(deleted)` paths);
- the complete set of checks passes again immediately before removal and the target device/inode/mtime/size fingerprint is unchanged.

The only private-fixture escape is `RETIRE_VENV_WORK_ROOT`; the production default is fixed and the same direct-child/canonical checks apply. Removal uses Python `shutil.rmtree` only after final validation. Its bounded callback restores owner-write permission only on paths lexically inside the validated named target; it does not recurse or modify permissions outside that target and does not follow symlinked directories.

## Exact source identity

Authoritative predecessor hashes captured before authoring:

- `orch/bin/dispatcher-daemon`: `b68f1d9aafe3d4cca6feb9413fcd9e4d51da5d8e30c4b2c7ed107ebf79a79dee`
- `orch/bin/request-child-venv`: `f9e5ea6f2ff577ebd25218a1eba751e17fafd474b1e1a3a3adbb8524a80c440e`
- retained `orch/bin/make-child-venv`: `39450feacd8ff7d566e19fd6ce0aadc5c02366db1bccd9c88f9cd3a3ceef614f`
- retained prior maker candidate `make-runtime.candidate`: `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`

The packet dispatcher differs from its predecessor by exactly one added source line. Packet hashes are recorded in `evidence/hashmanifest.txt`.

## Evidence and commands

All commands ran against private fixtures or read-only source copies; no actual dispatcher daemon, `ensure-daemons`, `run-manager`, `hub-sync`, real venv build, or real venv retirement ran.

- `bash -n evidence/kit/* /tmp/w-7e810730de/run-retire-tests.sh` — **PASS**.
- `/tmp/w-7e810730de/run-retire-tests.sh` — **PASS**, `pass=35 fail=0`. This covers eligible aged read-only retirement; wrong names and slash/space/quote/newline injection; missing, young, exact 3600-second, symlink, and root-symlink refusal; suite/env/pending references; running-worker metadata; uninspectable suite; running cwd; open FD; target replacement race; FIFO continuation after refusal and success; request writer and private dispatcher call-shape smoke.
- `diff -u orch/bin/dispatcher-daemon evidence/kit/dispatcher-daemon` — **PASS**, one added branch line.
- ShellCheck was checked and is unavailable in this environment; `bash -n` is the available syntax gate.

The matrix used private `RETIRE_VENV_ORCH_ROOT` and `RETIRE_VENV_WORK_ROOT` fixtures only. It did not inject child identity markers or production identity environment, and it retained fixture outside paths unchanged. No full/browser/native/journey suite was requested.

## Installation boundary

Independent review and normal publication/installation remain pending. The author did not edit or install live `orch/bin`, create a timestamped `.bak`, run host daemon tools, or emit a `KIT CHANGE` board line. The installer must perform the existing idle/not-executing check, atomic `.new` replacement, timestamped predecessor backup, and normal publication; if the persistent daemon cannot be safely quiesced, the lead needs the precise host-install receipt instead of a worker-side host-tool run.

