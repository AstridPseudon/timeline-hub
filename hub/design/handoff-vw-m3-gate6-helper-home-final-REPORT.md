# HOME merge-forward report

## Result

Resolved the normal HOME merge-forward in the App worktree. The worktree
contains HOME692 content plus the exact approved corrected helper patch
5754a2690b92c9f767e2a4d3684a14a602caa88817862d7ba72c242f30fe049a.

The current source parent is 909d2bfa186985db9791be0ab090b9f4e7824f9b.
The intended true merge parents for the harness commit are, in order,
909d2bfa186985db9791be0ab090b9f4e7824f9b and
692765846fef511047445fecef3e55ec8bb6a5bf.

The final delta relative to HOME692 is exactly:

- tests/e2e/timeline/viewing-parity/bootstrap.ts
- tests/e2e/timeline/viewing-parity/harness.test.ts
- tests/e2e/timeline/viewing-parity/harness.ts

The HOME-only additions and product changes are present and byte-checked
against HOME. The HOME-relative three-file diff has the exact approved PATCH
SHA-256. Source/helper, cleanup, credential, package, pin, generated, and
unrelated product paths are unchanged in the new delta.

Before the harness commit, ordinary Git status also lists eight HOME-only
added files as untracked because they were materialized from HOME692; those
files are preserved verbatim and are not new merge delta.

## Tests and controls

All commands used Node 20.19.4 where applicable:

- Targeted viewing-parity four-file command with the frozen d0a Agent,
  8f Runtime, and b70 helper carriers — PASS, 4 files / 4 passed.
- The helper custody lane contains exactly 9 test(...) controls in
  harness.test.ts; its full-file run passed all 9 controls — PASS, 9/9.
- Touched-file ESLint with max-warnings 0 — PASS.
- git diff --check — PASS.
- Production import-origin probe with PYTHONDONTWRITEBYTECODE=1,
  PYTHONNOUSERSITE=1, and Agent/Runtime PYTHONPATH — PASS; all four imports
  resolved from Agent d0a.
- b70 carrier custody — PASS: clean Git status; commit
  b70b9d569b2c80885d72734c61cd57e64c3715a8; tree
  687f077c4771e3dbb66bfb7ff2b98f310ac054b6; helper size 10,938 bytes; helper
  SHA-256 bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b;
  realpath ancestors mode 555 and helper mode 444.
- HOME parity and exact patch checks — PASS: all HOME paths outside the three
  owned files match; HOME-relative diff SHA matches the approved PATCH SHA.

## Not run / not locally provable

No browser, render, live socket, Runtime listener, full suite, install, or
central test-service run was performed, as prohibited by this task. The
harness has not yet created the two-parent commit in this worker sandbox, so
actual post-harness ancestor verification is pending the harness; the exact
parent order and tree/delta proof above are prepared for it.

## Recommended next step

Have the harness create the true two-parent commit with parents 909 then 692,
then verify both git merge-base --is-ancestor checks and re-run the recorded
HOME-relative filelist check against the committed merge tree.
