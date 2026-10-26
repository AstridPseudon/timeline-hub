# P4 D141l CLI selector handoff

Source-only preparation is complete for the one changed CLI original on Agent `ecdc242e` with Runtime `95d98f03`, qualified App `82e9e13d`, and Composition `635f4de0`. The target test is unchanged and retains every existing predicate.

The existing suite key `p4-current-becfe-http-3legs` has a new candidate row selecting only:

`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`

The input manifest is separate from body evidence, and the single durable JUnit path is consistent across the generated input, future runmanifest, and actual argv. The candidate is not installed. The existing controller owns the later CAS replacement and one normal request-test; no forced run or admission release is authorized.

The same `check-source.py check` invocation is the author/reviewer control. It runs only the unchanged production launcher with the original positive stub and Agent-SHA-only poison. It does not collect or run pytest, submit a service request, install a row, or create behavior evidence.

The production input is not ready because the exact supported profile state file is missing: `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.astrid-registry-state.json`. This is reported as a finite missing input, not an assumed receiving failure. The future heavy dispatch remains at least `4714564096` bytes free at dispatch, with a real 5-second trace, continuous 4 GB stop, and one heavy body; this preparation does not re-gate it.

Historical 10086/0114/0159/0202 artifacts remain references only and were not rewritten or retargeted. Historical 19479/8912 remain held and unstarted.
