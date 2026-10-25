# U4a validation

## Source identity

- Agent base: `0b586e4b56cffbcd066ea8792adf46b660f5395a`, tree `bb23455ea5f38120c251a91f4a4afeeb1ea3d5ce`.
- Runtime producer: `/home/user/work/runtime`.
- Runtime SHA: `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.
- Runtime tree: `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- Runtime source was clean before and after refresh.

## Change

- Normal command: `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/runtime` — PASS.
- Tracked diff: `runtime.lock.json` only.
- Lock change: `source_commit` `42aad0e92f6da8ea83dd0a382a87e3acd12651b0` -> `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`; no client/schema/fixture bytes changed.

## Acceptance checks

- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime` — PASS.
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — PASS.
- Canonical 15 mapping/hash audit against Agent normal base and released Runtime — PASS; all 15 equal both, lock hashes match current bytes.
- Relevant tools/client `py_compile` to `/tmp/w-667bcc498a/agt-U4a-tags-normal-1323-compile` — PASS.
- `git diff --check` — PASS.

## Test admission

- Free disk at admission: 4,640,792 KB (4.64 GB). Under the 5 GB threshold, so the brief required source-only/static checks; no focused pytest/tool test lane was started. Node/test proof remains pending for the central service or a later admission with sufficient disk.

## Evidence files

- `adoption.json`: exact source/tree, before/after lock identity, canonical 15 rows and equality results.
- `identity-before.txt`, `identity-after-refresh.txt`, `canonical-before.tsv`, `release-source-hashes.tsv`: source and hash receipts.
- `refresh-runtime-client.log`, `vendor-lock-check.log`, `artifact-manifest-check.log`, `compile-tools.log`, `git-diff-check.log`, `final-diff-name-status.log`: command outputs.
