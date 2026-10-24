# D52/G4 READ-ONLY investigation report

## Root cause

The failures are caused by missing Runtime distribution availability in child interpreters:

- Agent’s `pyproject.toml` does not declare `astrid-runtime`.
- Runtime’s separate `astrid-runtime` distribution owns `runtime_protocol`.
- Current `venv-agent` lacks that distribution.
- Installed child setup strips `PYTHONPATH`; source child filtering only admits site/dist-packages roots, not arbitrary Runtime checkouts.

The first import sites are:

- `astrid/core/execution/generic_host.py:42` — generic-host worker startup.
- `astrid/core/rendering/remotion_runtime.py:26` — registry probe/bootstrap.
- `astrid/core/rendering/publication.py:18` and Three.js renderer imports — rendering paths.

Current source has no `_sanitize_child_env` symbol; the equivalent path is `CommandTransport._build_environment()` → `build_child_subprocess_env()` → child process launch.

## Traceback-chain comparison

These are a shared environment condition, but not one identical caller chain:

1. 15 local bootstrap cases:
   `ensure_pack_host` → Remotion validation → registry discovery → `remotion_runtime.py:26` → `ModuleNotFoundError: runtime_protocol`.

2. Four retained generic-child cases:
   `generic_host_worker.py:23` → `generic_host.py:42` → missing `runtime_protocol` before child payload execution.

3. Fourteen retained rendering cases:
   `CommandTransport` or generic-host worker → selected renderer/publication module → missing `runtime_protocol`.

The remaining summary-only/unknown cases and the stale `255b` profile case are not included in this conclusion.

## Evidence

- Exact local run: 15 failures, exit 1, 133.04s.
- Evidence: `/tmp/.../workers/agt-F-D52-bootstrap-local-1156/evidence/local15.xml`
- XML hash: `3c6dd12b277c553ece06acb8cf6ad0bc5697279f6e920fe6396cd7ba3db9f110`
- All natural stderr records report `ModuleNotFoundError: No module named 'runtime_protocol'`.
- Local probe metadata shows `census_complete=true` and `custody_admitted=true`; the failure is `original_wait_exit_code=1`, so this is not an attestation/custody rejection.
- Existing properly installed child evidence passed with Runtime available, proving the package boundary is functional when provisioned correctly. It does not qualify the current `venv-agent` tuple.

## Classification

- (a) Required Runtime distribution missing from child setup: **confirmed**.
- (b) Unnecessary eager Runtime import: **not supported**. SDK/package roots and renderer launcher selection are lazy; affected host/rendering modules use Runtime platform/custody APIs.
- (c) Legitimate source-custody boundary: **present but not the failure**. Do not add arbitrary Runtime checkout paths or weaken guards.
- (d) Unsupported fixture boundary: **confirmed for source-only generic child fixtures** that provide Agent source but no Runtime package/source closure.

## Smallest legitimate fix

Provision every supported child environment with the exact compatible `astrid-runtime` distribution matching the selected Runtime/client tuple. If Agent is intended to be independently installable, add that compatible Runtime dependency to Agent’s production package metadata; do not solve this with a generic `PYTHONPATH` overlay or lazy-import weakening.

The existing 10:16 schema/child-admission hold remains. Exact current installed-child origin evidence is still required before qualification.

## Verification and changes

No product or test files were modified; the v2 request/receipt contract remains untouched. No source execution or new probe was performed by this worker.

Read-only checks:

- `git status --short` — clean.
- `git diff --check` — clean.
- Required `DONE` marker created.
- Commit message written for the harness.