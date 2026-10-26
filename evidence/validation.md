# P4 D141c operational validation

## PASS_OPERATIONAL_SOURCE

- `git status --short --branch` — clean product worktree before packet edits; only this operational packet is changed.
- `git -C <Agent|Runtime|App|Composition> rev-parse HEAD HEAD^{tree}` and `git status --porcelain --untracked-files=all` — exact four-way tuple and clean source snapshots; before/after receipts are in the task evidence `body-evidence/` directory.
- `sha256sum` of the immutable final manifest — `67ef4348b4b77eb02b74abe20ad6fefdb075f980dc8ca563c0a3c79d1f0e5b9f`; private selector copy — `59a41669300bdd97fbe7925a36958534abb7a5d7e793dd4ee26fb8c197668ac4`.
- Production launcher `tools/p4-d73-pinned-launch.sh` — unchanged SHA-256 `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`.
- Positive exact launcher `run` control on the durable packet paths — preflight exit `0`, body exit `17`, unchanged approved 2234 stub counter `1`; genuine materialized manifest hash equals immutable input hash.
- Poison exact launcher control with only `agent_sha` changed — exit `1` with `D73 launcher: agent SHA mismatch`, counter `0`, no body receipts.
- `for f in evidence/receiving.json evidence/controls.json evidence/source-manifest.json evidence/findings-map.json; do python3 -m json.tool "$f" >/dev/null; done` — PASS.
- Candidate row token inspection — contains `run -- -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration --junitxml=...` and exactly the three primary selectors in settled order.
- `git diff --check` — PASS.

The actual service `agent-p4-current-becfe-http-3legs-1026005145-1347` remains retained as exit 1 before pytest, with zero selectors and no JUnit. No body, suite CAS installation, original submission, full suite, or alternate route was run here.
