## Report

Result: no already-supported dependency-only reuse route exists.

The current route is:

`request-child-venv` → authenticated exact-child scan → queue one request → `make-child-venv` → pinned requirements install → source archive/install → provenance/RECORD/freeze verification → `bench_store.Store.ensure()` registration.

Reuse requires the exact tuple:

- Agent source SHA
- Runtime backend SHA
- generated Runtime-client file tuple
- installed source snapshots, origins, markers, lock metadata, and RECORD

The bench key is derived from all three identity components. Therefore the immutable older child (`3b5c`, Agent `ba8f`) cannot qualify for the new Agent source (`bb50`, discovery fix), even with the same `proof.lock`.

Evidence:

- Failed candidate: `venv-agent-child-discovery-bb50-f320`, `pinned-requirements`, rc `124` after 600 seconds; operational timeout.
- `proof.lock` SHA-256 verified as `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`.
- Retained genuine child metadata confirms qualified non-editable source URLs, import origins, distribution metadata, and RECORD-backed installation.
- No package/network/provision probe or test suite was run, per the readonly assessment brief.

Missing private maker input: one normal maker completion for the exact tuple `(Agent bb50, Runtime f320, exact Runtime-client identity)` using the existing lock and custody path. The old child must remain untouched; no relabeling, cloning, in-place install, PYTHONPATH authority, or competing request is supported.

No Runtime files changed. `DONE` and the requested conventional commit message were created.