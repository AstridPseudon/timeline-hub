Implemented the normal private Runtime pin.

Changed:

- Vendored generated clients and metadata from Runtime `95202c2b09e83aaae028287d6c59b773410141f3`
- Runtime tree: `d438d3e28a29ad80fa6b7c19c55e1b7a4485eae2`
- Updated `runtime.lock.json`
- Preserved schema `55/29/12`; schema bytes remain `613123...`

Tests:

- Vendor/schema: 32 passed
- Provider/capture: 175 passed, 9 integration deselected, 2 pre-existing xfails
- SDK client: 9 passed
- Parity/lane: 23 passed
- Runtime artifact manifest: current
- Vendor lock check: passed

No full suites, integration merge, public release, or version adoption performed. `commit-msg`, `commit-msg.txt`, and empty `DONE` are written.