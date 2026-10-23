# Agent F-D13 independent review — installed preflight inputs

Date: 2026-10-23

## Verdict

**PASS for the D13 input carrier and the one permitted original preflight.**

The exact original node `tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight` was independently collected once and passed once. This qualifies only the installed preflight. It does not qualify Runtime service activation, the native body, browser execution, or rendering.

## Reviewed inputs and custody

- Agent source under test: commit `ef851b22c506245441b9a630c093b3460e39cbdc`, tree `b11eee891208d11e23c55950f8954ddd3377d5a8`.
- Profile: `/home/user/work/venv-agent-child-f1012-installed/profile/astrid.json`, a regular non-symlink file; SHA-256 `8339f65743af469f940dbc5e25780e97204d048e35ebc83a773584fc3ab72352`.
- Seven-key carrier: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D13-inputs-1017/d13-bindings.json`, a regular non-symlink file. Its exact keys are `agent_commit`, `agent_tree`, `agent_wheel`, `agent_wheel_sha256`, `runtime_environment`, `source_checkout`, and `source_digest`.
- Carrier values resolve to the durable f1012 installed site-packages tree and environment, current Agent `ef851`/`b11eee`, wheel SHA-256 `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`, and source digest `302834da6581954c2cb070e99fb4021bea6775cdde2ba351057ca832279f2326`.
- Installed package versions are Agent `0.1.0`, Runtime `0.1.0`, and `astrid-runtime-client 0.2.14`. Required imports resolve inside the selected site-packages tree: `astrid`, `runtime_protocol`, `astrid_runtime_client`, and `banodoco_timeline_schema`.
- Installed Agent wheel/source/RECORD parity and the profile path/origin/symlink checks are exercised by the original preflight and passed.
- Tool identities used by the preflight are the existing selected values: Node 20.19.4 (`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`), Composition lock (`b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`), Chromium (`85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`), FFmpeg (`ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41`), and FFprobe (`272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f`). The test hashed these paths but did not launch them.

## Compatibility correction

The input handoff's statement that Runtime `1365` is not proof of the frozen Runtime tuple and therefore must be replaced by a newly installed exact `34e` pair before native activation is too strong as a general claim.

Observed facts:

- Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4` / tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa` is a descendant of frozen `34eac0041b0891e9011966b39bcbd26053fde5bc` (`git merge-base --is-ancestor` passed).
- The installed client bytes match the published Agent tuple in `runtime.lock.json`: `astrid_runtime_client/__init__.py` `78a69901…`, `contract_metadata.py` `a79b2e12…`, `generated.py` `9b5686c3…`, and `timeline_commit_types.py` `88c67d9e…`.
- The installed `astrid/core/timeline/schema/edit-command.schema.json` is exactly SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, equal to the Agent worktree's frozen file. The installed client reports contract `0.2.14` and schema digest `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.

Therefore the correct rule is: freeze the published client/schema tuple and require the actual test's source-custody contract if that contract explicitly requires exact Runtime source bytes. A Runtime source SHA differing from `34e` does not automatically invalidate a compatible execution descendant, and no new installed `34e` build is required absent such a real test-contract/source-custody requirement. This review does not waive any later native test's explicit custody requirement; it only corrects the automatic-invalidity claim.

## Exact test evidence

The source tree was clean at `ef851b22…`; no product/test/environment files were changed.

1. Collection:

   `env -i ... /home/user/work/venv-agent-child-f1012-installed/venv/bin/python -P -B -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight`

   Result: **1 test collected in 0.86s**.

2. Qualification:

   `env -i ... /home/user/work/venv-agent-child-f1012-installed/venv/bin/python -P -B -m pytest -q -o addopts= -p no:cacheprovider tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight`

   The `...` expands to the exact profile, seven-key carrier, wheel/source, Node, Composition, Chromium, FFmpeg, FFprobe, and private `TMPDIR` bindings listed above. Result: **1 passed in 4.43s**.

3. Installed-only import/hash audit from `/tmp` with `PYTHONPATH` set only to the selected site-packages: **PASS**. It confirmed the four required package origins, versions, contract `0.2.14`, schema digest, all four client hashes, and d106 schema hash.

4. Read-only source check: Runtime `1365` descendant check **PASS**; current Agent `git status --short` was empty.

## Negative custody and limits

The preflight implementation refuses wrong source/profile paths, source digest drift, wheel hash drift, source-archive mismatch, missing or symlinked RECORD members, package tampering, substituted native-tool hashes, symlinked tool/project/node-module paths, and origin escapes. The original file retains explicit negative tests for wrong source profile, substituted tool, installed package tamper, and unsafe/symlinked RECORD paths. They were inspected but not run, because this task permits qualification of only the one named original test.

The direct helper probe was not used as evidence: importing the test module outside pytest hit Astrid's intentional direct-pack invocation guard, and I did not bypass that guard. No service, launcher, daemon, socket, Runtime HTTP path, native journey, browser, renderer, package build, shared dependency, pin, or Git write was performed. The prior 24359 targeted run used an unconfirmed projection environment and failed four nodes including D13; the present authentic f1012 installed carrier is a meaningful input change and independently passes the exact preflight.

