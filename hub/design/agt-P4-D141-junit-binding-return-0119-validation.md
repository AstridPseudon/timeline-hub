# P4 D141c operational validation

## PASS_OPERATIONAL_SOURCE

- Read-only Git blob review: PLAN §3 P4/C0, `tl/agt-P4-D141-result-review-0114:evidence/{review.json,findings.md,handoff.md}`, and the prior 0101/0106 operational packet. The prior result review's single finding is `P4-D141c-R001`.
- Frozen source tuple: Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`; Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / tree `ac5b862744bece65b2e30565db1777bacd60da28`; App `867cb2737af1b46dc608c7cd37c349e920fe9422` / tree `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`. All four were clean on both read-only checks.
- `sha256sum` of the new immutable input: `95f5ce93705a50cff41559d5a23cd1c43fd9d3611f269bb3acb197ed942a4ab3`; selector copy: `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`; candidate row: `630bb12343a20b336092480553acf77bbf192d866b1598421723417c79ee3df4`.
- Field-by-field diff against preserved original manifest: only `junit_paths` changes. All pin, origin, parent, source guard, profile, version, selector, timeout, and service fields are unchanged. See `manifest-diff.json`.
- Python key-value diff — PASS: normal input differs from the preserved original only in `junit_paths`; poison differs from normal only in `agent_sha`.
- Existing launcher `/home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh` hash `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`; existing CAS installer hash `1fbcbc866a170212709e3e0f647f6d7082338eb819d42199f74b25b7e9d01805`. No installer or registry invocation occurred.
- `bash -n /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh` — PASS.
- Positive unchanged launcher control: `.../p4-d73-pinned-launch.sh <new-manifest> run -- -c <stub>` — preflight `0`, body `17`, counter `1`; generated materialized manifest and runmanifest both contain the new bound JUnit path.
- Agent-SHA-only poison launcher control: same `run` mode with poison manifest — launcher exit `1`, diagnostic `D73 launcher: agent SHA mismatch`, no preflight/body exit receipt, counter `0`.
- Realpath/symlink/same-file checks: immutable input and launcher materialization are distinct regular files, not symlinks, and the materialized bytes equal the input bytes. The intended JUnit path was absent before any actual proof; no fake XML was created.
- Stale-path check — PASS: absent 0047 JUnit path remains absent; preserved 10086 XML remains at its original 0055 path with SHA `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d`; new bound XML path is intentionally absent pending the corrected actual proof. `df -B1 /tmp` available bytes `4767846400`, above the 4.6 GB source floor.
- `python3 -m json.tool` on all five JSON outputs — PASS; Python stdlib `shlex`, `json`, `hashlib`, and `pathlib` invariant script — PASS; `git diff --check` for the worktree — PASS.

## Preserved and not claimed

- The genuine service `agent-p4-current-becfe-http-3legs-1026011042-10086` remains the prior `3 passed / 0 failed / 0 errors / 0 skipped`, exit `0`, with JUnit SHA `afca45b778f118b22f30e2cac08654a902dd86241b76442f146ae0ad8623316d` at its original 0055 path. It is not relabeled as the new durable path.
- Historical service `agent-p4-current-becfe-http-3legs-1026005145-1347` remains exit `1`, zero selectors, no JUnit.
- This packet claims no pytest/body rerun, suite installation, full suite, product qualification, cumulative P4 verdict, MAIN GO, REG, ship, or behavior credit.
