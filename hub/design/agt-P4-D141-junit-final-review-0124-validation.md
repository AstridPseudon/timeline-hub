# Validation

All validation was read-only. No pytest, product import, collection, original body, socket, suite installation, registry mutation, controller dispatch, product typecheck, or lint was run.

- `git status --short --branch` in the review worktree — PASS; no worktree edits.
- `git diff --stat tl/agt-P4-D141-junit-binding-return-0119...HEAD` — PASS; no source diff.
- `git -C <pinned checkout> rev-parse HEAD HEAD^{tree}` and `git status --porcelain --untracked-files=all` for Agent, Runtime, App, and Composition — PASS; exact frozen commits/trees and clean status.
- `sha256sum /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh` and `git hash-object` — PASS; launcher file SHA `9f668e…110c`, blob `f1bde17…d988`.
- `bash -n /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh` — PASS.
- Stdlib JSON/key-value/hash validator over old/new manifests, generated control manifest/runmanifest, poison manifest, source packet, and receipts — PASS; only old/new manifest field difference is `junit_paths`; poison differs only in `agent_sha`.
- Stdlib `shlex` validator over `candidate-row.txt` — PASS; `run -- -m pytest`, later `-m integration`, `-o addopts=`, `-p no:cacheprovider`, timeout `45`, three selectors, and the environment-expanded `--junitxml` path are all present.
- `sha256sum`/`cmp` over 0047, 0055, and 0119 selector copies — PASS; all equal at `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`.
- Read-only positive/poison receipt checks — PASS; positive preflight `0`, stub body `17`, one counter line; poison launcher refuses with Agent SHA mismatch, no body receipt, zero counter lines.
- Stdlib XML/hash validator over retained 10086 receipts — PASS; request/summary/snapshot/ext/command/runmanifest hashes match retained records; JUnit SHA `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`, 3 tests, 0 failures/errors/skips, preflight/body exit `0`.
- Read-only retained 1347 check — PASS; exit `1`, zero selectors, no JUnit, same-file `cp` failure preserved.
- Read-only CAS receipt check — PASS as historical receiving evidence; current registry SHA `f59adb4816a5e8d0db445956af585daf9a771679cfbe2f2f1a6780529edb2aa0`, mode `0600`, prior installed row SHA `21f407…c2f0b`, outside-row SHA `660b72…c063c`. No 0119 install was attempted.
- Actual `KEEP` marker existence checks — PASS for workers 0047/0055/0105/0119 and raw services 1347/10086; durable ORCH record directories remain.

The missing direct body-process `__file__` telemetry remains explicitly bounded (W003). The App receiver-owned final body receipt remains pending (W004). These do not fail the candidate source packet.
