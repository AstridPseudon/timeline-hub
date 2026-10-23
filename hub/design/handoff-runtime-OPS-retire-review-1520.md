# Independent OPS-retire-venv review — rt-OPS-retire-review-resume-1534

## Verdict

**FAIL — return to author; do not install or publish the packet.** The exact
three-file packet is intact and its positive path is qualified, but the handler
does not fail closed for every uninspectable pending/worker entry. In the
independent fixtures below, it retired an otherwise eligible target while
these safety inputs were present:

1. A dangling symlink in `queue/pending/` is skipped by
   `retire-child-venv:84` (`[ -f "$file" ] || continue`).
2. A non-regular pending directory is skipped by the same guard.
3. A dangling `env` symlink for a running worker is skipped by
   `retire-child-venv:104` (`[ -e "$file" ] || continue`).

These are uninspectable safety conditions. The brief requires unreadable
inspection to fail closed and requires checking all pending and running-worker
metadata/brief/env references. The fixture output records `rc=0` and
`retired ...` for all three cases. No production source was changed.

## Reviewed packet and source identity

Packet directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-venv-1512/evidence/kit/`

The packet contains exactly:

- `request-retire-venv`
- `dispatcher-daemon`
- `retire-child-venv`

Packet SHA-256 recheck (matches the author manifest):

```text
f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15  dispatcher-daemon
4713b456ae4b0dcabdbc64ddf41aff731ac10fe4d11695d315e6743b864aef10  request-retire-venv
47a3661c0bd667fc7a457318717861a8821fe13b90b92bdaa42d0012b2467f36  retire-child-venv
```

Current authoritative predecessor hashes were unchanged and matched the
author manifest:

```text
b68f1d9aafe3d4cca6feb9413fcd9e4d51da5d8e30c4b2c7ed107ebf79a79dee  orch/bin/dispatcher-daemon
f9e5ea6f2ff577ebd25218a1eba751e17fafd474b1e1a3a3adbb8524a80c440e  orch/bin/request-child-venv
39450feacd8ff7d566e19fd6ce0aadc5c02366db1bccd9c88f9cd3a3ceef614f  orch/bin/make-child-venv
```

`diff -u` shows exactly one added dispatcher branch line; all other dispatcher
bytes are retained. The branch parses `RETIREVENV ` with `head -c11`, passes
one quoted argument to the handler, and leaves the existing FIFO/result paths
unchanged.

The marker names and format match the existing provisioner: `make-child-venv`
writes `.astrid-source-commit` and `.astrid-runtime-source-commit` at its
lines 160–161. The handler requires both existing regular readable files and
40–64 lowercase hexadecimal characters.

## Independent evidence

Test source (reconstructed independently; author test script was not reused):

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-review-resume-1534/independent-review.sh`

Fixture output:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-review-resume-1534/independent-tests.log`

Exact commands and results:

- `bash -n <packet>/request-retire-venv <packet>/dispatcher-daemon <packet>/retire-child-venv` — **PASS**, exit 0.
- `bash -n independent-review.sh` — **PASS**, exit 0.
- `independent-review.sh` — **FAIL as expected for this review**, exit 1; `SUMMARY pass=33 fail=3`.
- `sha256sum <packet>/*` — **PASS**, hashes above.
- `diff -u orch/bin/dispatcher-daemon <packet>/dispatcher-daemon` — **PASS**, one added line.
- `command -v shellcheck` — unavailable; no ShellCheck result is claimed.

The 33 passing cases cover the eligible aged read-only target; strict exact
names; slash, dot-dot, spaces, quotes and newline names; young and exact-one-
hour targets; target and nested symlinks; partial/active builder siblings;
missing and malformed provisioner markers; suite and env references; env
symlink inspection; running-worker metadata references; unreadable suite
inspection; live process target use; outside-fixture preservation; exact
dispatcher normal call shape; malformed request refusal; and the positional
request payload.

The handler's Linux process inspector was exercised through `/proc` with a
fixture process holding a target file. It refused with status 2. The review
did not launch the actual dispatcher daemon or any host tool.

One ancillary observation: successful fixture runs emitted repeated
`line 114: echo: write error: Broken pipe` diagnostics from the
`ancestor_pid` process-substitution scan, although the handler still returned
0. This is noisy normal-path behavior, not the verdict-driving safety failure.

## Limitations and required author follow-up

- No live install, atomic replacement, predecessor backup, daemon invocation,
  venv build/removal, provisioning, network, Git write, `ensure-daemons`,
  `run-manager`, or `hub-sync` was performed.
- The fixture-only `RETIRE_VENV_WORK_ROOT` redirect was used solely to keep the
  handler away from `/home/user/work`; the outside sentinel stayed unchanged.
  Production compatibility still requires the dispatcher environment not to
  inherit an attacker-controlled redirect.
- The two-stage fingerprint and final Python recheck were inspected, but no
  independent adversarial swap was run in the small interval between the
  final `os.stat` and `shutil.rmtree`; no stronger race-proof claim is made.
- Author evidence reports 35/35, but this review is independent and its three
  failures are concrete. The packet must be corrected and re-reviewed before
  any `KIT CHANGE` installation or board publication.

