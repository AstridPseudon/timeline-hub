# P1 D21 dispatcher runtimebench: packet PASS; production NOTREADY

Completed the single host-builder packet. No App repository edits. PLAN §3 P1/D21 and settled exact inputs remain unchanged. No independent review was requested or launched.

## Authoritative publication packet

- Final standalone builder: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-make-runtime.sh`
  SHA-256 `6e346ea55a5df4df6d772f86e99c7d2797555c2fde830d978bc5fad74adbbee9`.
- Patch against `/home/user/timeline-hub/hub/kit/bin/make-runtime`: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-authoritative.patch`
  SHA-256 `263c467b740146c1fe00ef66c90142cfe120b7628f9e29ccf6117c68208c51b7`.
- Hash manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-sha256.txt`.
- Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-runtime-bench-sol-1310/report.md`.
- Flat report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310.md`.

Main/Codex kit owner must publish the patch from the hub repository root (paths are `kit/bin/make-runtime`) through the normal authoritative kit process. It passed `git apply --check`; this worker did not apply it. Local ORCH/bin/make-runtime was deliberately left untouched because hub sync replaces its bytes. No unwired helper is required: selection, acquisition, verification, build and publication are all in make-runtime. Existing child-venv packet 1303 needs its separate main publication; it was untouched.

Current authoritative/local builder SHA-256 remains `0bba1f5e69319dad8b68295eac1fddf7ba35ea21cc32d784407852700e7df202`, so production is NOTREADY until authoritative publication and a successful normal host queue run. This is a complete implementation packet, not a claim that a real runtime has been provisioned.

## Behavior and decisions

The unchanged public API is `make-runtime NAME AGENT_SHA [LOCK_SHA256]`. It accepts an exact Agent commit, rejects existing runtime paths (including dangling symlinks), aggregates independent preflight failures, validates engine declarations and the requested lock, and checks registration templates, commands, Linux/x86_64, atomic-rename availability, destination permissions and a 2 GiB free-space floor. There is no Git fetch/write or source checkout.

The builder selects an already-exact Node 20.19.4/npm 10.8.2 installation without changing it. An explicitly selected wrong toolchain is refused. Otherwise it downloads the fixed canonical Node archive and checksum manifest into the runtime's own unique partial directory, not a shared toolchain. It checks both pinned hashes and the manifest's archive entry before extraction, then checks executable versions. If bundled npm differs, its supported npm CLI installs npm@10.8.2 into a private prefix with engine-strict enabled, and the exact CLI/version and lifecycle-script PATH are used for npm ci. No engines, package-lock or dependency pins are rewritten; no --force is used.

The archive SHA `7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4` and manifest SHA `f8537bd20c8fdc951a20a4278e380e03e58e0a1689eaaa5c170b221435f3a22e` match the existing authoritative `/home/user/timeline-hub/hub/kit/bin/provision-agent-machine` pins exactly. They were verified by local source comparison, not guessed or fetched by this worker. Production verifies downloaded bytes against them; actual archive acquisition was not exercised here.

Agent input remains `5b1b4db8253f46e0e085908e79f309d492877386`; its actual Git lock blob hashes to `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`. Before and after npm ci, package.json and package-lock.json must retain their exact source hashes. Installed Remotion and Composition versions must match the lock (4.0.509 and 0.0.14 for this input). All files are made read-only before Linux renameat2(RENAME_NOREPLACE) atomically publishes the fresh runtime. This refuses even an empty destination introduced during the build. Failures retain unique partials and a stage-specific failure marker; nothing is cleaned up or overwritten. Registration is prepared before publication and uses noclobber for the env file. A post-publication registration I/O failure is explicitly reported as failure with the immutable runtime retained; a new name is needed for another build.

Limits: each curl has a 10s connect timeout, 60s attempt limit, one retry, 125s retry budget and 150s outer timeout (+5s kill grace); HTTPS is enforced for original/redirect URLs. npm acquisition is bounded to 120s (+10s kill grace), npm ci to 600s (+10s), executable version probes to 10s (+2s). The host job self-execs under an 840s total build timeout (+10s kill grace); read-only aggregate preflight also runs before this self-exec. Mock cases each have a 25s subprocess deadline; the actual JS guard has a 10s deadline. Acquisition/build commands in this packet execute only when the dispatcher runs the published builder outside the worker sandbox.

## Exact verification commands and results

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-make-runtime.sh` — PASS, exit 0.
- `python3 /tmp/w-183d5f447e/runtime_builder_mocks.py > /tmp/w-183d5f447e/mock-results.txt 2>&1` — PASS, exit 0. Eighteen isolated cases: aggregate missing prerequisites; wrong package engines; wrong explicitly selected toolchain; existing immutable destination; dangling destination; wrong manifest checksum; wrong archive checksum; interrupted download with retained bytes; wrong extracted Node; failed npm ci; mutated lock; module-verification failure; populated publish race; empty publish race; successful acquisition/build simulation; supported exact npm fallback; exact existing-toolchain selection without acquisition; old partial retained across successful fresh build.
- The same mock command also runs the real request-runtime writer with only its root constant redirected into scratch, then the actual dispatcher RUNTIME branch and packet builder. PASS: the exact name/commit/lock reach make-runtime and publish only in isolated mock storage. The production dispatcher/daemon was never started or changed, and the production queue was never written.
- The same mock command executes the builder's actual installed-module JavaScript against two JSON fixtures using the ambient Node interpreter. PASS for matching versions; expected nonzero for a mismatched Remotion version. No dependency installation/build is involved.
- `git -C /home/user/timeline-hub/hub apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-authoritative.patch` — PASS, exit 0 (read-only applicability check).
- `sha256sum -c /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-P1-runtime-bench-sol-1310-sha256.txt` from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design` — PASS, both files OK.
- Read-only Python comparison of both embedded pins to authoritative provision-agent-machine — PASS; exact Agent lock hash comparison — PASS.
- `sha256sum tests/e2e/local/three-products.p1-chain.spec.ts tests/e2e/local/three-products.spec.ts` — P1 `f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133`; P3 `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.
- `git hash-object tests/e2e/local/three-products.p1-chain.spec.ts` — `221d05890ba9f42d50520c9b655c21338aece782`; `git hash-object tests/e2e/local/three-products.spec.ts` — `37caf28577d42fbe98afd2320dffa3c72e6e74b1`. Both original bodies byte-exact.
- `git diff --check` and `git status --porcelain=v1 --untracked-files=all` from `/home/user/work/wt/ap2-P1-runtime-bench-sol-1310` — PASS, exit 0, empty status; HEAD remains `ce82f9dc1797e39172b4b0d78b202066935bbbd0`. Full v2 requests/replies, production callers, C0 schema/client pins and all product/test/generated files remain untouched.

Final retained mock output: `/tmp/w-183d5f447e/mock-results.txt`; final fixture/call/failure outputs: `/tmp/w-183d5f447e/runtime-mocks-f99j1eo0`. The harness-assigned `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-runtime-bench-sol-1310/tmpdir` is a pointer file containing `/tmp/w-183d5f447e`, not a directory. Scratch was placed in that assigned target. No files were deleted.

## Production wiring, readiness and next normal command

Production wiring is unchanged: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime` writes `RUNTIME NAME AGENT_SHA LOCK_SHA256` to queue/pending/runtime-NAME; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/dispatcher-daemon` executes `$O/bin/make-runtime` with that payload and uses the builder's exit status for done/refused. The builder replacement therefore executes acquisition through the existing route once main publishes it. Current request writer SHA-256 `15b07daf4cd46a225ecc020c11e3ec8f3a62368c73d9ba6940ad3ce4ea8191ff`; dispatcher SHA-256 `b68f1d9aafe3d4cca6feb9413fcd9e4d51da5d8e30c4b2c7ed107ebf79a79dee`.

After authoritative kit publication/sync, the manager's next normal queue command (suggested new name; never replace an existing destination) is:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-runtime agent-remotion-ap2-p1-5b1-1310b 5b1b4db8253f46e0e085908e79f309d492877386 f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
```

Manager owns matching the P1 suite's environment binding to the successful fresh name, obtaining the separately published child-venv, and then running the existing P1 service with its original bodies. No current host census was repeated. Real network reachability, real checksums/extraction, npm acquisition/ci and real production queue success remain unverified. No network/download/install/provision/build/full/browser/socket/HTTP-body/P1/P3 run or test-service request occurred. No shared dependency/cache writes, kit/hub-sync/dispatcher/host-process edits, Git mutations, pin changes, or independent review occurred. No safety/permission denial occurred. Worker completion does not clear the host readiness gate.
