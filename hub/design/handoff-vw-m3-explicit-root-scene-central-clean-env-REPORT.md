# D09 explicit-root central qualification

Scoped result: **APPROVE for the six existing root-preparation cases**, with
the central pytest process passing all six. The central lane's wrapper exit was
nonzero only because its first cleanup implementation removed the private
stage contents but forgot the empty stage root; the helper was corrected and
the private cleanup was then verified locally. No test assertion failed.

Exact tuple and origins:

- Agent source: `4611a59fc398d15180d9c93c1ce3557135d6e291`.
- Runtime archive/module source: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Node: SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Peer graph: `f8164bef73215272562c4d6974acadbd82c2898a`.
- Composition public12: 77 files, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Preflight imported `astrid` from the central snapshot and `runtime_protocol`
  / `astrid_runtime` from the private Runtime archive; no installed-source
  shortcut or old helper path was used.

Evidence:

- Central request `1020161031-2219`: `6 passed in 18.32s`; result log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-explicit-root-scene-central-clean-env-integration-viewing-explicit-root-scene-clean-1020161031-2219/log.txt`.
- Local pure import preflight: PASS, recorded in `preflight.json`.
- Local corrected private-stage cleanup helper: PASS; stage absent afterward.
- `git diff --check`: PASS.

No product, browser, fresh-PNG, full-suite, install, network, SDK activation,
or private deletion changes were made. The SDK caller remains unqualified as
directed.
