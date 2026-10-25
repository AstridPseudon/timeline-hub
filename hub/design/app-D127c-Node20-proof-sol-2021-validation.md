# D127c Node20 validation

**BLOCKED / NOTPASS. F002 remains unqualified.**

The prior author2009 PASS assertion is corrected: `^(D127c source guard|D127c reviewed-profiler validator)$` matches zero registered titles because the actual names have suffixes. The reviewed-new title uses `D127`, without `c`. Review2013 correctly withheld Node20 credit, but its claimed sandbox-spawn cause was not established by its malformed selector alone. Old artifacts were not modified.

The corrected exact selection is:

```text
^(D127c source guard accepts every reviewed arm and rejects wrong hash or source|D127c reviewed-profiler validator enforces the exact safe cProfile projection|D127 reviewed-new validator rejects field, lifecycle, phase, truncation, and safety mutations)$
```

Intended full titles:

- D127c source guard accepts every reviewed arm and rejects wrong hash or source
- D127c reviewed-profiler validator enforces the exact safe cProfile projection
- D127 reviewed-new validator rejects field, lifecycle, phase, truncation, and safety mutations

| Execution | Result | Intended named passes |
| --- | --- | --- |
| Node22.22.0, same process (`--experimental-test-isolation=none`) | exit 0, pass 3/fail 0/skipped 0 | 3 |
| Supported Node20.19.4, sandbox | 30-second timeout, exit 124, TAP header only | 0 |
| Supported Node20.19.4, ordinary outside test service | terminal timeout, exit 124 after 48 seconds; command bounded at 45 seconds | 0 |

Service ID: `app-D127c-Node20-proof-sol-2021-d127c-node20-three-controls-2021-1025202505-11856`. Exactly one request was queued and followed to terminal status. The service printed the exact supported binary/version and required App source SHA-256. Its snapshot tree is `6d2744e271f016206854ab33f57b3cfc737ad54d`; no cache hit.

The separate sandbox Node20 fork probe returned `spawnSync ... EPERM`, child stdout empty, despite child status 0. That status is not credited. This establishes a sandbox spawn-probe failure in the current run; it does not establish the outside-service timeout cause. That cause remains unresolved. A TAP header or file-wrapper event never substitutes for intended test passes. Missing counts/events are not synthesized into success.

Source conservation: App fd586440/tree6d2744e equals final466c; exact support file SHA-256 `59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`. All tracked paths and the worktree remained unchanged. Runtime fb4addba/tree8d568 and committed helper095c verified read-only. Runtime61 evidence was reused without rerun. The `/home/user/work/runtime` environment value is only the path input used by these pure unit assertions; the three controls do not read or run its current helper. It is not claimed as the protected095c checkout.

Shared node_modules and the supported toolchain were read-only; TSX cache disabled. Every sandbox execution started above 5,000,000,000 available bytes (minimum 5,333,868,544). Final available bytes 5519310848. Scratch was approximately 1.44 MB. No heavy run, installation, acquisition, source fix, or prohibited body started.

One exact unit suite row was registered under the existing physical bench-store mutex with full-byte CAS and atomic replacement, preserving all pre-existing registry bytes. See `registration.json` and `named-suite-entry.txt`; no dispatcher/other row changes. The initial cross-device temporary-file rename failed without mutating the registry and was corrected to the normal same-directory atomic replacement.

Next: manager-owned bounded supported-Node20 interpreter/loader/child-registration diagnosis using the ordinary test service. This run provides a terminal failure packet, not an execution-qualified packet for closure2013. Keep F002 and D130 SWAP/WAL/recovery/full-tour/activation held; do not repeat the unchanged request or substitute Node22.
