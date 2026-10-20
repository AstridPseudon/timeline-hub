# App refresh onto owner main — in progress

Worker: app-m2-refresh-main-current. Base integration: `18becfbede00038830b97e63345445eeef54fa42` (tree `44d514b44c864ff9dbb3b99aba2b0a41891af83f`). Exact locally verified origin/main: `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`. Merge base: `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2`. No fetch needed.

## External harness action needed

The authorized command `bin/merge-forward app-m2-refresh-main-current origin/main` failed before changes, exit 128: `fatal: update_ref failed for ref 'ORIG_HEAD': ... ORIG_HEAD.lock: Read-only file system`. `.git` is read-only in this worker's sandbox. The worker is preparing the complete resolved source using a private object directory and read-only Git inputs, and will run focused tests. The manager/outer harness must establish the actual merge parent outside this sandbox before final commit. Do not accept a single-parent source copy as the requested upstream merge. No attempt to change permissions or bypass the sandbox will be made.

Final source audit and results will replace this progress report.
