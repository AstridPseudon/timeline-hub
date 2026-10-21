# Agent handoff: Remotion readiness inventory repair

Base: `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`

Flat three-file unit:

1. Add `astrid/core/rendering/_remotion_package.py` with the exact approved
   Composition 0.0.13 manifest/export/dist validator from the current runtime.
2. Remove that 104-line cohesive block from
   `astrid/core/rendering/remotion_runtime.py`; retain module-local private
   aliases for `_COMPOSITION_PACKAGE_NAME`, `_COMPOSITION_PACKAGE_VERSION`,
   `_REQUIRED_COMPOSITION_EXPORTS`, and `_composition_package_problem`.
3. Update only row 31 in `docs/giant-file-rationale.md` to the verified 1,296
   lines and extraction reason. Preserve row 10 (`remotion/run.py`) for the
   separate Viewing worker.

Counts: 1,296 runtime + 104 helper; 1,296 is within the fixed 1,265+50
allowance. Package readiness tests pass: 6 passed, 1 deselected. No custody,
admission, source authority, caller activation, SDK/CLI, provider/compiler, or
pin changes. No independent custody review is needed for this packet.

The complete evidence is in the worker report:
`workers/vw-m4-current-remotion-readiness-inventory-repair-0349/REPORT.md`.
