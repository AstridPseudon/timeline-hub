## Result

Completed the normal Agent consumer pin for Runtime `0.2.14`.

- Runtime: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- Runtime tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- Schema: `sha256:ce3781c2…30d59`
- Artifact: `sha256:f021e771…f20fa0`
- All 75 producer artifact hashes verified.
- Vendored bytes match the producer exactly.

Changed paths:

```text
astrid_runtime_client/__init__.py
astrid_runtime_client/contract_metadata.py
astrid_runtime_client/generated.py
astrid_runtime_client/timeline_commit_types.py
runtime.lock.json
```

Tests:

- Targeted local lane: **279 passed**
- Exact-provider central integration lane: **143 passed, 10 deselected**
- `vendor_lock.py check`: passed
- `git diff --check`: passed

No full suite, App browser journey, release, activation, integration pin, or shared dependency mutation was performed.

Report: [agent-ordinary014-normal-pin-candidate.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-ordinary014-normal-pin-candidate.md)

App’s same-cohort qualification and manager/peer review remain pending.