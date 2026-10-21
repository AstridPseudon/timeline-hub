# Agent to Runtime: Gate 7 element typing

Goal: repair only concrete current-only typing findings in existing project-pack/schema resolver boundaries. This is delegated Agent source work; Agent will not dispatch a competing worker.

Base: current Agent integration, initially bb9abfd9348880601224cd85af78de9e8c8212d8; merge forward onto current HOME just before remote submission.

Allowed product files: astrid/core/element/project_packs.py and astrid/core/element/schema.py. Existing direct tests only if needed. Runtime, generated contracts, pins, schemas and public shapes are unchanged.

Evidence: design/agent-mypy96-current-owner-classification-0639.md and exact raw current/Main streams under workers/agt-m4-mypy-current-raw-diagnostics-capture-0625. Sites are project_packs.py483/502 index findings and schema.py405/419 return-value plus406/414 assignment. Read exact messages rather than relying on stale line numbers.

Done: existing types or checked control flow fix those concrete findings without Any/cast/ignore, source authority changes, fallback declarations, latest selection, local-disk replay, or weaker schema/retention guards. Preserve exact DocumentPin/snapshot bytes/owner lookup. Run smallest selected-pack/schema direct controls and module-level typecheck. No repeated full/global mypy/native/HTTP. Return current-preserving commit with exact source/test report through request-merge-remote; Agent supplies normal source-owner gate. If a real semantic correction is required, report it before changing the contract.

Shared dependencies remain read-only. No new DTO, store, endpoint, version, release or pin.

