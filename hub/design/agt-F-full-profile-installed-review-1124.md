# Report

## Verdict

**STRICT ACTUAL INSTALLATION: PASS**

Receipt identity:

- Installer worker: `agt-F-full-profile-install-1118`
- Source commit: `4a2a3472d1d921a29dd07462d542a51338abd8b6`
- Source tree: `1c2e81a69562a581817b8af7f945b5e5adb6702d`
- Candidate blob: `33c851af2ab5373fd60714e155d92acd84c1e6b1`

## Verification

- Installed row SHA: `0bdf88d2a61f89a6fb51ec7bf2fe1cca21268462e23b7e8cb5d430f4e248dd81`
- Registry SHA: `18deaf1e759fdb97b578ace0138139ae69940c21ae4b4bc9483c6c49e2c9e07c`
- Exactly one `agent full` row; 172 outside rows byte-identical, SHA `f14b6ef0…a8efc7`.
- Backup: `suites.conf.pre-20261024T112046Z.bak`, mode `0600`, SHA `31cfddf295b376036c62e08d935373a78fdc37f153f1445f4a69f08437c56133`.
- Candidate and installed row are byte-identical.
- `bash -n` passed.
- Mounted caller preserves existing profile `agent-remotion-v3-819acf-1110`, venv-agent, Node `v20.19.4`, Runtime `becfe6db88`, projection/schema `PYTHONPATH`, and `pytest -q -n 3`.
- Finite profile/archive/source preflight passed; fixture hash remains `ce4fb6c08ee5c682d3163eb0ab3eda856b59df59`.
- Existing profile manifest, lock, artifact, registry state, mode, archive contents, and read-only baseline all passed.

## Commands

- `git diff --check 4a2a3472d1^ 4a2a3472d1` — PASS
- Registry/hash/parity Python checks — PASS
- Installed-row extraction plus `bash -n` — PASS
- Finite `env -i ... python -P` profile/source/archive preflight — PASS
- No pytest, full suite, service request, registry mutation, or product test was run. Type/lint: N/A.

Worktree remains clean. Existing admission hold remains in force; next step is an orchestrator-authorized full run after the hold is lifted.