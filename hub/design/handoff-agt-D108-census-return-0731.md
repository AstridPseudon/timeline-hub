# F-D108 first-return report

The census0724 output-target error is corrected. The Agent-owned derivative
handoff is now at `handoff-agt-D108-census-0724.md/.json`.

Findings preserved exactly:

- raw Agent selectors: 105;
- declared selectors: 104 = raw minus the approved D18 scope exclusion;
- reconstructed family rows: 103 = raw minus D18 and the unresolved Windows registration selector;
- `declared - reconstructed` is exactly `tests/test_installer_windows_tasks.py::test_register_scheduled_task_accepts_rendered_xml_string`;
- D18 is an approved scope exclusion, not retirement. Its fresh and current predicates are not exact-equivalent;
- the current `tests/test_installer_windows_tasks.py` source exists and retains the sibling cleanup selector, but the registration selector is absent. Both Windows selectors remain required for F-final;
- no durable source corruption is proven and no Windows body was run.

The accidentally amended Runtime-authored files were first snapshotted under
the return worker's evidence directory, then restored byte-for-byte from the
prior worker's logged reverse-patch preimages:

- Markdown git blob: `354c2aa0a41371568eb672d434dba9743b15d004`;
- JSON git blob: `cd7847582b8f73f445768d3ac519de4d28f06630`.

## Validation

- Own JSON parse/marker/set assertions: PASS.
- Runtime JSON parse after restoration: PASS.
- `git hash-object` preimage checks: PASS for both Runtime files.
- `git diff --check`: PASS; no Agent repository files changed.
- No tests, imports, collection, helper execution, services, probes, Windows body, install, render, host scripts, or product/test/ledger/pin/generated edits were performed.

Blocked/unverified: the Windows registration test remains an explicit F-final
gap; this source-only return does not author or execute its body.

