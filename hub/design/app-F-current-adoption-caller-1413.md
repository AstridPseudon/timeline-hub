## Report

Implemented the guarded current-adoption caller refresh.

- Refreshed actual tuple:
  - App: `be98aac54e…`, tree `2839c7e7…`
  - Agent: `5ffc1f4dfa…`, tree `73a9a1fd…`
  - Runtime: `e68cf23164…`, tree `a2cbedd1…`
- Added pending-adoption handling without relabeling Agent’s old lock.
- Added source-only P2/P3 preflight using the separate pure-target metadata.
- Preserved 51 request and 133 reply/history fields.
- Recorded row hashes, outsider hash, candidate hashes, protected/native/encoded hashes.
- No product, tests, generated files, pins, registry, or design files changed.

Tests:

- `current-service-inputs.py --refresh`: PASS, status `pending_agent_runtime_adoption`
- P2/P3 normal and `-O` source preflight: PASS
- Adapter controls: PASS as explicit pending refusal; positive baseline not established
- Full preparation normal and `-O`: correctly refused with Agent lock mismatch
- Negative caller controls: refused as expected
- `py_compile`, JSON validation, and `git diff --check`: PASS

Remaining dependency: `/home/user/work/agent/runtime.lock.json` still names Runtime `becfe6db…`; it must be updated through normal Agent U4a adoption to Runtime `e68cf231…`. No service, HTTP request, install, or full suite was run.