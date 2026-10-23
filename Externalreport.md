# F legacy admission external report

## Result

Fixed the generic-host admission failure for the supported minimal capability
record used by the legacy assembler refusal test. `_renderer_selection` now
treats a record without an adapter as having no selected Remotion adapter and
returns no renderer selection. Real `CapabilityRecord` instances still use
their existing adapter and all existing admission guards remain unchanged.

The production caller is `GenericPackHost._run_task_impl` at
`astrid/core/execution/generic_host.py:8898`; it runs during the real leased
task admission path before the immutable legacy-assembler refusal at line
8955.

## Exact source and delta

- Base commit SHA: `2e21af300abbefc8afbad217189fa4715cf82616`
- Changed source: `astrid/core/execution/generic_host.py`
- Source delta: 2 insertions, 1 deletion
- Working-tree source blob SHA after the fix: `8f48f8f7c3126df26ab5499f945b48e0c5e5f450`
- No tests, fixtures, environment files, pins, schemas, clients, contracts,
  shared dependencies, routes, or alternate executors changed.

## Evidence

- Acceptance: `1 passed in 4.86s`
- Adjacent renderer-selection controls: `8 passed in 89.08s`
- Ruff: `current=2149 baseline=2149`
- Mypy baseline: `current=1912 baseline=1912`
- Vendor lock: `ok runtime.lock.json`
- Artifact manifest: `artifacts.json is current`
- Diff check: passed

The acceptance test preserved the `immutable original target` refusal, one
fenced Runtime failure call, no execution calls, and byte-identical proposal
artifact. No full, browser, render, heavy-journey, P1/P4 HTTP, native14, or
crash24 suite was run.

Independent review remains required before home merge.
