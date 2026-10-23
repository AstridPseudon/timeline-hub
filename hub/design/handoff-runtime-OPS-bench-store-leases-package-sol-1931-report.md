# OPS-bench-store lease package1931 — PACKAGE SOURCE PASS

2026-10-23. Packaging/custody correction only. Combined store remains **FAIL/UNQUALIFIED**; permission1905 remains **STOPPED**. This packet does not qualify installation, combined creation, or readonly publication/deletion.

All release files are flat in this report's directory with prefix `handoff-runtime-OPS-bench-store-leases-package-sol-1931-`. Runtime base is `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`. Product, caller, core, fixture, tests, generated clients, pins and live kit/config/queue files were not edited. The Runtime integration worktree remains clean at that head. Only new documentation/custody files were added to this worker worktree. The harness owns the eventual commit; no Git mutation was performed.

## Custody correction and preserved failure

The original sixteen-entry final1918 manifest is retained byte-for-byte as `oldmanifest.sha256`; all fifteen stable entries still pass. Its one failing entry records worker `report.md` as `a90a816b56c51e568129b77491888776ba3267a0aaa6fb4b79d583cdfd209286`, but the surviving harness summary is `d66d207226ea20a4d8414a5b8702af98d33b7c337533dfa45f1069fc0192d143`. That surviving summary is retained byte-for-byte as `oldreport.md`. The separate surviving canonical detailed report is retained as `old-flat-report.md` and hashes `a90a816b56c51e568129b77491888776ba3267a0aaa6fb4b79d583cdfd209286`. This does not establish the lost worker report's exact bytes: those bytes were not recovered or reconstructed. No old artifact was rewritten and the historical 15/16 failure remains disclosed.

This complete stable report was written before generating the new relative-name `hashmanifest.sha256`. That manifest covers every other file in this packet, including this report, the frozen validation log, original source logs and custody mapping. It excludes itself and every mutable worker summary, final author response and DONE/commit-message file. No released bytes are changed after hashing. Verification output goes only to the worker's separate manifest-check log.

## Exact unchanged sources and retained independent proof

Core dependency: `88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`. Caller test-run: `f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4`. Embedded seam: `c20bcba62165c3498899e731c3dfcaaff8316bffbeb48008cbe0307beb9a2bc9`. Fixture: `0081fff4a924346674686399570234fae4c64a054575709fee7e18fcbb3c3577`. Both patches and the original caller also pass SHA/cmp against final1918. The already independently passing production two-line caller fix is retained unchanged.

Authoritative independent1923 log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-bench-store-leases-review-1923/log.txt`.
Original uncompressed SHA256: `8270363f759051e4b1fd2ead11b1d628ea40e3cd061c480cf876665f0d99d669`; exact length 2,617,735 bytes. Its lossless deterministic gzip copy is `handoff-runtime-OPS-bench-store-leases-package-sol-1931-independent1923-source.log.gz`. Decompression and SHA/cmp against the authoritative original passed. The complete log, including commands, before/after source hashes, all 24 test names, `Ran 24 tests in 8.631s` and `OK`, is retained without excerpting or rewriting. `custody.json` records original absolute paths, uncompressed digests and local flat filenames for all 23 copied artifacts. Independent report and handoff are also retained byte-for-byte.

The independent historical command was `TMPDIR=/tmp/rtleases1923b.dAm3YO python3 -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-leases-return-1918-test-leases.py`: **24/24 PASS, 8.631s**. This worker did not run that command, the 15 projection tests, or the 18 core tests. No behavioral retest was needed because their executable bytes did not change.

## Validation and evidence-only validator delta

Exact command run from this worktree:

```bash
python3 -I docs/handoff-runtime-OPS-bench-store-leases-package-sol-1931-validate.py --originals --runtime /home/user/work/runtime > docs/handoff-runtime-OPS-bench-store-leases-package-sol-1931-validation.log 2>&1
```

Exit 0: 23 custody artifacts SHA/cmp PASS; prior stable manifest 15/15 PASS plus the one preserved historical mismatch; `bash -n` caller PASS; in-memory compile of core, seam, unchanged fixture, old validator and new validator PASS; embedded seam byte equality PASS; full patch dry-run/replay/cmp PASS; caller-only patch dry-run/replay/cmp from lease1850 PASS; all bytes outside the embedded seam unchanged; independent proof lossless preservation PASS; Runtime2a9 clean status and diff check PASS. The frozen log records the actual expanded commands and outputs.

Only the evidence validator is new. `oldvalidate.py` preserves its predecessor exactly. The new validator resolves packet inputs relative to itself, uses the immutable local custody mapping, and verifies portable patch replay/cmp and compilation without executing the fixture. Optional `--originals` checks authoritative external paths; optional `--runtime` checks a supplied readonly checkout. The original fixture source retains its original absolute/naming dependencies unchanged and is preserved as evidence, not repointed to a new runtime. Historical live/immutable input manifests and source logs are retained unchanged; the portable default does not require their external paths.

After final report creation, the manifest is generated from sorted packet filenames and checked using `(cd docs && sha256sum -c handoff-runtime-OPS-bench-store-leases-package-sol-1931-hashmanifest.sha256)`. The standalone validator is then run again without `--originals` against the sealed packet to check portability and the full final manifest. These checks do not modify packet files; results are recorded outside the release in this worker's `manifest-check.log`.

Additional source checks: `git diff --exit-code` and `git diff --check` exit 0; HEAD remains Runtime2a9. Full C0v2 request/reply contract bytes equal HEAD and integration (`SHA256 4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`). Frozen34e remains `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.

## Decisions, limits and next action

A separate stable report replaces mutable worker-summary custody. Relative filenames make the release manifest portable; lossless gzip keeps the full authoritative log within the 2 MiB durable budget. Packet payload is below 1 MiB and private scratch below 5 MiB; no fixture allocation occurred. No full suite, test service, combined child, readonly publication/deletion, HOST, chmod, denied-path retry, alternative cleanup/publication, install/provision/network or live kit action occurred.

Core1915's separate original matrix remains **17/18** (inode-nonreuse assertion, also red on frozen1858). Permission1905's readonly/combined lifecycle remains unresolved. Historical timeout/escaped-descendant limits in the retained original reports still apply. Source/package PASS grants no combined or installation qualification. Next: independent **PACKAGE-ONLY** custody review of this manifest/report/log and exact sources; no behavioral retest. Orchestrator owns subsequent disposition.
