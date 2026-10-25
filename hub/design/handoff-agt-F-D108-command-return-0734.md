# F-D108a first-return publication refinement

Updated `design/agent-core-full-command.md` only. The published Agent
`agent-core-full` recipe keeps the existing 22 selector roots and row body,
the exact Agent `070dfc` and Runtime `1daca` guards, the existing launcher,
environment, timeout, JUnit, source-pair guards, and production caller
reminder.

The runnable fragment now takes only MAIN-bound checkout, manifest, and
evidence variables. It no longer invents a profile path or duplicates the
launcher’s manifest-bound profile/schema/Node exports. The preflight section
now gives the existing launcher dry-mode argv for MAIN’s parsed-row positive
and poison controls, with MAIN-bound control and counter paths. It requires
positive exit 17 plus one counter line and poison nonzero plus zero counter
lines. These controls are specified, not claimed as run by this worker.

Validation performed without executing the preflight or body:

- `bash -n` on both published shell fragments: PASS.
- Placeholder/redundant manifest-variable check: PASS.
- Existing launcher mode/argv, timeout, JUnit, and source-selector checks: PASS.
- Document inventory and exact command argv: 22 roots, byte-for-byte path/order
  equality: PASS.
- `git diff --check`: PASS.

No pytest/import/collection/body/helper/probe/service/browser/render/install or
registry write was performed. MAIN still owns parsing, installation, CAS, the
two controls, and submission.
